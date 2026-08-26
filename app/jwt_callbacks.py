from http import HTTPStatus

from flask import Flask, Response

from app.errors import error_response
from app.extensions import jwt


def register_jwt_callbacks(app: Flask) -> None:
    @jwt.unauthorized_loader
    def handle_missing_token(reason: str) -> tuple[Response, int]:
        return error_response(
            "AUTHENTICATION_REQUIRED",
            "Autenticação é obrigatória.",
            HTTPStatus.UNAUTHORIZED,
        )

    @jwt.invalid_token_loader
    def handle_invalid_token(reason: str) -> tuple[Response, int]:
        return error_response(
            "INVALID_TOKEN", "Token de acesso inválido.", HTTPStatus.UNAUTHORIZED
        )

    @jwt.expired_token_loader
    def handle_expired_token(
        jwt_header: dict[str, object], jwt_payload: dict[str, object]
    ) -> tuple[Response, int]:
        return error_response(
            "TOKEN_EXPIRED", "Token de acesso expirado.", HTTPStatus.UNAUTHORIZED
        )

    @jwt.revoked_token_loader
    def handle_revoked_token(
        jwt_header: dict[str, object], jwt_payload: dict[str, object]
    ) -> tuple[Response, int]:
        return error_response(
            "INVALID_TOKEN", "Token de acesso inválido.", HTTPStatus.UNAUTHORIZED
        )

    @jwt.needs_fresh_token_loader
    def handle_non_fresh_token(
        jwt_header: dict[str, object], jwt_payload: dict[str, object]
    ) -> tuple[Response, int]:
        return error_response(
            "INVALID_TOKEN", "Token de acesso inválido.", HTTPStatus.UNAUTHORIZED
        )
