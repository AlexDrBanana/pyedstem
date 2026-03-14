"""Custom exception hierarchy for pyedstem."""

from __future__ import annotations


class EdStemError(Exception):
    """Base exception for pyedstem failures."""


class AuthenticationError(EdStemError):
    """Raised when the Ed API rejects authentication or permissions."""


class NotFoundError(EdStemError):
    """Raised when an Ed resource cannot be found."""


class ValidationError(EdStemError):
    """Raised when the Ed API rejects request input."""


class RateLimitError(EdStemError):
    """Raised when the Ed API rate-limits a request."""


class ServerError(EdStemError):
    """Raised when the Ed API returns a server-side error."""
