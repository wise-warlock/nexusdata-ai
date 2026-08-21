from langgraph.graph import StateGraph, START, END
from app.agents.state import AgentState
from app.agents.planner import planner_node
from app.agents.sql_agent import sql_agent_node
from app.agents.rag_agent import rag_agent_node
from app.agents.viz_agent import viz_agent_node
from app.agents.synthesis_agent import synthesis_agent_node
from loguru import logger

def route_by_intent(state: AgentState) -> str:
    intent = state.get("intent", "SQL_ONLY")
    if intent == "RAG_ONLY":
        return "rag_agent"
    elif intent == "HYBRID_ANALYTICS":
        return "sql_agent" # In hybrid, run SQL then RAG
    else:
        return "sql_agent"

def route_after_sql(state: AgentState) -> str:
    intent = state.get("intent", "SQL_ONLY")
    if intent == "HYBRID_ANALYTICS":
        return "rag_agent"
    return "viz_agent"

# Build LangGraph State Machine
builder = StateGraph(AgentState)

# 1. Add Nodes
builder.add_node("planner", planner_node)
builder.add_node("sql_agent", sql_agent_node)
builder.add_node("rag_agent", rag_agent_node)
builder.add_node("viz_agent", viz_agent_node)
builder.add_node("synthesis_agent", synthesis_agent_node)

# 2. Add Edges & Conditional Routing
builder.add_edge(START, "planner")

builder.add_conditional_edges(
    "planner",
    route_by_intent,
    {
        "sql_agent": "sql_agent",
        "rag_agent": "rag_agent"
    }
)

builder.add_conditional_edges(
    "sql_agent",
    route_after_sql,
    {
        "rag_agent": "rag_agent",
        "viz_agent": "viz_agent"
    }
)

builder.add_edge("rag_agent", "viz_agent")
builder.add_edge("viz_agent", "synthesis_agent")
builder.add_edge("synthesis_agent", END)

# Compile Graph
nexus_agent_graph = builder.compile()
logger.info("[LangGraph] NexusData Agent Workflow compiled successfully.")