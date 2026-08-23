from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.agents.graph import nexus_agent_graph
from app.agents.state import AgentState

router = APIRouter()

class DashboardGenRequest(BaseModel):
    prompt: str
    user_role: Optional[str] = "builder"

@router.post("/generate")
def generate_dashboard(req: DashboardGenRequest):
    state: AgentState = {
        "user_query": req.prompt,
        "user_role": req.user_role or "builder",
        "session_id": "dash_session",
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
        "hitl_approved": False,
        "retrieved_chunks": None,
        "citations": None,
        "rag_context_text": None,
        "chart_schemas": None,
        "executive_insights": None,
        "final_markdown_response": ""
    }

    result = nexus_agent_graph.invoke(state)
    return {
        "title": f"Executive Dashboard: {req.prompt}",
        "charts": result.get("chart_schemas") or [],
        "insights": result.get("executive_insights") or [],
        "sql_query": result.get("sql_query"),
        "raw_data": result.get("query_result_data") or []
    }