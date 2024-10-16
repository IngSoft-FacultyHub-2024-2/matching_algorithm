from pydantic import BaseModel, constr

from .role_model import RoleModel, RoleType


class GroupModel(BaseModel):
    my_role: list[RoleType]  
    subject: constr(min_length=1)  
    other_teacher: list[RoleModel]  