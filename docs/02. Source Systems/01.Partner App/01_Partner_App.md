# Partner App

# 1. Tổng quan

Partner App là hệ thống tiếp xúc trực tiếp với khách hàng trong Consumer Finance Analytics Platform.

Đây là điểm bắt đầu của toàn bộ hành trình vay vốn. Khách hàng sử dụng Partner App để tìm hiểu các sản phẩm vay, đăng ký vay và gửi hồ sơ đến Loan Origination System (LOS).

Partner App chỉ đóng vai trò **tiếp nhận và chuyển tiếp thông tin**, không tham gia vào quá trình thẩm định, phê duyệt hay quản lý khoản vay.

Dữ liệu nghiệp vụ của Partner App được lưu trữ trên:

- PostgreSQL: Master Data và Transaction Data.
- MongoDB: Activity Log và Notification Log.

---

# 2. Vai trò của hệ thống

Partner App chịu trách nhiệm:

- Hiển thị danh sách sản phẩm vay được cung cấp từ Loan Origination System.
- Tiếp cận và thu hút khách hàng.
- Tiếp nhận thông tin đăng ký vay.
- Ghi nhận nguồn khách hàng và chiến dịch Marketing.
- Ghi nhận hành vi sử dụng ứng dụng.
- Gửi hồ sơ vay sang Loan Origination System.

Partner App không chịu trách nhiệm:

- Quản lý hồ sơ khách hàng chính thức.
- eKYC.
- Chấm điểm tín dụng.
- Thẩm định hồ sơ.
- Phê duyệt khoản vay.
- Sinh hợp đồng.
- Giải ngân.
- Thu hồi nợ.

---

# 3. Nghiệp vụ của hệ thống

## 3.1 Hiển thị sản phẩm vay

Partner App hiển thị danh sách sản phẩm vay được cung cấp từ Loan Origination System.

Thông tin hiển thị bao gồm:

- Tên sản phẩm.
- Hạn mức vay.
- Lãi suất.
- Kỳ hạn vay.
- Điều kiện cơ bản.
- Mô tả sản phẩm.

Partner App chỉ đọc và hiển thị dữ liệu, không quản lý thông tin sản phẩm vay.

---

## 3.2 Tiếp nhận khách hàng

Khách hàng nhập thông tin ban đầu để đăng ký vay.

Ví dụ:

- Họ tên.
- CCCD.
- Số điện thoại.
- Thu nhập hàng tháng.
- Khoản vay mong muốn.
- Kỳ hạn vay.
- Mục đích vay.

Partner App thực hiện kiểm tra dữ liệu cơ bản trước khi cho phép gửi hồ sơ.

---

## 3.3 Gửi hồ sơ vay

Sau khi khách hàng hoàn tất đăng ký:

- Kiểm tra dữ liệu đầu vào.
- Tạo yêu cầu gửi hồ sơ.
- Gửi hồ sơ sang Loan Origination System.

Sau khi gửi thành công, Partner App chỉ lưu thông tin phục vụ việc theo dõi quá trình gửi.

Toàn bộ vòng đời của hồ sơ vay sẽ được quản lý bởi Loan Origination System.

---

## 3.4 Quản lý chiến dịch Marketing

Partner App ghi nhận nguồn khách hàng và chiến dịch Marketing.

Ví dụ:

- Facebook Ads
- Google Ads
- TikTok
- Referral
- Partner
- Organic

Dữ liệu này phục vụ phân tích hiệu quả Marketing.

---

## 3.5 Ghi nhận hành vi khách hàng

Partner App ghi nhận các hành vi của khách hàng trong quá trình sử dụng ứng dụng.

Ví dụ:

- View Product
- View Campaign
- Start Registration
- Submit Application

Các dữ liệu này phục vụ phân tích hành vi người dùng và tối ưu trải nghiệm.

---

## 3.6 Gửi thông báo

Partner App gửi các thông báo tới khách hàng.

Ví dụ:

- Đăng ký thành công.
- Hồ sơ đã được tiếp nhận.
- Thông báo chương trình khuyến mại.
- Thông báo chiến dịch Marketing.

---

# 4. Thiết kế dữ liệu

## 4.1 PostgreSQL

### Partner

Lưu thông tin các đối tác phân phối sản phẩm vay.

Ví dụ:

- MoMo
- ZaloPay
- Shopee
- FPT Shop

---

### Campaign

Lưu thông tin các chiến dịch Marketing.

Mỗi Campaign thuộc về một Partner.

---

### Customer Registration

Lưu thông tin khách hàng tại thời điểm đăng ký vay.

Đây chỉ là dữ liệu đăng ký ban đầu.

Sau khi hồ sơ được tiếp nhận và xử lý, thông tin khách hàng chính thức sẽ được quản lý bởi Customer Management System.

---

### Application Submission

Lưu thông tin việc gửi hồ sơ sang Loan Origination System.

Bảng này chỉ ghi nhận quá trình gửi hồ sơ.

Loan Application chính thức sẽ được quản lý tại Loan Origination System.

---

## 4.2 MongoDB

### Customer Activity

Lưu toàn bộ hành vi sử dụng của khách hàng.

Ví dụ:

- View Product
- View Campaign
- Start Registration
- Submit Application

---

### Notification Log

Lưu lịch sử gửi thông báo tới khách hàng.

---

# 5. Quan hệ dữ liệu

## PostgreSQL

```text
Partner (1)
      │
      ▼
Campaign (N)
      │
      ▼
Customer Registration (N)
      │
      ▼
Application Submission (1)
```

## MongoDB

```text
Customer Registration
        │
        ├── Customer Activity
        └── Notification Log
```

---

# 6. Luồng dữ liệu

```text
Khách hàng

↓

Mở Partner App

↓

Xem sản phẩm vay

↓

Xem chương trình Marketing

↓

Đăng ký vay

↓

Nhập thông tin

↓

Kiểm tra dữ liệu

↓

Gửi hồ sơ sang Loan Origination System

↓

Chờ kết quả xử lý
```

---

# 7. Phạm vi dữ liệu

## Partner App sở hữu

- Partner
- Campaign
- Customer Registration
- Application Submission
- Customer Activity
- Notification Log

## Partner App không sở hữu

- Loan Product (được quản lý bởi Loan Origination System và chỉ được Partner App hiển thị thông qua API).

## Chuyển dữ liệu sang hệ thống khác

- Hồ sơ đăng ký vay → Loan Origination System.
- Thông tin khách hàng → Customer Management System (sau khi hồ sơ được tiếp nhận).

---

# 8. Business Rules

- Partner App chỉ tiếp nhận và chuyển tiếp hồ sơ vay.
- Partner App không quản lý vòng đời khoản vay.
- Partner App không quyết định phê duyệt hay từ chối khoản vay.
- Partner App không quản lý thông tin khách hàng chính thức.
- Mọi hành vi của khách hàng đều được ghi nhận phục vụ phân tích.
- Sau khi gửi thành công, Loan Origination System trở thành hệ thống sở hữu hồ sơ vay.