from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from core.logging_config import setup_logging
from api.routes.ingestion import router as ingestion_router
from api.routes.rag import router as rag_router
from dotenv import load_dotenv

load_dotenv()
setup_logging()

app = FastAPI(title="Multi-Tenant RAG")

app.include_router(ingestion_router)
app.include_router(rag_router)

static_path = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def home():
    return FileResponse(static_path / "index.html")

@app.get("/health")
def health():
    return {"status": "ok"}
