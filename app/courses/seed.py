import click
from flask import Flask
from sqlalchemy import select

from app.extensions import db
from app.models import (
    Category,
    Course,
    CourseLevel,
    Lesson,
    Module,
    User,
    UserRole,
)
from app.security import hash_password

COURSES = (
    ("Pizza Napolitana", "Pizzas", "pizzas", CourseLevel.BEGINNER),
    ("Panificação Artesanal", "Panificação", "panificacao", CourseLevel.BEGINNER),
    ("Confeitaria Essencial", "Confeitaria", "confeitaria", CourseLevel.BEGINNER),
    ("Bolos Decorados", "Confeitaria", "confeitaria", CourseLevel.INTERMEDIATE),
    ("Massas Frescas", "Massas", "massas", CourseLevel.BEGINNER),
    ("Cozinha Profissional", "Cozinha", "cozinha", CourseLevel.INTERMEDIATE),
)


def seed_courses() -> None:
    instructor = db.session.scalar(select(User).where(User.email == "chef@demo.local"))
    if instructor is None:
        instructor = User(
            name="Chef Demo",
            email="chef@demo.local",
            password_hash=hash_password("demo-password-change-me"),
            role=UserRole.INSTRUCTOR,
        )
        db.session.add(instructor)

    for title, category_name, slug, level in COURSES:
        if db.session.scalar(select(Course.id).where(Course.title == title)):
            continue
        category = db.session.scalar(select(Category).where(Category.slug == slug))
        if category is None:
            category = Category(name=category_name, slug=slug)
            db.session.add(category)
        course = Course(
            title=title,
            description=f"Curso demonstrativo de {title.lower()}.",
            thumbnail_url=(
                "https://images.unsplash.com/photo-1547592180-85f173990554"
                f"?{slug}"
            ),
            level=level,
            instructor=instructor,
            category=category,
        )
        for module_position in (1, 2):
            module = Module(title=f"Módulo {module_position}", position=module_position)
            for lesson_position in (1, 2, 3):
                module.lessons.append(
                    Lesson(
                        title=f"Aula {lesson_position}",
                        description="Conteúdo demonstrativo.",
                        video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                        position=lesson_position,
                        is_preview=lesson_position == 1,
                    )
                )
            course.modules.append(module)
        db.session.add(course)
    db.session.commit()


def register_seed_command(app: Flask) -> None:
    @app.cli.command("seed-courses")
    def seed_courses_command() -> None:
        seed_courses()
        click.echo("Catálogo de demonstração criado/atualizado.")
