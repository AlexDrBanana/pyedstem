"""Top-level client for the Ed Stem API."""

from __future__ import annotations

from typing import Any

import httpx

from pyedstem.config import get_settings
from pyedstem.resources.analytics import Analytics
from pyedstem.resources.challenges import Challenges
from pyedstem.resources.courses import Courses
from pyedstem.resources.lessons import Lessons
from pyedstem.resources.threads import Threads
from pyedstem.resources.user import User
from pyedstem.transport import EdStemTransport


class EdStemClient:
    """High-level sync client for the Ed Stem API."""

    def __init__(
        self,
        *,
        api_token: str,
        base_url: str = "https://edstem.org/api",
        timeout_seconds: float = 30.0,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._transport = EdStemTransport(
            api_token=api_token,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            client=http_client,
        )
        self.user = User(self._transport)
        self.courses = Courses(self._transport)
        self.threads = Threads(self._transport)
        self.lessons = Lessons(self._transport)
        self.analytics = Analytics(self._transport)
        self.challenges = Challenges(self._transport)

    @classmethod
    def from_env(cls) -> "EdStemClient":
        """Create a client from environment configuration."""
        settings = get_settings()
        return cls(
            api_token=settings.api_token.get_secret_value(),
            base_url=settings.base_url,
            timeout_seconds=settings.timeout_seconds,
        )

    def close(self) -> None:
        """Close the underlying HTTP transport."""
        self._transport.close()

    def get_json(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Perform a raw JSON GET request for less common endpoints."""
        return self._transport.get_json(path, params=params)

    def __enter__(self) -> "EdStemClient":
        """Enter a context-managed client session."""
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        """Always close HTTP resources when leaving a context manager."""
        self.close()
