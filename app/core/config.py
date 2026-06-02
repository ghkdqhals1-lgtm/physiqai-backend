from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    app_secret_key: str = "changeme"
    app_debug: bool = True

    database_url: str = ""

    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_key: str = ""

    anthropic_api_key: str = ""

    jwt_secret_key: str = "changeme"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
