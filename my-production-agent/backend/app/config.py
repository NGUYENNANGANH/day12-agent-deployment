from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Production AI Agent"
    app_version: str = "1.0.0"
    environment: str = "production"
    
    # Server config
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    allowed_origins: list[str] = ["*"]

    # External services
    redis_url: str = "redis://redis:6379/0"
    
    # Security
    agent_api_key: str = "my-super-secret-key"
    openai_api_key: str | None = None
    google_maps_api_key: str | None = None
    
    # Logic configs
    rate_limit_per_minute: int = 10
    monthly_budget_usd: float = 10.0
    
    # Mock LLM settings
    llm_model: str = "gpt-4o-mini" # Default to a real model name

    class Config:
        env_file = ".env"

settings = Settings()
