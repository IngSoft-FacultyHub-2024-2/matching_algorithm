from fastapi import APIRouter, HTTPException

from src.matching_algorithm.models import TeacherModel

router = APIRouter()

@router.post("/", summary="Assign teachers to classes",
            # TODO: Add description and responses   
            # description="Assign teachers to classes based on their available times and roles.",
            # responses={
            #       200: {"description": "Successful assignment", "model": dict},
            #       400: {"description": "Bad Request"},
            #   })
            )
async def assign_teachers_to_classes(teachers: dict[str, TeacherModel], classes):
    pass