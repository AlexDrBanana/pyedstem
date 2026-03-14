"""Helpers for discovering live IDs for endpoint contract tests."""

from __future__ import annotations

import re
from dataclasses import dataclass

from pyedstem.client import EdStemClient


@dataclass(frozen=True)
class LiveEndpointContext:
    """Reusable live IDs resolved from the current Ed account."""

    course_id: int
    lesson_id: int
    quiz_slide_id: int | None
    slide_id: int
    thread_id: int
    thread_number: int
    thread_search_query: str
    user_id: int


def gather_live_context(client: EdStemClient) -> LiveEndpointContext:
    """Resolve one consistent set of live IDs for contract tests."""
    current_user = client.user.get_current_user()
    active_courses = client.courses.list_active()
    course = active_courses[0] if active_courses else current_user.courses[0].course

    threads = client.threads.list(course.id, limit=20)
    if not threads:
        raise RuntimeError(f"No threads found for course {course.id}.")

    thread = threads[0]
    search_query = _derive_search_query(thread.title or course.code or str(course.id))

    lessons = client.lessons.list(course.id)
    if not lessons:
        raise RuntimeError(f"No lessons found for course {course.id}.")

    lesson_id, slide_id, quiz_slide_id = _discover_lesson_and_slide_ids(client, lessons)

    return LiveEndpointContext(
        course_id=course.id,
        lesson_id=lesson_id,
        quiz_slide_id=quiz_slide_id,
        slide_id=slide_id,
        thread_id=thread.id,
        thread_number=thread.number,
        thread_search_query=search_query,
        user_id=current_user.user.id,
    )


def _discover_lesson_and_slide_ids(
    client: EdStemClient,
    lessons: list,
) -> tuple[int, int, int | None]:
    """Find at least one lesson, one slide, and preferably one quiz slide."""
    fallback_lesson_id: int | None = None
    fallback_slide_id: int | None = None
    quiz_slide_id: int | None = None

    for lesson_summary in lessons:
        lesson = client.lessons.get(lesson_summary.id)
        if fallback_lesson_id is None:
            fallback_lesson_id = lesson.id
        for slide in lesson.slides:
            if fallback_slide_id is None:
                fallback_slide_id = slide.id
            if slide.type == "quiz":
                return lesson.id, slide.id, slide.id

    if fallback_lesson_id is None or fallback_slide_id is None:
        raise RuntimeError("No usable lesson slides found for live contract tests.")

    return fallback_lesson_id, fallback_slide_id, quiz_slide_id


def _derive_search_query(text: str) -> str:
    """Choose a short query that should match the chosen thread title."""
    tokens = [token for token in re.split(r"\W+", text) if len(token) >= 4]
    if tokens:
        return tokens[0]
    return text.strip() or "course"
