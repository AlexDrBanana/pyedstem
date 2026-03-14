"""Analytics-related Ed Stem API resources."""

from __future__ import annotations

from typing import Any

from pyedstem.transport import EdStemTransport


class Analytics:
    """Access course analytics endpoints.

    These endpoints return lightly structured analytics payloads, so the
    methods currently expose raw dictionaries and lists.
    """

    def __init__(self, transport: EdStemTransport) -> None:
        self._transport = transport

    def get_users(self, course_id: int) -> list[dict[str, Any]]:
        """Fetch user analytics rows.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            A list of raw user analytics rows.
        """
        payload = self._transport.get_json(f"/courses/{course_id}/analytics/users")
        return payload.get("users", [])

    def get_discussion(self, course_id: int) -> dict[str, Any]:
        """Fetch discussion analytics.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            The decoded JSON payload for course discussion analytics.
        """
        return self._transport.get_json(f"/courses/{course_id}/analytics/discussion")

    def get_challenges(self, course_id: int) -> dict[str, Any]:
        """Fetch challenge analytics.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            The decoded JSON payload for course challenge analytics.
        """
        return self._transport.get_json(f"/courses/{course_id}/analytics/challenges")
