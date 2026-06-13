import redis
from app.core.config import settings

# Initialize Redis connection client
# decode_responses=True ensures we get strings instead of bytes
redis_client = redis.from_url(
    settings.REDIS_URL, 
    decode_responses=True
)

def get_redis():
    """Dependency to get Redis client instance"""
    return redis_client
