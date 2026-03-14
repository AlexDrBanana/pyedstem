"""Tests for the public pyedstem client surface."""

from __future__ import annotations

import httpx

from pyedstem import EdStemClient


class TestEdStemClient:
    """Describe the expected public client ergonomics."""

    def test_client_exposes_resource_groups(self) -> None:
        """The top-level client should expose the documented resources."""
        client = EdStemClient(api_token="token")

        assert client.user is not None
        assert client.courses is not None
        assert client.threads is not None
        assert client.lessons is not None
        assert client.analytics is not None
        assert client.challenges is not None

        client.close()

    def test_client_supports_context_manager(self) -> None:
        """The client should manage its HTTP resources with a context manager."""
        with EdStemClient(api_token="token") as client:
            assert isinstance(client._transport.client, httpx.Client)

    def test_client_uses_workspace_default_base_url(self) -> None:
        """The client should default to the documented Ed Stem API base URL."""
        client = EdStemClient(api_token="token")

        assert str(client._transport.client.base_url) == "https://edstem.org/api/"

        client.close()
