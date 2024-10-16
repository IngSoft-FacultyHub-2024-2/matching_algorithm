from typing import Literal, Optional
from pydantic import BaseModel, conint, constr, Field

RoleType = Literal["Theory", "Practice"]

class RoleModel(BaseModel):
    role: list[RoleType] 

class SubjectModel(BaseModel):
    subject: constr(min_length=1) 
    role: list[RoleType] 

class AvailableTimesModel(BaseModel):
    Monday: Optional[list[conint(ge=8, le=23)]] = None  
    Tuesday: Optional[list[conint(ge=8, le=23)]] = None  
    Wednesday: Optional[list[conint(ge=8, le=23)]] = None  
    Thursday: Optional[list[conint(ge=8, le=23)]] = None  
    Friday: Optional[list[conint(ge=8, le=23)]] = None  

class GroupModel(BaseModel):
    my_role: list[RoleType]  
    subject: constr(min_length=1)  
    other_teacher: list[RoleModel]  

class TeacherModel(BaseModel):
    seniority: conint(ge=0) 
    subject_he_know_how_to_teach: list[SubjectModel] 
    available_times: AvailableTimesModel  
    weekly_hours_max_work: conint(ge=0)  
    groups: Optional[list[GroupModel]] 

# Example usage
teachers_data = {
    "teacher1": {
        "seniority": 1,
        "subject_he_know_how_to_teach": [
            {"subject": "Arq1", "role": ["Theory"]},
        ],
        "available_times": {
            "Monday": [9, 10, 11], 
        },
        "weekly_hours_max_work": 10,
        "groups": [{
            "my_role": ["Theory"],
            "subject": "Arq1",
            "other_teacher": [{"role": ["Theory"], "teacher": "teacher2"}]
        }]
    }
}

teacher = TeacherModel(**teachers_data["teacher1"])
print(teacher)
