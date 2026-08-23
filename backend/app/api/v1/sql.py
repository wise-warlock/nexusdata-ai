from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.engines.sql_engine import sql_engine
from app.engines.eval_engine import eval_engine

router = APIRouter()

class SQLExecuteRequest(BaseModel):
    sql_query: str
    max_rows: Optional[int] = 100

class SQLExecuteResponse(BaseModel):
    is_valid: bool
    cleaned_sql: Optional[str]
    error: Optional[str]
    estimated_bytes: int
    data: Optional[List[Dict[str, Any]]]
    columns: Optional[List[str]]

@router.post("/query", response_model=SQLExecuteResponse)
def execute_sql(req: SQLExecuteRequest):
    is_valid, cleaned, err = sql_engine.validate_and_lint_sql(req.sql_query)
    if not is_valid:
        return SQLExecuteResponse(
            is_valid=False, cleaned_sql=None, error=err,
            estimated_bytes=0, data=None, columns=None
        )

    cost_info = sql_engine.estimate_bytes_and_cost(cleaned)
    df, exec_err = sql_engine.execute_query(cleaned, max_rows=req.max_rows or 100)

    if exec_err:
        return SQLExecuteResponse(
            is_valid=True, cleaned_sql=cleaned, error=exec_err,
            estimated_bytes=cost_info["estimated_bytes"], data=None, columns=None
        )

    return SQLExecuteResponse(
        is_valid=True, cleaned_sql=cleaned, error=None,
        estimated_bytes=cost_info["estimated_bytes"],
        data=df.to_dict(orient="records") if df is not None else [],
        columns=list(df.columns) if df is not None else []
    )

@router.get("/schema")
def get_schema():
    con = sql_engine.get_connection()
    tables = con.execute("SHOW TABLES;").fetchall()
    schema_details = {}
    for (tname,) in tables:
        cols = con.execute(f"DESCRIBE {tname};").fetchall()
        schema_details[tname] = [{"name": c[0], "type": c[1]} for c in cols]
    con.close()
    return {"tables": schema_details}

@router.get("/benchmark/spider")
def get_spider_benchmark():
    return eval_engine.run_sql_spider_evaluation()