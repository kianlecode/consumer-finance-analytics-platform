CREATE TABLE partner (
    partner_id     UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_code   VARCHAR(30)  NOT NULL,
    partner_name   VARCHAR(255) NOT NULL,
    partner_type   VARCHAR(50)  NOT NULL,
    status         VARCHAR(20)  NOT NULL DEFAULT 'ACTIVE',
    created_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_partner_code
        UNIQUE (partner_code)
);

CREATE TRIGGER trg_partner_set_updated_at
BEFORE UPDATE ON partner
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();