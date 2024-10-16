from fastapi import FastAPI

from src.controllers import matching_algorithm

app = FastAPI()

app.include_router(matching_algorithm.router, prefix="/assignTeachers")

a = {
    "teachers": {
        "teacher1": {
            "seniority": 1,
            "subject_he_know_how_to_teach": [
                {"subject": "Arq1", "role": ["Theory"]}
            ],
            "available_times": {
                "Monday": [9, 10, 11]
            },
            "weekly_hours_max_work": 10,
            "groups": [{
                "my_role": ["Theory"],
                "subject": "Arq1",
                "other_teacher": [{"teacher": "teacher2", "role": ["Theory"]}]
            }]
        },
        "teacher2": {
            "seniority": 1,
            "subject_he_know_how_to_teach": [
                {"subject": "Arq1", "role": ["Theory"]}
            ],
            "available_times": {
                "Monday": [9, 10, 11]
            },
            "weekly_hours_max_work": 10,
            "groups": [{
                "my_role": ["Theory"],
                "subject": "Arq1",
                "other_teacher": [{"teacher": "teacher1", "role": ["Theory"]}]
            }]
        },
        "teacher3": {
            "seniority": 8,
            "subject_he_know_how_to_teach": [
                {"subject": "Arq1", "role": ["Theory"]}
            ],
            "available_times": {
                "Monday": [9, 10, 11]
            },
            "weekly_hours_max_work": 10
        }
    },
    "classes": {
        "class1": {
            "subject": "Arq1",
            "subClasses": [
                {
                    "role": "Theory",
                    "times": {"Monday": [9, 10]},
                    "num_teachers": 2
                }
            ]
        }
    }
}
from src.controllers.DTO.in_models.assignment_request_model import AssignmentRequestModel
data = AssignmentRequestModel(**a)
print(data)

@app.get("/", summary="SanityCheck")
async def sanity_check():
    return {"message": "Welcome to the Timetable Scheduling API"}