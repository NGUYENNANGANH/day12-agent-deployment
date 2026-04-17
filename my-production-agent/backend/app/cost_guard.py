from datetime import datetime, timezone
import redis
import logging
from fastapi import HTTPException
from app.config import settings

logger = logging.getLogger(__name__)

# Create a lazy redis client
r = redis.from_url(settings.redis_url, decode_responses=True)

def check_budget(user_id: str, estimated_cost: float) -> bool:
    """
    Track spending in Redis.
    Fails open if Redis is unavailable.
    """
    try:
        month_key = datetime.now(timezone.utc).strftime("%Y-%m")
        key = f"budget:{user_id}:{month_key}"
        
        current = float(r.get(key) or 0.0)
        
        if current + estimated_cost > settings.monthly_budget_usd:
            raise HTTPException(
                status_code=402, 
                detail=f"Payment Required: Monthly budget of ${settings.monthly_budget_usd} exceeded."
            )
        
        r.incrbyfloat(key, estimated_cost)
        r.expire(key, 32 * 24 * 3600)
        return True
    except redis.exceptions.RedisError as e:
        logger.warning(f"Redis Cost Guard failed (ignoring): {e}")
        return True
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in cost guard: {e}")
        return True
