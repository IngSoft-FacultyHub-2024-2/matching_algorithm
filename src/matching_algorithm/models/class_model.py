from pydantic import BaseModel

from .sub_class_model import SubClassModel


class ClassModel(BaseModel):
    subject: str
    subClasses: list[SubClassModel]
