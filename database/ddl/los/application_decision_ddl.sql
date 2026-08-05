CREATE TABLE application_decision (
    application_decision_id   UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id            UUID           NOT NULL,
    decision_code             VARCHAR(20)    NOT NULL,
    decision_method           VARCHAR(20)    NOT NULL DEFAULT 'AUTO',
    decision_reason_code      VARCHAR(50)    NOT NULL,
    decision_reason           VARCHAR(255),
    approved_amount           DECIMAL(18,2),
    approved_term             INTEGER,
    approved_credit_limit     DECIMAL(18,2),
    annual_interest_rate      DECIMAL(7,4),
    decided_by                VARCHAR(50)    NOT NULL DEFAULT 'LOS_ENGINE',
    decided_at                TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at                TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_application_decision_application
        UNIQUE (application_id),

    CONSTRAINT fk_application_decision_application
        FOREIGN KEY (application_id)
        REFERENCES application (application_id),

    CONSTRAINT ck_application_decision_approved_amount
        CHECK (approved_amount > 0),

    CONSTRAINT ck_application_decision_approved_term
        CHECK (approved_term > 0),

    CONSTRAINT ck_application_decision_credit_limit
        CHECK (approved_credit_limit > 0),

    CONSTRAINT ck_application_decision_interest_rate
        CHECK (annual_interest_rate >= 0)
);


-- Tự động cập nhật updated_at khi quyết định thay đổi
CREATE TRIGGER trg_application_decision_set_updated_at
BEFORE UPDATE ON application_decision
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Hỗ trợ incremental load theo thời điểm cập nhật
CREATE INDEX idx_application_decision_updated_at
    ON application_decision (updated_at);