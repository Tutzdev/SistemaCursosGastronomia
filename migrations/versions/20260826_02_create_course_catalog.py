"""Create course catalog tables.

Revision ID: 20260826_02
Revises: 20260825_01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260826_02"
down_revision: str | None = "20260825_01"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_categories_slug"), "categories", ["slug"])
    op.create_table(
        "courses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(160), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("thumbnail_url", sa.String(500)),
        sa.Column("level", sa.String(20), nullable=False),
        sa.Column("instructor_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
        sa.ForeignKeyConstraint(["instructor_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_courses_title"), "courses", ["title"])
    op.create_index(op.f("ix_courses_category_id"), "courses", ["category_id"])
    op.create_index(op.f("ix_courses_instructor_id"), "courses", ["instructor_id"])
    op.create_table(
        "modules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(160), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("course_id", "position"),
    )
    op.create_index(op.f("ix_modules_course_id"), "modules", ["course_id"])
    op.create_table(
        "lessons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("module_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(160), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("video_url", sa.String(500), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("is_preview", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["module_id"], ["modules.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("module_id", "position"),
    )
    op.create_index(op.f("ix_lessons_module_id"), "lessons", ["module_id"])


def downgrade() -> None:
    op.drop_table("lessons")
    op.drop_table("modules")
    op.drop_table("courses")
    op.drop_table("categories")
