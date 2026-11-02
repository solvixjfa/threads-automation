import re

p = "backend/app/api/v1/rag.py"
s = open(p).read()

# Target: Class GeneratePostRequest
old_class = """class GeneratePostRequest(BaseModel):
    account_id: str
    topic: str
    tone: Optional[str] = "Edukasi & Insight Kasual"
    custom_prompt: Optional[str] = None
    provider: Optional[str] = "gemini"
    model_name: Optional[str] = None"""

new_class = """class GeneratePostRequest(BaseModel):
    account_id: str
    topic: str
    tone: Optional[str] = "Edukasi & Insight Kasual"
    custom_prompt: Optional[str] = None
    provider: Optional[str] = "gemini"
    model_name: Optional[str] = None
    selected_knowledge_ids: Optional[list[str]] = None"""

if old_class not in s:
    print("[FAIL] Class GeneratePostRequest tidak ketemu.")
else:
    s = s.replace(old_class, new_class)
    print("[OK] Pydantic Model dipatch.")

# Cek apakah pemanggilan fungsinya udah bener
if "selected_knowledge_ids=payload.selected_knowledge_ids" not in s:
    # Fallback kalau pemanggilan fungsinya masih salah
    s = s.replace("model_name=payload.model_name\n        )", "model_name=payload.model_name,\n            selected_knowledge_ids=payload.selected_knowledge_ids\n        )")
    print("[OK] Parameter fungsional dipatch.")

open(p, "w").write(s)
