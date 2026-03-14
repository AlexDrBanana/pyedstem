"""Thread-related Ed Stem API resources."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, List

from pyedstem.content import markdown_to_ed_document
from pyedstem.models import PostedComment, ThreadDetail, ThreadSummary
from pyedstem.transport import EdStemTransport


class Threads:
    """Access discussion thread listing, search, detail, and answer posting.

    This resource wraps the main discussion endpoints used for reading course
    threads and posting staff answers.
    """

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
        """Fetch one page of threads for a course.

        Args:
            course_id: Numeric Ed course identifier.
            limit: Maximum number of threads to return.
            offset: Pagination offset for the result page.
            sort: Sort mode understood by Ed, such as ``"date"``.
            **filters: Additional query-string filters forwarded directly to
                the endpoint, for example ``filter="unanswered"``.

        Returns:
            A list of validated ``ThreadSummary`` models.
        """
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
        """Iterate through all available paginated thread results.

        Args:
            course_id: Numeric Ed course identifier.
            limit: Page size for each underlying list request.
            sort: Sort mode understood by Ed, such as ``"date"``.
            **filters: Additional query-string filters forwarded directly to
                each list request.

        Yields:
            ``ThreadSummary`` objects one at a time until the endpoint is
            exhausted.
        """
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
        """Fetch full details for one thread.

        Args:
            thread_id: Global Ed thread identifier.

        Returns:
            A validated ``ThreadDetail`` model including answers and comments.
        """
        payload = self._transport.get_json(f"/threads/{thread_id}")
        return ThreadDetail.model_validate(payload["thread"])

    def get_by_number(self, course_id: int, thread_number: int) -> ThreadDetail:
        """Fetch a course thread by its course-local thread number.

        Args:
            course_id: Numeric Ed course identifier.
            thread_number: Thread number as displayed within the course.

        Returns:
            A validated ``ThreadDetail`` model for the matching thread.
        """
        payload = self._transport.get_json(
            f"/courses/{course_id}/threads/{thread_number}"
        )
        return ThreadDetail.model_validate(payload["thread"])

    def search(self, course_id: int, *, query: str) -> List[ThreadSummary]:
        """Search for threads in a course.

        Args:
            course_id: Numeric Ed course identifier.
            query: Free-text search string.

        Returns:
            A list of validated ``ThreadSummary`` models matching the query.
        """
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
        """Post an answer to a thread using markdown input.

        The markdown is converted into the XML document format expected by the
        Ed comments endpoint.

        Args:
            thread_id: Global Ed thread identifier.
            markdown: Answer body written in markdown.
            is_anonymous: Whether the answer should be posted anonymously.
            is_private: Whether the answer should be visible only to staff and
                the thread author.

        Returns:
            A validated ``PostedComment`` model representing the created
            answer or comment object returned by Ed.
        """
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
