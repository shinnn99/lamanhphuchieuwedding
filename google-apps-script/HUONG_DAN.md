# Nối thiệp cưới Phúc Hiếu & Lâm Anh với Google Sheet

Lời chúc trong **Sổ lưu bút** và phản hồi **Xác nhận tham dự (RSVP)** trên thiệp sẽ tự động ghi vào Google Sheet (đồng thời khi chưa nối Sheet, thiệp vẫn lưu & hiển thị trực tiếp chế độ Demo trên trình duyệt rất mượt).

## Cài đặt (làm 1 lần, khoảng 5 phút)

1. Mở một file Google Sheet mới cho đám cưới **Phúc Hiếu & Lâm Anh**.
2. Vào menu **Tiện ích mở rộng → Apps Script** (`Extensions → Apps Script`).
3. Xoá nội dung mặc định trong `Code.gs`, dán toàn bộ nội dung file [`Code.gs`](Code.gs) vào và bấm **Lưu**.
4. Bấm **Triển khai → Tùy chọn triển khai mới** (`Deploy → New deployment`):
   - Chọn loại: **Ứng dụng web** (`Web app`).
   - **Thực thi với tư cách**: *Tôi* (`Me`).
   - **Người có quyền truy cập**: **Bất kỳ ai** (`Anyone`).
   - Bấm **Triển khai** và cấp quyền truy cập.
5. Copy **URL ứng dụng web** có dạng `https://script.google.com/macros/s/AKfy.../exec`.
6. Mở `index.html`, tìm cấu hình `WEDDING_CONFIG` ở cuối trang và dán URL vào trường `sheetWebAppUrl`:
   ```js
   sheetWebAppUrl: "https://script.google.com/macros/s/AKfy.../exec",
   ```

## Cấu trúc bảng tự tạo

| Tab | Các cột dữ liệu |
|---|---|
| **Sổ lưu bút** | Thời gian, Tên, Lời chúc, Khách mời (theo link) |
| **Xác nhận tham dự** | Thời gian, Họ và tên, Số điện thoại, Tham dự, Nơi tham dự, Số người, Lời nhắn, Khách mời (theo link) |
