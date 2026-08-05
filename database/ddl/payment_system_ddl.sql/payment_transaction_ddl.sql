CREATE TABLE payment_transaction (
    transaction_id          UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_reference   VARCHAR(100)   NOT NULL,
    contract_id              UUID           NOT NULL,
    installment_id           UUID,
    statement_id             UUID,
    transaction_type         VARCHAR(30)    NOT NULL,
    transaction_amount       DECIMAL(18,2)  NOT NULL,
    principal_amount         DECIMAL(18,2)  NOT NULL DEFAULT 0,
    interest_amount          DECIMAL(18,2)  NOT NULL DEFAULT 0,
    payment_method           VARCHAR(30)    NOT NULL,
    transaction_status       VARCHAR(20)    NOT NULL DEFAULT 'PENDING',
    external_reference       VARCHAR(100),
    transaction_at           TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at               TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at               TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_payment_transaction_reference
        UNIQUE (transaction_reference),

    CONSTRAINT fk_payment_transaction_contract
        FOREIGN KEY (contract_id)
        REFERENCES contract (contract_id),

    CONSTRAINT fk_payment_transaction_installment
        FOREIGN KEY (installment_id)
        REFERENCES repayment_schedule (installment_id),

    CONSTRAINT fk_payment_transaction_statement
        FOREIGN KEY (statement_id)
        REFERENCES card_statement (statement_id)
);


-- Tự động cập nhật updated_at khi giao dịch thay đổi
CREATE TRIGGER trg_payment_transaction_set_updated_at
BEFORE UPDATE ON payment_transaction
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Hỗ trợ incremental load theo thời điểm dữ liệu thay đổi
CREATE INDEX idx_payment_transaction_updated_at
    ON payment_transaction (updated_at);


-- Hỗ trợ truy vấn giao dịch theo hợp đồng
CREATE INDEX idx_payment_transaction_contract_id
    ON payment_transaction (contract_id);


-- Hỗ trợ truy vấn giao dịch theo kỳ trả nợ
CREATE INDEX idx_payment_transaction_installment_id
    ON payment_transaction (installment_id);


-- Hỗ trợ truy vấn giao dịch theo kỳ sao kê
CREATE INDEX idx_payment_transaction_statement_id
    ON payment_transaction (statement_id);