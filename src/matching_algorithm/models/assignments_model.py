from pydantic import BaseModel, Field
from typing import Any

from .role_model import RoleType

class MoreThanWeeklyHoursConflict(BaseModel):
    teacher: str
    weekly_hours: int
    assigned_hours: int

class ClassesWithoutTeachersConflict(BaseModel):
    class_name: str
    role: RoleType
    subject: str
    
class PartiallyUnassignedConflict(BaseModel):
    class_name: str
    role: RoleType
    assigned: int
    needed: int

class ConflictModel(BaseModel):
    teacher_without_any_classes: list[str] = Field(default_factory=list)
    teacher_has_more_than_weekly_hours: list[MoreThanWeeklyHoursConflict] = Field(default_factory=list)
    classes_without_teachers: list[ClassesWithoutTeachersConflict] = Field(default_factory=list)
    partially_unassigned: list[PartiallyUnassignedConflict] = Field(default_factory=list)

    def add_teacher_without_any_classes(self, teacher_name: str):
        self.teacher_without_any_classes.append(teacher_name)

    def add_teacher_has_more_than_weekly_hours(self, teacher_name: str, weekly_hours: int, assigned_hours: int):
        self.teacher_has_more_than_weekly_hours.append(
            MoreThanWeeklyHoursConflict(teacher=teacher_name, 
                                weekly_hours=weekly_hours, 
                                assigned_hours=assigned_hours)
                                )
        
    def add_classes_without_teachers(self, class_name: str, role: RoleType, subject: str):
        self.classes_without_teachers.append(ClassesWithoutTeachersConflict(
            class_name=class_name,
            role=role,
            subject=subject
        ))

    def add_partially_unassigned(self, class_name: str,role: str, assigned: int, needed: int):
        self.partially_unassigned.append(PartiallyUnassignedConflict(
            class_name=class_name,
            role=role,
            assigned=assigned,
            needed=needed
        ))


        
class Assignments(BaseModel):
    matches: dict[str, dict[RoleType, list[str]]]
    unassigned: list[tuple[str, str]]
    conflicts: ConflictModel