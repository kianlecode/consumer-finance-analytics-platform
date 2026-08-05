CREATE TABLE contract (
    contract_id                 UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_number             VARCHAR(12)    NOT NULL,
    payment_reference_id        VARCHAR(100)   NOT NULL,
    application_id              UUID           NOT NULL,
    customer_id                 UUID           NOT NULL,
    fulfillment_request_no      VARCHAR(50)    NOT NULL,
    product_group               VARCHAR(20)    NOT NULL,
    product_code                VARCHAR(30)    NOT NULL,
    principal_amount            DECIMAL(18,2),
    term_months                 INTEGER,
    annual_interest_rate        DECIMAL(7,4),
    contract_date               DATE           NOT NULL,
    disbursement_date           DATE,
    maturity_date               DATE,
    outstanding_principal       DECIMAL(18,2)  DEFAULT 0,
    credit_limit                DECIMAL(18,2),
    available_credit_limit      DECIMAL(18,2),
    card_outstanding_balance    DECIMAL(18,2)  DEFAULT 0,
    statement_day               INTEGER,
    payment_due_day             INTEGER,
    contract_status             VARCHAR(30)    NOT NULL DEFAULT 'PENDING_FULFILLMENT',
    created_at                  TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                  TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_contract_contract_number
        UNIQUE (contract_number),

    CONSTRAINT uq_contract_payment_reference
        UNIQUE (payment_reference_id),

    CONSTRAINT uq_contract_application
        UNIQUE (application_id),

    CONSTRAINT uq_contract_fulfillment_request
        UNIQUE (fulfillment_request_no)
);


-- Tự động cập nhật updated_at khi thông tin hợp đồng thay đổi
CREATE TRIGGER trg_contract_set_updated_at
BEFORE UPDATE ON contract
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Hỗ trợ incremental load theo thời điểm dữ liệu thay đổi
CREATE INDEX idx_contract_updated_at
    ON contract (updated_at);