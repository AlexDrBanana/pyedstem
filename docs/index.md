# pyedstem

`pyedstem` is a typed, sync-first Python client for the Ed Stem API.

The docs site is generated from the package's docstrings, so your API reference
can stay close to the implementation instead of drifting off into a sad little
wiki graveyard.

## What you get

- typed models for common Ed Stem responses
- a high-level `EdStemClient`
- grouped resources for courses, threads, lessons, analytics, and challenges
- workflow helpers for common moderation and support tasks

## Install

```bash
pip install pyedstem
```

Or in a `uv` project:

```bash
uv add pyedstem
```

## Quick example

```python
from pyedstem import EdStemClient

with EdStemClient.from_env() as client:
    threads = client.workflows.list_course_unanswered_threads(course_id=12345)

for thread in threads:
    print(thread.number, thread.title)
```

## Writing docs

Most API reference pages are generated from docstrings. To preview the site
locally:

```bash
uv sync --group dev --group docs
uv run mkdocs serve
```

Then open the local URL shown by MkDocs.
