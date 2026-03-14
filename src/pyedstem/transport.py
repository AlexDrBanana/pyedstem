"""Shared HTTP transport for pyedstem resources."""

from __future__ import annotations

from typing import Any

import httpx

from pyedstem.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class EdStemTransport:
    """Thin typed wrapper around httpx for the Ed API."""

    def __init__(
        self,
        *,
        api_token: str,
        base_url: str,
        timeout_seconds: float,
        client: httpx.Client | None = None,
    ) -> None:
        self.client = client or httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_token}"},
            timeout=timeout_seconds,
        )

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self.client.close()

    def get_json(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Perform a GET request and decode JSON."""
        return self._request_json("GET", path, params=params)

    def post_json(
        self,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        """Perform a POST request and decode JSON."""
        return self._request_json("POST", path, json_body=json_body)

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        """Perform an HTTP request and map Ed HTTP failures to library exceptions."""
        response = self.client.request(method, path, params=params, json=json_body)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            self._raise_for_status_error(exc.response)

        return response.json()

    @staticmethod
    def _raise_for_status_error(response: httpx.Response) -> None:
        """Raise a library-specific exception for the failing response."""
        message = response.text
        status_code = response.status_code

        if status_code in {401, 403}:
            raise AuthenticationError(message)
        if status_code == 404:
            raise NotFoundError(message)
        if status_code == 429:
            raise RateLimitError(message)
        if 400 <= status_code < 500:
            raise ValidationError(message)

        raise ServerError(message)
