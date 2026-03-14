"""Typed data models for pyedstem."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FlexibleModel(BaseModel):
    """Base model that tolerates undocumented response fields.

    Ed Stem responses may include fields that are undocumented or vary between
    endpoints. Models inherit from this base so extra keys do not break parsing.
    """

    model_config = ConfigDict(extra="allow")


class UserSummary(FlexibleModel):
    """Minimal user details used across multiple endpoints.

    Attributes:
        id: Numeric Ed user identifier.
        name: Display name for the user.
        role: Course or platform role, when present.
        email: User email address, when exposed by the endpoint.
        username: Ed username, when available.
    """

    id: int
    name: str | None = None
    role: str | None = None
    email: str | None = None
    username: str | None = None


class CourseInfo(FlexibleModel):
    """Core course metadata.

    Attributes:
        id: Numeric Ed course identifier.
        code: Course code such as ``QBUS6860``.
        name: Human-readable course name.
        status: Course status, for example ``"active"`` or ``"archived"``.
        year: Academic year, when provided.
        session: Session or term label, when provided.
    """

    id: int
    code: str | None = None
    name: str | None = None
    status: str | None = None
    year: str | None = None
    session: str | None = None


class CourseEnrollment(FlexibleModel):
    """Course membership information from ``GET /user``.

    Attributes:
        course: Embedded course metadata.
        role: The authenticated user's role in the course.
        lab: Lab or tutorial assignment, when present.
        last_active: Timestamp for recent course activity, when present.
    """

    course: CourseInfo
    role: str | None = None
    lab: str | None = None
    last_active: str | None = None


class CurrentUser(FlexibleModel):
    """Authenticated user profile.

    Attributes:
        id: Numeric Ed user identifier.
        name: Display name.
        role: Global or contextual Ed role, when present.
        email: User email address, when present.
        username: Ed username, when present.
    """

    id: int
    name: str | None = None
    role: str | None = None
    email: str | None = None
    username: str | None = None


class CurrentUserResponse(FlexibleModel):
    """Typed response payload for ``GET /user``.

    Attributes:
        user: Authenticated user profile.
        courses: Course enrollments visible to the authenticated user.
        realms: Additional realm/account metadata returned by Ed.
    """

    user: CurrentUser
    courses: list[CourseEnrollment] = Field(default_factory=list)
    realms: list[dict[str, Any]] = Field(default_factory=list)


class CommentSummary(FlexibleModel):
    """Thread answer/comment representation.

    Attributes:
        id: Numeric comment identifier.
        type: Ed comment type such as ``"answer"`` or ``"comment"``.
        content: Raw Ed content payload, usually HTML or XML-like markup.
        user_id: Identifier of the comment author.
        created_at: Creation timestamp, when present.
    """

    id: int
    type: str | None = None
    content: str | None = None
    user_id: int | None = None
    created_at: str | None = None


class ThreadSummary(FlexibleModel):
    """Thread summary returned from list endpoints.

    Attributes:
        id: Global Ed thread identifier.
        number: Course-local thread number.
        course_id: Numeric Ed course identifier.
        title: Thread title.
        type: Thread type such as ``"question"``.
        category: Optional category label.
        content: Raw thread content snippet, when present.
        user_id: Identifier of the thread author.
        is_answered: Whether the thread is marked answered.
        is_staff_answered: Whether staff has answered the thread.
        deleted_at: Deletion timestamp, if the thread was deleted.
        created_at: Creation timestamp, when present.
    """

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
    """Thread detail with answers and comments.

    Attributes:
        answers: Answer objects attached to the thread.
        comments: Non-answer comments attached to the thread.
    """

    answers: list[CommentSummary] = Field(default_factory=list)
    comments: list[CommentSummary] = Field(default_factory=list)


class PostedComment(FlexibleModel):
    """Representation of a posted answer or comment.

    Attributes:
        id: Numeric comment identifier.
        type: Ed comment type.
        content: Raw returned content payload.
        user_id: Identifier of the comment author.
        created_at: Creation timestamp, when present.
    """

    id: int
    type: str | None = None
    content: str | None = None
    user_id: int | None = None
    created_at: str | None = None


class LessonSummary(FlexibleModel):
    """Lesson summary metadata.

    Attributes:
        id: Numeric Ed lesson identifier.
        title: Lesson title.
        course_id: Owning course identifier.
        module_id: Owning module identifier, when present.
        slide_count: Number of slides, when present.
    """

    id: int
    title: str | None = None
    course_id: int | None = None
    module_id: int | None = None
    slide_count: int | None = None


class SlideSummary(FlexibleModel):
    """Lesson slide metadata.

    Attributes:
        id: Numeric Ed slide identifier.
        title: Slide title.
        type: Slide type such as ``"quiz"``.
        lesson_id: Owning lesson identifier.
        challenge_id: Linked challenge identifier, when present.
    """

    id: int
    title: str | None = None
    type: str | None = None
    lesson_id: int | None = None
    challenge_id: int | None = None


class LessonDetail(LessonSummary):
    """Expanded lesson detail payload.

    Attributes:
        slides: Slide summaries included in the lesson detail response.
    """

    slides: list[SlideSummary] = Field(default_factory=list)
