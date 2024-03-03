from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8002
