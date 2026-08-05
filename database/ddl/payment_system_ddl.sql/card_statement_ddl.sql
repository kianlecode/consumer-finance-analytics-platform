CREATE TABLE card_statement (
    statement_id             UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id              UUID           NOT NULL,
    statement_number         INTEGER        NOT NULL,
    statement_period_start   DATE           NOT NULL,
    statement_period_end     DATE           NOT NULL,
    statement_date           DATE           NOT NULL,
    payment_due_date         DATE           NOT NULL,
    opening_balance          DECIMAL(18,2)  NOT NULL DEFAULT 0,
    purchase_amount          DECIMAL(18,2)  NOT NULL DEFAULT 0,
    interest_amount          DECIMAL(18,2)  NOT NULL DEFAULT 0,
    fee_amount               DECIMAL(18,2)  NOT NULL DEFAULT 0,
    payment_amount           DECIMAL(18,2)  NOT NULL DEFAULT 0,
    statement_balance        DECIMAL(18,2)  NOT NULL DEFAULT 0,
    minimum_payment_due      DECIMAL(18,2)  NOT NULL DEFAULT 0,
    statement_status         VARCHAR(20)    NOT NULL DEFAULT 'OPEN',
    paid_at                  TIMESTAMP,
    created_at               TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at               TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_card_statement_contract
        FOREIGN KEY (contract_id)
        REFERENCES contract (contract_id),

    CONSTRAINT uq_card_statement_contract_number
        UNIQUE (contract_id, statement_number)
);


-- Tự động cập nhật updated_at khi thông tin sao kê thay đổi
CREATE TRIGGER trg_card_statement_set_updated_at
BEFORE UPDATE ON card_statement
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Hỗ trợ incremental load theo thời điểm dữ liệu thay đổi
CREATE INDEX idx_card_statement_updated_at
    ON card_statement (updated_at);