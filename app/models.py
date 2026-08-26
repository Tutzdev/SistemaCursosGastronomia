from datetime import UTC, datetime
from enum import StrEnum

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


def utc_now() -> datetime:
    return datetime.now(UTC)


class UserRole(StrEnum):
    STUDENT = "STUDENT"
    INSTRUCTOR = "INSTRUCTOR"
    ADMIN = "ADMIN"


class CourseLevel(StrEnum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"


class CourseStatus(StrEnum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(254), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole, native_enum=False, length=20),
        default=UserRole.STUDENT,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    instructed_courses: Mapped[list["Course"]] = relationship(
        back_populates="instructor"
    )


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    courses: Mapped[list["Course"]] = relationship(back_populates="category")


class Course(db.Model):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text())
    thumbnail_url: Mapped[str | None] = mapped_column(String(500))
    level: Mapped[CourseLevel] = mapped_column(
        SqlEnum(CourseLevel, native_enum=False, length=20), nullable=False
    )
    instructor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), index=True, nullable=False
    )
    status: Mapped[CourseStatus] = mapped_column(
        SqlEnum(CourseStatus, native_enum=False, length=20),
        default=CourseStatus.PUBLISHED,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    instructor: Mapped[User] = relationship(back_populates="instructed_courses")
    category: Mapped[Category] = relationship(back_populates="courses")
    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
    modules: Mapped[list["Module"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Module.position",
    )


class Module(db.Model):
    __tablename__ = "modules"
    __table_args__ = (UniqueConstraint("course_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    course: Mapped[Course] = relationship(back_populates="modules")
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="Lesson.position",
    )


class Lesson(db.Model):
    __tablename__ = "lessons"
    __table_args__ = (UniqueConstraint("module_id", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.id", ondelete="CASCADE"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text())
    video_url: Mapped[str] = mapped_column(String(500), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    is_preview: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    module: Mapped[Module] = relationship(back_populates="lessons")


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="uq_enrollments_user_course"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), index=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    user: Mapped[User] = relationship(back_populates="enrollments")
    course: Mapped[Course] = relationship(back_populates="enrollments")
