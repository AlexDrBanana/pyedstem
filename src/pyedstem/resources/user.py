"""User-related Ed Stem API resources."""

from __future__ import annotations

from pyedstem.models import CurrentUserResponse
from pyedstem.transport import EdStemTransport


class UserResource:
    """Access user-centric Ed endpoints."""

    def __init__(self, transport: EdStemTransport) -> None:
        self._transport = transport

    def get_current_user(self) -> CurrentUserResponse:
        """Fetch the authenticated user profile and enrollments."""
        payload = self._transport.get_json("/user")
        return CurrentUserResponse.model_validate(payload)

    def list_tokens(self) -> list[dict]:
        """List API tokens visible to the authenticated user."""
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
        """Fetch recent activity for one user in a course."""
        payload = self._transport.get_json(
            f"/users/{user_id}/profile/activity",
            params={"courseID": course_id, "limit": limit, "filter": filter_by},
        )
        return payload.get("items", [])
