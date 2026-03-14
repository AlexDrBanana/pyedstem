"""Course-related Ed Stem API resources."""

from __future__ import annotations

from typing import Any

from pyedstem.models import CourseInfo, CurrentUserResponse, UserSummary
from pyedstem.transport import EdStemTransport


class Courses:
    """Access course endpoints and common derived course views."""

    def __init__(self, transport: EdStemTransport) -> None:
        self._transport = transport

    def list_active(self) -> list[CourseInfo]:
        """Return only courses marked active by Ed."""
        payload = self._transport.get_json("/user")
        current_user = CurrentUserResponse.model_validate(payload)
        return [
            enrollment.course
            for enrollment in current_user.courses
            if enrollment.course.status == "active"
        ]

    def get(self, course_id: int) -> CourseInfo:
        """Fetch detailed metadata for one course."""
        payload = self._transport.get_json(f"/courses/{course_id}")
        return CourseInfo.model_validate(payload["course"])

    def get_admin(self, course_id: int) -> dict[str, Any]:
        """Fetch course admin metadata."""
        return self._transport.get_json(f"/courses/{course_id}/admin")

    def list_users(
        self, course_id: int, *, limit: int | None = None
    ) -> list[UserSummary]:
        """List users enrolled in a course."""
        params = {"limit": limit} if limit is not None else None
        payload = self._transport.get_json(f"/courses/{course_id}/users", params=params)
        return [UserSummary.model_validate(item) for item in payload.get("users", [])]

    def list_labs(self, course_id: int) -> list[dict[str, Any]]:
        """List course labs/tutorials."""
        payload = self._transport.get_json(f"/courses/{course_id}/labs")
        return payload.get("labs", [])

    def list_groups(self, course_id: int) -> list[dict[str, Any]]:
        """List course groups."""
        payload = self._transport.get_json(f"/courses/{course_id}/groups")
        return payload.get("groups", [])

    def get_stats(self, course_id: int) -> dict[str, Any]:
        """Fetch high-level course stats."""
        payload = self._transport.get_json(f"/courses/{course_id}/stats")
        return payload.get("stats", {})

    def list_resources(self, course_id: int) -> list[dict[str, Any]]:
        """List course resources."""
        payload = self._transport.get_json(f"/courses/{course_id}/resources")
        return payload.get("resources", [])

    def list_bots(self, course_id: int) -> list[dict[str, Any]]:
        """List course AI bots."""
        payload = self._transport.get_json(f"/courses/{course_id}/bots")
        return payload.get("bots", [])

    def list_workspaces(self, course_id: int) -> dict[str, Any]:
        """List course workspace metadata."""
        return self._transport.get_json(f"/courses/{course_id}/workspaces")
