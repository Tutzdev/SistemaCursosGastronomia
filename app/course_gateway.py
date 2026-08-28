from collections.abc import Mapping, Sequence

from sqlalchemy import MetaData, Table, select
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.sql.schema import Column

from app.errors import CourseIntegrationUnavailableError
from app.extensions import db
from app.models import Enrollment

PUBLIC_COURSE_FIELDS = ("id", "title", "description", "thumbnail_url", "level")


def _get_course_table() -> Table:
    try:
        course_table = Table("courses", MetaData(), autoload_with=db.engine)
    except NoSuchTableError as error:
        raise CourseIntegrationUnavailableError() from error

    if "id" not in course_table.c:
        raise CourseIntegrationUnavailableError()

    return course_table


def course_exists(course_id: int) -> bool:
    course_table = _get_course_table()
    statement = select(course_table.c.id).where(course_table.c.id == course_id)

    return db.session.scalar(statement) is not None


def get_courses_for_user(user_id: int) -> Sequence[Mapping[str, object]]:
    course_table = _get_course_table()
    missing_fields = set(PUBLIC_COURSE_FIELDS).difference(course_table.c.keys())

    if missing_fields:
        raise CourseIntegrationUnavailableError()

    public_columns: list[Column[object]] = [
        course_table.c[field] for field in PUBLIC_COURSE_FIELDS
    ]
    statement = (
        select(*public_columns)
        .join(Enrollment, Enrollment.course_id == course_table.c.id)
        .where(Enrollment.user_id == user_id)
        .order_by(Enrollment.created_at, Enrollment.id)
    )

    return db.session.execute(statement).mappings().all()
