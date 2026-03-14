# pyedstem

Typed Python client for the Ed Stem API.

**Documentation:** [alexdrbanana.github.io/pyedstem](https://alexdrbanana.github.io/pyedstem/)

`pyedstem` provides a small, sync-first interface for common Ed Stem tasks such
as listing active courses, retrieving discussion threads, reading lessons, and
posting answers back to Ed using the XML document format the API expects.

## Installation

### Install with pip

```bash
pip install pyedstem
```

### Add to a uv project

```bash
uv add pyedstem
```

## Configuration

You can create a client directly with an API token:

```python
from pyedstem import EdStemClient

client = EdStemClient(api_token="your-edstem-token")
```

Or load configuration from environment variables:

- `EDSTEM_API_TOKEN` — required
- `EDSTEM_BASE_URL` — optional, defaults to `https://edstem.org/api`
- `EDSTEM_TIMEOUT_SECONDS` — optional, defaults to `30.0`

```python
from pyedstem import EdStemClient

with EdStemClient.from_env() as client:
    current_user = client.user.get_current_user()
```

## Quick start

### List active courses

```python
from pyedstem import EdStemClient

with EdStemClient.from_env() as client:
    active_courses = client.courses.list_active()

for course in active_courses:
    print(course.id, course.code, course.name)
```

### Fetch recent discussion threads

```python
from pyedstem import EdStemClient

course_id = 12345

with EdStemClient.from_env() as client:
    threads = client.threads.list(course_id, limit=20, sort="date")

for thread in threads:
    print(f"#{thread.number}: {thread.title}")
```

### Post an answer

```python
from pyedstem import EdStemClient

with EdStemClient.from_env() as client:
    client.threads.post_answer(
        thread_id=67890,
        markdown="Hi there,\n\nThanks for the question...",
    )
```

## Features

- typed models for common Ed Stem responses
- sync-first client API with resource groups
- markdown-to-Ed document conversion for answer posting
- opt-in live contract tests for undocumented API drift detection

## Development

Clone the repository, then install development dependencies with uv:

```bash
uv sync --group dev
```

Run the test suite:

```bash
uv run pytest tests
```

### Live contract tests

The repository includes an opt-in live suite under `tests/live/` that probes
documented Ed endpoints so API changes can be detected early.

Safe read-only live tests:

```bash
EDSTEM_RUN_LIVE_TESTS=1 uv run pytest tests/live/test_endpoint_contracts.py tests/live/test_restricted_endpoint_contracts.py
```

Opt-in write test for posting answers:

```bash
EDSTEM_RUN_WRITE_TESTS=1 \
EDSTEM_WRITE_TEST_THREAD_ID=12345 \
uv run pytest tests/live/test_write_endpoint_contracts.py
```

Only enable the write suite when it is safe to mutate real Ed data.

## Documentation

Full documentation is available at:

[alexdrbanana.github.io/pyedstem](https://alexdrbanana.github.io/pyedstem/)

If you're contributing to the project and want to preview the docs locally:

```bash
uv sync --group dev --group docs
uv run mkdocs serve
```

Then open the local URL shown by MkDocs.
