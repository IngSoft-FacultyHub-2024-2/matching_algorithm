from fastapi import APIRouter

from .DTO.in_models.assignment_request_model import AssignmentRequestModel
from src.matching_algorithm import solve_timetable, Assignments
router = APIRouter()

@router.post("/", summary="Assign teachers to classes",
            description="Assign teachers to classes based on their available times and roles.",
            # responses={
            #       200: {"description": "Successful assignment"},
            #       400: {"description": "Bad Request"},
            #   }
             response_model=Assignments
            )
async def assign_teachers_to_classes(data: AssignmentRequestModel) -> Assignments:
    teachers = data.teachers
    classes = data.classes
    return solve_timetable(teachers, classes)

