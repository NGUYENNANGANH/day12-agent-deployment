from datetime import datetime, timezone
import redis
from fastapi import HTTPException
from app.config import settings

r = redis.from_url(settings.redis_url)

def check_budget(user_id: str, estimated_cost: float) -> bool:
    """
    Return True if within budget, otherwise raise HTTPException.
    
    Logic:
    - Each user has a budget of $10/month
    - Track spending in Redis using key: budget:<user_id>:<YYYY-MM>
    - Reset beginning of month
    """
    month_key = datetime.now(timezone.utc).strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    
    current = float(r.get(key) or 0.0)
    
    if current + estimated_cost > settings.monthly_budget_usd:
        raise HTTPException(
            status_code=402, 
            detail=f"Payment Required: Monthly budget of ${settings.monthly_budget_usd} exceeded."
        )
    
    r.incrbyfloat(key, estimated_cost)
    # Expire in 32 days
    r.expire(key, 32 * 24 * 3600)
    return True
