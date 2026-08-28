from datetime import UTC, datetime
from enum import Enum
from typing import TypeAlias

from app.models import Enrollment, User

JsonValue: TypeAlias = str | int | float | bool | None


def _serialize_datetime(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)

    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def serialize_user(user: User) -> dict[str, JsonValue]:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "created_at": _serialize_datetime(user.created_at),
    }


def serialize_enrollment(enrollment: Enrollment) -> dict[str, JsonValue]:
    return {
        "id": enrollment.id,
        "user_id": enrollment.user_id,
        "course_id": enrollment.course_id,
        "created_at": _serialize_datetime(enrollment.created_at),
    }


def serialize_scalar(value: object) -> JsonValue:
    if isinstance(value, datetime):
        return _serialize_datetime(value)
    if isinstance(value, Enum):
        return str(value.value)

    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    return str(value)
