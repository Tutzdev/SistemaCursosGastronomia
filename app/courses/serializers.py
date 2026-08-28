from app.models import Category, Course


def serialize_category(category: Category) -> dict[str, object]:
    return {"id": category.id, "name": category.name, "slug": category.slug}


def serialize_course(course: Course, *, detailed: bool = False) -> dict[str, object]:
    data: dict[str, object] = {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "thumbnail_url": course.thumbnail_url,
        "level": course.level.value,
        "category": serialize_category(course.category),
        "instructor": {"id": course.instructor.id, "name": course.instructor.name},
    }

    if detailed:
        data["modules"] = [
            {
                "id": module.id,
                "title": module.title,
                "position": module.position,
                "lessons": [
                    {
                        "id": lesson.id,
                        "title": lesson.title,
                        "description": lesson.description,
                        "video_url": lesson.video_url,
                        "position": lesson.position,
                        "is_preview": lesson.is_preview,
                    }
                    for lesson in module.lessons
                ],
            }
            for module in course.modules
        ]

    return data
