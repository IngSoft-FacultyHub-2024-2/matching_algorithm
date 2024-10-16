from typing import Optional
from pydantic import BaseModel, conint

class AvailableTimesModel(BaseModel):
    Monday: Optional[list[conint(ge=8, le=23)]] = None  
    Tuesday: Optional[list[conint(ge=8, le=23)]] = None  
    Wednesday: Optional[list[conint(ge=8, le=23)]] = None  
    Thursday: Optional[list[conint(ge=8, le=23)]] = None  
    Friday: Optional[list[conint(ge=8, le=23)]] = None  

    def items(self):
        return {k: v for k, v in self.dict().items() if v is not None}.items()
    
    def keys(self):
        return {k: v for k, v in self.dict().items() if v is not None}.keys()
    
    def values(self):
       return {k: v for k, v in self.dict().items() if v is not None}.values()