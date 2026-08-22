import pytest
import sys
import os

sys.path.insert(0, "E:/nexusdata-ai/backend")

from app.engines.sql_engine import sql_engine
from app.engines.rag_engine import rag_engine
from app.engines.eval_engine import eval_engine
from app.agents.graph import nexus_agent_graph
from app.agents.state import AgentState

def test_sql_validator_and_linter():
    # 1. Valid SELECT query
    is_valid, cleaned, err = sql_engine.validate_and_lint_sql("SELECT region_name, SUM(total_amount) FROM orders JOIN regions ON orders.region_id = regions.region_id GROUP BY region_name;")
    assert is_valid is True
    assert err is None

    # 2. Destructive query blocking (Security Linter)
    is_valid_drop, _, err_drop = sql_engine.validate_and_lint_sql("DROP TABLE customers;")
    assert is_valid_drop is False
    assert "Security Violation" in err_drop

def test_sql_execution():
    df, err = sql_engine.execute_query("SELECT * FROM regions ORDER BY region_id;")
    assert err is None
    assert df is not None
    assert len(df) == 4
    assert "region_name" in df.columns

def test_rag_hybrid_search():
    results = rag_engine.hybrid_search("chiết khấu đại lý cấp 1", top_k=2)
    assert len(results) > 0
    assert any("chinh_sach_chiet_khau" in r["doc_name"] for r in results)
    assert "citation" in results[0]

def test_eval_engine_spider_and_ragas():
    spider_res = eval_engine.run_sql_spider_evaluation()
    assert "execution_accuracy_percent" in spider_res
    assert spider_res["execution_accuracy_percent"] >= 80.0

    ragas_res = eval_engine.run_ragas_evaluation()
    assert "ragas_overall_score" in ragas_res
    assert ragas_res["ragas_overall_score"] >= 0.85

def test_auto_tuning_grid_search():
    tune_res = eval_engine.run_auto_tuning_grid_search()
    assert "recommended_optimal_config" in tune_res
    assert len(tune_res["all_pareto_experiments"]) == 3

def test_full_agent_graph_execution():
    state: AgentState = {
        "user_query": "Doanh thu theo từng khu vực",
        "user_role": "analyst",
        "session_id": "test_session",
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
    assert result["intent"] in ["SQL_ONLY", "HYBRID_ANALYTICS"]
    assert result["sql_query"] is not None
    assert len(result["query_result_data"]) > 0
    assert len(result["chart_schemas"]) > 0