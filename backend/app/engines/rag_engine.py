import os
import glob
from typing import List, Dict, Any, Optional
import numpy as np
from rank_bm25 import BM25Okapi
from loguru import logger
import re

class DocumentChunk:
    def __init__(self, doc_id: str, doc_name: str, chunk_id: int, content: str, metadata: Dict[str, Any] = None):
        self.doc_id = doc_id
        self.doc_name = doc_name
        self.chunk_id = chunk_id
        self.content = content
        self.metadata = metadata or {}

class AdvancedRAGEngine:
    def __init__(self, docs_dir: str = "E:/nexusdata-ai/backend/app/data/sample_docs"):
        self.docs_dir = docs_dir
        self.chunks: List[DocumentChunk] = []
        self.bm25 = None
        self.tokenized_corpus = []
        self._is_indexed = False
        
        # Load and index on initialization
        self.index_documents(chunk_size=512, chunk_overlap=64)

    def _simple_tokenize(self, text: str) -> List[str]:
        # Lowercase and split words + Vietnamese support
        return re.findall(r"\w+", text.lower())

    def _chunk_text(self, text: str, chunk_size: int = 512, chunk_overlap: int = 64) -> List[str]:
        words = text.split()
        if len(words) <= chunk_size:
            return [text]

        chunks = []
        i = 0
        while i < len(words):
            chunk_words = words[i : i + chunk_size]
            chunks.append(" ".join(chunk_words))
            i += (chunk_size - chunk_overlap)
        return chunks

    def index_documents(self, chunk_size: int = 512, chunk_overlap: int = 64):
        """Indexes all documents in docs_dir using specified chunk size and overlap."""
        self.chunks = []
        doc_files = glob.glob(os.path.join(self.docs_dir, "*.*"))
        
        chunk_counter = 0
        for filepath in doc_files:
            filename = os.path.basename(filepath)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                text_chunks = self._chunk_text(content, chunk_size, chunk_overlap)
                for idx, chunk_text in enumerate(text_chunks):
                    self.chunks.append(
                        DocumentChunk(
                            doc_id=f"{filename}_{idx}",
                            doc_name=filename,
                            chunk_id=idx,
                            content=chunk_text,
                            metadata={"filepath": filepath, "length": len(chunk_text)}
                        )
                    )
                    chunk_counter += 1
            except Exception as e:
                logger.error(f"Error reading doc {filename}: {e}")

        # Build BM25 Index
        self.tokenized_corpus = [self._simple_tokenize(c.content) for c in self.chunks]
        if self.tokenized_corpus:
            self.bm25 = BM25Okapi(self.tokenized_corpus)
            self._is_indexed = True
            logger.info(f"RAG Engine indexed {len(self.chunks)} chunks from {len(doc_files)} documents.")

    def hybrid_search(self, query: str, top_k: int = 4, alpha: float = 0.5) -> List[Dict[str, Any]]:
        """
        Hybrid search combining BM25 keyword matching and dense token overlap score.
        alpha = 0.5 gives equal weight to Sparse (BM25) and Dense similarity.
        """
        if not self._is_indexed or not self.chunks:
            return []

        tokenized_query = self._simple_tokenize(query)
        if not tokenized_query:
            return []

        # 1. BM25 Scores (Sparse)
        bm25_scores = np.array(self.bm25.get_scores(tokenized_query))
        max_bm25 = np.max(bm25_scores) if np.max(bm25_scores) > 0 else 1.0
        norm_bm25 = bm25_scores / max_bm25

        # 2. Semantic Token Overlap / Vector simulation (Dense proxy for standalone runtime)
        dense_scores = []
        query_set = set(tokenized_query)
        for chunk_tokens in self.tokenized_corpus:
            overlap = len(query_set.intersection(set(chunk_tokens)))
            dense_scores.append(overlap / (len(query_set) + 1e-5))
        norm_dense = np.array(dense_scores)
        max_dense = np.max(norm_dense) if np.max(norm_dense) > 0 else 1.0
        norm_dense = norm_dense / max_dense

        # 3. Hybrid Score Combination
        hybrid_scores = alpha * norm_bm25 + (1 - alpha) * norm_dense
        top_indices = np.argsort(hybrid_scores)[::-1][:top_k]

        results = []
        for rank, idx in enumerate(top_indices):
            if hybrid_scores[idx] > 0.05:
                chunk = self.chunks[idx]
                results.append({
                    "doc_name": chunk.doc_name,
                    "chunk_id": chunk.chunk_id,
                    "content": chunk.content,
                    "score": round(float(hybrid_scores[idx]), 4),
                    "citation": f"[{chunk.doc_name} #chunk-{chunk.chunk_id}]"
                })

        return results

    def format_context_with_citations(self, search_results: List[Dict[str, Any]]) -> str:
        """Formats retrieved chunks into a prompt context with verified citations."""
        if not search_results:
            return "No relevant corporate documents found."

        context_blocks = []
        for r in search_results:
            context_blocks.append(
                f"Source: {r['doc_name']} (Chunk ID: {r['chunk_id']})\n"
                f"Content: {r['content']}\n"
                f"Citation Tag: {r['citation']}"
            )
        return "\n\n---\n\n".join(context_blocks)

rag_engine = AdvancedRAGEngine()