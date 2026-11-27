import asyncio
import logging
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import rag, history, leads, queue, analytics, admin, payment, trending, threads_extra, chat
from app.workers.replies import reply_worker_loop

logging.basicConfig(level=logging.WARNING, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", force=True)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

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
app.include_router(queue.router, prefix="/api/v1/queue", tags=["Queue Manager"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(payment.router, prefix="/api/v1/payment", tags=["Payment"])
app.include_router(trending.router, prefix="/api/v1/trending", tags=["Trending & Outreach"])
app.include_router(threads_extra.router, prefix="/api/v1/threads-extra", tags=["Threads Location & Mentions"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Support Chat"])

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(reply_worker_loop())

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "ok", "service": "Ixiera Threads AI Engine"}

