from fastapi import APIRouter

from src.matching_algorithm import Assignments, solve_timetable

from .DTO.in_models.assignment_request_model import AssignmentRequestModel

router = APIRouter()


@router.post(
    "/",
    summary="Assign teachers to classes",
    description="Assign teachers to classes based on their available times and roles.",
    # responses={
    #       200: {"description": "Successful assignment"},
    #       400: {"description": "Bad Request"},
    #   }
    response_model=Assignments,
)
async def assign_teachers_to_classes(data: AssignmentRequestModel) -> Assignments:
    teachers = data.teachers
    classes = data.classes
    modules = data.modules
    teacher_names_with_classes = data.teacher_names_with_classes
    preassigned = data.preassigned
    return solve_timetable(teachers, classes, modules, teacher_names_with_classes, preassigned)
