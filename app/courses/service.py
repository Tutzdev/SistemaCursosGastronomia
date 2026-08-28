from sqlalchemy import or_, select
from sqlalchemy.orm import joinedload, selectinload

from app.errors import CourseNotFoundError, ValidationError
from app.extensions import db
from app.models import Category, Course, CourseLevel, CourseStatus, Module


def list_courses(
    search: str | None, category: str | None, level: str | None
) -> list[Course]:
    statement = (
        select(Course)
        .where(Course.status == CourseStatus.PUBLISHED)
        .options(joinedload(Course.category), joinedload(Course.instructor))
        .order_by(Course.id)
    )
    if search and (term := search.strip()):
        pattern = f"%{term}%"
        statement = statement.where(
            or_(Course.title.ilike(pattern), Course.description.ilike(pattern))
        )

    if category:
        statement = statement.join(Course.category).where(Category.slug == category)
    if level:
        try:
            normalized_level = CourseLevel(level.strip().upper())
        except ValueError as error:
            raise ValidationError({"level": "Nível inválido."}) from error
        statement = statement.where(Course.level == normalized_level)

    return list(db.session.scalars(statement).all())


def get_course(course_id: int) -> Course:
    statement = (
        select(Course)
        .where(Course.id == course_id, Course.status == CourseStatus.PUBLISHED)
        .options(
            joinedload(Course.category),
            joinedload(Course.instructor),
            selectinload(Course.modules).selectinload(Module.lessons),
        )
    )
    course = db.session.scalar(statement)
    if course is None:
        raise CourseNotFoundError()

    return course


def list_categories() -> list[Category]:
    return list(db.session.scalars(select(Category).order_by(Category.name)).all())
