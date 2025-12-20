from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def read_root():
    """Welcome to Humanoid Robotics"""
    return {"message": "Welcome to Humanoid Robotics"}
