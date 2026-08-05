CREATE TABLE customer_registration (
    registration_id          UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id               UUID           NOT NULL,
    campaign_id              UUID,
    customer_id              UUID           NOT NULL,
    full_name                VARCHAR(255)   NOT NULL,
    phone_number             VARCHAR(20)    NOT NULL,
    citizen_id               VARCHAR(20)    NOT NULL,
    date_of_birth            DATE           NOT NULL,
    gender                   VARCHAR(10)    NOT NULL,
    monthly_income           DECIMAL(18,2)  NOT NULL,
    requested_amount         DECIMAL(18,2),
    requested_credit_limit   DECIMAL(18,2),
    requested_term           INTEGER,
    loan_purpose             VARCHAR(100),
    customer_type            VARCHAR(20)    NOT NULL,
    status                   VARCHAR(30)    NOT NULL DEFAULT 'NEW',
    product_group            VARCHAR(30)    NOT NULL,
    product_code             VARCHAR(30)    NOT NULL,
    created_at               TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at               TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_registration_partner
        FOREIGN KEY (partner_id)
        REFERENCES partner (partner_id),

    CONSTRAINT fk_registration_campaign
        FOREIGN KEY (campaign_id)
        REFERENCES campaign (campaign_id),

    CONSTRAINT ck_registration_monthly_income
        CHECK (monthly_income >= 0),

    CONSTRAINT ck_registration_requested_amount
        CHECK (requested_amount > 0),

    CONSTRAINT ck_registration_requested_credit_limit
        CHECK (requested_credit_limit > 0),

    CONSTRAINT ck_registration_requested_term
        CHECK (requested_term > 0)
);


-- Tự động cập nhật updated_at khi bản ghi thay đổi
CREATE TRIGGER trg_customer_registration_set_updated_at
BEFORE UPDATE ON customer_registration
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Hỗ trợ join và truy vấn theo đối tác
CREATE INDEX idx_customer_registration_partner_id
    ON customer_registration (partner_id);


-- Hỗ trợ phân tích hiệu quả chiến dịch
CREATE INDEX idx_customer_registration_campaign_id
    ON customer_registration (campaign_id);


-- Hỗ trợ truy xuất lịch sử đăng ký của khách hàng
CREATE INDEX idx_customer_registration_customer_id
    ON customer_registration (customer_id);