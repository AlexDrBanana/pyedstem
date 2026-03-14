# pyedstem

Typed Python client for the Ed Stem API, designed for this workspace and its Ed automation workflows.

## Installation

From the repo root, sync the workspace environment:

```bash
uv sync
```

## Quick start

```python
from pyedstem import EdStemClient

with EdStemClient.from_env() as client:
    current_user = client.user.get_current_user()
    active_courses = client.courses.list_active()
    unanswered = client.workflows.list_course_unanswered_threads(active_courses[0].id)
```

## Live contract tests

The package includes an opt-in live suite under `tests/live/` that probes documented Ed endpoints so API changes are caught early.

Safe read-only live tests:

```bash
EDSTEM_RUN_LIVE_TESTS=1 uv run --package pyedstem pytest pyedstem/tests/live/test_endpoint_contracts.py
```

Opt-in write test for posting answers:

```bash
EDSTEM_RUN_WRITE_TESTS=1 \
EDSTEM_WRITE_TEST_THREAD_ID=12345 \
uv run --package pyedstem pytest pyedstem/tests/live/test_write_endpoint_contracts.py
```

Only enable the write suite when it is safe to mutate real Ed data.
