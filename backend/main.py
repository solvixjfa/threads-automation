import asyncio
import logging
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import rag, history, leads
from app.workers.replies import reply_worker_loop
from app.services.importer import import_threads_history
from app.core.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
from supabase import create_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", force=True)

app = FastAPI(title="Ixiera Threads AI Engine", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rag.router, prefix="/api/v1/rag", tags=["RAG"])
app.include_router(history.router, prefix="/api/v1/history", tags=["History Importer"])
app.include_router(leads.router, prefix="/api/v1/leads", tags=["Lead Detector"])

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(reply_worker_loop())

@app.post("/api/v1/metrics/sync")
async def trigger_metrics_sync(background_tasks: BackgroundTasks):
    db = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    acc_res = db.schema("threads").from_("threads_accounts").select("id, settings").eq("connection_status", "connected").execute()
    
    if not acc_res.data:
        return {"success": False, "message": "Tidak ada akun terhubung"}
        
    for acc in acc_res.data:
        token = acc.get("settings", {}).get("access_token")
        if token:
            background_tasks.add_task(import_threads_history, acc["id"], token)
            
    return {"success": True, "message": "Sinkronisasi berjalan di latar belakang."}

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "ok", "service": "Ixiera Threads AI Engine"}
