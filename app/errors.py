from collections.abc import Mapping
from http import HTTPStatus

from flask import Flask, Response, current_app, jsonify
from werkzeug.exceptions import HTTPException


class DomainError(Exception):
    code = "INTERNAL_ERROR"
    message = "Ocorreu um erro interno."
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, details: Mapping[str, object] | None = None) -> None:
        super().__init__(self.message)
        self.details = details


class ValidationError(DomainError):
    code = "VALIDATION_ERROR"
    message = "Os dados enviados são inválidos."
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class EmailAlreadyRegisteredError(DomainError):
    code = "EMAIL_ALREADY_REGISTERED"
    message = "Já existe uma conta com este e-mail."
    status_code = HTTPStatus.CONFLICT


class InvalidCredentialsError(DomainError):
    code = "INVALID_CREDENTIALS"
    message = "E-mail ou senha inválidos."
    status_code = HTTPStatus.UNAUTHORIZED


class InvalidTokenError(DomainError):
    code = "INVALID_TOKEN"
    message = "Token de acesso inválido."
    status_code = HTTPStatus.UNAUTHORIZED


class UserNotFoundError(DomainError):
    code = "USER_NOT_FOUND"
    message = "Usuário não encontrado."
    status_code = HTTPStatus.NOT_FOUND


class CourseNotFoundError(DomainError):
    code = "COURSE_NOT_FOUND"
    message = "Curso não encontrado."
    status_code = HTTPStatus.NOT_FOUND


class AlreadyEnrolledError(DomainError):
    code = "ALREADY_ENROLLED"
    message = "O usuário já está inscrito neste curso."
    status_code = HTTPStatus.CONFLICT


class CourseIntegrationUnavailableError(DomainError):
    code = "COURSE_INTEGRATION_UNAVAILABLE"
    message = "O catálogo de cursos ainda não está disponível."
    status_code = HTTPStatus.SERVICE_UNAVAILABLE


def error_response(
    code: str,
    message: str,
    status_code: int,
    details: Mapping[str, object] | None = None,
) -> tuple[Response, int]:
    response = jsonify(
        {"error": {"code": code, "message": message, "details": details}}
    )
    if status_code == HTTPStatus.UNAUTHORIZED:
        response.headers["WWW-Authenticate"] = "Bearer"

    return response, status_code


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(DomainError)
    def handle_domain_error(error: DomainError) -> tuple[Response, int]:
        return error_response(
            error.code, error.message, error.status_code, error.details
        )

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException) -> tuple[Response, int]:
        return error_response(
            "HTTP_ERROR",
            error.description,
            error.code or HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> tuple[Response, int]:
        current_app.logger.exception("Unexpected application error", exc_info=error)
        return error_response(
            "INTERNAL_ERROR",
            "Ocorreu um erro interno.",
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
