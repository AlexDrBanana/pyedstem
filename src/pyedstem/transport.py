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
    """Thin HTTP transport wrapper for Ed Stem API calls.

    Resource classes share a single transport so authentication, base URL, and
    error mapping are configured in one place.

    Args:
        api_token: Ed Stem API bearer token.
        base_url: Base URL for the Ed Stem API.
        timeout_seconds: Request timeout in seconds.
        client: Optional preconfigured ``httpx.Client`` to reuse.

    Attributes:
        client: The underlying ``httpx.Client`` used for all requests.
    """

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
        """Close the underlying HTTP client.

        Returns:
            ``None``.
        """
        self.client.close()

    def get_json(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Perform a ``GET`` request and decode the JSON response.

        Args:
            path: API path relative to the configured base URL.
            params: Optional query-string parameters.

        Returns:
            The decoded JSON payload. The exact type depends on the endpoint.

        Raises:
            AuthenticationError: If the API token is rejected.
            NotFoundError: If the requested resource does not exist.
            RateLimitError: If the API rate-limits the request.
            ValidationError: If Ed rejects the request as invalid.
            ServerError: If Ed returns a server-side failure.
        """
        return self._request_json("GET", path, params=params)

    def post_json(
        self,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        """Perform a ``POST`` request and decode the JSON response.

        Args:
            path: API path relative to the configured base URL.
            json_body: Optional JSON payload to send in the request body.

        Returns:
            The decoded JSON payload. The exact type depends on the endpoint.

        Raises:
            AuthenticationError: If the API token is rejected.
            NotFoundError: If the requested resource does not exist.
            RateLimitError: If the API rate-limits the request.
            ValidationError: If Ed rejects the request as invalid.
            ServerError: If Ed returns a server-side failure.
        """
        return self._request_json("POST", path, json_body=json_body)

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        """Perform an HTTP request and decode its JSON body.

        Args:
            method: HTTP method, such as ``"GET"`` or ``"POST"``.
            path: API path relative to the configured base URL.
            params: Optional query-string parameters.
            json_body: Optional JSON request body.

        Returns:
            The decoded JSON payload returned by Ed.

        Raises:
            AuthenticationError: If the API token is rejected.
            NotFoundError: If the requested resource does not exist.
            RateLimitError: If the API rate-limits the request.
            ValidationError: If Ed rejects the request as invalid.
            ServerError: If Ed returns a server-side failure.
        """
        response = self.client.request(method, path, params=params, json=json_body)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            self._raise_for_status_error(exc.response)

        return response.json()

    @staticmethod
    def _raise_for_status_error(response: httpx.Response) -> None:
        """Raise a library-specific exception for a failing HTTP response.

        Args:
            response: The failing HTTP response.

        Raises:
            AuthenticationError: For ``401`` and ``403`` responses.
            NotFoundError: For ``404`` responses.
            RateLimitError: For ``429`` responses.
            ValidationError: For other ``4xx`` responses.
            ServerError: For ``5xx`` responses.
        """
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
