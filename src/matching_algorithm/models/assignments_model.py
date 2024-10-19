from pydantic import BaseModel
from typing import Any

class ConflictModel(BaseModel):
    teacher_without_any_classes: list[str]
    teacher_has_more_than_weekly_hours: list[dict[str, Any]]
    classes_without_teachers: list[dict[str, str]]
    partially_unassigned: list[dict[str, Any]]


class Assignments(BaseModel):
    matches: dict[str, dict[str, list[str]]]
    unassigned: list[tuple[str, str]]
    conflicts: ConflictModel

