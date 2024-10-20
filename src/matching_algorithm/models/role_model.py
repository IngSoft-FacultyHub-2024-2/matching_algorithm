from typing import Literal

from pydantic import BaseModel

RoleType = Literal["Theory", "Practice"]


class RoleModel(BaseModel):
    role: list[RoleType]
