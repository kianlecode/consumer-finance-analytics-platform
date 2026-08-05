CREATE TABLE customer (
    customer_id       UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_code     VARCHAR(20)   NOT NULL,
    citizen_id        VARCHAR(20)   NOT NULL,
    full_name         VARCHAR(150)  NOT NULL,
    date_of_birth     DATE          NOT NULL,
    gender            VARCHAR(10)   NOT NULL,
    phone_number      VARCHAR(20)   NOT NULL,
    customer_status   VARCHAR(20)   NOT NULL,
    created_at        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_customer_customer_code
        UNIQUE (customer_code),

    CONSTRAINT uq_customer_citizen_id
        UNIQUE (citizen_id)
);


CREATE TRIGGER trg_customer_set_updated_at
BEFORE UPDATE ON customer
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


CREATE INDEX idx_customer_updated_at
    ON customer (updated_at);