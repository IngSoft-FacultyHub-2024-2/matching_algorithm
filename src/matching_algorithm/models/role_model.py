from typing import Literal

from pydantic import BaseModel

RoleType = Literal["Theory", "Technology"]


class RoleModel(BaseModel):
    role: list[RoleType]
