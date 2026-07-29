# Loan Origination System (LOS)

## 1. Tổng quan

Loan Origination System (LOS) là hệ thống trung tâm chịu trách nhiệm tiếp nhận, xử lý và quản lý hồ sơ vay từ thời điểm hồ sơ được gửi từ Partner App cho đến khi hồ sơ được phê duyệt, từ chối, chuyển sang xử lý thủ công hoặc phát sinh yêu cầu giải ngân.

LOS đóng vai trò là lớp xử lý nghiệp vụ chính trong nền tảng Consumer Finance Analytics Platform. Hệ thống tiếp nhận hồ sơ từ Partner App, thực hiện kiểm tra dữ liệu đầu vào, đánh giá tín dụng, áp dụng các quy tắc nghiệp vụ và đưa ra quyết định xử lý phù hợp.

Trong trường hợp hồ sơ được phê duyệt, LOS tạo yêu cầu giải ngân và gửi sang Payment System. LOS không trực tiếp thực hiện giao dịch chuyển tiền.

Ngoài kết quả xử lý cuối cùng, LOS còn ghi nhận trạng thái hiện tại, lịch sử trạng thái, kết quả đánh giá tín dụng, kết quả thực thi business rule và các thông tin vận hành liên quan đến từng hồ sơ vay.

---

## 2. Vai trò trong hệ thống

Trong kiến trúc tổng thể, LOS là hệ thống xử lý nghiệp vụ chính của quy trình cấp tín dụng.

Hệ thống chịu trách nhiệm:

* Tiếp nhận hồ sơ vay từ Partner App.
* Sinh mã hồ sơ và quản lý hồ sơ trong LOS.
* Kiểm tra tính đầy đủ và hợp lệ của dữ liệu đầu vào.
* Thực hiện đánh giá tín dụng và xác định mức độ rủi ro.
* Thực thi các quy tắc nghiệp vụ đối với từng hồ sơ.
* Đưa ra quyết định tự động hoặc chuyển hồ sơ sang xử lý thủ công.
* Ghi nhận trạng thái hiện tại và lịch sử xử lý của hồ sơ.
* Tạo yêu cầu giải ngân đối với hồ sơ được phê duyệt.
* Gửi yêu cầu giải ngân sang Payment System.
* Đồng bộ trạng thái cần thiết trở lại Partner App.
* Cung cấp dữ liệu nguồn cho Analytics Platform.

---

## 3. Trách nhiệm cốt lõi

LOS tập trung vào các trách nhiệm nghiệp vụ sau:

### 3.1 Tiếp nhận hồ sơ vay

* Nhận hồ sơ được gửi từ Partner App.
* Ghi nhận các mã tham chiếu từ Partner App.
* Sinh mã hồ sơ vay trong LOS.
* Kiểm tra dữ liệu đầu vào.
* Ghi nhận thời điểm tiếp nhận hồ sơ.

Hồ sơ được tiếp nhận từ Partner App thông qua các khóa tham chiếu nghiệp vụ như:

* `request_id`
* `registration_id`

Các khóa này giúp liên kết dữ liệu giữa Partner App và LOS nhưng không phải foreign key vật lý giữa hai cơ sở dữ liệu.

### 3.2 Quản lý hồ sơ vay

* Lưu trữ thông tin chính của hồ sơ vay.
* Theo dõi trạng thái hiện tại.
* Ghi nhận thời điểm tạo và cập nhật hồ sơ.
* Quản lý hồ sơ trong suốt quá trình xử lý tại LOS.

Mỗi hồ sơ vay được đại diện bởi một bản ghi trong bảng `loan_application`.

### 3.3 Kiểm tra và xác minh dữ liệu

* Kiểm tra tính đầy đủ của thông tin hồ sơ.
* Kiểm tra tính hợp lệ của dữ liệu đầu vào.
* Sử dụng thông tin thu nhập do khách hàng khai báo.
* Ghi nhận thu nhập được xác minh khi có dữ liệu.
* Thu thập thông tin về nghĩa vụ nợ hiện tại của khách hàng.

Trong phạm vi Phase 1, LOS chưa mô phỏng quy trình upload, lưu trữ hoặc xác minh giấy tờ.

### 3.4 Đánh giá tín dụng

* Tính toán điểm tín dụng.
* Xác định nhóm rủi ro của hồ sơ.
* Đánh giá thu nhập và khả năng trả nợ.
* Tính toán tỷ lệ nghĩa vụ nợ trên thu nhập.
* Đưa ra kết quả đánh giá tín dụng tổng hợp.

Kết quả của bước này được lưu tại bảng `credit_assessment`.

Kết quả đánh giá tín dụng có thể bao gồm:

* `PASS`
* `REFER`
* `FAIL`

Kết quả này là đầu vào cho quá trình thực thi business rule và chưa phải quyết định cuối cùng của hồ sơ.

### 3.5 Thực thi quy tắc nghiệp vụ

LOS thực thi nhiều business rule đối với từng hồ sơ vay.

Ví dụ:

* Kiểm tra độ tuổi.
* Kiểm tra thu nhập tối thiểu.
* Kiểm tra điểm tín dụng tối thiểu.
* Kiểm tra tỷ lệ nghĩa vụ nợ trên thu nhập.
* Kiểm tra giới hạn số tiền vay.
* Kiểm tra các điều kiện rủi ro hoặc blacklist.

Mỗi rule được ghi nhận riêng tại bảng `rule_evaluation`, bao gồm:

* Giá trị đầu vào.
* Toán tử so sánh.
* Ngưỡng áp dụng.
* Kết quả thực thi.
* Mức độ ảnh hưởng đến quyết định hồ sơ.
* Phiên bản rule.

Kết quả rule có thể bao gồm:

* `PASS`
* `FAIL`
* `REFER`
* `SKIPPED`

### 3.6 Ra quyết định xử lý

Sau khi hoàn tất đánh giá tín dụng và thực thi business rule, LOS đưa ra quyết định xử lý hồ sơ.

Các kết quả chính gồm:

* `APPROVED`
* `REJECTED`
* `MANUAL_REVIEW`

Quyết định có thể được đưa ra theo hai phương thức:

* `AUTO`: quyết định tự động bởi LOS.
* `MANUAL`: quyết định bởi nhân sự thẩm định.

Đối với hồ sơ được phê duyệt, LOS ghi nhận:

* Số tiền được phê duyệt.
* Kỳ hạn được phê duyệt.
* Lãi suất năm áp dụng.

Kết quả quyết định được lưu tại bảng `application_decision`.

Trong Phase 1, `MANUAL_REVIEW` chỉ thể hiện việc hồ sơ được chuyển sang xử lý thủ công. Quy trình phân công, xử lý và ghi chú của nhân viên thẩm định chưa được mô phỏng chi tiết.

### 3.7 Quản lý trạng thái hồ sơ

LOS lưu trạng thái hiện tại của hồ sơ trong bảng `loan_application` và lưu toàn bộ lịch sử thay đổi trạng thái trong bảng `application_status_history`.

Các trạng thái chính gồm:

* `RECEIVED`
* `VALIDATING`
* `CREDIT_ASSESSMENT`
* `RULE_EVALUATION`
* `MANUAL_REVIEW`
* `APPROVED`
* `REJECTED`
* `DISBURSEMENT_REQUESTED`

Lịch sử trạng thái được sử dụng để:

* Theo dõi tiến trình xử lý hồ sơ.
* Xây dựng funnel hồ sơ vay.
* Tính thời gian xử lý.
* Theo dõi SLA.
* Phân tích các bước gây chậm trễ.

### 3.8 Tạo và gửi yêu cầu giải ngân

Sau khi hồ sơ được phê duyệt, LOS tạo yêu cầu giải ngân và gửi sang Payment System.

Yêu cầu giải ngân bao gồm:

* Mã yêu cầu giải ngân.
* Số tiền yêu cầu giải ngân.
* Thông tin tài khoản thụ hưởng.
* Mã quyết định phê duyệt.
* Mã hồ sơ vay.
* Trạng thái gửi yêu cầu.

Các trạng thái yêu cầu giải ngân trong LOS gồm:

* `PENDING`
* `SENT`
* `ACCEPTED`
* `REJECTED`
* `FAILED`

LOS chỉ quản lý vòng đời của yêu cầu từ góc nhìn hệ thống gửi. Trạng thái giao dịch giải ngân thực tế được quản lý bởi Payment System.

Sau khi Payment System tiếp nhận yêu cầu, hệ thống có thể trả về `payment_reference_id` để liên kết và đối soát dữ liệu giữa hai hệ thống.

---

## 4. Dữ liệu nghiệp vụ chính

LOS Phase 1 gồm sáu bảng nghiệp vụ chính:

| Bảng | Vai trò |
|---|---|
| `loan_application` | Lưu thông tin chính và trạng thái hiện tại của hồ sơ vay. |
| `application_status_history` | Lưu toàn bộ lịch sử trạng thái của hồ sơ. |
| `credit_assessment` | Lưu kết quả đánh giá tín dụng và khả năng trả nợ. |
| `rule_evaluation` | Lưu kết quả thực thi từng business rule. |
| `application_decision` | Lưu quyết định xử lý cuối cùng của LOS. |
| `disbursement_request` | Lưu yêu cầu giải ngân gửi sang Payment System. |

Quan hệ tổng quát:

```text
loan_application
    │
    ├── 1 ── N    application_status_history
    ├── 1 ── 0..1 credit_assessment
    ├── 1 ── N    rule_evaluation
    ├── 1 ── 0..1 application_decision
    └── 1 ── 0..1 disbursement_request

application_decision
    │
    └── 1 ── 0..1 disbursement_request
```

---

## 5. Phạm vi trách nhiệm

### LOS chịu trách nhiệm

* Tiếp nhận và quản lý hồ sơ vay.
* Kiểm tra dữ liệu đầu vào.
* Đánh giá tín dụng.
* Thực thi các quy tắc nghiệp vụ.
* Đưa ra quyết định xử lý.
* Quản lý trạng thái hồ sơ.
* Ghi nhận lịch sử xử lý.
* Tạo và gửi yêu cầu giải ngân.
* Đồng bộ thông tin với các hệ thống liên quan.
* Cung cấp dữ liệu nguồn cho quá trình ELT và phân tích.

### LOS không chịu trách nhiệm

* Hiển thị giao diện trực tiếp cho khách hàng.
* Quản lý thông tin khách hàng master.
* Upload và lưu trữ giấy tờ trong Phase 1.
* Thực hiện giao dịch giải ngân.
* Quản lý khoản vay sau giải ngân.
* Quản lý lịch trả nợ.
* Thu tiền và quản lý thanh toán khoản vay.
* Thu hồi nợ.
* Xây dựng báo cáo hoặc dashboard phân tích.

---

## 6. Kết nối với các hệ thống khác

### 6.1 Partner App

Partner App là hệ thống gửi hồ sơ vay sang LOS.

Các khóa tham chiếu chính:

```text
Partner App.application_submission.request_id
        │
        ▼
LOS.loan_application.request_id
```

```text
Partner App.customer_registration.registration_id
        │
        ▼
LOS.loan_application.registration_id
```

Thông qua `registration_id`, dữ liệu LOS có thể liên kết với:

* Thông tin khách hàng đăng ký.
* Đối tác.
* Chiến dịch Marketing.
* Số tiền và kỳ hạn khách hàng yêu cầu.
* Mục đích vay.
* Thu nhập khách hàng khai báo.

### 6.2 Payment System

LOS gửi yêu cầu giải ngân sang Payment System thông qua `request_no`.

```text
LOS.disbursement_request.request_no
        │
        ▼
Payment System
```

Sau khi tiếp nhận, Payment System trả về:

```text
payment_reference_id
```

Khóa này được sử dụng để liên kết và đối soát dữ liệu giữa hai hệ thống.

### 6.3 Customer Management System

Trong Phase 1, LOS chưa sử dụng `customer_id` từ Customer Management System vì hệ thống CMS chưa được thiết kế.

Khi CMS được xây dựng, LOS có thể bổ sung khóa tham chiếu đến customer master mà không thay đổi cấu trúc nghiệp vụ cốt lõi.

### 6.4 Analytics Platform

LOS cung cấp dữ liệu nguồn cho Analytics Platform để phục vụ:

* Funnel hồ sơ vay.
* Thời gian xử lý và SLA.
* Tỷ lệ phê duyệt, từ chối và manual review.
* Phân tích điểm tín dụng và nhóm rủi ro.
* Phân tích business rule.
* Phân tích nguyên nhân từ chối.
* Phân tích số tiền yêu cầu và số tiền được phê duyệt.
* Theo dõi tỷ lệ chuyển yêu cầu sang Payment System.
* Phân tích theo đối tác, chiến dịch, sản phẩm và mục đích vay.

---

## 7. Vị trí trong kiến trúc hệ thống

```text
Customer
    │
    ▼
Partner App
    │
    │ Hồ sơ vay
    ▼
Loan Origination System (LOS)
    │
    ├────────► Customer Management System
    │           Tham chiếu customer master
    │
    ├────────► Credit Services
    │           Dữ liệu phục vụ đánh giá tín dụng
    │
    ├────────► Partner App
    │           Đồng bộ trạng thái hồ sơ
    │
    ▼
Payment System
    │
    │ Yêu cầu và kết quả giải ngân
    ▼
Analytics Platform
```

LOS là hệ thống trung tâm điều phối quy trình xử lý hồ sơ vay, từ tiếp nhận hồ sơ đến đánh giá tín dụng, thực thi business rule, ra quyết định và tạo yêu cầu giải ngân.

---

## 8. Kết luận

LOS là lớp xử lý nghiệp vụ cốt lõi của hành trình cấp tín dụng.

Hệ thống không chỉ đưa ra kết quả phê duyệt, từ chối hoặc chuyển xử lý thủ công, mà còn tạo ra các dữ liệu quan trọng về trạng thái hồ sơ, đánh giá tín dụng, business rule, quyết định và yêu cầu giải ngân.

Các dữ liệu này là đầu vào trực tiếp cho Payment System và Analytics Platform, đồng thời tạo nền tảng để triển khai các quy trình ELT, mô hình dữ liệu và dashboard phân tích trong các phase tiếp theo của dự án.
