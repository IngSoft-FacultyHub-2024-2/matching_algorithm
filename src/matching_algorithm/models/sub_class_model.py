from pydantic import BaseModel, conint

from .role_model import RoleType
from .available_times_model import AvailableTimesModel

class SubClassModel(BaseModel):
    role: RoleType
    times: AvailableTimesModel  
    num_teachers: conint(ge=1)