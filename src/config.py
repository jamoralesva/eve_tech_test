from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "jamv_llm_policy_verificator"
    ENVIRONMENT: str = "dev"
    API_V1_STR: str = "/api/v1"
    
    # Configuración de base de datos u otras variables
    # DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()