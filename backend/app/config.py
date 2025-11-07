from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables and defaults."""
    app_name: str = "WhatsApp Appointment Scheduler"
    database_url: str = "sqlite:///./appointments.db"
    whatsapp_from_number: str = ""
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    reminder_lead_minutes: int = 60
    reminder_check_interval_minutes: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance so the app reads env vars once."""

    return Settings()

