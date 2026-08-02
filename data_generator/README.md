# Source Data Generator — Smoke Test v1

Bộ generator nhỏ cho 14 bảng PostgreSQL của bốn source system trong Consumer Finance Analytics Platform. Hai bảng MongoDB `customer_activity` và `notification_log` không nằm trong phạm vi.

## Nguyên tắc

- Sinh dữ liệu theo dependency nghiệp vụ, không sinh độc lập từng bảng.
- Dùng seed cố định để tái lập và debug được.
- `citizen_id` được CMS resolve thành một `customer_id` dùng xuyên hệ thống.
- Chỉ submission thành công mới tạo hồ sơ LOS.
- Credit assessment, rule evaluation, decision và disbursement chỉ xuất hiện khi hồ sơ đi tới bước tương ứng.
- Chỉ quyết định `APPROVED` mới được tạo yêu cầu giải ngân.
- Chỉ yêu cầu `ACCEPTED` mới tạo hợp đồng Payment.
- Chỉ giao dịch `SUCCESS` mới làm giảm dư nợ và cập nhật kỳ trả nợ.

## Bộ smoke test mặc định

28 registration, gồm 2 bản ghi cho mỗi nhánh:

`CANCELLED`, `SUBMISSION_FAILED`, `RECEIVED`, `VALIDATING`, `ASSESSMENT_FAIL`, `RULE_REJECT`, `MANUAL_REVIEW`, `APPROVED_NO_DISBURSEMENT`, `DISBURSEMENT_REJECTED`, `PENDING_DISBURSEMENT`, `ACTIVE_NO_REPAYMENT`, `ACTIVE_PARTIAL`, `ACTIVE_PAID`, `CLOSED`.

## Chạy

```bash
cd data_generation
python generate_data.py --registrations 28 --seed 20260801 --output output/smoke
python validate_data.py --input output/smoke
python -m unittest -v test_data_gen.py
```

Kết quả gồm CSV theo từng system, `manifest.json` và `validation_report.json`.

## Phạm vi validation

- PK và business key không trùng.
- FK vật lý và khóa tham chiếu xuyên hệ thống không mồ côi.
- Timeline trạng thái LOS liên tục, đúng thứ tự và khớp current status.
- Snapshot thu nhập và công thức DTI đúng.
- Rule không trùng theo `(loan_application_id, rule_code, rule_version)`.
- Decision phù hợp với assessment/rule và chỉ APPROVED mới có điều khoản vay.
- Disbursement amount bằng approved amount.
- Lịch trả nợ đủ số kỳ, tổng gốc bằng principal và `total_due = principal_due + interest_due`.
- Chỉ repayment SUCCESS làm giảm outstanding principal; hợp đồng CLOSED phải trả đủ.

## Cố ý chưa mô phỏng ở v1

- MongoDB event/log.
- Nhiều lần retry submission hoặc nhiều lần đánh giá lại rule.
- Gia hạn, miễn giảm (`WAIVED`), write-off và chuyển `DEFAULTED`.
- Thay đổi thông tin khách hàng theo thời gian/SCD.
- Late-arriving data và dữ liệu lỗi có chủ đích cho bài tập data quality.
