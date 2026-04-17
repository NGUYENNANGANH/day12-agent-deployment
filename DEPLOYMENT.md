# Day 12 Lab - Deployment Information (RENDER)
**Student:** Nguyễn Năng Anh (2A202600184)

## 🌐 Live Access
- **Frontend (Giao diện người dùng):** [https://eco-health-web.onrender.com](https://eco-health-web.onrender.com)
- **Backend (API Endpoint):** `https://eco-health-api.onrender.com`

## Platform
Render (Docker Runtime)

## tech Stack
- **Backend**: FastAPI (Python 3.11)
- **Deployment**: Render Blueprint (Infrastructure as Code)
- **Database**: Redis (Native Render Service)
- **Security**: JWT Authentication + Rate Limiting

## Verification Commands

### 1. Health Check
```bash
curl https://eco-health-api.onrender.com/health
```
**Expected Response**: `{"status": "ok", ...}`

### 2. API Test (Protection Check)
```bash
curl -i https://eco-health-api.onrender.com/api/ask
```
**Expected Response**: `401 Unauthorized` (Chứng minh API đã được bảo vệ)

## Environment Variables Configuration
- `PORT`: 8000
- `AGENT_API_KEY`: [Configured on Render Dashboard]
- `OPENAI_API_KEY`: [Configured on Render Dashboard]
- `ENVIRONMENT`: production
- `MONGO_URI`: [Configured on Render Dashboard]

## Screenshots
- [Deployment Dashboard](screenshots/render_dashboard.png)
- [Service Running/Logs](screenshots/render_logs.png)
- [Health Check Result](screenshots/render_health.png)
- [Rate Limiting Test](screenshots/4.3.png)
- [Cost Guard Tracking](screenshots/4.2.png)
