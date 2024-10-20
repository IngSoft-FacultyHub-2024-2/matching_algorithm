from typing import Dict

from pydantic import BaseModel

from src.matching_algorithm import ClassModel, TeacherModel


class AssignmentRequestModel(BaseModel):
    teachers: Dict[str, TeacherModel]
    classes: Dict[str, ClassModel]
