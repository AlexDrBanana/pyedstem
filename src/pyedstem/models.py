"""Typed data models for pyedstem."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FlexibleModel(BaseModel):
    """Base model that tolerates undocumented response fields."""

    model_config = ConfigDict(extra="allow")


class UserSummary(FlexibleModel):
    """Minimal user details used across multiple endpoints."""

    id: int
    name: str | None = None
    role: str | None = None
    email: str | None = None
    username: str | None = None


class CourseInfo(FlexibleModel):
    """Core course metadata."""

    id: int
    code: str | None = None
    name: str | None = None
    status: str | None = None
    year: str | None = None
    session: str | None = None


class CourseEnrollment(FlexibleModel):
    """Course membership information from GET /user."""

    course: CourseInfo
    role: str | None = None
    lab: str | None = None
    last_active: str | None = None


class CurrentUser(FlexibleModel):
    """Authenticated user profile."""

    id: int
    name: str | None = None
    role: str | None = None
    email: str | None = None
    username: str | None = None


class CurrentUserResponse(FlexibleModel):
    """Typed response payload for GET /user."""

    user: CurrentUser
    courses: list[CourseEnrollment] = Field(default_factory=list)
    realms: list[dict[str, Any]] = Field(default_factory=list)


class CommentSummary(FlexibleModel):
    """Thread answer/comment representation."""

    id: int
    type: str | None = None
    content: str | None = None
    user_id: int | None = None
    created_at: str | None = None


class ThreadSummary(FlexibleModel):
    """Thread summary returned from list endpoints."""

    id: int
    number: int
    course_id: int
    title: str
    type: str
    category: str | None = None
    content: str | None = None
    user_id: int
    is_answered: bool = False
    is_staff_answered: bool = False
    deleted_at: str | None = None
    created_at: str | None = None


class ThreadDetail(ThreadSummary):
    """Thread detail with answers and comments."""

    answers: list[CommentSummary] = Field(default_factory=list)
    comments: list[CommentSummary] = Field(default_factory=list)


class PostedComment(FlexibleModel):
    """Representation of a posted answer/comment."""

    id: int
    type: str | None = None
    content: str | None = None
    user_id: int | None = None
    created_at: str | None = None


class LessonSummary(FlexibleModel):
    """Lesson summary metadata."""

    id: int
    title: str | None = None
    course_id: int | None = None
    module_id: int | None = None
    slide_count: int | None = None


class SlideSummary(FlexibleModel):
    """Lesson slide metadata."""

    id: int
    title: str | None = None
    type: str | None = None
    lesson_id: int | None = None
    challenge_id: int | None = None


class LessonDetail(LessonSummary):
    """Expanded lesson detail payload."""

    slides: list[SlideSummary] = Field(default_factory=list)
