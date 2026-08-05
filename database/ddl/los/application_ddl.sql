CREATE TABLE application (
    application_id            UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id                VARCHAR(100)   NOT NULL,
    registration_id           UUID           NOT NULL,
    customer_id               UUID           NOT NULL,
    los_application_no        VARCHAR(30)    NOT NULL,
    application_status_code   VARCHAR(30)    NOT NULL DEFAULT 'RECEIVED',
    product_group             VARCHAR(20)    NOT NULL,
    product_code              VARCHAR(30)    NOT NULL,
    requested_amount          DECIMAL(18,2),
    requested_term            INTEGER,
    requested_credit_limit    DECIMAL(18,2),
    loan_purpose              VARCHAR(100),
    submitted_at              TIMESTAMP      NOT NULL,
    created_at                TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_application_request_id
        UNIQUE (request_id),

    CONSTRAINT uq_application_no
        UNIQUE (los_application_no),

    CONSTRAINT ck_application_requested_amount
        CHECK (requested_amount > 0),

    CONSTRAINT ck_application_requested_term
        CHECK (requested_term > 0),

    CONSTRAINT ck_application_requested_credit_limit
        CHECK (requested_credit_limit > 0)
);


-- Tự động cập nhật updated_at khi bản ghi thay đổi
CREATE TRIGGER trg_application_set_updated_at
BEFORE UPDATE ON application
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Hỗ trợ truy vết hồ sơ từ Partner App
CREATE INDEX idx_application_registration_id
    ON application (registration_id);


-- Hỗ trợ truy xuất các hồ sơ của một khách hàng
CREATE INDEX idx_application_customer_id
    ON application (customer_id);