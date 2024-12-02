from fastapi import FastAPI

from src.controllers import matching_algorithm

app = FastAPI()

app.include_router(matching_algorithm.router, prefix="/assignTeachers")


@app.get("/", summary="SanityCheck")
async def sanity_check() -> dict:
    return {"message": "Welcome to the Timetable Scheduling API"}
