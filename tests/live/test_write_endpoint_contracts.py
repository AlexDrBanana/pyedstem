"""Opt-in live write contract tests for Ed endpoints.

These are intentionally disabled by default because they mutate real course data.
Enable them only with a dedicated target thread and explicit consent.
"""

from __future__ import annotations

import os

import pytest

from pyedstem import EdStemClient

pytestmark = pytest.mark.skipif(
    os.getenv("EDSTEM_RUN_WRITE_TESTS") != "1",
    reason="Set EDSTEM_RUN_WRITE_TESTS=1 only when it is safe to mutate Ed data.",
)


def test_post_thread_answer_contract() -> None:
    """Posting answers should keep working when explicitly enabled."""
    thread_id = os.environ["EDSTEM_WRITE_TEST_THREAD_ID"]
    message = os.environ.get(
        "EDSTEM_WRITE_TEST_MESSAGE",
        "Automated pyedstem contract test. Please ignore.",
    )

    with EdStemClient.from_env() as client:
        response = client.threads.post_answer(
            thread_id=int(thread_id), markdown=message
        )

    assert response.id is not None
