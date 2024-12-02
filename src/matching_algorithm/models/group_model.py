from pydantic import BaseModel, constr

from .role_model import RoleType

class OtherTeacherGroup(BaseModel):
    teacher: str
    role: list[RoleType]
    
class GroupModel(BaseModel):
    my_role: list[RoleType]  
    subject: str 
    other_teacher: list[OtherTeacherGroup]  
