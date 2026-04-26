from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Gemini API key
    GEMINI_API_KEY: str

    # Embedding model
    EMBEDDING_MODEL_ID: str = "models/gemini-embedding-exp-03-07"
    EMBEDDING_MODEL_SIZE: int = 3072

    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_JWT_SECRET: str

    # Redis
    REDIS_URL: str

    # Qdrant
    QDRANT_API_KEY: str
    QDRANT_HOST: str

    # Service URLs
    FILE_PROCESSOR_URL: str
    AGENT_SERVICE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()