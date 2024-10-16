from fastapi import FastAPI

from src.controllers import matching_algorithm

app = FastAPI()

app.include_router(matching_algorithm.router, prefix="/assignTeachers", tags=["assignTeachers"])


@app.get("/", summary="SanityCheck")
async def sanity_check():
    return {"message": "Welcome to the Timetable Scheduling API"}