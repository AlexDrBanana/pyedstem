"""Thread-related Ed Stem API resources."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, List

from pyedstem.content import markdown_to_ed_document
from pyedstem.models import PostedComment, ThreadDetail, ThreadSummary
from pyedstem.transport import EdStemTransport


class ThreadsResource:
    """Access thread listing, details, and answer posting."""

    def __init__(self, transport: EdStemTransport) -> None:
        self._transport = transport

    def list(
        self,
        course_id: int,
        *,
        limit: int = 20,
        offset: int = 0,
        sort: str = "date",
        **filters: Any,
    ) -> List[ThreadSummary]:
        """Fetch a page of threads for a course."""
        params = {"limit": limit, "offset": offset, "sort": sort, **filters}
        payload = self._transport.get_json(
            f"/courses/{course_id}/threads", params=params
        )
        return [
            ThreadSummary.model_validate(item) for item in payload.get("threads", [])
        ]

    def iter_all(
        self,
        course_id: int,
        *,
        limit: int = 50,
        sort: str = "date",
        **filters: Any,
    ) -> Iterator[ThreadSummary]:
        """Iterate through paginated thread results."""
        offset = 0

        while True:
            batch = self.list(
                course_id,
                limit=limit,
                offset=offset,
                sort=sort,
                **filters,
            )
            if not batch:
                return

            for thread in batch:
                yield thread

            if len(batch) < limit:
                return

            offset += limit

    def get(self, thread_id: int) -> ThreadDetail:
        """Fetch full details for one thread."""
        payload = self._transport.get_json(f"/threads/{thread_id}")
        return ThreadDetail.model_validate(payload["thread"])

    def get_by_number(self, course_id: int, thread_number: int) -> ThreadDetail:
        """Fetch a course thread by its local number."""
        payload = self._transport.get_json(
            f"/courses/{course_id}/threads/{thread_number}"
        )
        return ThreadDetail.model_validate(payload["thread"])

    def search(self, course_id: int, *, query: str) -> List[ThreadSummary]:
        """Search for threads in a course."""
        payload = self._transport.get_json(
            f"/courses/{course_id}/threads/search",
            params={"query": query},
        )
        return [
            ThreadSummary.model_validate(item) for item in payload.get("threads", [])
        ]

    def post_answer(
        self,
        *,
        thread_id: int,
        markdown: str,
        is_anonymous: bool = False,
        is_private: bool = False,
    ) -> PostedComment:
        """Post an Ed XML answer to a thread."""
        payload = self._transport.post_json(
            f"/threads/{thread_id}/comments",
            json_body={
                "comment": {
                    "type": "answer",
                    "content": markdown_to_ed_document(markdown),
                    "is_anonymous": is_anonymous,
                    "is_private": is_private,
                }
            },
        )
        comment_payload = payload.get("comment") or payload.get("answer") or payload
        return PostedComment.model_validate(comment_payload)
