CREATE TABLE fulfillment_request (
    fulfillment_request_id   UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id           UUID           NOT NULL,
    application_decision_id  UUID           NOT NULL,
    request_no               VARCHAR(50)    NOT NULL,
    fulfillment_type         VARCHAR(30)    NOT NULL,
    fulfillment_amount       DECIMAL(18,2),
    beneficiary_account_no   VARCHAR(50),
    beneficiary_bank_code    VARCHAR(20),
    beneficiary_name         VARCHAR(255),
    request_status           VARCHAR(30)    NOT NULL DEFAULT 'PENDING',
    payment_reference_id     VARCHAR(100),
    failure_code             VARCHAR(50),
    failure_message          VARCHAR(500),
    requested_at             TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sent_at                  TIMESTAMP,
    responded_at             TIMESTAMP,
    created_at               TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at               TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_fulfillment_request_application
        FOREIGN KEY (application_id)
        REFERENCES application (application_id),

    CONSTRAINT fk_fulfillment_request_decision
        FOREIGN KEY (application_decision_id)
        REFERENCES application_decision (application_decision_id),

    CONSTRAINT uq_fulfillment_request_application
        UNIQUE (application_id),

    CONSTRAINT uq_fulfillment_request_decision
        UNIQUE (application_decision_id),

    CONSTRAINT uq_fulfillment_request_request_no
        UNIQUE (request_no),

    CONSTRAINT uq_fulfillment_request_payment_reference
        UNIQUE (payment_reference_id),

    CONSTRAINT ck_fulfillment_request_amount
        CHECK (fulfillment_amount > 0)
);


-- Tự động cập nhật updated_at khi trạng thái yêu cầu thay đổi
CREATE TRIGGER trg_fulfillment_request_set_updated_at
BEFORE UPDATE ON fulfillment_request
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Hỗ trợ incremental load theo thời điểm cập nhật
CREATE INDEX idx_fulfillment_request_updated_at
    ON fulfillment_request (updated_at);