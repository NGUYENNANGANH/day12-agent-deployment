import time
import redis
from fastapi import HTTPException
from app.config import settings

r = redis.from_url(settings.redis_url)

def check_rate_limit(user_id: str):
    """
    Sliding window rate limit using Redis sorted sets (ZSET).
    """
    now = time.time()
    window_start = now - 60
    key = f"rate_limit:{user_id}"

    pipeline = r.pipeline()
    # Remove older requests
    pipeline.zremrangebyscore(key, 0, window_start)
    # Count current requests
    pipeline.zcard(key)
    # Add new request
    pipeline.zadd(key, {str(now): now})
    # Set expiry to clean up
    pipeline.expire(key, 60)
    
    results = pipeline.execute()
    current_count = results[1]
    
    if current_count >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {settings.rate_limit_per_minute} req/min",
            headers={"Retry-After": "60"},
        )
