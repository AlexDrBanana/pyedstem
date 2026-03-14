"""Course-related Ed Stem API resources."""

from __future__ import annotations

from typing import Any

from pyedstem.models import CourseInfo, CurrentUserResponse, UserSummary
from pyedstem.transport import EdStemTransport


class Courses:
    """Access course endpoints and course-scoped collections.

    Methods on this resource cover both direct course metadata and related
    collections such as enrolled users, labs, groups, resources, bots, and
    workspaces.
    """

    def __init__(self, transport: EdStemTransport) -> None:
        self._transport = transport

    def list_active(self) -> list[CourseInfo]:
        """Return only courses marked active by Ed.

        This method derives its result from the authenticated user's
        ``GET /user`` payload rather than from a dedicated active-courses
        endpoint.

        Returns:
            A list of ``CourseInfo`` objects whose ``status`` is ``"active"``.
        """
        payload = self._transport.get_json("/user")
        current_user = CurrentUserResponse.model_validate(payload)
        return [
            enrollment.course
            for enrollment in current_user.courses
            if enrollment.course.status == "active"
        ]

    def get(self, course_id: int) -> CourseInfo:
        """Fetch detailed metadata for one course.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            A validated ``CourseInfo`` model for the requested course.
        """
        payload = self._transport.get_json(f"/courses/{course_id}")
        return CourseInfo.model_validate(payload["course"])

    def get_admin(self, course_id: int) -> dict[str, Any]:
        """Fetch course admin metadata.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            The decoded JSON payload from ``GET /courses/{course_id}/admin``.
        """
        return self._transport.get_json(f"/courses/{course_id}/admin")

    def list_users(
        self, course_id: int, *, limit: int | None = None
    ) -> list[UserSummary]:
        """List users enrolled in a course.

        Args:
            course_id: Numeric Ed course identifier.
            limit: Optional maximum number of users to request.

        Returns:
            A list of validated ``UserSummary`` models.
        """
        params = {"limit": limit} if limit is not None else None
        payload = self._transport.get_json(f"/courses/{course_id}/users", params=params)
        return [UserSummary.model_validate(item) for item in payload.get("users", [])]

    def list_labs(self, course_id: int) -> list[dict[str, Any]]:
        """List course labs or tutorials.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            A list of lab dictionaries returned by Ed.
        """
        payload = self._transport.get_json(f"/courses/{course_id}/labs")
        return payload.get("labs", [])

    def list_groups(self, course_id: int) -> list[dict[str, Any]]:
        """List course groups.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            A list of group dictionaries returned by Ed.
        """
        payload = self._transport.get_json(f"/courses/{course_id}/groups")
        return payload.get("groups", [])

    def get_stats(self, course_id: int) -> dict[str, Any]:
        """Fetch high-level course statistics.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            The ``stats`` object from the endpoint response, or an empty
            dictionary if the key is absent.
        """
        payload = self._transport.get_json(f"/courses/{course_id}/stats")
        return payload.get("stats", {})

    def list_resources(self, course_id: int) -> list[dict[str, Any]]:
        """List course resources.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            A list of resource dictionaries returned by Ed.
        """
        payload = self._transport.get_json(f"/courses/{course_id}/resources")
        return payload.get("resources", [])

    def list_bots(self, course_id: int) -> list[dict[str, Any]]:
        """List course AI bots.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            A list of bot dictionaries returned by Ed.
        """
        payload = self._transport.get_json(f"/courses/{course_id}/bots")
        return payload.get("bots", [])

    def list_workspaces(self, course_id: int) -> dict[str, Any]:
        """List course workspace metadata.

        Args:
            course_id: Numeric Ed course identifier.

        Returns:
            The decoded JSON response from the workspaces endpoint.
        """
        return self._transport.get_json(f"/courses/{course_id}/workspaces")
