from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openrouter_api_key: str
    langsmith_api_key: str

    models: list[str] = [
        "meta-llama/llama-3.1-8b-instruct",
        "openai/gpt-oss-20b",
        "nvidia/nemotron-3-super-120b-a12b:free"
        ]

    http_referer: str = "some.web.site"
    x_title: str = "Testing chat agent"
    provider: dict = dict(sort=dict(by="price", partition="none"))
    temperature: float = 0.2

    # loading .env
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
