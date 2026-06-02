from flask import Blueprint, request, jsonify
import logging
from .tasks import generate_answer_task
from celery.result import AsyncResult

# Create a blueprint for the bot routes
bot_bp = Blueprint('bot', __name__)
logger = logging.getLogger(__name__)

@bot_bp.route("/generate", methods=['POST'])
def generate_answer():
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Query parameter is required"}), 400
        
        query = data['query']
        task = generate_answer_task.delay(query)
        return jsonify({"task_id": task.id}), 202

    except Exception as e:
        logger.error(f"Error in generate_answer: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@bot_bp.route("/status/<task_id>", methods=['GET'])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }
    return jsonify(result), 200
