import sys, re

# ========= BACKEND SERVICE =========
svc = "backend/app/services/rag.py"
s = open(svc).read()

# Signature
old_sig = 'async def generate_rag_post(account_id: str, topic: str, tone: str = "Edukasi & Insight Kasual", custom_prompt: str = None, provider: str = "gemini", model_name: str = None) -> list[dict]:'
new_sig = 'async def generate_rag_post(account_id: str, topic: str, tone: str = "Edukasi & Insight Kasual", custom_prompt: str = None, provider: str = "gemini", model_name: str = None, selected_knowledge_ids: list[str] = None) -> list[dict]:'
if old_sig in s:
    s = s.replace(old_sig, new_sig, 1)
    print("[OK] signature service")
elif "selected_knowledge_ids: list[str] = None" in s:
    print("[SKIP] signature sudah ada")
else:
    print("[FAIL] signature tidak ketemu"); sys.exit(1)

# RAG block
old_rag = '''    gemini_embed_key = custom_gemini if custom_gemini else GEMINI_KEY
    if not gemini_embed_key: raise Exception("Gemini API Key is required for RAG embeddings. Please add it in Settings.")

    knowledge = await search_knowledge(account_id, topic, limit=3, api_key=gemini_embed_key)
    context_text = "\\n".join([f"- [{k.get('category', 'Fakta')} - {k.get('title')}]: {k.get('content')}" for k in knowledge])'''

new_rag = '''    if selected_knowledge_ids and len(selected_knowledge_ids) > 0:
        knowledge_res = db.schema("threads").from_("brand_knowledge").select("category, title, content").in_("id", selected_knowledge_ids).eq("account_id", account_id).execute()
        knowledge = knowledge_res.data or []
    else:
        gemini_embed_key = custom_gemini if custom_gemini else GEMINI_KEY
        if not gemini_embed_key: raise Exception("Gemini API Key is required for RAG embeddings. Please add it in Settings.")
        knowledge = await search_knowledge(account_id, topic, limit=3, api_key=gemini_embed_key)
    context_text = "\\n".join([f"- [{k.get('category', 'Fakta')} - {k.get('title')}]: {k.get('content')}" for k in knowledge])'''

if "if selected_knowledge_ids and len(selected_knowledge_ids) > 0:" in s:
    print("[SKIP] RAG block sudah ada")
elif old_rag in s:
    s = s.replace(old_rag, new_rag, 1)
    print("[OK] RAG block")
else:
    print("[FAIL] RAG block tidak ketemu"); sys.exit(1)

# list_knowledge_docs
if "async def list_knowledge_docs" not in s:
    fn = '\n\nasync def list_knowledge_docs(account_id: str) -> list[dict]:\n    db = get_supabase()\n    res = db.schema("threads").from_("brand_knowledge").select("id, title, category").eq("account_id", account_id).order("created_at", desc=True).execute()\n    return res.data or []\n\n'
    s = s.replace("async def generate_rag_post(", fn + "async def generate_rag_post(", 1)
    print("[OK] list_knowledge_docs")
else:
    print("[SKIP] list_knowledge_docs sudah ada")

open(svc, "w").write(s)

# ========= BACKEND API =========
api = "backend/app/api/v1/rag.py"
a = open(api).read()

if "selected_knowledge_ids: Optional[list[str]] = None" not in a:
    old_m = 'class GeneratePostRequest(BaseModel):\n    account_id: str\n    topic: str\n    tone: Optional[str] = "Edukasi & Insight Kasual"\n    custom_prompt: Optional[str] = None\n    provider: Optional[str] = "gemini"\n    model_name: Optional[str] = None'
    new_m = old_m + '\n    selected_knowledge_ids: Optional[list[str]] = None'
    if old_m in a:
        a = a.replace(old_m, new_m, 1); print("[OK] pydantic field")
    else:
        print("[FAIL] pydantic"); sys.exit(1)
else:
    print("[SKIP] pydantic sudah ada")

if "selected_knowledge_ids=payload.selected_knowledge_ids" not in a:
    if "model_name=payload.model_name\n        )" in a:
        a = a.replace("model_name=payload.model_name\n        )", "model_name=payload.model_name,\n            selected_knowledge_ids=payload.selected_knowledge_ids\n        )", 1)
        print("[OK] api passthrough")
    else:
        print("[FAIL] api passthrough tidak ketemu"); sys.exit(1)
else:
    print("[SKIP] api passthrough sudah ada")

open(api, "w").write(a)

# ========= FRONTEND =========
vue = "frontend/src/views/ComposerView.vue"
v = open(vue).read()

if "watch(currentAccountId," not in v:
    old_fn = '''async function fetchKnowledge() {
  if (!currentAccountId.value) return
  try {
    const res = await fetch(`https://threads-automation-r9so.onrender.com/api/v1/rag/knowledge?account_id=${currentAccountId.value}`)
    const data = await res.json()
    if (data.knowledge) availableKnowledge.value = data.knowledge
  } catch (err) { console.error('Failed to fetch knowledge:', err) }
}'''
    if old_fn in v:
        v = v.replace(old_fn, old_fn + '\n\nwatch(currentAccountId, (newVal) => {\n  if (newVal) fetchKnowledge()\n})', 1)
        print("[OK] frontend watch")
    else:
        print("[FAIL] fetchKnowledge function tidak ketemu"); sys.exit(1)
else:
    print("[SKIP] watch sudah ada")

open(vue, "w").write(v)
print("\n[DONE]")
