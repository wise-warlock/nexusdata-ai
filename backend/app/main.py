from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.api.v1.chat import router as chat_router
from app.api.v1.sql import router as sql_router
from app.api.v1.rag import router as rag_router
from app.api.v1.dashboard import router as dash_router
from app.api.v1.eval import router as eval_router
from loguru import logger
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Unified Enterprise AI Platform: Text-to-SQL (DATA-01) + Auto-Dashboard (DATA-16) + Self-Optimizing Advanced RAG (AIP-04)"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register v1 API routes
app.include_router(chat_router, prefix="/api/v1", tags=["Conversational AI Agent"])
app.include_router(sql_router, prefix="/api/v1/sql", tags=["DATA-01 Text-to-SQL Engine"])
app.include_router(rag_router, prefix="/api/v1/rag", tags=["AIP-04 Advanced RAG Engine"])
app.include_router(dash_router, prefix="/api/v1/dashboard", tags=["DATA-16 Visualization Engine"])
app.include_router(eval_router, prefix="/api/v1/eval", tags=["AIP-04 & DATA-01 Evaluation Studio"])

# Static Web UI Dashboard Mount
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_ui():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "online",
        "platform": settings.PROJECT_NAME,
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "engines": ["DuckDB_OLAP", "Hybrid_RAG", "LangGraph_Orchestrator"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)