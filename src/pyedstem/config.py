"""Configuration helpers for pyedstem."""

from __future__ import annotations

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EdStemSettings(BaseSettings):
    """Environment-backed settings for the Ed Stem API client."""

    api_token: SecretStr
    base_url: str = "https://edstem.org/api"
    timeout_seconds: float = 30.0

    model_config = SettingsConfigDict(
        env_prefix="EDSTEM_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> EdStemSettings:
    """Load and cache environment-backed settings for the client."""
    return EdStemSettings()
