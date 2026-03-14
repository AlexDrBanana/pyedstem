"""Client-bound workflow helpers built on top of the core resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pyedstem.models import ThreadDetail, UserSummary
from pyedstem.workflows import build_staged_thread, list_unanswered_threads

if TYPE_CHECKING:
    from pyedstem.client import EdStemClient


class WorkflowClient:
    """Convenience workflows for common Ed automation tasks."""

    def __init__(self, client: "EdStemClient") -> None:
        self._client = client

    def list_course_unanswered_threads(self, course_id: int) -> list[ThreadDetail]:
        """Fetch unanswered actionable threads and expand them with replies."""
        thread_summaries = list(
            self._client.threads.iter_all(
                course_id,
                filter="unanswered",
                sort="date",
                limit=50,
            )
        )
        users = self._client.courses.list_users(course_id, limit=500)
        users_by_id = {user.id: UserSummary.model_validate(user) for user in users}
        actionable = list_unanswered_threads(
            threads=thread_summaries,
            users_by_id=users_by_id,
        )
        return [self._client.threads.get(thread.id) for thread in actionable]

    def build_staging_payload(self, course_id: int) -> list[tuple[ThreadDetail, str]]:
        """Prepare unanswered threads for markdown staging."""
        staged_threads = []
        for thread in self.list_course_unanswered_threads(course_id):
            staged = build_staged_thread(thread)
            staged_threads.append((staged.thread, staged.markdown_question))
        return staged_threads
