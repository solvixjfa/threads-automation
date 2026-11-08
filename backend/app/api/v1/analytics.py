from fastapi import APIRouter, HTTPException
from app.services.rag import get_supabase
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import json

router = APIRouter()

WEEKDAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# STOPWORDS DIPERBANYAK (termasuk kata umum yang sering muncul tapi bukan topik)
INDONESIAN_STOPWORDS = [
    "yang", "yg", "dan", "di", "ke", "dari", "untuk", "dengan", "ini", "itu", 
    "aja", "saja", "gak", "tidak", "ga", "enggak", "bikin", "buat", "ada", 
    "adalah", "pada", "saya", "aku", "gw", "gue", "kamu", "lu", "lo", 
    "dia", "kita", "kami", "mereka", "jadi", "bisa", "sudah", "udah", 
    "akan", "lagi", "juga", "banyak", "banget", "bgt", "kalau", "kalo", 
    "tapi", "namun", "atau", "karena", "soalnya", "bahwa", "dalam", "oleh", 
    "seperti", "bagi", "saat", "waktu", "hari", "kali", "orang", "hal",
    "apa", "salah", "selalu", "mau", "malam", "warga", "sekarang",
    "terus", "biar", "sampe", "sama", "kayak", "gitu", "gini", "disini",
    "disana", "kemana", "mana", "kapan", "siapa", "kenapa", "gimana",
    "harus", "boleh", "tahu", "nggak", "ngga", "belum", "pernah", "sering",
    "kadang", "kayaknya", "sepertinya", "mungkin", "pasti", "bener",
    "beneran", "sih", "deh", "dong", "nih", "tuh", "yuk", "ayo", "mari",
    "kan", "lah", "kah", "pun", "instagram", "threads", "twitter",
    "post", "posting", "konten", "content", "video", "foto", "gambar",
    "the", "and", "is", "in", "it", "to", "of", "for", "on", "with", "as"
]

def fetch_posts_with_metrics(account_id: str):
    db = get_supabase()
    sp_res = db.schema("threads").from_("scheduled_posts").select("published_media_id, text, scheduled_for").eq("account_id", account_id).eq("status", "published").execute()
    sp_map = {}
    for row in (sp_res.data or []):
        if row.get("published_media_id"):
            sp_map[str(row["published_media_id"])] = row

    posts_res = db.schema("threads").from_("posts").select("id, threads_media_id, posted_at, created_at, hook_type, topic_cluster, length_bucket, sentiment, ai_analyzed_at, post_metrics(views, likes, replies, reposts, snapshot_label)").eq("account_id", account_id).execute()
    
    formatted = []
    for p in (posts_res.data or []):
        media_id = str(p.get("threads_media_id"))
        sp = sp_map.get(media_id)
        # Fallback: pakai posts.text kalau gak ada scheduled_posts row
        text = (sp.get("text") if sp else None) or (p.get("text") or "")
        if not text or len(text.strip()) < 5:
            continue

        metrics_arr = p.get("post_metrics", [])
        latest = next((m for m in metrics_arr if m.get("snapshot_label") == "latest"), None)
        if not latest and metrics_arr: latest = metrics_arr[0]
        if not latest or not latest.get("views") or latest["views"] <= 0: continue

        engagement = ((latest.get("likes", 0) + latest.get("replies", 0) + latest.get("reposts", 0)) / latest["views"]) * 100
        ts = sp.get("scheduled_for") or p.get("posted_at") or p.get("created_at")
        
        formatted.append({"id": p.get("id"), "text": text, "er": engagement, "views": latest["views"], "timestamp": ts, "hook_type": p.get("hook_type"), "topic_cluster": p.get("topic_cluster"), "length_bucket": p.get("length_bucket"), "sentiment": p.get("sentiment"), "ai_analyzed_at": p.get("ai_analyzed_at")})
    return formatted

@router.get("/best-time/{account_id}")
async def get_best_time(account_id: str):
    try:
        posts = fetch_posts_with_metrics(account_id)
        sum_matrix = [[0.0]*24 for _ in range(7)]
        count_matrix = [[0]*24 for _ in range(7)]
        total_posts = 0
        for p in posts:
            ts = p["timestamp"]
            if not ts: continue
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            wib_dt = dt + timedelta(hours=7)
            day = (wib_dt.weekday() + 1) % 7
            hour = wib_dt.hour
            sum_matrix[day][hour] += p["er"]
            count_matrix[day][hour] += 1
            total_posts += 1

        matrix = [[0.0]*24 for _ in range(7)]
        for d in range(7):
            for h in range(24):
                if count_matrix[d][h] > 0:
                    matrix[d][h] = round(sum_matrix[d][h] / count_matrix[d][h], 2)

        TIME_BLOCKS = [("Dini Hari",0,4),("Subuh",4,8),("Pagi",8,12),("Siang",12,16),("Sore",16,20),("Malam",20,24)]
        block_matrix = []
        for d in range(7):
            day_blocks = []
            for name, hs, he in TIME_BLOCKS:
                b_sum = 0.0; b_count = 0
                for h in range(hs, he):
                    b_sum += sum_matrix[d][h]; b_count += count_matrix[d][h]
                day_blocks.append({"name": name, "hour_start": f"{hs:02d}:00", "hour_end": f"{he:02d}:00", "er_pct": round(b_sum/b_count,2) if b_count>0 else 0.0, "sample_size": b_count})
            block_matrix.append(day_blocks)

        slots = []
        for d in range(7):
            for h in range(24):
                if count_matrix[d][h] > 0:
                    slots.append({"weekday": WEEKDAY_NAMES[d], "weekday_num": d, "hour": f"{h:02d}:00", "er_pct": matrix[d][h], "sample_size": count_matrix[d][h]})

        best_slots_per_day = []
        for d in range(7):
            ds = [s for s in slots if s["weekday_num"] == d]
            if ds: ds.sort(key=lambda x: x["er_pct"], reverse=True); best_slots_per_day.append(ds[0])

        best_block_per_day = []
        for d in range(7):
            dbs = [b for b in block_matrix[d] if b["sample_size"] > 0]
            if dbs:
                dbs.sort(key=lambda x: x["er_pct"], reverse=True)
                best_block_per_day.append({"weekday": WEEKDAY_NAMES[d], "weekday_num": d, "has_data": True, **dbs[0]})
            else:
                best_block_per_day.append({"weekday": WEEKDAY_NAMES[d], "weekday_num": d, "has_data": False, "name": "-", "hour_start": "-", "hour_end": "-", "er_pct": 0.0, "sample_size": 0})

        confidence = "low"
        if total_posts >= 50: confidence = "high"
        elif total_posts >= 20: confidence = "medium"

        next_best = None
        if confidence != "low":
            cands = [b for b in best_block_per_day if b["has_data"] and b["sample_size"] >= 2]
            if not cands: cands = [b for b in best_block_per_day if b["has_data"]]
            if cands: cands.sort(key=lambda x: x["er_pct"], reverse=True); next_best = cands[0]

        benchmark = None
        if confidence == "low":
            benchmark = {
                "weekday_peak": ["Selasa 09:00-11:00 WIB", "Rabu 09:00-11:00 WIB", "Kamis 19:00-21:00 WIB"],
                "weekend_peak": ["Sabtu 10:00-12:00 WIB", "Minggu 20:00-22:00 WIB"],
                "note": "Benchmark industri Threads, bukan data personal akun Anda."
            }

        return {"success": True, "matrix": matrix, "block_matrix": block_matrix,
                "time_blocks": [{"name": n, "hour_start": f"{hs:02d}:00", "hour_end": f"{he:02d}:00"} for n,hs,he in TIME_BLOCKS],
                "top_slots": best_slots_per_day, "best_block_per_day": best_block_per_day,
                "next_best": next_best, "benchmark": benchmark,
                "total_posts": total_posts, "confidence": confidence}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hook-performance/{account_id}")
async def get_hook_performance(account_id: str):
    try:
        import re as _re
        posts = fetch_posts_with_metrics(account_id)
        HOOK_CATS = ["Data-Point", "Contrarian", "Confession", "Curiosity", "Listicle", "Question", "Statement"]
        buckets = {c: [] for c in HOOK_CATS}

        def classify_regex(first_line: str) -> str:
            fl = first_line.lower()
            if _re.search(r'\d+\.\d+[a-zA-Z%]|\d{2,}%|\d+x\b|Rp\s*\d|[\d.]+\s*(ribu|juta|rb|jt)', fl): return "Data-Point"
            if any(m in fl for m in ["kebanyakan orang salah","sebenarnya","jangan percaya","unpopular opinion","hot take","salah kaprah","mitos","overrated","underrated"]): return "Contrarian"
            if any(m in fl for m in ["gw baru sadar","aku baru sadar","gw salah","aku salah","i was wrong","i lost","we failed","gw gagal","aku gagal","jujur gw","confession"]): return "Confession"
            if any(m in fl for m in ["nggak ada yang bilang","tidak ada yang bilang","rahasia","trik","hack","gak banyak yang tau","jarang yang tau","sebelum lo tau"]): return "Curiosity"
            if _re.match(r'^\d+[\.\):]\s', first_line) or any(m in fl for m in ["tips","cara ","thread:","berikut","hal yang","alasan"]): return "Listicle"
            if "?" in first_line: return "Question"
            return "Statement"

        for p in posts:
            text = (p.get("text") or "").strip()
            if not text: continue
            cached = p.get("hook_type")
            if cached:
                normalized = cached.replace("_", "-").title()
                if normalized in buckets: buckets[normalized].append(p["er"])
                else: buckets["Statement"].append(p["er"])
            else:
                cat = classify_regex(text.split("\n")[0])
                buckets[cat].append(p["er"])

        results = []
        for cat, ers in buckets.items():
            if len(ers) > 0:
                results.append({"type": cat, "avg_er": round(sum(ers)/len(ers),2), "count": len(ers)})
        results.sort(key=lambda x: (x["type"] == "Statement", -x["avg_er"]))

        analyzed = sum(1 for p in posts if p.get("ai_analyzed_at"))
        confidence = "low"
        if len(posts) >= 50: confidence = "high"
        elif len(posts) >= 20: confidence = "medium"

        best_insight = None
        if confidence != "low":
            valid = [r for r in results if r["count"] >= 3 and r["type"] != "Statement"]
            if not valid: valid = [r for r in results if r["type"] != "Statement"]
            if valid:
                valid.sort(key=lambda x: x["avg_er"], reverse=True)
                best_insight = valid[0]

        benchmark = None
        if confidence == "low":
            benchmark = {"best_hook": "Data-Point", "avg_er": "4.5%"}

        return {
            "success": True, "data": results, "best_insight": best_insight,
            "benchmark": benchmark, "total_posts": len(posts),
            "analyzed_posts": analyzed, "confidence": confidence,
            "mode": "llm" if analyzed > 0 else "regex",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/length-performance/{account_id}")
async def get_length_performance(account_id: str):
    try:
        posts = fetch_posts_with_metrics(account_id)
        BUCKETS = ["<100", "100-200", "200-300", "300-500", ">500"]
        buckets = {b: [] for b in BUCKETS}

        def get_bucket(text_len: int, cached: str = None) -> str:
            if cached:
                c = cached.replace("_", "-").replace("100-300","100-200") if cached == "100_300" else cached.replace("_", "-")
                if c in buckets: return c
            if text_len < 100: return "<100"
            if text_len < 200: return "100-200"
            if text_len < 300: return "200-300"
            if text_len < 500: return "300-500"
            return ">500"

        for p in posts:
            text = p.get("text") or ""
            if not text: continue
            bucket = get_bucket(len(text), p.get("length_bucket"))
            buckets[bucket].append(p["er"])

        results = []
        for b, ers in buckets.items():
            results.append({
                "bucket": b, "avg_er": round(sum(ers)/len(ers),2) if ers else 0.0,
                "count": len(ers),
            })
        results.sort(key=lambda x: BUCKETS.index(x["bucket"]))

        analyzed = sum(1 for p in posts if p.get("ai_analyzed_at"))
        confidence = "low"
        if len(posts) >= 50: confidence = "high"
        elif len(posts) >= 20: confidence = "medium"

        best_bucket = None
        if confidence != "low":
            valid = [r for r in results if r["count"] >= 3]
            if valid:
                valid.sort(key=lambda x: x["avg_er"], reverse=True)
                best_bucket = valid[0]

        benchmark = None
        if confidence == "low":
            benchmark = {"best_bucket": "150-250", "avg_er": "4.0%", "note": "Threads optimal: 150-250 karakter"}

        return {
            "success": True, "data": results, "best_bucket": best_bucket,
            "benchmark": benchmark, "total_posts": len(posts),
            "analyzed_posts": analyzed, "confidence": confidence,
            "mode": "llm" if analyzed > 0 else "regex",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/topic-clusters/{account_id}")
async def get_topic_clusters(account_id: str):
    try:
        posts = fetch_posts_with_metrics(account_id)
        
        # Filter post pendek (biasanya bukan konten substansial)
        posts = [p for p in posts if len(p["text"].strip()) > 20]
        
        if len(posts) < 5:
            return {"success": True, "data": [], "message": "Need at least 5 substantial posts to cluster."}

        texts = [p["text"] for p in posts]
        ers = [p["er"] for p in posts]

        vectorizer = TfidfVectorizer(
            stop_words=INDONESIAN_STOPWORDS, 
            max_features=1000,
            ngram_range=(1, 2),
            min_df=2  # Kata harus muncul di minimal 2 post
        )
        X = vectorizer.fit_transform(texts)

        num_clusters = min(4, max(2, len(texts) // 10)) 
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        kmeans.fit(X)
        labels = kmeans.labels_

        order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names_out()
        
        # Ambil keywords yang "bermakna" (panjang > 3 huruf, bukan angka)
        cluster_keywords = {}
        for i in range(num_clusters):
            top_terms = []
            for ind in order_centroids[i, :20]:
                term = terms[ind]
                # Skip kata yang terlalu pendek atau ada angka
                if len(term) > 3 and not any(c.isdigit() for c in term):
                    top_terms.append(term)
                if len(top_terms) >= 3:
                    break
            cluster_keywords[i] = top_terms

        cluster_stats = {i: {"ers": [], "count": 0, "posts": []} for i in range(num_clusters)}
        for idx, label in enumerate(labels):
            cluster_stats[label]["ers"].append(ers[idx])
            cluster_stats[label]["count"] += 1
            cluster_stats[label]["posts"].append(posts[idx])

        results = []
        for i in range(num_clusters):
            stats = cluster_stats[i]
            
            # Skip cluster yang cuma 1 post
            if stats["count"] < 2:
                continue
            
            avg_er = sum(stats["ers"]) / len(stats["ers"])
            
            # Ambil 2 post terbaik (ER tertinggi) sebagai sample
            top_posts = sorted(stats["posts"], key=lambda x: x["er"], reverse=True)[:2]
            samples = []
            for p in top_posts:
                snippet = p["text"][:120].replace("\n", " ")
                if len(p["text"]) > 120:
                    snippet += "..."
                samples.append(snippet)
            
            keywords = cluster_keywords[i]
            # Nama topik: gabung 2 keyword teratas
            if keywords:
                topic_name = " & ".join(keywords[:2]).title()
            else:
                topic_name = f"Group {len(results) + 1}"
            
            results.append({
                "topic": topic_name,
                "keywords": keywords,
                "samples": samples,
                "avg_er": round(avg_er, 2),
                "count": stats["count"]
            })

        results.sort(key=lambda x: x["avg_er"], reverse=True)
        return {"success": True, "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sentiment-performance/{account_id}")
async def get_sentiment_performance(account_id: str):
    try:
        posts = fetch_posts_with_metrics(account_id)
        cats = {"positive": [], "neutral": [], "negative": []}
        for p in posts:
            sent = (p.get("sentiment") or "").lower()
            if sent in cats: cats[sent].append(p["er"])
        results = [{"sentiment": k, "avg_er": round(sum(v)/len(v),2) if v else 0.0, "count": len(v)} for k, v in cats.items()]
        analyzed = sum(1 for p in posts if p.get("ai_analyzed_at"))
        return {"success": True, "data": results, "total_posts": len(posts), "analyzed_posts": analyzed, "mode": "llm" if analyzed > 0 else "none"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis-status/{account_id}")
async def get_analysis_status(account_id: str):
    try:
        db = get_supabase()
        posts_res = db.schema("threads").from_("posts").select("id, ai_analyzed_at").eq("account_id", account_id).execute()
        posts = posts_res.data or []
        analyzed = sum(1 for p in posts if p.get("ai_analyzed_at"))
        acc_res = db.schema("threads").from_("threads_accounts").select("last_deep_analyze_at, plan").eq("id", account_id).limit(1).execute()
        acc = acc_res.data[0] if acc_res.data else {}
        return {"success": True, "total_posts": len(posts), "analyzed_posts": analyzed,
                "needs_analyze": analyzed < len(posts), "last_analyzed_at": acc.get("last_deep_analyze_at"),
                "plan": acc.get("plan"), "is_cached": analyzed > 0 and analyzed == len(posts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/deep-analyze/{account_id}")
async def run_deep_analyze(account_id: str, payload: dict = None):
    from app.services.billing import check_and_spend, refund_credits, BillingError
    from app.services.rag import GEMINI_KEY
    from google import genai
    from google.genai import types
    from datetime import datetime, timezone

    db = get_supabase()
    acc_res = db.schema("threads").from_("threads_accounts").select("plan, credit_balance, custom_gemini_key").eq("id", account_id).limit(1).execute()
    if not acc_res.data: raise HTTPException(404, "Account not found")
    acc = acc_res.data[0]
    plan = acc.get("plan", "none")
    is_paid = plan in ("paid_credit", "paid_byok")

    ref_id = None
    if is_paid:
        try: ref_id = check_and_spend(account_id, "deep_analyze")
        except BillingError as e: raise HTTPException(403, e.message)

    try:
        sp_res = db.schema("threads").from_("scheduled_posts").select("published_media_id, text").eq("account_id", account_id).eq("status", "published").execute()
        sp_map = {str(r["published_media_id"]): r.get("text","") for r in (sp_res.data or []) if r.get("published_media_id")}

        posts_res = db.schema("threads").from_("posts").select("id, threads_media_id, ai_analyzed_at").eq("account_id", account_id).execute()
        all_posts = posts_res.data or []

        to_analyze = []
        for p in all_posts:
            text = (sp_map.get(str(p.get("threads_media_id"))) or "").strip()
            if len(text) < 20: continue
            if p.get("ai_analyzed_at"): continue
            to_analyze.append({"id": p["id"], "text": text[:1000]})

        if not to_analyze:
            if ref_id:
                try: refund_credits(account_id, "deep_analyze", ref_id)
                except: pass
            return {"success": True, "analyzed_count": 0, "message": "Nothing new to analyze"}

        gemini_key = acc.get("custom_gemini_key") or GEMINI_KEY
        if not gemini_key:
            if ref_id:
                try: refund_credits(account_id, "deep_analyze", ref_id)
                except: pass
            raise HTTPException(400, "Gemini API Key required")

        client = genai.Client(api_key=gemini_key)
        all_results = []
        CHUNK = 50
        for i in range(0, len(to_analyze), CHUNK):
            chunk = to_analyze[i:i+CHUNK]
            prompt = f"""Classify each Threads post below. Return ONLY valid JSON array.

Fields per post:
- id: same as input
- hook_type: data_point|contrarian|confession|curiosity|listicle|question|statement
- topic_cluster: 2-4 words (e.g. "AI Startup Tips", "Personal Finance")
- length_bucket: <100|100_300|300_500|>500
- sentiment: positive|neutral|negative

POSTS:
{json.dumps(chunk, ensure_ascii=False)}

Return JSON array only, no markdown."""

            resp = None
            last_err = ""
            _user_model = (payload or {}).get("model") if isinstance(payload, dict) else None
            if _user_model == "hemat":
                _models = ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-flash-latest"]
            elif _user_model == "akurat":
                _models = ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"]
            else:
                _models = ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"]
            for m in _models:
                try:
                    resp = client.models.generate_content(
                        model=m, contents=prompt,
                        config=types.GenerateContentConfig(response_mime_type="application/json", max_output_tokens=8000)
                    )
                    break
                except Exception as e:
                    last_err = str(e)

            if not resp:
                raise Exception(f"LLM failed: {last_err}")

            raw = resp.text.strip()
            if raw.startswith("```json"): raw = raw.replace("```json","",1).rstrip("`").strip()
            batch = json.loads(raw)
            all_results.extend(batch if isinstance(batch, list) else batch.get("results", []))

        now_iso = datetime.now(timezone.utc).isoformat()
        updated = 0
        for r in all_results:
            pid = r.get("id")
            if not pid: continue
            db.schema("threads").from_("posts").update({
                "hook_type": r.get("hook_type"),
                "topic_cluster": r.get("topic_cluster"),
                "length_bucket": r.get("length_bucket"),
                "sentiment": r.get("sentiment"),
                "ai_analyzed_at": now_iso,
            }).eq("id", pid).execute()
            updated += 1

        db.schema("threads").from_("threads_accounts").update({"last_deep_analyze_at": now_iso}).eq("id", account_id).execute()

        return {"success": True, "analyzed_count": updated, "total_posts": len(all_posts), "requested": len(to_analyze)}
    except Exception as e:
        if ref_id:
            try: refund_credits(account_id, "deep_analyze", ref_id)
            except: pass
        raise HTTPException(500, detail=str(e))

@router.post("/backfill-permalinks/{account_id}")
async def backfill_permalinks(account_id: str):
    """One-time: fetch missing permalinks from Meta API per-post"""
    import httpx
    db = get_supabase()

    acc_res = db.schema("threads").from_("threads_accounts").select("settings").eq("id", account_id).limit(1).execute()
    if not acc_res.data:
        raise HTTPException(404, "Account not found")

    token = (acc_res.data[0].get("settings") or {}).get("access_token")
    if not token:
        raise HTTPException(400, "No access token in account settings")

    posts_res = db.schema("threads").from_("posts").select("id, threads_media_id, permalink").eq("account_id", account_id).execute()
    posts = posts_res.data or []

    to_fetch = []
    for p in posts:
        perm = p.get("permalink")
        if not perm:
            to_fetch.append(p)
        elif "/post/" in perm and "/@" not in perm:
            to_fetch.append(p)

    updated = 0
    still_null = []
    failed = []

    async with httpx.AsyncClient() as client:
        for p in to_fetch:
            media_id = p["threads_media_id"]
            try:
                url = f"https://graph.threads.net/v1.0/{media_id}?fields=permalink,shortcode&access_token={token}"
                res = await client.get(url, timeout=15.0)
                if res.status_code == 200:
                    data = res.json()
                    perm = data.get("permalink")
                    if perm and perm.startswith("http"):
                        db.schema("threads").from_("posts").update({"permalink": perm}).eq("id", p["id"]).execute()
                        updated += 1
                    else:
                        still_null.append({"media_id": media_id, "reason": "API returned no permalink"})
                else:
                    failed.append({"media_id": media_id, "status": res.status_code, "error": res.text[:200]})
            except Exception as e:
                failed.append({"media_id": media_id, "error": str(e)})

    return {
        "success": True,
        "total_scanned": len(posts),
        "to_fetch": len(to_fetch),
        "updated": updated,
        "still_null": still_null,
        "failed": failed,
    }
