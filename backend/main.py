import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import rag, history, leads
from app.workers.replies import reply_worker_loop


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    force=True,
)


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


@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "ok", "service": "Ixiera Threads AI Engine"}
