"""Live contract tests for restricted Ed endpoints.

These endpoints are intentionally expected to fail for the current token/role.
If they start succeeding or change status codes, the skill catalog likely needs an update.
"""

from __future__ import annotations

import os

import pytest
from pyedstem.exceptions import AuthenticationError

from pyedstem import EdStemClient

pytestmark = pytest.mark.skipif(
    os.getenv("EDSTEM_RUN_LIVE_TESTS") != "1",
    reason="Set EDSTEM_RUN_LIVE_TESTS=1 to exercise the live Ed API.",
)


@pytest.mark.parametrize(
    ("path", "params"),
    [
        ("/realms", None),
        ("/status", None),
        ("/courses", None),
    ],
    ids=["realms", "status", "courses"],
)
def test_restricted_endpoints_still_raise_authentication_error(
    path: str,
    params: dict | None,
) -> None:
    """Restricted endpoints should still map 403 responses to AuthenticationError."""
    with EdStemClient.from_env() as client:
        with pytest.raises(AuthenticationError):
            client.get_json(path, params=params)
