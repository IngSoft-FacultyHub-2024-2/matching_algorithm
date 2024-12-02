from typing import Literal
from pydantic import BaseModel, constr

from .role_model import RoleType

class SubjectModel(BaseModel):
    subject: constr(min_length=1) 
    role: list[RoleType] 