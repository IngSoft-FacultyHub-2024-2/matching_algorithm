from typing import Optional

from pydantic import BaseModel

from .available_times_model import AvailableTimesModel
from .group_model import GroupModel
from .subject_model import SubjectModel


class TeacherModel(BaseModel):
    seniority: int
    subject_he_know_how_to_teach: list[SubjectModel]
    available_times: AvailableTimesModel
    weekly_hours_max_work: int
    groups: Optional[list[GroupModel]] = None
