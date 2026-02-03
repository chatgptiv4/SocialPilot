from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "SocialPilot AI"
    api_v1_prefix: str = "/api"

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/socialpilot"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7

    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"

    redis_url: str = "redis://localhost:6379/0"

    media_root: str = "media"


settings = Settings()
