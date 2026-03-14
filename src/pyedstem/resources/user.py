"""User-related Ed Stem API resources."""

from __future__ import annotations

from pyedstem.models import CurrentUserResponse
from pyedstem.transport import EdStemTransport


class User:
    """Access user-centric Ed endpoints for the authenticated account."""

    def __init__(self, transport: EdStemTransport) -> None:
        self._transport = transport

    def get_current_user(self) -> CurrentUserResponse:
        """Fetch the authenticated user profile and enrollments.

        Returns:
            A validated ``CurrentUserResponse`` model containing the current
            user plus enrolled courses.
        """
        payload = self._transport.get_json("/user")
        return CurrentUserResponse.model_validate(payload)

    def list_tokens(self) -> list[dict]:
        """List API tokens visible to the authenticated user.

        Returns:
            A list of raw token dictionaries returned by Ed.
        """
        payload = self._transport.get_json("/user/tokens")
        return payload.get("tokens", [])

    def get_activity(
        self,
        user_id: int,
        *,
        course_id: int,
        limit: int,
        filter_by: str,
    ) -> list[dict]:
        """Fetch recent activity for one user in a course.

        Args:
            user_id: Numeric Ed user identifier.
            course_id: Numeric Ed course identifier used to scope the activity.
            limit: Maximum number of activity items to request.
            filter_by: Ed activity filter string forwarded as the ``filter``
                query parameter.

        Returns:
            A list of raw activity item dictionaries.
        """
        payload = self._transport.get_json(
            f"/users/{user_id}/profile/activity",
            params={"courseID": course_id, "limit": limit, "filter": filter_by},
        )
        return payload.get("items", [])
