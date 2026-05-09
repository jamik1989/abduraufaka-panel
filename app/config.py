from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./abduraufaka_panel.db"
    secret_key: str = "change-me-super-secret"
    admin_username: str = "admin"
    admin_password: str = "12345"
    app_title: str = "Abduraufaka Panel"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
