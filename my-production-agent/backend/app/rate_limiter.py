import time
import redis
import logging
from fastapi import HTTPException
from app.config import settings

logger = logging.getLogger(__name__)

# Create a lazy redis client
r = redis.from_url(settings.redis_url, decode_responses=True)

def check_rate_limit(user_id: str):
    """
    Sliding window rate limit using Redis.
    Fails open if Redis is unavailable to prevent blocking user requests.
    """
    try:
        now = time.time()
        window_start = now - 60
        key = f"rate_limit:{user_id}"

        pipeline = r.pipeline()
        pipeline.zremrangebyscore(key, 0, window_start)
        pipeline.zcard(key)
        pipeline.zadd(key, {str(now): now})
        pipeline.expire(key, 60)
        
        results = pipeline.execute()
        current_count = results[1]
        
        if current_count >= settings.rate_limit_per_minute:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded: {settings.rate_limit_per_minute} req/min",
                headers={"Retry-After": "60"},
            )
    except redis.exceptions.RedisError as e:
        logger.warning(f"Redis Rate Limiter failed (ignoring): {e}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in rate limiter: {e}")
