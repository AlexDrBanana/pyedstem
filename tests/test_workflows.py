"""Tests for unanswered-thread workflow helpers."""

from __future__ import annotations

from pyedstem.models import CourseEnrollment, CourseInfo, ThreadSummary, UserSummary
from pyedstem.workflows import get_active_courses, list_unanswered_threads


def test_get_active_courses_filters_on_course_status() -> None:
    """Only Ed courses marked active should be returned for active-course scans."""
    enrollments = [
        CourseEnrollment(
            course=CourseInfo(id=1, code="QBUS6860", name="Active", status="active"),
            role="admin",
            lab=None,
            last_active=None,
        ),
        CourseEnrollment(
            course=CourseInfo(
                id=2, code="QBUS6600", name="Archived", status="archived"
            ),
            role="admin",
            lab=None,
            last_active=None,
        ),
    ]

    active_courses = get_active_courses(enrollments)

    assert [course.id for course in active_courses] == [1]


def test_list_unanswered_threads_excludes_staff_and_recruitment_posts() -> None:
    """Workflow helper should keep only actionable student-authored questions."""
    threads = [
        ThreadSummary(
            id=101,
            number=7,
            course_id=9,
            title="Need help with assignment",
            type="question",
            category="General",
            content="<p>Can someone explain the rubric?</p>",
            user_id=1,
            is_answered=False,
            is_staff_answered=False,
            deleted_at=None,
            created_at="2026-03-14T00:00:00Z",
        ),
        ThreadSummary(
            id=102,
            number=8,
            course_id=9,
            title="Looking for group members",
            type="question",
            category="General",
            content="<p>Join my group please</p>",
            user_id=2,
            is_answered=False,
            is_staff_answered=False,
            deleted_at=None,
            created_at="2026-03-14T00:00:00Z",
        ),
        ThreadSummary(
            id=103,
            number=9,
            course_id=9,
            title="Staff post",
            type="question",
            category="General",
            content="<p>Status update</p>",
            user_id=3,
            is_answered=False,
            is_staff_answered=False,
            deleted_at=None,
            created_at="2026-03-14T00:00:00Z",
        ),
    ]
    users = {
        1: UserSummary(id=1, name="Student", role="user"),
        2: UserSummary(id=2, name="Recruiter", role="user"),
        3: UserSummary(id=3, name="Tutor", role="tutor"),
    }

    unanswered = list_unanswered_threads(threads=threads, users_by_id=users)

    assert [thread.id for thread in unanswered] == [101]
    assert [thread.id for thread in unanswered] == [101]
    assert [thread.id for thread in unanswered] == [101]
