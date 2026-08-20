from app.agents.state import AgentState
from app.engines.rag_engine import rag_engine
from loguru import logger

def rag_agent_node(state: AgentState) -> AgentState:
    """
    AIP-04 Advanced Hybrid RAG retrieval node with citations.
    """
    if state["intent"] not in ["RAG_ONLY", "HYBRID_ANALYTICS"]:
        return state

    query = state["user_query"]
    results = rag_engine.hybrid_search(query, top_k=3, alpha=0.5)

    state["retrieved_chunks"] = results
    state["citations"] = [r["citation"] for r in results]
    state["rag_context_text"] = rag_engine.format_context_with_citations(results)

    logger.info(f"[RAG Agent] Retrieved {len(results)} chunks for query: '{query}'")
    return state