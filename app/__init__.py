from collections.abc import Mapping
from datetime import timedelta

from flask import Flask, Response, abort, jsonify, render_template

from app.config import load_environment_config, validate_app_config
from app.courses.seed import register_seed_command
from app.errors import register_error_handlers
from app.extensions import cors, db, jwt, migrate
from app.jwt_callbacks import register_jwt_callbacks


def create_app(config_object: object | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=60),
        CORS_ALLOWED_ORIGINS=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
    )

    if config_object is None:
        app.config.from_mapping(load_environment_config())
    elif isinstance(config_object, Mapping):
        app.config.from_mapping(config_object)
    else:
        app.config.from_object(config_object)

    validate_app_config(app.config)
    _initialize_extensions(app)
    _register_blueprints(app)
    register_error_handlers(app)
    register_jwt_callbacks(app)
    register_seed_command(app)

    return app


def _initialize_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    jwt.init_app(app)

    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["CORS_ALLOWED_ORIGINS"],
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Authorization", "Content-Type"],
            }
        },
    )


def _register_blueprints(app: Flask) -> None:
    from app import models as _models  # noqa: F401
    from app.auth.routes import auth_blueprint
    from app.courses.routes import courses_blueprint
    from app.enrollments.routes import enrollments_blueprint
    from app.site_catalog import SITE_COURSES, get_site_course
    from app.users.routes import users_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(courses_blueprint)
    app.register_blueprint(enrollments_blueprint)
    app.register_blueprint(users_blueprint)

    @app.get("/")
    def index() -> str:
        return render_template("index.html")

    @app.get("/cursos")
    def courses_page() -> str:
        return render_template("courses.html")

    @app.get("/cursos/<slug>")
    def course_page(slug: str) -> str:
        course = get_site_course(slug)
        if course is None:
            abort(404)
        return render_template("course_detail.html", course=course)

    @app.get("/sobre")
    def about_page() -> str:
        return render_template("about.html")

    @app.get("/contato")
    def contact_page() -> str:
        return render_template("contact.html")

    @app.context_processor
    def site_context() -> dict[str, object]:
        return {"site_courses": SITE_COURSES}

    @app.get("/api/health")
    def health() -> tuple[Response, int]:
        return jsonify({"status": "ok"}), 200
