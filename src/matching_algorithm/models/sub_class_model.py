from pydantic import BaseModel

from .role_model import RoleType
from .available_times_model import AvailableTimesModel

class SubClassModel(BaseModel):
    role: RoleType
    times: AvailableTimesModel  
    num_teachers: int