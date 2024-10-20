from typing import Optional
from pydantic import BaseModel, conint

class AvailableTimesModel(BaseModel):
    Monday: Optional[list[int]] = None  
    Tuesday: Optional[list[int]] = None  
    Wednesday: Optional[list[int]] = None  
    Thursday: Optional[list[int]] = None  
    Friday: Optional[list[int]] = None  
