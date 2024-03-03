from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    host: str = "0.0.0.0"  # noqa: S104
    port: int = 8002
