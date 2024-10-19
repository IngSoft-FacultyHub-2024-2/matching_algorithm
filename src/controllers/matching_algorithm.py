from fastapi import APIRouter, Body

from .DTO.in_models.assignment_request_model import AssignmentRequestModel
from src.matching_algorithm import solve_timetable
router = APIRouter()

@router.post("/", summary="Assign teachers to classes",
            description="Assign teachers to classes based on their available times and roles.",
            # responses={
            #       200: {"description": "Successful assignment"},
            #       400: {"description": "Bad Request"},
            #   }
            )
async def assign_teachers_to_classes(data: AssignmentRequestModel):
    data = data.dict()
    teachers = data["teachers"]
    classes = data["classes"]
    result, unassigned, conflicts = solve_timetable(teachers, classes)
    return {"matches": result, "unassigned": unassigned, "conflicts": conflicts}
