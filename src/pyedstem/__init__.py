"""Public package exports for pyedstem."""

from importlib.metadata import PackageNotFoundError, version

from pyedstem.client import EdStemClient

try:
    __version__ = version("pyedstem")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["EdStemClient", "__version__"]
