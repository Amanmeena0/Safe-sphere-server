from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def hello_world():
    return {"message": "Hi, Welcome to Safe-sphere Backend System"}
