from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel

class AgentState(TypedDict):
    # User Input & Session
    user_query: str
    user_role: str
    session_id: str
    
    # Intent & Routing
    intent: str # "SQL_ONLY", "RAG_ONLY", "HYBRID_ANALYTICS", "DRILLDOWN"
    planner_reasoning: str
    
    # DATA-01: SQL Engine State
    sql_query: Optional[str]
    sql_is_valid: bool
    sql_error: Optional[str]
    sql_retry_count: int
    query_result_data: Optional[List[Dict[str, Any]]]
    sql_column_names: Optional[List[str]]
    estimated_scan_bytes: int
    hitl_required: bool
    hitl_approved: bool
    
    # AIP-04: RAG Engine State
    retrieved_chunks: Optional[List[Dict[str, Any]]]
    citations: Optional[List[str]]
    rag_context_text: Optional[str]
    
    # DATA-16: Visualization & Dashboard State
    chart_schemas: Optional[List[Dict[str, Any]]]
    executive_insights: Optional[List[str]]
    
    # Final Unified Response
    final_markdown_response: str