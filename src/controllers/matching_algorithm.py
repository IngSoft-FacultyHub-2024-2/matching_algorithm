from fastapi import APIRouter, Body

from .DTO.in_models.assignment_request_model import AssignmentRequestModel
from src.matching_algorithm import solve_timetable
router = APIRouter()

@router.post("/", summary="Assign teachers to classes",
            # TODO: Add description and responses   
            # description="Assign teachers to classes based on their available times and roles.",
            # responses={
            #       200: {"description": "Successful assignment", "model": dict},
            #       400: {"description": "Bad Request"},
            #   })
            )
async def assign_teachers_to_classes(data: AssignmentRequestModel):

    teachers = data.teachers
    classes = data.classes
    print(dict(teachers))
    print(dict(teachers)["teacher1"])

    print(classes)
    return {"message": "Assignment successful"}
