from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.api.dependencies import get_current_user
from app.bot.retrival import get_rag_chain
from app.models.models import User
from celery.result import AsyncResult
import logging
from starlette.concurrency import run_in_threadpool

router = APIRouter()
logger = logging.getLogger(__name__)

class BotQuery(BaseModel):
    query: str

@router.post("/generate")
async def generate_answer(
    data: BotQuery,
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"Generating answer for query: {data.query}")
        chain = get_rag_chain()
        # Using run_in_threadpool for synchronous chain.invoke to avoid blocking
        result = await run_in_threadpool(chain.invoke, data.query)
        return {"result": result["result"]}
    except Exception as e:
        logger.error(f"Error in generate_answer: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{task_id}")
async def get_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }
