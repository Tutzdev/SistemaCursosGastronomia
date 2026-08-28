from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.auth.validation import LoginData, RegistrationData
from app.errors import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError,
)
from app.extensions import db
from app.models import User, UserRole
from app.security import hash_password, verify_password


def register_user(data: RegistrationData) -> User:
    existing_user = db.session.scalar(select(User).where(User.email == data.email))
    if existing_user is not None:
        raise EmailAlreadyRegisteredError()

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=UserRole.STUDENT,
    )

    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise EmailAlreadyRegisteredError() from error

    return user


def authenticate_user(data: LoginData) -> str:
    user = db.session.scalar(select(User).where(User.email == data.email))
    if user is None or not verify_password(data.password, user.password_hash):
        # A resposta é genérica para não revelar quais e-mails estão cadastrados.
        raise InvalidCredentialsError()

    return create_access_token(identity=str(user.id))


def get_current_user() -> User:
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError) as error:
        raise InvalidTokenError() from error

    if user_id <= 0:
        raise InvalidTokenError()

    user = db.session.get(User, user_id)
    if user is None:
        raise UserNotFoundError()

    return user
