import pandas as pd
from app.agents.state import AgentState
from app.engines.viz_engine import viz_engine
from loguru import logger

def viz_agent_node(state: AgentState) -> AgentState:
    """
    DATA-16 Visualization & Chart recommendation node.
    """
    query_data = state.get("query_result_data")
    if not query_data:
        state["chart_schemas"] = []
        return state

    df = pd.DataFrame(query_data)
    charts = viz_engine.recommend_and_build_charts(df, title="Kết Quả Phân Tích Dữ Liệu")
    state["chart_schemas"] = charts

    logger.info(f"[Viz Agent] Generated {len(charts)} chart schemas.")
    return state