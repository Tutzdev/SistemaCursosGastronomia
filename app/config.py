import os
from datetime import timedelta


class ConfigurationError(RuntimeError):
    pass


def _read_positive_int(name: str, default: int) -> int:
    raw_value = os.getenv(name, str(default))
    try:
        value = int(raw_value)
    except ValueError as error:
        raise ConfigurationError(f"{name} deve ser um número inteiro.") from error

    if value <= 0:
        raise ConfigurationError(f"{name} deve ser maior que zero.")

    return value


def _read_origins() -> list[str]:
    raw_origins = os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    )

    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    if not origins or "*" in origins:
        raise ConfigurationError("CORS_ALLOWED_ORIGINS deve listar origens explícitas.")

    return origins


def load_environment_config() -> dict[str, object]:
    jwt_secret_key = os.getenv("JWT_SECRET_KEY", "").strip()
    if not jwt_secret_key:
        raise ConfigurationError("JWT_SECRET_KEY é obrigatória.")

    expires_minutes = _read_positive_int("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 60)
    return {
        "APP_ENV": os.getenv("APP_ENV", "development"),
        "SQLALCHEMY_DATABASE_URI": os.getenv("DATABASE_URL", "sqlite:///app.db"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": jwt_secret_key,
        "JWT_ACCESS_TOKEN_EXPIRES": timedelta(minutes=expires_minutes),
        "CORS_ALLOWED_ORIGINS": _read_origins(),
    }


def validate_app_config(config: dict[str, object]) -> None:
    if not config.get("SQLALCHEMY_DATABASE_URI"):
        raise ConfigurationError("DATABASE_URL é obrigatória.")
    if not config.get("JWT_SECRET_KEY"):
        raise ConfigurationError("JWT_SECRET_KEY é obrigatória.")

    origins = config.get("CORS_ALLOWED_ORIGINS")

    if not isinstance(origins, (list, tuple)) or not origins or "*" in origins:
        raise ConfigurationError("CORS_ALLOWED_ORIGINS deve listar origens explícitas.")
