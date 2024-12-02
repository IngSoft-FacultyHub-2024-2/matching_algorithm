from typing import Optional
from pydantic import BaseModel, conint

class AvailableTimesModel(BaseModel):
    Monday: Optional[list[conint(ge=8, le=23)]] = None  
    Tuesday: Optional[list[conint(ge=8, le=23)]] = None  
    Wednesday: Optional[list[conint(ge=8, le=23)]] = None  
    Thursday: Optional[list[conint(ge=8, le=23)]] = None  
    Friday: Optional[list[conint(ge=8, le=23)]] = None  
