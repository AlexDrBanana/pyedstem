"""Live contract tests for documented Ed Stem endpoints.

These tests are opt-in and hit the live Ed API so we can detect undocumented
contract changes over time. They are skipped unless EDSTEM_RUN_LIVE_TESTS=1.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Iterable
from dataclasses import dataclass

import pytest
from pyedstem.live import LiveEndpointContext, gather_live_context

from pyedstem import EdStemClient

pytestmark = pytest.mark.skipif(
    os.getenv("EDSTEM_RUN_LIVE_TESTS") != "1",
    reason="Set EDSTEM_RUN_LIVE_TESTS=1 to exercise the live Ed API.",
)


@dataclass(frozen=True)
class EndpointExpectation:
    """Expected top-level contract for one endpoint probe."""

    name: str
    call: Callable[[EdStemClient, LiveEndpointContext], object]


def _require_quiz_slide(context: LiveEndpointContext) -> int:
    """Return a quiz slide ID or skip quiz-only contract tests."""
    if context.quiz_slide_id is None:
        pytest.skip("No quiz slide available in the discovered live course context.")
    return context.quiz_slide_id


@pytest.fixture(scope="session")
def live_client() -> Iterable[EdStemClient]:
    """Create one shared live client for the contract suite."""
    with EdStemClient.from_env() as client:
        yield client


@pytest.fixture(scope="session")
def live_context(live_client: EdStemClient) -> LiveEndpointContext:
    """Resolve reusable live IDs once per test session."""
    return gather_live_context(live_client)


def _expectations() -> list[EndpointExpectation]:
    """Enumerate documented endpoints that should keep working."""
    return [
        EndpointExpectation(
            "get_current_user", lambda client, ctx: client.user.get_current_user()
        ),
        EndpointExpectation(
            "list_active_courses", lambda client, ctx: client.courses.list_active()
        ),
        EndpointExpectation(
            "get_course", lambda client, ctx: client.courses.get(ctx.course_id)
        ),
        EndpointExpectation(
            "list_course_users",
            lambda client, ctx: client.courses.list_users(ctx.course_id, limit=5),
        ),
        EndpointExpectation(
            "list_course_labs",
            lambda client, ctx: client.courses.list_labs(ctx.course_id),
        ),
        EndpointExpectation(
            "list_course_groups",
            lambda client, ctx: client.courses.list_groups(ctx.course_id),
        ),
        EndpointExpectation(
            "get_course_stats",
            lambda client, ctx: client.courses.get_stats(ctx.course_id),
        ),
        EndpointExpectation(
            "list_course_resources",
            lambda client, ctx: client.courses.list_resources(ctx.course_id),
        ),
        EndpointExpectation(
            "list_course_bots",
            lambda client, ctx: client.courses.list_bots(ctx.course_id),
        ),
        EndpointExpectation(
            "list_course_workspaces",
            lambda client, ctx: client.courses.list_workspaces(ctx.course_id),
        ),
        EndpointExpectation(
            "list_threads",
            lambda client, ctx: client.threads.list(ctx.course_id, limit=5),
        ),
        EndpointExpectation(
            "get_thread", lambda client, ctx: client.threads.get(ctx.thread_id)
        ),
        EndpointExpectation(
            "get_thread_by_number",
            lambda client, ctx: client.threads.get_by_number(
                ctx.course_id, ctx.thread_number
            ),
        ),
        EndpointExpectation(
            "search_threads",
            lambda client, ctx: client.threads.search(
                ctx.course_id, query=ctx.thread_search_query
            ),
        ),
        EndpointExpectation(
            "list_lessons", lambda client, ctx: client.lessons.list(ctx.course_id)
        ),
        EndpointExpectation(
            "get_lesson", lambda client, ctx: client.lessons.get(ctx.lesson_id)
        ),
        EndpointExpectation(
            "list_lesson_slides",
            lambda client, ctx: client.lessons.list_slides(ctx.lesson_id),
        ),
        EndpointExpectation(
            "get_lesson_results",
            lambda client, ctx: client.lessons.list_results(ctx.lesson_id, limit=5),
        ),
        EndpointExpectation(
            "get_lesson_activity",
            lambda client, ctx: client.lessons.get_activity(ctx.lesson_id),
        ),
        EndpointExpectation(
            "get_slide", lambda client, ctx: client.lessons.get_slide(ctx.slide_id)
        ),
        EndpointExpectation(
            "get_quiz_questions",
            lambda client, ctx: client.lessons.get_slide_questions(
                _require_quiz_slide(ctx)
            ),
        ),
        EndpointExpectation(
            "get_quiz_results",
            lambda client, ctx: client.lessons.get_slide_results(
                _require_quiz_slide(ctx)
            ),
        ),
        EndpointExpectation(
            "analytics_users",
            lambda client, ctx: client.analytics.get_users(ctx.course_id),
        ),
        EndpointExpectation(
            "analytics_discussion",
            lambda client, ctx: client.analytics.get_discussion(ctx.course_id),
        ),
        EndpointExpectation(
            "analytics_challenges",
            lambda client, ctx: client.analytics.get_challenges(ctx.course_id),
        ),
        EndpointExpectation(
            "list_challenges", lambda client, ctx: client.challenges.list(ctx.course_id)
        ),
        EndpointExpectation(
            "user_activity",
            lambda client, ctx: client.user.get_activity(
                ctx.user_id, course_id=ctx.course_id, limit=5, filter_by="thread"
            ),
        ),
        EndpointExpectation(
            "get_user_tokens", lambda client, ctx: client.user.list_tokens()
        ),
        EndpointExpectation(
            "get_course_admin",
            lambda client, ctx: client.courses.get_admin(ctx.course_id),
        ),
    ]


@pytest.mark.parametrize(
    "expectation",
    _expectations(),
    ids=lambda expectation: expectation.name,
)
def test_documented_endpoint_contracts(
    live_client: EdStemClient,
    live_context: LiveEndpointContext,
    expectation: EndpointExpectation,
) -> None:
    """Each documented live endpoint should respond without a breaking contract change."""
    result = expectation.call(live_client, live_context)

    assert result is not None
