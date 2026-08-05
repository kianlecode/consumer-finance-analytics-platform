CREATE TABLE application_submission (
    submission_id      UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    registration_id    UUID          NOT NULL,
    request_id         VARCHAR(100)  NOT NULL,
    submit_status      VARCHAR(30)   NOT NULL DEFAULT 'PENDING',
    submitted_at       TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    los_reference_id   VARCHAR(100),
    error_code         VARCHAR(50),
    error_message      VARCHAR(500),
    created_at         TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_application_submission_request_id
        UNIQUE (request_id),

    CONSTRAINT fk_application_submission_registration
        FOREIGN KEY (registration_id)
        REFERENCES customer_registration (registration_id)
);


-- Tự động cập nhật updated_at khi bản ghi thay đổi
CREATE TRIGGER trg_application_submission_set_updated_at
BEFORE UPDATE ON application_submission
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


-- Hỗ trợ truy vấn lịch sử gửi hồ sơ theo registration_id
CREATE INDEX idx_application_submission_registration_id
    ON application_submission (registration_id);