# Hướng dẫn Deploy Monorepo lên Render

Render cho phép bạn quản lý hạ tầng dưới dạng code (Infrastructure as Code) thông qua file `render.yaml`. Dưới đây là quy trình nộp bài.

## Bước 1: Chuẩn bị MongoDB Atlas

Vì Render không có dịch vụ MongoDB tích hợp:

1. Đăng ký tài khoản miễn phí tại MongoDB Atlas (mongodb.com).
2. Tạo một Cluster mới và thêm một Database User.
3. Trong phần Network Access, thêm địa chỉ 0.0.0.0/0 (để Render có thể truy cập).
4. Lấy chuỗi kết nối (Connection String), ví dụ: `mongodb+srv://user:pass@cluster.mongodb.net/test`.

## Bước 2: Deploy bằng Blueprints

1. Đẩy code của bạn lên GitHub.
2. Tại dashboard Render, chọn **Blueprints**.
3. Kết nối với repository của bạn.
4. Render sẽ đọc file `render.yaml` và liệt kê các service:
   - eco-health-api (Backend)
   - eco-health-web (Frontend)
   - eco-health-redis (Redis)

## Bước 3: Cấu hình Biến môi trường

Trong quá trình khởi tạo, Render sẽ yêu cầu bạn nhập các giá trị còn thiếu:

- `MONGO_URI`: Dán chuỗi kết nối từ MongoDB Atlas ở Bước 1.
- `OPENAI_API_KEY`: Dán API Key của bạn.

Các biến khác như `REDIS_URL` và `JWT_SECRET` đã được cấu hình tự động.

## Bước 4: Kiểm tra kết nối

Khi tất cả các dịch vụ báo **Live** (màu xanh):

1. Truy cập vào URL của `eco-health-web`.
2. Kiểm tra xem các yêu cầu đăng ký/đăng nhập có hoạt động không.
3. Nếu Nginx không tìm thấy API, hãy kiểm tra lại tên service trong phần cấu hình biến môi trường của Nginx.

---
Lưu ý: Version miễn phí của Render có thể "ngủ" sau 15 phút không hoạt động. Lần truy cập đầu tiên sau đó có thể mất khoảng 30s để khởi động lại.
