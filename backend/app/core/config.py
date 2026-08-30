from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_env: str

    debug: bool

    host: str
    port: int

    llm_provider: str
    llm_api_key: str
    llm_base_url: str
    llm_model: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()