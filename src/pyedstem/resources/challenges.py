"""Challenge-related Ed Stem API resources."""

from __future__ import annotations

from typing import Any

from pyedstem.transport import EdStemTransport


class ChallengesResource:
    """Access challenge listing endpoints."""

    def __init__(self, transport: EdStemTransport) -> None:
        self._transport = transport

    def list(self, course_id: int) -> list[dict[str, Any]]:
        """List challenges for a course."""
        payload = self._transport.get_json(f"/courses/{course_id}/challenges")
        return payload.get("challenges", [])
