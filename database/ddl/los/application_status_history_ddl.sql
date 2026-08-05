CREATE TABLE application_status_history (
    status_history_id          UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id             UUID          NOT NULL,
    status_sequence            INTEGER       NOT NULL,
    application_status_code    VARCHAR(30)   NOT NULL,
    status_reason              VARCHAR(255),
    changed_by                 VARCHAR(50)   NOT NULL DEFAULT 'SYSTEM',
    changed_at                 TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_status_history_application
        FOREIGN KEY (application_id)
        REFERENCES application (application_id),

    CONSTRAINT uq_status_history_sequence
        UNIQUE (application_id, status_sequence),

    CONSTRAINT ck_status_history_sequence
        CHECK (status_sequence >= 1)
);


-- Hỗ trợ truy vấn và incremental load theo thời gian thay đổi
CREATE INDEX idx_application_status_history_changed_at
    ON application_status_history (changed_at);