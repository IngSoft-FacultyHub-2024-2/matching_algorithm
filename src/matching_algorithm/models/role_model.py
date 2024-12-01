from typing import Literal

from pydantic import BaseModel

RoleType = Literal["Teórico", "Tecnología"]


class RoleModel(BaseModel):
    role: list[RoleType]
