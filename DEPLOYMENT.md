# Day 12 Lab - Deployment Information (RENDER)

## Public Service URL
**https://eco-health-web.onrender.com**

## Tech Stack
- **Frontend**: Nginx (Dockerized)
- **Backend**: FastAPI (Python 3.11)
- **Database**: MongoDB Atlas (Managed)
- **Cache/Session**: Redis (Render Managed)
- **Deployment**: Render (Multi-service Blueprint)

## Core Features Implemented
- **User Authentication**: JWT (JSON Web Token) with multi-page support.
- **Rate Limiting**: 10 requests per minute (Redis-based) per user.
- **Cost Guard**: Token budget protection ($1.0/user/day).
- **Geolocation**: Browser-based coordinates integrated with AI Tools.
- **Architecture**: Decoupled Monorepo with Nginx reverse proxy.

## Verification Commands

### 1. Health Check
```bash
curl https://eco-health-web.onrender.com/api/health
```
**Expected Response**: `{"status": "ok"}`

### 2. Registration (Test User)
```bash
curl -X POST https://eco-health-web.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "render_test", "password": "password123"}'
```

### 3. Login & Token Retrieval
```bash
curl -X POST https://eco-health-web.onrender.com/api/auth/token \
  -d "username=render_test&password=password123"
```

## Environment Variables Configuration
- `MONGO_URI`: mongodb+srv://... (Atlas connection string)
- `REDIS_URL`: redis://... (Internal Render service)
- `JWT_SECRET`: [AUTO_GENERATED_BY_RENDER]
- `OPENAI_API_KEY`: [YOUR_API_KEY]
- `BACKEND_HOST`: eco-health-api (Internal networking)
