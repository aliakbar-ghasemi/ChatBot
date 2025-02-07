from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Chat API"
    API_VERSION: str = "v1"
    HOST: str = "127.0.0.1"
    PORT: int = 8072
    DEBUG: bool = True

    # Ollama Model Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # CORS Settings
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"  # Load environment variables from a .env file

# Create a settings instance
settings = Settings()
