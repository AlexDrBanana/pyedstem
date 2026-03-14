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
    """High-level synchronous client for the Ed Stem API.

    This is the main entry point for the library. It owns a shared HTTP
    transport and exposes grouped resource clients for the supported endpoint
    areas, such as courses, threads, lessons, analytics, challenges, and the
    authenticated user.

    Args:
        api_token: Ed Stem API bearer token.
        base_url: Base URL for the Ed Stem API. Defaults to the public hosted
            API endpoint.
        timeout_seconds: Request timeout applied to the underlying HTTP client.
        http_client: Optional preconfigured ``httpx.Client``. When provided,
            it is used directly instead of constructing a new client.

    Attributes:
        user: User-related endpoints.
        courses: Course metadata and course-scoped collections.
        threads: Discussion thread listing, search, detail lookup, and answer
            posting.
        lessons: Lesson, slide, and result endpoints.
        analytics: Course analytics endpoints.
        challenges: Course challenge listing endpoints.
    """

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
        """Create a client from environment-backed settings.

        The settings are loaded from ``EDSTEM_*`` environment variables and,
        by default, from a local ``.env`` file.

        Returns:
            A configured ``EdStemClient`` instance.

        Raises:
            pydantic.ValidationError: If required settings such as
                ``EDSTEM_API_TOKEN`` are missing or invalid.
        """
        settings = get_settings()
        return cls(
            api_token=settings.api_token.get_secret_value(),
            base_url=settings.base_url,
            timeout_seconds=settings.timeout_seconds,
        )

    def close(self) -> None:
        """Close the underlying HTTP transport.

        Call this method when the client is no longer needed, unless the client
        is already being managed via a ``with`` statement.
        """
        self._transport.close()

    def get_json(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Perform a raw JSON ``GET`` request for less common endpoints.

        This is a convenience escape hatch for endpoints that are not yet
        wrapped by a first-class resource method.

        Args:
            path: API path relative to the configured base URL, for example
                ``"/courses/123/resources"``.
            params: Optional query-string parameters.

        Returns:
            The decoded JSON response body as a dictionary.

        Raises:
            AuthenticationError: If the API token is rejected.
            NotFoundError: If the requested endpoint or resource does not
                exist.
            RateLimitError: If the API rate-limits the request.
            ValidationError: If Ed rejects the request as invalid.
            ServerError: If Ed returns a server-side failure.
        """
        return self._transport.get_json(path, params=params)

    def __enter__(self) -> "EdStemClient":
        """Enter a context-managed client session.

        Returns:
            The current client instance.
        """
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        """Close HTTP resources when leaving a context manager.

        Args:
            exc_type: Exception type raised inside the context, if any.
            exc: Exception instance raised inside the context, if any.
            tb: Traceback associated with the exception, if any.
        """
        self.close()
