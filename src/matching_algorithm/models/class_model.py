
from pydantic import BaseModel, constr

from .sub_class_model import SubClassModel

class ClassModel(BaseModel):
    subject: constr(min_length=1)
    subClasses: list[SubClassModel]