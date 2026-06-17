from app.utils.celery_app import celery
from .retrival import get_rag_chain
import logging

logger = logging.getLogger(__name__)

@celery.task(name="app_bot.generate_answer_task")
def generate_answer_task(query):
    try:
        logger.info(f"Processing query in task: {query}")
        chain = get_rag_chain()
        result = chain.invoke(query)
        logger.info(f"Task result successfully generated")
        return result["result"]
    except Exception as e:
        logger.error(f"Error in generate_answer_task: {e}", exc_info=True)
        raise e
