from fastapi import APIRouter
from app.engines.eval_engine import eval_engine

router = APIRouter()

@router.get("/ragas")
def run_ragas():
    return eval_engine.run_ragas_evaluation()

@router.get("/spider")
def run_spider():
    return eval_engine.run_sql_spider_evaluation()

@router.post("/auto-tune")
def run_auto_tuning():
    return eval_engine.run_auto_tuning_grid_search()