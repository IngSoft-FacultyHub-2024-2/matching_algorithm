from pydantic import BaseModel


class Module(BaseModel):
    id: int
    time: str
    turn: str
