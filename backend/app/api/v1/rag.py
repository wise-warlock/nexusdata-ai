from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.engines.rag_engine import rag_engine
import os
import glob

router = APIRouter()

class RAGSearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 4
    alpha: Optional[float] = 0.5

@router.post("/search")
def search_documents(req: RAGSearchRequest):
    results = rag_engine.hybrid_search(req.query, top_k=req.top_k or 4, alpha=req.alpha or 0.5)
    return {"query": req.query, "results_count": len(results), "chunks": results}

@router.get("/documents")
def list_documents():
    docs_dir = rag_engine.docs_dir
    files = glob.glob(os.path.join(docs_dir, "*.*"))
    doc_list = []
    for fpath in files:
        fname = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        doc_list.append({
            "name": fname,
            "path": fpath,
            "size_bytes": os.path.getsize(fpath),
            "preview": content[:200] + "..." if len(content) > 200 else content
        })
    return {"total_documents": len(doc_list), "documents": doc_list}