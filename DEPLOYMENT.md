# Day 12 Lab - Deployment Information (RAILWAY)
**Student:** Nguyễn Năng Anh (2A202600184)

## Public Service URL
**https://eco-health-agent-2a202600184.onrender.com**

## Tech Stack
- **Backend**: FastAPI (Python 3.11)
- **Deployment**: Render (Blueprint/Docker)
- **Security**: JWT Authentication + Rate Limiting
- **Reliability**: Health Check + Graceful Shutdown implemented

## Core Features Verified
- **Health Check**: Endpoint `/health` returns `200 OK`.
- **JWT Auth**: Protected `/ask` endpoint (401 without token).
- **Rate Limiting**: Integrated sliding window (10 requests/min).
- **Cost Guard**: Token usage tracking enabled.

## Verification Commands

### 1. Health Check
```bash
curl https://eco-health-agent-2a202600184.onrender.com/health
```
**Expected Response**: `{"status": "ok", ...}`

### 2. Protected Endpoint (Authentication required)
```bash
curl -i https://eco-health-agent-2a202600184.onrender.com/ask
```
**Expected Response**: `401 Unauthorized`

## Environment Variables Configuration (Railway)
- `PORT`: 8000
- `AGENT_API_KEY`: [SECRET_KEY]
- `ENVIRONMENT`: production
