"""Higher-level workflow helpers for common Ed automation tasks."""

from __future__ import annotations

import re
from dataclasses import dataclass

from pyedstem.content import html_to_markdown
from pyedstem.models import (
    CourseEnrollment,
    CourseInfo,
    ThreadDetail,
    ThreadSummary,
    UserSummary,
)

STAFF_ROLES = {"admin", "tutor", "instructor", "moderator", "staff"}
_RECRUITMENT_RE = re.compile(
    r"looking for (group|team)|join my group|need group members|need teammates",
    re.IGNORECASE,
)


def get_active_courses(enrollments: list[CourseEnrollment]) -> list[CourseInfo]:
    """Return only courses whose Ed status is active."""
    return [
        enrollment.course
        for enrollment in enrollments
        if enrollment.course.status == "active"
    ]


def list_unanswered_threads(
    *,
    threads: list[ThreadSummary],
    users_by_id: dict[int, UserSummary],
) -> list[ThreadSummary]:
    """Filter thread pages down to actionable unanswered student questions."""
    actionable: list[ThreadSummary] = []

    for thread in threads:
        user = users_by_id.get(thread.user_id)
        role = (user.role or "").lower() if user else ""
        searchable_text = f"{thread.title}\n{thread.content or ''}"

        if thread.is_answered or thread.is_staff_answered:
            continue
        if thread.deleted_at is not None:
            continue
        if thread.type != "question":
            continue
        if role in STAFF_ROLES:
            continue
        if _RECRUITMENT_RE.search(searchable_text):
            continue

        actionable.append(thread)

    return actionable


@dataclass(frozen=True)
class StagedThread:
    """Content prepared for the unanswered-thread markdown staging file."""

    thread: ThreadDetail
    markdown_question: str


def build_staged_thread(thread: ThreadDetail) -> StagedThread:
    """Convert a thread's HTML body into markdown for offline drafting."""
    return StagedThread(
        thread=thread, markdown_question=html_to_markdown(thread.content or "")
    )
