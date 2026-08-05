CREATE TABLE credit_assessment (
    credit_assessment_id       UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id             UUID           NOT NULL,
    score_model_code           VARCHAR(30)    NOT NULL,
    credit_score               INTEGER        NOT NULL,
    risk_level                 VARCHAR(20)    NOT NULL,
    declared_income            DECIMAL(18,2)  NOT NULL,
    verified_income            DECIMAL(18,2),
    monthly_debt_obligation    DECIMAL(18,2)  NOT NULL DEFAULT 0,
    debt_to_income_ratio       DECIMAL(7,4),
    assessment_result          VARCHAR(20)    NOT NULL,
    assessed_at                TIMESTAMP      NOT NULL,
    created_at                 TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                 TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_credit_assessment_application
        UNIQUE (application_id),

    CONSTRAINT fk_credit_assessment_application
        FOREIGN KEY (application_id)
        REFERENCES application (application_id),

    CONSTRAINT ck_credit_assessment_credit_score
        CHECK (credit_score >= 0),

    CONSTRAINT ck_credit_assessment_declared_income
        CHECK (declared_income >= 0),

    CONSTRAINT ck_credit_assessment_verified_income
        CHECK (verified_income >= 0),

    CONSTRAINT ck_credit_assessment_monthly_debt
        CHECK (monthly_debt_obligation >= 0),

    CONSTRAINT ck_credit_assessment_dti
        CHECK (debt_to_income_ratio >= 0)
);


-- Tự động cập nhật updated_at khi kết quả đánh giá thay đổi
CREATE TRIGGER trg_credit_assessment_set_updated_at
BEFORE UPDATE ON credit_assessment
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();