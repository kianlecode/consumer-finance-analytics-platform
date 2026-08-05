CREATE TABLE rule_evaluation (
    rule_evaluation_id    UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id        UUID          NOT NULL,
    rule_code             VARCHAR(50)   NOT NULL,
    rule_name             VARCHAR(255)  NOT NULL,
    rule_category         VARCHAR(30)   NOT NULL,
    input_value           VARCHAR(255),
    comparison_operator   VARCHAR(20),
    threshold_value       VARCHAR(255),
    evaluation_result     VARCHAR(20)   NOT NULL,
    decision_impact       VARCHAR(20)   NOT NULL DEFAULT 'NONE',
    failure_reason        VARCHAR(255),
    rule_version          VARCHAR(20)   NOT NULL DEFAULT 'V1',
    evaluated_at          TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at            TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_rule_evaluation_application
        FOREIGN KEY (application_id)
        REFERENCES application (application_id),

    CONSTRAINT uq_rule_evaluation_application_rule
        UNIQUE (application_id, rule_code, rule_version)
);


-- Hỗ trợ incremental load theo thời điểm thực thi rule
CREATE INDEX idx_rule_evaluation_evaluated_at
    ON rule_evaluation (evaluated_at);