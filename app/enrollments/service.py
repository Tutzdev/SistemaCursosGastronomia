from collections.abc import Mapping, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.course_gateway import course_exists, get_courses_for_user
from app.errors import AlreadyEnrolledError, CourseNotFoundError
from app.extensions import db
from app.models import Enrollment, User


def enroll_user(user: User, course_id: int) -> Enrollment:
    if not course_exists(course_id):
        raise CourseNotFoundError()

    existing_enrollment = db.session.scalar(
        select(Enrollment).where(
            Enrollment.user_id == user.id,
            Enrollment.course_id == course_id,
        )
    )
    
    if existing_enrollment is not None:
        raise AlreadyEnrolledError()

    enrollment = Enrollment(user_id=user.id, course_id=course_id)
    db.session.add(enrollment)
    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()

        if not course_exists(course_id):
            raise CourseNotFoundError() from error
        
        raise AlreadyEnrolledError() from error
    
    return enrollment


def list_user_courses(user: User) -> Sequence[Mapping[str, object]]: return get_courses_for_user(user.id)
