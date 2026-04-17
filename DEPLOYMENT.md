# Day 12 Lab - Deployment Information

## Public Service URL
https://lab12-production-651a.up.railway.app

## Tech Stack
- Backend: FastAPI (Python 3.11)
- Database: MongoDB
- Cache/Session: Redis
- Deployment: Railway (Dockerized)

## Core Features Implemented
- User Authentication: JWT (JSON Web Token)
- Rate Limiting: 10 requests per minute (Redis-based)
- Cost Guard: Token budget protection ($1.0/user/day)
- Geolocation: Browser-based environmental data lookup
- Architecture: Decoupled Frontend (Nginx) and Backend (FastAPI)

## Verification Commands

### 1. Health Check
curl https://lab12-production-651a.up.railway.app/api/health
# Expected: {"status": "ok"}

### 2. Registration (Clean Test)
curl -X POST https://lab12-production-651a.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "student_test", "password": "password123"}'

### 3. Login & Token Retrieval
curl -X POST https://lab12-production-651a.up.railway.app/api/auth/token \
  -d "username=student_test&password=password123"

## Environment Variables Configuration
- PORT: 80
- MONGO_URI: mongodb://mongodb:27017
- REDIS_URL: redis://redis:6379/0
- JWT_SECRET: [REDACTED_IN_REPORT]
- OPENAI_API_KEY: [REDACTED_IN_REPORT]
