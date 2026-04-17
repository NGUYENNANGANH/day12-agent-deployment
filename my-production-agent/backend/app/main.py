import json
import logging
import signal
import time
import asyncio
from typing import Optional
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
import redis
import openai
import httpx

from app.config import settings
from app.db import connect_to_mongo, close_mongo_connection, db
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.rate_limiter import check_rate_limit
from app.cost_guard import check_budget

# -----------------
# Setup Logging
# -----------------
logging.basicConfig(level=logging.INFO, format='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}')
logger = logging.getLogger(__name__)

# -----------------
# Globals & State
# -----------------
START_TIME = time.time()
_is_ready = False
r: Optional[redis.Redis] = None

# -----------------
# Lifespan
# -----------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready, r
    try:
        r = redis.from_url(settings.redis_url, decode_responses=True)
        await connect_to_mongo()
        _is_ready = True
        yield
    finally:
        _is_ready = False
        await close_mongo_connection()
        if r: r.close()

# -----------------
# App Init
# -----------------
app = FastAPI(title="Eco-Health API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------
# Models
# -----------------
class UserRegister(BaseModel):
    username: str
    password: str

class AskRequest(BaseModel):
    question: str = Field(..., description="User's question")
    lat: Optional[float] = None
    lon: Optional[float] = None

class AskResponse(BaseModel):
    question: str
    answer: str
    history_length: int
    timestamp: str

# -----------------
# Auth Routes (Prefixed with /api)
# -----------------
@app.post("/api/auth/register")
async def register(user: UserRegister):
    existing_user = await db.db.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_dict = {
        "username": user.username,
        "hashed_password": get_password_hash(user.password),
        "created_at": datetime.utcnow()
    }
    await db.db.users.insert_one(user_dict)
    return {"msg": "User created successfully"}

@app.post("/api/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# -----------------
# Agent Tools
# -----------------
async def get_coordinates(location_name: str) -> dict:
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "EcoHealthAgent/1.0"}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params, headers=headers)
            data = resp.json()
            if data: return {"lat": data[0]["lat"], "lon": data[0]["lon"]}
        except: pass
    return {}

async def fetch_environmental_data(lat: float, lon: float) -> str:
    weather_url = "https://api.open-meteo.com/v1/forecast"
    aqi_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    w_params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
    aqi_params = {"latitude": lat, "longitude": lon, "hourly": "us_aqi,pm2_5"}
    async with httpx.AsyncClient() as client:
        try:
            w_res, a_res = await asyncio.gather(client.get(weather_url, params=w_params), client.get(aqi_url, params=aqi_params))
            w = w_res.json().get("current_weather", {})
            a = a_res.json().get("hourly", {}).get("us_aqi", [0])
            return json.dumps({"temp": w.get("temperature"), "aqi": a[-1]})
        except: return json.dumps({"error": "API error"})

async def call_openai(question: str, history: list, lat: Optional[float] = None, lon: Optional[float] = None) -> str:
    if not settings.openai_api_key: return "API Key not set"
    client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    
    sys_msg = "Bạn là Chuyên gia Tư vấn Sức khỏe môi trường. Hãy dùng tool để kiểm tra thời tiết/không khí và tư vấn cho người dùng."
    if lat and lon:
        sys_msg += f" Người dùng đang ở vị trí có tọa độ: {lat}, {lon}. Hãy ưu tiên lấy thông tin tại đây nếu họ hỏi về 'chỗ tôi' hoặc 'ở đây'."

    msgs = [{"role": "system", "content": sys_msg}]
    for h in history: msgs.append({"role": "user" if h.startswith("Q: ") else "assistant", "content": h[3:]})
    msgs.append({"role": "user", "content": question})
    
    tools = [{
        "type": "function",
        "function": {
            "name": "get_env", 
            "description": "Lấy thông tin thời tiết/AQI. Nếu không có địa điểm, dùng tọa độ người dùng.",
            "parameters": {
                "type": "object", 
                "properties": {
                    "loc": {"type": "string", "description": "Tên địa danh (tùy chọn)."},
                    "lat": {"type": "number", "description": "Vĩ độ (tùy chọn)."},
                    "lon": {"type": "number", "description": "Kinh độ (tùy chọn)."}
                }
            }
        }
    }]
    
    resp = await client.chat.completions.create(model=settings.llm_model, messages=msgs, tools=tools)
    m = resp.choices[0].message
    if m.tool_calls:
        for t in m.tool_calls:
            args = json.loads(t.function.arguments)
            target_lat = args.get("lat") or lat
            target_lon = args.get("lon") or lon
            loc = args.get("loc")
            
            if loc:
                c = await get_coordinates(loc)
                if c:
                    target_lat, target_lon = c["lat"], c["lon"]
            
            if target_lat and target_lon:
                out = await fetch_environmental_data(float(target_lat), float(target_lon))
            else:
                out = "Vui lòng cung cấp địa danh hoặc bật định vị."
                
            msgs.append(m)
            msgs.append({"role": "tool", "tool_call_id": t.id, "name": "get_env", "content": out})
        r2 = await client.chat.completions.create(model=settings.llm_model, messages=msgs)
        return r2.choices[0].message.content
    return m.content

# -----------------
# Main API Route
# -----------------
@app.post("/api/ask", response_model=AskResponse)
async def ask(body: AskRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user["username"]
    check_rate_limit(user_id)
    history = []
    history_key = f"history:{user_id}"
    
    if r:
        try:
            history = r.lrange(history_key, 0, -1)
        except Exception as e:
            logger.warning(f"Failed to fetch history from Redis: {e}")

    ans = await call_openai(body.question, history, lat=body.lat, lon=body.lon)
    
    if r:
        try:
            r.rpush(history_key, f"Q: {body.question}", f"A: {ans}")
            r.expire(history_key, 86400)
        except Exception as e:
            logger.warning(f"Failed to save history to Redis: {e}")

    return AskResponse(
        question=body.question, 
        answer=ans, 
        history_length=len(history) // 2 + 1, 
        timestamp=datetime.now(timezone.utc).isoformat()
    )

@app.get("/api/health")
def health(): return {"status": "ok"}
