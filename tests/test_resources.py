"""Tests for read-only resource helpers."""

from __future__ import annotations

from typing import Any

from pyedstem.resources.courses import Courses
from pyedstem.resources.threads import Threads


class FakeTransport:
    """Minimal transport double for resource unit tests."""

    def __init__(
        self, responses: dict[tuple[str, tuple[tuple[str, Any], ...] | None], Any]
    ):
        self._responses = responses
        self.calls: list[tuple[str, dict[str, Any] | None]] = []

    def get_json(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        self.calls.append((path, params))
        key = (path, tuple(sorted(params.items())) if params is not None else None)
        return self._responses[key]


class TestCourses:
    def test_list_active_tolerates_object_role_from_user_payload(self) -> None:
        transport = FakeTransport(
            {
                (
                    "/user",
                    None,
                ): {
                    "user": {"id": 1, "name": "Staff Member"},
                    "courses": [
                        {
                            "course": {
                                "id": 101,
                                "code": "QBUS6860",
                                "name": "Visual Data Analytics",
                                "status": "active",
                                "year": "2026",
                                "session": "Semester 1",
                            },
                            "role": {
                                "user_id": 1,
                                "course_id": 101,
                                "role": "admin",
                            },
                        },
                        {
                            "course": {
                                "id": 102,
                                "code": "QBUS6600",
                                "name": "Capstone",
                                "status": "archived",
                            },
                            "role": {
                                "user_id": 1,
                                "course_id": 102,
                                "role": "admin",
                            },
                        },
                    ],
                    "realms": [],
                }
            }
        )

        result = Courses(transport).list_active()

        assert [course.id for course in result] == [101]
        assert result[0].code == "QBUS6860"


class TestThreads:
    def test_list_forwards_pagination_and_filters(self) -> None:
        transport = FakeTransport(
            {
                (
                    "/courses/123/threads",
                    (
                        ("filter", "unanswered"),
                        ("limit", 10),
                        ("offset", 20),
                        ("sort", "activity"),
                    ),
                ): {
                    "threads": [
                        {
                            "id": 7,
                            "number": 14,
                            "course_id": 123,
                            "title": "Question",
                            "type": "question",
                            "user_id": 55,
                        }
                    ]
                }
            }
        )

        result = Threads(transport).list(
            123,
            limit=10,
            offset=20,
            sort="activity",
            filter="unanswered",
        )

        assert len(result) == 1
        assert result[0].number == 14
        assert transport.calls == [
            (
                "/courses/123/threads",
                {"limit": 10, "offset": 20, "sort": "activity", "filter": "unanswered"},
            )
        ]

    def test_iter_all_stops_when_final_page_is_short(self) -> None:
        transport = FakeTransport(
            {
                (
                    "/courses/123/threads",
                    (("limit", 2), ("offset", 0), ("sort", "date")),
                ): {
                    "threads": [
                        {
                            "id": 1,
                            "number": 1,
                            "course_id": 123,
                            "title": "First",
                            "type": "question",
                            "user_id": 10,
                        },
                        {
                            "id": 2,
                            "number": 2,
                            "course_id": 123,
                            "title": "Second",
                            "type": "question",
                            "user_id": 10,
                        },
                    ]
                },
                (
                    "/courses/123/threads",
                    (("limit", 2), ("offset", 2), ("sort", "date")),
                ): {
                    "threads": [
                        {
                            "id": 3,
                            "number": 3,
                            "course_id": 123,
                            "title": "Third",
                            "type": "question",
                            "user_id": 10,
                        }
                    ]
                },
            }
        )

        result = list(Threads(transport).iter_all(123, limit=2))

        assert [thread.number for thread in result] == [1, 2, 3]
        assert transport.calls == [
            ("/courses/123/threads", {"limit": 2, "offset": 0, "sort": "date"}),
            ("/courses/123/threads", {"limit": 2, "offset": 2, "sort": "date"}),
        ]
