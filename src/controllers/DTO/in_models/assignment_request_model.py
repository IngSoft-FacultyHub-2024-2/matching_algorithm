from pydantic import BaseModel
from typing import Dict

from ....matching_algorithm import TeacherModel, ClassModel


class AssignmentRequestModel(BaseModel):
    teachers: Dict[str, TeacherModel]
    classes: Dict[str, ClassModel]
