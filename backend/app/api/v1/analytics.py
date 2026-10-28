from fastapi import APIRouter, HTTPException
from app.services.rag import get_supabase
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

router = APIRouter()

WEEKDAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# KAMUS BUANGAN BAHASA INDONESIA (Termasuk slang/singkatan)
INDONESIAN_STOPWORDS = [
    "yang", "yg", "dan", "di", "ke", "dari", "untuk", "dengan", "ini", "itu", 
    "aja", "saja", "gak", "tidak", "ga", "enggak", "bikin", "buat", "ada", 
    "adalah", "pada", "saya", "aku", "gw", "gue", "kamu", "lu", "lo", 
    "dia", "kita", "kami", "mereka", "jadi", "bisa", "sudah", "udah", 
    "akan", "lagi", "juga", "banyak", "banget", "bgt", "kalau", "kalo", 
    "tapi", "namun", "atau", "karena", "soalnya", "bahwa", "dalam", "oleh", 
    "seperti", "bagi", "saat", "waktu", "hari", "kali", "orang", "hal", 
    "the", "and", "is", "in", "it", "to", "of", "for", "on", "with", "as"
]

def fetch_posts_with_metrics(account_id: str):
    db = get_supabase()
    
    # 1. Ambil text dan tanggal publish dari scheduled_posts
    sp_res = db.schema("threads").from_("scheduled_posts").select("published_media_id, text, scheduled_for").eq("account_id", account_id).eq("status", "published").execute()
    sp_map = {}
    for row in (sp_res.data or []):
        if row.get("published_media_id"):
            sp_map[str(row["published_media_id"])] = row

    # 2. Ambil metrik dari tabel posts
    posts_res = db.schema("threads").from_("posts").select("id, threads_media_id, posted_at, created_at, post_metrics(views, likes, replies, reposts, snapshot_label)").eq("account_id", account_id).execute()
    
    formatted = []
    for p in (posts_res.data or []):
        media_id = str(p.get("threads_media_id"))
        sp = sp_map.get(media_id)
        if not sp or not sp.get("text"): continue

        metrics_arr = p.get("post_metrics", [])
        latest = next((m for m in metrics_arr if m.get("snapshot_label") == "latest"), None)
        if not latest and metrics_arr: latest = metrics_arr[0]
        if not latest or not latest.get("views") or latest["views"] <= 0: continue

        engagement = ((latest.get("likes", 0) + latest.get("replies", 0) + latest.get("reposts", 0)) / latest["views"]) * 100
        ts = sp.get("scheduled_for") or p.get("posted_at") or p.get("created_at")
        
        formatted.append({
            "text": sp.get("text", ""), 
            "er": engagement, 
            "views": latest["views"], 
            "timestamp": ts
        })
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

        slots = []
        for d in range(7):
            for h in range(24):
                if count_matrix[d][h] > 0:
                    slots.append({
                        "weekday": WEEKDAY_NAMES[d],
                        "hour": f"{h:02d}:00",
                        "er_pct": matrix[d][h],
                        "sample_size": count_matrix[d][h]
                    })
        
        slots.sort(key=lambda x: x["er_pct"], reverse=True)

        confidence = "low"
        if total_posts >= 50: confidence = "high"
        elif total_posts >= 20: confidence = "medium"

        return {"success": True, "matrix": matrix, "top_slots": slots[:5], "total_posts": total_posts, "confidence": confidence}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hook-performance/{account_id}")
async def get_hook_performance(account_id: str):
    try:
        posts = fetch_posts_with_metrics(account_id)
        hooks = {"Question": [], "List": [], "Story": [], "Statement": []}

        for p in posts:
            text = p["text"].strip()
            if not text: continue
            
            first_line = text.split("\n")[0].lower()
            
            if "?" in first_line:
                hooks["Question"].append(p["er"])
            elif any(first_line.startswith(str(i)) for i in range(1, 10)) or "cara" in first_line or "tips" in first_line:
                hooks["List"].append(p["er"])
            elif "gw" in first_line or "saya" in first_line or "aku" in first_line or "i " in first_line or "my " in first_line:
                hooks["Story"].append(p["er"])
            else:
                hooks["Statement"].append(p["er"])

        results = []
        for h_type, ers in hooks.items():
            if len(ers) > 0:
                avg_er = sum(ers) / len(ers)
                results.append({"type": h_type, "avg_er": round(avg_er, 2), "count": len(ers)})
                
        results.sort(key=lambda x: x["avg_er"], reverse=True)
        return {"success": True, "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/length-performance/{account_id}")
async def get_length_performance(account_id: str):
    try:
        posts = fetch_posts_with_metrics(account_id)
        lengths = {"<100 chars": [], "100-300 chars": [], "300-500 chars": [], ">500 chars": []}

        for p in posts:
            l = len(p["text"])
            if l < 100: lengths["<100 chars"].append(p["er"])
            elif l <= 300: lengths["100-300 chars"].append(p["er"])
            elif l <= 500: lengths["300-500 chars"].append(p["er"])
            else: lengths[">500 chars"].append(p["er"])

        results = []
        for l_type, ers in lengths.items():
            if len(ers) > 0:
                avg_er = sum(ers) / len(ers)
                results.append({"range": l_type, "avg_er": round(avg_er, 2), "count": len(ers)})

        return {"success": True, "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topic-clusters/{account_id}")
async def get_topic_clusters(account_id: str):
    try:
        posts = fetch_posts_with_metrics(account_id)
        if len(posts) < 5:
            return {"success": True, "data": [], "message": "Need at least 5 posts to cluster topics."}

        texts = [p["text"] for p in posts]
        ers = [p["er"] for p in posts]

        # Pake stopwords Indo + N-Gram (biar "machine learning" gak kepisah)
        vectorizer = TfidfVectorizer(
            stop_words=INDONESIAN_STOPWORDS, 
            max_features=1000,
            ngram_range=(1, 2)
        )
        X = vectorizer.fit_transform(texts)

        # Batasi max cluster. Jangan lebih dari 1/3 jumlah post, minimal 2
        num_clusters = min(4, max(2, len(texts) // 10)) 
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
        kmeans.fit(X)
        labels = kmeans.labels_

        order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names_out()
        
        cluster_keywords = {}
        for i in range(num_clusters):
            top_terms = [terms[ind] for ind in order_centroids[i, :3]]
            cluster_keywords[i] = ", ".join(top_terms).title()

        cluster_stats = {i: {"ers": [], "count": 0} for i in range(num_clusters)}
        for idx, label in enumerate(labels):
            cluster_stats[label]["ers"].append(ers[idx])
            cluster_stats[label]["count"] += 1

        results = []
        for i in range(num_clusters):
            stats = cluster_stats[i]
            if stats["count"] > 0:
                avg_er = sum(stats["ers"]) / stats["count"]
                results.append({
                    "topic": cluster_keywords[i] or f"Topic {i+1}",
                    "avg_er": round(avg_er, 2),
                    "count": stats["count"]
                })

        results.sort(key=lambda x: x["avg_er"], reverse=True)
        return {"success": True, "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
