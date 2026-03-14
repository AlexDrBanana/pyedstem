# pyedstem

Typed Python client for the Ed Stem API.

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

### Fetch unanswered discussion threads

```python
from pyedstem import EdStemClient

course_id = 12345

with EdStemClient.from_env() as client:
    threads = client.workflows.list_course_unanswered_threads(course_id)

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
- workflow helpers for active-course and unanswered-thread automation
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

## Publishing

Build distribution artifacts with:

```bash
uv build
```

### Recommended: GitHub Actions trusted publishing

This repository now includes `.github/workflows/publish.yml`, which:

- runs tests
- builds the wheel and source distribution
- checks package metadata with `twine check`
- publishes to PyPI using GitHub Actions OIDC trusted publishing

To enable it for this repository:

1. In PyPI, open the `pyedstem` project and add a **Trusted Publisher** under **Manage → Publishing**.
2. Use these values for the publisher configuration:
    - **Owner**: `AlexDrBanana`
    - **Repository name**: `pyedstem`
    - **Workflow name**: `publish.yml`
    - **Environment name**: leave this blank
3. Publish by creating a GitHub release, or run the workflow manually from the Actions tab.

No PyPI token needs to be stored in GitHub secrets for this flow.

If you later want an approval gate in GitHub before publishing, you can add a
GitHub environment such as `pypi` and then update the trusted publisher config
to match it.

### Manual fallback

If you ever want to publish locally instead, you can still use the named `uv`
index and provide credentials through environment variables:

```bash
UV_INDEX_PYPI_RELEASE_USERNAME=__token__ \
UV_INDEX_PYPI_RELEASE_PASSWORD=your-pypi-token \
uv publish --index pypi-release
```

The `pypi-release` index is configured in `pyproject.toml` with the correct
PyPI download and upload URLs. Keep credentials out of the file and provide
them only at publish time.
