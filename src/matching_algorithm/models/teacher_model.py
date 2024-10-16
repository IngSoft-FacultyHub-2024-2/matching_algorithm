from typing import Optional
from pydantic import BaseModel, conint, constr

from .available_times_model import AvailableTimesModel
from .subject_model import SubjectModel
from .role_model import RoleType
from .group_model import GroupModel

class TeacherModel(BaseModel):
    seniority: conint(ge=0) 
    subject_he_know_how_to_teach: list[SubjectModel] 
    available_times: AvailableTimesModel  
    weekly_hours_max_work: conint(ge=0)  
    groups: Optional[list[GroupModel]] = None

