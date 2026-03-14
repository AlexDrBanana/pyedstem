"""Analytics-related Ed Stem API resources."""

from __future__ import annotations

from typing import Any

from pyedstem.transport import EdStemTransport


class AnalyticsResource:
    """Access course analytics endpoints."""

    def __init__(self, transport: EdStemTransport) -> None:
        self._transport = transport

    def get_users(self, course_id: int) -> list[dict[str, Any]]:
        """Fetch user analytics rows."""
        payload = self._transport.get_json(f"/courses/{course_id}/analytics/users")
        return payload.get("users", [])

    def get_discussion(self, course_id: int) -> dict[str, Any]:
        """Fetch discussion analytics."""
        return self._transport.get_json(f"/courses/{course_id}/analytics/discussion")

    def get_challenges(self, course_id: int) -> dict[str, Any]:
        """Fetch challenge analytics."""
        return self._transport.get_json(f"/courses/{course_id}/analytics/challenges")
