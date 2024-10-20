from pydantic import BaseModel

from .available_times_model import AvailableTimesModel
from .role_model import RoleType


class SubClassModel(BaseModel):
    role: RoleType
    times: AvailableTimesModel
    num_teachers: int
