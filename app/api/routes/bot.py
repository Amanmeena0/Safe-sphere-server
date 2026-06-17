from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.api.dependencies import get_current_user
from app.models.models import User
from app.bot.retrival import get_rag_chain
from starlette.concurrency import run_in_threadpool
import logging

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
        logger.info(f"Generating synchronous answer for query: {data.query}")
        chain = get_rag_chain()
        # Run the synchronous LangChain invoke in a threadpool to keep FastAPI async
        result = await run_in_threadpool(chain.invoke, data.query)
        
        # We return both 'result' for direct access and 'task_id' as 'sync' 
        # to allow the frontend to bypass polling if it detects this.
        return {
            "result": result["result"],
            "task_id": "sync_completed" 
        }
    except Exception as e:
        logger.error(f"Error in generate_answer: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{task_id}")
async def get_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    # Compatibility shim for frontend polling. 
    # If the frontend still polls 'sync_completed', we return the status immediately.
    if task_id == "sync_completed":
        return {
            "task_id": task_id,
            "status": "SUCCESS",
            "result": None # Result was already sent in the /generate response
        }
    
    # Fallback for any actual background tasks if they still exist
    from celery.result import AsyncResult
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }
