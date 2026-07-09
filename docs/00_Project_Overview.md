# Project Ideation

> Tài liệu ghi lại các ý tưởng ban đầu, định hướng và những quyết định thiết kế của dự án.

---

# 1. Project Objective

Xây dựng một **end-to-end Analytics Engineering Project** mô phỏng hệ thống dữ liệu của một công ty **Consumer Finance**, nhằm thể hiện đầy đủ quy trình từ thu thập dữ liệu, xây dựng Data Warehouse đến phân tích dữ liệu.

## Mục tiêu kỹ thuật

- Data Modeling
- ELT Pipeline Design
- dbt Best Practices
- Data Quality Testing
- Data Orchestration
- Analytics Engineering Workflow

> Mục tiêu của dự án không chỉ là xây dựng một project dbt, mà là mô phỏng một **Mini Analytics Platform** gần với môi trường doanh nghiệp thực tế.

---

# 2. Domain

## Domain được lựa chọn

**Consumer Finance / Banking**

## Lý do lựa chọn

- Phù hợp với background hiện tại.
- Dễ tìm kiếm và kết hợp các bộ dữ liệu công khai.
- Business Flow rõ ràng, thuận lợi để mô hình hóa dữ liệu.
- Phù hợp để xây dựng Data Warehouse theo mô hình doanh nghiệp.
- Có khả năng mở rộng thêm các domain khác trong tương lai.

---

# 3. Dataset Strategy

Hiện chưa kỳ vọng sẽ tìm được một bộ dữ liệu hoàn chỉnh phục vụ toàn bộ dự án.

Thay vào đó, dự án sẽ áp dụng **Hybrid Dataset Strategy**.

## Nguyên tắc

- Ưu tiên sử dụng dữ liệu thật từ các nguồn công khai (Kaggle, GitHub, Open Dataset...).
- Có thể kết hợp nhiều dataset khác nhau nếu cần.
- Chỉ generate dữ liệu khi không thể tìm được dữ liệu phù hợp.
- Dữ liệu generate phải tuân theo business rules và phản ánh đúng nghiệp vụ.
- Mọi dữ liệu generate đều phải có nguồn gốc và có thể giải thích được.

---

# 4. Business Scope (Draft)

Phiên bản đầu tiên của dự án sẽ tập trung vào các domain sau:

Business Domain
└── Consumer Finance

Business Scenario
└── Loan Origination through Partner Channel

Partner Channel
└── Partner App (Example: MoMo)

Core Business
└── Financial Company

> **Lưu ý:** Business Scope có thể được điều chỉnh trong quá trình nghiên cứu dataset và thiết kế hệ thống.

---

# 5. Technology Stack (Draft)

| Thành phần | Công nghệ | Mục đích |
|------------|-----------|----------|
| Programming Language | Python | Generate dữ liệu, ETL Scripts |
| Database | PostgreSQL *(TBD)* | Source Database |
| Transformation | dbt Core | ELT Transformation |
| Version Control | Git & GitHub | Quản lý source code |
| Containerization | Docker *(Optional)* | Môi trường phát triển |
| Visualization | Power BI | Dashboard |
| Orchestration | Airflow / GitHub Actions *(TBD)* | Điều phối workflow |

---

# Guiding Principles

## Principle 1

Không xây dựng project chỉ để học hoặc demo dbt.

Mục tiêu là xây dựng một **Mini Analytics Platform** mô phỏng hệ thống doanh nghiệp.

---

## Principle 2

**Design First. Implementation Later.**

Ưu tiên thiết kế kiến trúc, business flow và data model trước khi bắt đầu code.

---

## Principle 3

Business phải hợp lý.

Không generate dữ liệu ngẫu nhiên chỉ để đủ số lượng.

---

## Principle 4

Mọi quyết định thiết kế đều phải có lý do.

Nếu thay đổi kiến trúc hoặc công nghệ, cần ghi lại nguyên nhân.

---

## Principle 5

Ưu tiên chất lượng hơn số lượng.

Một business flow hoàn chỉnh có giá trị hơn nhiều business flow rời rạc.

---

# Open Questions

Các nội dung hiện vẫn đang trong quá trình nghiên cứu.

- Nên sử dụng PostgreSQL hay DuckDB?
- Bộ dataset nào phù hợp nhất?
- Có cần kết hợp nhiều dataset hay không?
- Dashboard sẽ sử dụng Power BI hay một công cụ khác?
- Nên sử dụng Airflow hay GitHub Actions để orchestration?
- Có nên sử dụng Docker cho toàn bộ project?

---

# Decision Log

Các quyết định quan trọng của dự án sẽ được ghi lại tại đây theo mô hình **Architecture Decision Record (ADR)**.

| ID | Decision | Status |
|----|----------|--------|
| D001 | Chọn Consumer Finance / Banking làm domain chính | ✅ |
| D002 | Xây dựng Mini Analytics Platform thay vì chỉ demo dbt | ✅ |
| D003 | Áp dụng Hybrid Dataset Strategy (Public Dataset + Generated Data) | ✅ |
| D004 | Thiết kế trước, triển khai sau | ✅ |
| D005 | Chưa quyết định Database | ⏳ |

> Mỗi khi có một quyết định quan trọng (ví dụ lựa chọn database, dataset hoặc thay đổi kiến trúc), Decision Log sẽ được cập nhật để lưu lại quá trình phát triển của dự án.