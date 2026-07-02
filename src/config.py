from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "jamv_llm_policy_verificator"
    ENVIRONMENT: str = "dev"
    API_V1_STR: str = "/api/v1"
    MODEL_NAME: str = "llama3.2:3b"
    LOW_CONFIDENCE_THRESHOLD_ALLOW: float = 0.5
    LOW_CONFIDENCE_THRESHOLD_BLOCK: float = 0.2
    
    # Configuración de base de datos u otras variables
    # DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()