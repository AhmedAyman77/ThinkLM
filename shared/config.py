from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_JWT_SECRET: str

    # Redis
    REDIS_URL: str

    # Qdrant
    QDRANT_API_KEY: str
    QDRANT_HOST: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()