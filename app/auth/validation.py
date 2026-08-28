from collections.abc import Mapping
from dataclasses import dataclass

from email_validator import EmailNotValidError, validate_email

from app.errors import ValidationError

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 256
MAX_NAME_LENGTH = 120


@dataclass(frozen=True)
class RegistrationData:
    name: str
    email: str
    password: str


@dataclass(frozen=True)
class LoginData:
    email: str
    password: str


def normalize_email(email: str) -> str:
    normalized = email.strip().lower()

    try:
        result = validate_email(normalized, check_deliverability=False)
    except EmailNotValidError as error:
        raise ValidationError({"email": "Informe um e-mail válido."}) from error

    return result.normalized.lower()


def _require_string(payload: Mapping[str, object], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str):
        raise ValidationError({field: "Este campo é obrigatório."})

    return value


def _validate_password(password: str) -> None:
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(
            {
                "password": (
                    f"A senha deve ter pelo menos {MIN_PASSWORD_LENGTH} caracteres."
                )
            }
        )
    if len(password) > MAX_PASSWORD_LENGTH:
        raise ValidationError(
            {
                "password": (
                    f"A senha deve ter no máximo {MAX_PASSWORD_LENGTH} caracteres."
                )
            }
        )


def validate_registration_payload(payload: object) -> RegistrationData:
    if not isinstance(payload, Mapping):
        raise ValidationError({"body": "Envie um objeto JSON válido."})

    name = " ".join(_require_string(payload, "name").split())
    if not name or len(name) > MAX_NAME_LENGTH:
        raise ValidationError(
            {"name": f"O nome deve ter entre 1 e {MAX_NAME_LENGTH} caracteres."}
        )

    email = normalize_email(_require_string(payload, "email"))
    password = _require_string(payload, "password")
    confirmation = _require_string(payload, "password_confirmation")
    _validate_password(password)

    if password != confirmation:
        raise ValidationError(
            {"password_confirmation": "A confirmação da senha não corresponde."}
        )

    return RegistrationData(name=name, email=email, password=password)


def validate_login_payload(payload: object) -> LoginData:
    if not isinstance(payload, Mapping):
        raise ValidationError({"body": "Envie um objeto JSON válido."})

    email = normalize_email(_require_string(payload, "email"))
    password = _require_string(payload, "password")

    if not password:
        raise ValidationError({"password": "Este campo é obrigatório."})

    return LoginData(email=email, password=password)
