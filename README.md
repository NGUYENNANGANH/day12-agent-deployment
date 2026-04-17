# 🌍 Eco-Health AI Agent (Day 12 Production)

## 🔗 Live Demo URL: [https://eco-health-web.onrender.com](https://eco-health-web.onrender.com)

---

## 📖 Giới thiệu dự án
Eco-Health AI Agent là một trợ lý AI thông minh chuyên tư vấn về sức khỏe và môi trường. Dự án được phát triển theo kiến trúc **Decoupled (Tách biệt)** hoàn toàn giữa Frontend và Backend để tối ưu hiệu năng và khả năng mở rộng trên Cloud.

### Tính năng nổi bật:
- **Tư vấn môi trường**: Kết hợp dữ liệu thời tiết và chất lượng không khí (AQI) thực tế qua Open-Meteo.
- **Định vị GPS**: Tự động nhận diện tọa độ người dùng để đưa ra cảnh báo chính xác tại vị trí hiện tại.
- **Bảo mật JWT**: Hệ thống đăng ký/đăng nhập an toàn.
- **Quản lý chi phí (Cost Guard)**: Giới hạn ngân sách Token để tránh lãng phí API Key.
- **Giao diện tối giản**: Phong cách Notion monochrome, hỗ trợ Responsive (điện thoại & máy tính).

---

## 🚀 Hướng dẫn chạy Locally (Trên máy tính của bạn)

Để chạy dự án này mà không gặp lỗi, bạn cần cài đặt **Docker** và **Docker Desktop**.

1. **Clone Repository (Nếu chưa có):**
   ```bash
   git clone <link-repo-github>
   cd day12_ha-tang-cloud_va_deployment/my-production-agent
   ```

2. **Cấu hình Biến môi trường:**
   Tạo file `.env` từ file mẫu:
   ```bash
   cp .env.example .env
   ```
   Sau đó mở file `.env` và điền `OPENAI_API_KEY` của bạn vào.

3. **Khởi động dự án bằng Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Truy cập:**
   - Website chính: `http://localhost:8080`
   - API Backend: `http://localhost:8000/api/health`

---

## 🏗️ Kiến trúc hệ thống
- **Frontend**: Nginx (Alpine) phục vụ file tĩnh và Proxy API.
- **Backend**: FastAPI (Python 3.11) xử lý logic nghiệp vụ và Agent.
- **Database**: MongoDB (Lưu trữ người dùng và lịch sử chat).
- **Cache**: Redis (Xử lý Rate Limiting và Memory).

---
*Dự án thuộc chương trình đào tạo AI thực chiến - Day 12.*
