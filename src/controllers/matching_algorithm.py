from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

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
    try:
        teachers = data.teachers
        classes = data.classes
        modules = data.modules
        teacher_names_with_classes = data.teacher_names_with_classes
        preassigned = data.preassigned
        return solve_timetable(teachers, classes, modules, teacher_names_with_classes, preassigned)
    except ValidationError as ve:
        # Handle Pydantic validation errors
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request data: {ve.errors()}",
        )

    except ValueError as ve:
        # Handle specific ValueError cases from the algorithm
        raise HTTPException(
            status_code=422,
            detail=f"Assignment process failed: {str(ve)}. Please review the provided data.",
        )

    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred while assigning teachers to classes. "
                f"Details: {str(e)}"
            ),
        )
