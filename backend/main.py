from fastapi import FastAPI
from app.api.v1 import rag, history, leads

app = FastAPI(title="Ixiera Threads AI Engine")

app.include_router(rag.router, prefix="/api/v1/rag", tags=["RAG"])
app.include_router(history.router, prefix="/api/v1/history", tags=["History Importer"])
app.include_router(leads.router, prefix="/api/v1/leads", tags=["Lead Detector"])

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Python AI Engine Active"}
