# BÁO CÁO HOÀN THÀNH PART 1: 01-localhost-vs-production

## Ngày: 17/04/2026
## Thực hành: Từ Localhost Đến Production

---

## 1. Mục tiêu

- Hiểu tại sao "it works on my machine" là vấn đề
- Nhận ra sự khác biệt giữa dev và production environment
- Áp dụng 4 nguyên tắc 12-factor cơ bản

---

## 2. Các file đã có sẵn

### 2.1. Develop (Basic - Anti-patterns)
| File | Mô tả |
|------|-------|
| `app.py` | ❌ Hardcode secrets, không health check, debug mode bật cứng |
| `requirements.txt` | fastapi==0.115.0, uvicorn[standard]==0.30.0 |
| `utils/mock_llm.py` | Mock LLM response |

### 2.2. Production (Advanced - 12-Factor)
| File | Mô tả |
|------|-------|
| `app.py` | ✅ Config từ env, health check, graceful shutdown, structured logging |
| `config.py` | ✅ Centralized config management với validation |
| `.env.example` | Template cho environment variables |
| `.env` | File config (không commit) |
| `requirements.txt` | Thêm python-dotenv==1.0.1 |

---

## 3. Các vấn đề phát hiện trong code

### Develop (`develop/app.py`):
1. ❌ API key hardcode: `OPENAI_API_KEY = "sk-hardcoded-fake-key..."`
2. ❌ Database URL hardcode trong code
3. ❌ Không có health check endpoint
4. ❌ Port cố định 8000, không đọc từ environment
5. ❌ Debug reload bật sẵn trong production
6. ❌ Log ra secrets: `print(f"[DEBUG] Using key: {OPENAI_API_KEY}")`

### Production (`production/app.py`):
✅ Đã tuân thủ 12-factor:
- Config từ environment variables
- Structured JSON logging
- Health check endpoints (`/health`, `/ready`, `/metrics`)
- Graceful shutdown với SIGTERM handling
- 0.0.0.0 binding (chạy được trong container)
- Port từ PORT env var

---

## 4. Các thay đổi đã thực hiện

### 4.1. Tạo file mới
- `develop/.env.example` - Template cho development environment

### 4.2. Sửa lỗi
- `production/config.py`: Thêm `import warnings` để hàm `validate()` hoạt động đúng

### 4.3. Kiểm tra
- Cài đặt dependencies: ✅ Thành công
- Chạy thử app develop: ✅ Chạy được trên http://localhost:8000

---

## 5. So sánh Basic vs Advanced

| Tiêu chí | Basic (❌) | Advanced (✅) |
|----------|-----------|---------------|
| Config | Hardcode trong code | Đọc từ env vars |
| Secrets | `api_key = "sk-abc123"` | `os.getenv("OPENAI_API_KEY")` |
| Port | Cố định `8000` | Từ `PORT` env var |
| Health check | Không có | `GET /health`, `/ready` |
| Shutdown | Tắt đột ngột | Graceful — hoàn thành request |
| Logging | `print()` | Structured JSON logging |
| CORS | Không có | Có thể cấu hình |
| Binding | `localhost` | `0.0.0.0` |

---

## 6. Hướng dẫn chạy thử

### Develop (Basic):
```bash
cd develop
pip install -r requirements.txt
python app.py
# Truy cập: http://localhost:8000
```

### Production (Advanced):
```bash
cd production
pip install -r requirements.txt
cp .env.example .env
# Sửa .env nếu cần
python app.py
# Truy cập: http://localhost:8000
```

---

## 7. Kết luận

Part 1 đã hoàn thành. Học viên hiểu được:
- Sự khác biệt giữa localhost và production environment
- Các anti-patterns khi deploy lên cloud
- Cách áp dụng 12-factor app methodology
- Tầm quan trọng của config management và health checks

---

## 8. Trạng thái

- [x] Hoàn thành
- [ ] Cần review thêm
- [ ] Có vấn đề cần giải quyết