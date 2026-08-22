from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.engines.gatekv_engine import gatekv_engine
from app.engines.eval_engine import eval_engine
from app.core.config import settings
from loguru import logger

router = APIRouter()

class SimulateRequest(BaseModel):
    prompt: str = Field(
        default="SELECT r.region_name, SUM(o.total_amount) as total_revenue, SUM(o.total_profit) as total_profit FROM orders o JOIN regions r ON o.region_id = r.region_id WHERE o.year = 2025 GROUP BY r.region_name ORDER BY total_revenue DESC;",
        description="Prompt text or Enterprise Schema DDL to simulate KV eviction on"
    )
    target_retention_ratio: Optional[float] = Field(default=0.65, ge=0.1, le=1.0)

@router.get("/stats")
def get_gatekv_stats() -> Dict[str, Any]:
    """
    Returns GateKV optimization overview, VRAM reduction percentages, and architectural specs.
    """
    benchmarks = gatekv_engine.get_enterprise_benchmark_comparison()
    layers = gatekv_engine.compute_layer_sensitivity_curve()
    return {
        "gatekv_enabled": settings.ENABLE_GATEKV,
        "default_retention_ratio": settings.GATEKV_DEFAULT_RETENTION_RATIO,
        "sensitive_protected_layers": settings.GATEKV_SENSITIVE_LAYERS,
        "benchmarks": benchmarks,
        "layer_count": len(layers)
    }

@router.get("/sensitivity-curve")
def get_layer_sensitivity_curve() -> List[Dict[str, Any]]:
    """
    Returns the layer sensitivity profile showing early-layer sensitivity vs deep-layer elasticity.
    """
    return gatekv_engine.compute_layer_sensitivity_curve()

@router.post("/simulate")
def simulate_kv_eviction(req: SimulateRequest) -> Dict[str, Any]:
    """
    Simulates token-level GateKV eviction on an arbitrary prompt (e.g. SQL Schema DDL or RAG chunks).
    """
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt text cannot be empty.")
    
    result = gatekv_engine.simulate_kv_eviction(
        prompt_text=req.prompt,
        target_retention=req.target_retention_ratio
    )
    return result

@router.post("/benchmark")
def run_gatekv_benchmark() -> Dict[str, Any]:
    """
    Runs live benchmark testing Spider SQL & RAGAS fidelity under GateKV compression.
    """
    try:
        return eval_engine.run_gatekv_evaluation()
    except Exception as e:
        logger.error(f"Error running GateKV benchmark: {e}")
        raise HTTPException(status_code=500, detail=str(e))
