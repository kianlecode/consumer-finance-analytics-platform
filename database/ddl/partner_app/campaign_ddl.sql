CREATE TABLE campaign (
    campaign_id     UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id      UUID          NOT NULL,
    campaign_code   VARCHAR(30)   NOT NULL,
    campaign_name   VARCHAR(255)  NOT NULL,
    campaign_type   VARCHAR(30)   NOT NULL,
    channel         VARCHAR(30)   NOT NULL,
    start_date      DATE          NOT NULL,
    end_date        DATE          NOT NULL,
    budget          DECIMAL(18,2) DEFAULT 0,
    status          VARCHAR(20)   NOT NULL DEFAULT 'DRAFT',
    created_at      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_campaign_code
        UNIQUE (campaign_code),

    CONSTRAINT fk_campaign_partner
        FOREIGN KEY (partner_id)
        REFERENCES partner (partner_id),

    CONSTRAINT ck_campaign_date
        CHECK (end_date >= start_date),

    CONSTRAINT ck_campaign_budget
        CHECK (budget >= 0)
);


-- Tự động cập nhật updated_at khi bản ghi thay đổi
CREATE TRIGGER trg_campaign_set_updated_at
BEFORE UPDATE ON campaign
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Hỗ trợ truy vấn và join campaign theo partner_id
CREATE INDEX idx_campaign_partner_id
    ON campaign (partner_id);