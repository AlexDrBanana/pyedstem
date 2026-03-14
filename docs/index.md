# pyedstem

`pyedstem` is a typed, sync-first Python client for the Ed Stem API.

## What you get

- typed models for common Ed Stem responses
- a high-level `EdStemClient`
- grouped resources for courses, threads, lessons, analytics, and challenges

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
    threads = client.threads.list(course_id=12345, limit=20, sort="date")

for thread in threads:
    print(thread.number, thread.title)
```

## Next steps

- Browse the `API reference` section for the full client surface.
- Use `EdStemClient.from_env()` when working with environment variables.
- Build task-specific automation in your own scripts or instructions using the generic client resources.
