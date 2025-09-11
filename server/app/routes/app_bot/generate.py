from flask import Blueprint, request, jsonify
import logging
from .retrival import build_rag_chain

# Create a blueprint for the bot routes
bot_bp = Blueprint('bot', __name__)
rag_chain = build_rag_chain()
logger = logging.getLogger(__name__)

@bot_bp.route("/generate", methods=['POST'])
def generate_answer():
    try:
        # Get JSON data from request
        data = request.get_json()
        logger.info(f"Received request data: {data}")
        if not data or 'query' not in data:
            logger.warning("Query parameter is missing in request.")
            return jsonify({"error": "Query parameter is required"}), 400
        query = data['query']
        logger.info(f"Processing query: {query}")
        result = rag_chain.invoke(query)
        logger.info(f"RAG chain result: {result}")
        return jsonify({"result": result["result"]})
    except Exception as e:
        logger.error(f"Error in generate_answer: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
