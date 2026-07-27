# Loan Origination System (LOS)

## 1. Tổng quan

Loan Origination System (LOS) là hệ thống trung tâm chịu trách nhiệm tiếp nhận, xử lý và quản lý toàn bộ vòng đời của một hồ sơ vay, từ thời điểm khách hàng gửi yêu cầu vay cho đến khi hồ sơ được phê duyệt, từ chối hoặc chuyển sang xử lý thủ công.

LOS đóng vai trò là bộ não xử lý nghiệp vụ trong nền tảng Consumer Finance Analytics Platform. Hệ thống nhận hồ sơ từ Partner App, thực hiện các bước kiểm tra và đánh giá cần thiết, áp dụng các quy tắc nghiệp vụ, sau đó đưa ra quyết định xử lý phù hợp.

Ngoài việc hỗ trợ quy trình phê duyệt khoản vay, LOS còn ghi nhận đầy đủ trạng thái và lịch sử xử lý của hồ sơ, tạo nền tảng dữ liệu cho vận hành, báo cáo và phân tích.

## 2. Vai trò trong hệ thống

Trong kiến trúc tổng thể, LOS là hệ thống xử lý nghiệp vụ chính của quy trình cấp tín dụng.

Hệ thống chịu trách nhiệm:

* Tiếp nhận hồ sơ vay từ Partner App.
* Quản lý toàn bộ vòng đời của hồ sơ vay.
* Kiểm tra tính đầy đủ và hợp lệ của thông tin khách hàng.
* Thực hiện đánh giá tín dụng và áp dụng các quy tắc nghiệp vụ.
* Phối hợp với các hệ thống nội bộ hoặc bên thứ ba để xác minh thông tin khi cần thiết.
* Đưa ra quyết định tự động hoặc chuyển hồ sơ sang xử lý thủ công.
* Chuyển hồ sơ đã được phê duyệt sang Payment System để thực hiện giải ngân.
* Đồng bộ trạng thái xử lý trở lại Partner App để khách hàng theo dõi.

## 3. Trách nhiệm cốt lõi

LOS tập trung vào các trách nhiệm nghiệp vụ sau:

### 3.1 Tiếp nhận hồ sơ vay

* Nhận hồ sơ từ Partner App.
* Sinh mã hồ sơ vay.
* Kiểm tra dữ liệu đầu vào.
* Ghi nhận thời điểm tiếp nhận.

### 3.2 Quản lý hồ sơ vay

* Lưu trữ thông tin hồ sơ.
* Cập nhật trạng thái xử lý.
* Theo dõi lịch sử thay đổi.
* Quản lý vòng đời của hồ sơ.

### 3.3 Xác minh thông tin

* Kiểm tra tính đầy đủ của dữ liệu.
* Xác minh thông tin khách hàng.
* Kiểm tra giấy tờ được cung cấp.
* Đối chiếu thông tin với các nguồn dữ liệu liên quan.

### 3.4 Đánh giá tín dụng

* Thu thập dữ liệu phục vụ đánh giá.
* Tính toán điểm tín dụng.
* Áp dụng các quy tắc nghiệp vụ.
* Xác định mức độ rủi ro của hồ sơ.

### 3.5 Ra quyết định xử lý

* Phê duyệt tự động.
* Từ chối tự động.
* Chuyển sang xử lý thủ công khi cần thiết.

### 3.6 Quản lý trạng thái

* Theo dõi trạng thái hiện tại của hồ sơ.
* Ghi nhận lịch sử chuyển trạng thái.
* Đồng bộ trạng thái sang các hệ thống liên quan.

### 3.7 Chuyển yêu cầu giải ngân

Sau khi hồ sơ được phê duyệt, LOS tạo yêu cầu giải ngân và chuyển sang Payment System để tiếp tục quy trình cấp khoản vay.

## 4. Phạm vi trách nhiệm

LOS chịu trách nhiệm:

* Xử lý nghiệp vụ hồ sơ vay.
* Quản lý trạng thái hồ sơ.
* Điều phối quy trình phê duyệt.
* Ghi nhận lịch sử xử lý.
* Cung cấp dữ liệu cho các hệ thống downstream.

LOS không chịu trách nhiệm:

* Hiển thị giao diện cho khách hàng.
* Thực hiện giải ngân.
* Quản lý thanh toán khoản vay.
* Thu hồi nợ.
* Báo cáo và phân tích dữ liệu.

## 5. Vị trí trong kiến trúc hệ thống

```text
Customer
    │
    ▼
Partner App
    │
    ▼
Loan Origination System (LOS)
    │
    ├────────► Customer Management System
    │
    ├────────► Credit / Fraud Services
    │
    ▼
Payment System
    │
    ▼
Analytics Platform
```

LOS là hệ thống trung tâm điều phối toàn bộ quy trình xử lý hồ sơ vay và kết nối với các hệ thống khác trong nền tảng Consumer Finance Analytics Platform.

## 6. Kết luận

LOS là lớp xử lý nghiệp vụ cốt lõi của toàn bộ hành trình vay vốn. Hệ thống này không chỉ quyết định hồ sơ được chấp thuận hay từ chối, mà còn tạo ra toàn bộ trạng thái, lịch sử và dữ liệu vận hành quan trọng cho các bước tiếp theo trong platform.