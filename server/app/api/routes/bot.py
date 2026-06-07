from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.bot.tasks import generate_answer_task
from celery.result import AsyncResult
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class BotQuery(BaseModel):
    query: str

@router.post("/generate", status_code=status.HTTP_202_ACCEPTED)
async def generate_answer(data: BotQuery):
    try:
        task = generate_answer_task.delay(data.query)
        return {"task_id": task.id}
    except Exception as e:
        logger.error(f"Error in generate_answer: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }
