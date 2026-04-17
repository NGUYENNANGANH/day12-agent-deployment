# Hướng dẫn Deploy Monorepo (FE/BE) lên Railway

Vì bạn đã tách biệt Frontend và Backend, chúng ta sẽ deploy theo dạng **Multi-service**. Điều này giúp bạn có thể nâng cấp Backend mà không ảnh hưởng đến Frontend và ngược lại.

## Bước 1: Chuẩn bị cơ sở dữ liệu trên Railway

Đừng dùng container tự dựng cho DB khi lên Cloud. Hãy dùng dịch vụ DB của Railway:

1. Vào Dashboard Railway, nhấn **+ New** -> **Database** -> **Add MongoDB**.
2. Nhấn tiếp **+ New** -> **Database** -> **Add Redis**.
3. Railway sẽ tự động tạo thông tin kết nối cho bạn.

## Bước 2: Deploy Backend Unit (API)

1. Nhấn **+ New** -> **GitHub Repo** -> Chọn repo của bạn.
2. Tại màn hình cấu hình Service:
   - **Root Directory**: Nhập `backend`.
   - **Service Name**: Đặt là `api`.
3. Vào tab **Variables**, thêm các biến sau:
   - `JWT_SECRET`: (Chọn 1 chuỗi bí mật bất kỳ)
   - `OPENAI_API_KEY`: (API Key của bạn)
   - `MONGO_URI`: (Tham chiếu từ service MongoDB: `${{MongoDB.MONGODB_URL}}`)
   - `REDIS_URL`: (Tham chiếu từ service Redis: `${{Redis.REDIS_URL}}`)

## Bước 3: Deploy Frontend Unit (Nginx)

1. Nhấn **+ New** -> **GitHub Repo** -> Chọn repo của bạn một lần nữa.
2. Tại màn hình cấu hình Service:
   - **Root Directory**: Nhập `frontend`.
   - **Service Name**: Đặt là `web`.
3. Railway sẽ tự động build Dockerfile của Nginx mà tôi đã viết cho bạn.

## Bước 4: Cấu hình Proxy nội bộ

Trong file `frontend/nginx.conf` mà tôi đã tạo, tôi đã để sẵn dòng:
`proxy_pass http://api:8000;`

**Quan trọng**: Để Nginx tìm thấy Backend, bạn cần đảm bảo Service Backend trên Railway có tên là `api` hoặc cập nhật URL này cho khớp với tên service bạn đặt.

## Bước 5: Kiểm tra kết quả

- Lấy URL công khai của service `web`.
- Truy cập vào và thử Đăng ký/Đăng nhập.
- Kiểm tra tính năng "Chia sẻ vị trí" trong Chat.

> [!TIP]
> Bạn có thể dùng tính năng **Railway Private Networking**. Các service trong cùng project sẽ nhìn thấy nhau bằng tên service. Ví dụ: Frontend gọi sang `http://api:8000`.

---
Chúc bạn deploy thành công! Nếu gặp lỗi lúc build, hãy gửi log cho tôi nhé!
