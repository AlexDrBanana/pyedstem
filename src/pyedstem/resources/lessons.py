"""Lesson-related Ed Stem API resources."""

from __future__ import annotations

from typing import Any, Dict, List

from pyedstem.models import LessonDetail, LessonSummary, SlideSummary
from pyedstem.transport import EdStemTransport


class LessonsResource:
    """Access lessons, slides, and lesson-derived endpoints."""

    def __init__(self, transport: EdStemTransport) -> None:
        self._transport = transport

    def list(self, course_id: int) -> List[LessonSummary]:
        """List lessons for a course."""
        payload = self._transport.get_json(f"/courses/{course_id}/lessons")
        return [
            LessonSummary.model_validate(item) for item in payload.get("lessons", [])
        ]

    def get(self, lesson_id: int) -> LessonDetail:
        """Fetch full lesson details including slides."""
        payload = self._transport.get_json(f"/lessons/{lesson_id}")
        return LessonDetail.model_validate(payload["lesson"])

    def list_slides(self, lesson_id: int) -> List[SlideSummary]:
        """List slides for a lesson."""
        payload = self._transport.get_json(f"/lessons/{lesson_id}/slides")
        return [SlideSummary.model_validate(item) for item in payload.get("slides", [])]

    def list_results(
        self,
        lesson_id: int,
        *,
        user_id: int | None = None,
        limit: int | None = None,
    ) -> List[Dict[str, Any]]:
        """Fetch lesson result rows."""
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        if limit is not None:
            params["limit"] = limit
        payload = self._transport.get_json(
            f"/lessons/{lesson_id}/results", params=params
        )
        if isinstance(payload, list):
            return payload
        return payload.get("results", [])

    def get_activity(self, lesson_id: int) -> dict[str, Any]:
        """Fetch lesson activity logs."""
        return self._transport.get_json(f"/lessons/{lesson_id}/activity")

    def get_slide(self, slide_id: int) -> SlideSummary:
        """Fetch one slide by ID."""
        payload = self._transport.get_json(f"/lessons/slides/{slide_id}")
        return SlideSummary.model_validate(payload["slide"])

    def get_slide_questions(self, slide_id: int) -> List[Dict[str, Any]]:
        """Fetch quiz questions for one slide."""
        payload = self._transport.get_json(f"/lessons/slides/{slide_id}/questions")
        return payload.get("questions", [])

    def get_slide_results(self, slide_id: int) -> dict[str, Any]:
        """Fetch quiz results for one slide."""
        return self._transport.get_json(f"/lessons/slides/{slide_id}/results")
