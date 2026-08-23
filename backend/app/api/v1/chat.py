from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.agents.graph import nexus_agent_graph
from app.agents.state import AgentState
from app.core.security import get_current_user, User, UserRole

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "session_default"
    user_role: Optional[str] = "analyst"
    hitl_approved: Optional[bool] = False

class ChatResponse(BaseModel):
    intent: str
    planner_reasoning: str
    markdown_response: str
    sql_query: Optional[str] = None
    sql_is_valid: bool = True
    sql_error: Optional[str] = None
    query_result_data: Optional[List[Dict[str, Any]]] = None
    sql_column_names: Optional[List[str]] = None
    estimated_scan_bytes: int = 0
    hitl_required: bool = False
    citations: Optional[List[str]] = None
    chart_schemas: Optional[List[Dict[str, Any]]] = None
    executive_insights: Optional[List[str]] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    initial_state: AgentState = {
        "user_query": req.query,
        "user_role": req.user_role or "analyst",
        "session_id": req.session_id or "session_default",
        "intent": "",
        "planner_reasoning": "",
        "sql_query": None,
        "sql_is_valid": False,
        "sql_error": None,
        "sql_retry_count": 0,
        "query_result_data": None,
        "sql_column_names": None,
        "estimated_scan_bytes": 0,
        "hitl_required": False,
        "hitl_approved": req.hitl_approved or False,
        "retrieved_chunks": None,
        "citations": None,
        "rag_context_text": None,
        "chart_schemas": None,
        "executive_insights": None,
        "final_markdown_response": ""
    }

    result = nexus_agent_graph.invoke(initial_state)

    return ChatResponse(
        intent=result.get("intent", "UNKNOWN"),
        planner_reasoning=result.get("planner_reasoning", ""),
        markdown_response=result.get("final_markdown_response", ""),
        sql_query=result.get("sql_query"),
        sql_is_valid=result.get("sql_is_valid", True),
        sql_error=result.get("sql_error"),
        query_result_data=result.get("query_result_data"),
        sql_column_names=result.get("sql_column_names"),
        estimated_scan_bytes=result.get("estimated_scan_bytes", 0),
        hitl_required=result.get("hitl_required", False),
        citations=result.get("citations"),
        chart_schemas=result.get("chart_schemas"),
        executive_insights=result.get("executive_insights")
    )