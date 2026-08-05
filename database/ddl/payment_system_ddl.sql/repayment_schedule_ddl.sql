CREATE TABLE repayment_schedule (
    installment_id       UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id          UUID           NOT NULL,
    installment_number   INTEGER        NOT NULL,
    due_date             DATE           NOT NULL,
    principal_due        DECIMAL(18,2)  NOT NULL,
    interest_due         DECIMAL(18,2)  NOT NULL,
    total_due            DECIMAL(18,2)  NOT NULL,
    installment_status   VARCHAR(20)    NOT NULL DEFAULT 'PENDING',
    paid_at               TIMESTAMP,
    created_at            TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at            TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_repayment_schedule_contract
        FOREIGN KEY (contract_id)
        REFERENCES contract (contract_id),

    CONSTRAINT uq_repayment_schedule_contract_installment
        UNIQUE (contract_id, installment_number)
);


-- Tự động cập nhật updated_at khi kỳ thanh toán thay đổi
CREATE TRIGGER trg_repayment_schedule_set_updated_at
BEFORE UPDATE ON repayment_schedule
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Hỗ trợ incremental load theo thời điểm dữ liệu thay đổi
CREATE INDEX idx_repayment_schedule_updated_at
    ON repayment_schedule (updated_at);