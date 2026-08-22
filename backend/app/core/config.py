from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "NexusData AI Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # LLM Settings
    LLM_PROVIDER: str = "openai"  # openai, gemini, anthropic, ollama, mock
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_REASONING_MODEL: str = "gpt-4o"
    
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b"
    
    # Data Engine Settings (DATA-01)
    DATABASE_PATH: str = "E:/nexusdata-ai/backend/app/data/sample_dw.duckdb"
    MAX_QUERY_SCAN_LIMIT_MB: int = 100
    ENABLE_HITL_FOR_HIGH_COST: bool = True
    
    # RAG & Vector Engine Settings (AIP-04)
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    RERANKER_MODEL: str = "BAAI/bge-reranker-base"
    DEFAULT_CHUNK_SIZE: int = 512
    DEFAULT_CHUNK_OVERLAP: int = 64
    
    # Security & RBAC
    JWT_SECRET_KEY: str = "nexusdata_super_secret_jwt_key_2026_change_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # GateKV Infrastructure & KV-Cache Optimization Settings
    ENABLE_GATEKV: bool = True
    GATEKV_DEFAULT_RETENTION_RATIO: float = 0.65  # Retain 65% on average (35% overall VRAM savings)
    GATEKV_SENSITIVE_LAYERS: list = [1, 2, 3]    # Early layers protected from aggressive eviction
    GATEKV_DEEP_LAYER_EVICTION_RATIO: float = 0.35 # Retain only 35% in deep layers (65% pruned)
    
    # Observability
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    LANGFUSE_SECRET_KEY: Optional[str] = None
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    class Config:
        env_file = "E:/nexusdata-ai/.env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
