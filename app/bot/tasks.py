from app.utils.celery_app import celery
from .retrival import build_rag_chain
import logging

logger = logging.getLogger(__name__)

# Cache the chain globally in the worker
_rag_chain = None

def get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        _rag_chain = build_rag_chain()
    return _rag_chain

@celery.task(name="app_bot.generate_answer_task")
def generate_answer_task(query):
    try:
        logger.info(f"Processing query in task: {query}")
        chain = get_rag_chain()
        result = chain.invoke(query)
        logger.info(f"Task result: {result}")
        return result["result"]
    except Exception as e:
        logger.error(f"Error in generate_answer_task: {e}", exc_info=True)
        return str(e)
