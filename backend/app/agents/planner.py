import os
from app.agents.state import AgentState
from loguru import logger

def planner_node(state: AgentState) -> AgentState:
    """
    Step 1: Analyzes user query to route between SQL Engine, RAG Engine, or Hybrid Analytics.
    """
    query = state["user_query"].lower()
    
    # Heuristics + LLM classification
    has_sql_keywords = any(w in query for w in ["doanh thu", "lợi nhuận", "bán", "đơn hàng", "sản phẩm", "khách hàng", "chỉ tiêu", "bao nhiêu", "top", "quý", "tháng", "tổng", "revenue", "sales"])
    has_rag_keywords = any(w in query for w in ["chính sách", "chiết khấu", "quy định", "bảo hành", "chiến lược", "quy trình", "hướng dẫn", "thưởng", "policy", "rule", "giám đốc"])

    if has_sql_keywords and has_rag_keywords:
        intent = "HYBRID_ANALYTICS"
        reasoning = "Query requires quantitative data (SQL) and qualitative policy context (RAG)."
    elif has_sql_keywords:
        intent = "SQL_ONLY"
        reasoning = "Query is quantitative data analytics on warehouse database."
    else:
        intent = "RAG_ONLY"
        reasoning = "Query is qualitative corporate policy / knowledge retrieval."

    state["intent"] = intent
    state["planner_reasoning"] = reasoning
    logger.info(f"[Planner] Routing query: intent={intent} | query='{state['user_query']}'")
    return state