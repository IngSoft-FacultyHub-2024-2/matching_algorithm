from pydantic import BaseModel

from .role_model import RoleType

class SubjectModel(BaseModel):
    subject: str 
    role: list[RoleType] 