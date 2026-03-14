"""Challenge-related Ed Stem API resources."""

from __future__ import annotations

from typing import Any

from pyedstem.transport import EdStemTransport


class Challenges:
    """Access challenge listing endpoints."""

    def __init__(self, transport: EdStemTransport) -> None:
        self._transport = transport

    def list(self, course_id: int) -> list[dict[str, Any]]:
        """List challenges for a course.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            A list of raw challenge dictionaries returned by Ed.
        """
        payload = self._transport.get_json(f"/courses/{course_id}/challenges")
        return payload.get("challenges", [])
