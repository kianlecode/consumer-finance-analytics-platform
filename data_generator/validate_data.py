from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_tables(root: Path) -> dict[str, list[dict[str, str]]]:
    return {
        str(path.relative_to(root).with_suffix("")): load_csv(path)
        for path in sorted(root.glob("*/*.csv"))
    }


def validate(root: Path) -> dict[str, object]:
    tables = load_tables(root)
    errors: list[str] = []
    checks: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    def unique(table: str, column: str) -> set[str]:
        values = [row[column] for row in tables[table]]
        require(all(values), f"{table}.{column}: contains null/blank primary or unique key")
        require(len(values) == len(set(values)), f"{table}.{column}: duplicate values found")
        checks.append(f"UNIQUE {table}.{column}")
        return set(values)

    primary_keys = {
        "partner_app/partner": "partner_id", "partner_app/campaign": "campaign_id",
        "partner_app/customer_registration": "registration_id", "partner_app/application_submission": "submission_id",
        "cms/customer": "customer_id", "los/loan_application": "loan_application_id",
        "los/application_status_history": "status_history_id", "los/credit_assessment": "credit_assessment_id",
        "los/rule_evaluation": "rule_evaluation_id", "los/application_decision": "application_decision_id",
        "los/disbursement_request": "disbursement_request_id", "payment/loan_contract": "contract_id",
        "payment/repayment_schedule": "installment_id", "payment/payment_transaction": "transaction_id",
    }
    ids = {table: unique(table, column) for table, column in primary_keys.items()}

    for table, column in (
        ("partner_app/partner", "partner_code"), ("partner_app/campaign", "campaign_code"),
        ("partner_app/application_submission", "request_id"), ("cms/customer", "customer_code"),
        ("cms/customer", "citizen_id"), ("los/loan_application", "request_id"),
        ("los/loan_application", "los_application_no"), ("payment/loan_contract", "contract_number"),
        ("payment/payment_transaction", "transaction_reference"),
    ):
        unique(table, column)

    composite_unique_specs = (
        ("partner_app/application_submission", ("registration_id",)),
        ("los/loan_application", ("registration_id",)),
        ("los/application_status_history", ("loan_application_id", "status_sequence")),
        ("los/credit_assessment", ("loan_application_id",)),
        ("los/rule_evaluation", ("loan_application_id", "rule_code", "rule_version")),
        ("los/application_decision", ("loan_application_id",)),
        ("los/disbursement_request", ("loan_application_id",)),
        ("los/disbursement_request", ("application_decision_id",)),
        ("los/disbursement_request", ("request_no",)),
        ("payment/loan_contract", ("payment_reference_id",)),
        ("payment/loan_contract", ("loan_application_id",)),
        ("payment/loan_contract", ("disbursement_request_no",)),
        ("payment/repayment_schedule", ("contract_id", "installment_number")),
    )
    for table, columns in composite_unique_specs:
        keys = [tuple(row[column] for column in columns) for row in tables[table]]
        require(len(keys) == len(set(keys)), f"{table}: duplicate composite key {columns}")
        checks.append(f"UNIQUE {table}{columns}")

    domains = {
        ("partner_app/partner", "partner_type"): {"FINTECH", "ECOMMERCE"},
        ("partner_app/partner", "status"): {"ACTIVE", "INACTIVE"},
        ("partner_app/campaign", "campaign_type"): {"NORMAL", "PROMOTION", "SEASONAL"},
        ("partner_app/campaign", "channel"): {"APP", "WEB", "FACEBOOK", "GOOGLE"},
        ("partner_app/campaign", "status"): {"ACTIVE", "CLOSED"},
        ("partner_app/customer_registration", "gender"): {"MALE", "FEMALE"},
        ("partner_app/customer_registration", "customer_type"): {"NEW_TO_BANK", "RELOAN"},
        ("partner_app/customer_registration", "status"): {"NEW", "SUBMITTED", "CANCELLED"},
        ("partner_app/application_submission", "submit_status"): {"PENDING", "SUCCESS", "FAILED"},
        ("cms/customer", "gender"): {"MALE", "FEMALE", "OTHER"},
        ("cms/customer", "customer_status"): {"ACTIVE", "BLOCKED", "INACTIVE"},
        ("los/loan_application", "application_status_code"): {"RECEIVED", "VALIDATING", "CREDIT_ASSESSMENT", "RULE_EVALUATION", "MANUAL_REVIEW", "APPROVED", "REJECTED", "DISBURSEMENT_REQUESTED"},
        ("los/credit_assessment", "risk_level"): {"LOW", "MEDIUM", "HIGH", "VERY_HIGH"},
        ("los/credit_assessment", "assessment_result"): {"PASS", "REFER", "FAIL"},
        ("los/rule_evaluation", "evaluation_result"): {"PASS", "FAIL", "REFER", "SKIPPED"},
        ("los/rule_evaluation", "decision_impact"): {"NONE", "WARNING", "REFER", "REJECT"},
        ("los/application_decision", "decision_code"): {"APPROVED", "REJECTED", "MANUAL_REVIEW"},
        ("los/application_decision", "decision_method"): {"AUTO", "MANUAL"},
        ("los/disbursement_request", "request_status"): {"PENDING", "SENT", "ACCEPTED", "REJECTED", "FAILED"},
        ("payment/loan_contract", "contract_status"): {"PENDING_DISBURSEMENT", "ACTIVE", "CLOSED", "CANCELLED", "DEFAULTED"},
        ("payment/repayment_schedule", "installment_status"): {"PENDING", "PARTIALLY_PAID", "PAID", "OVERDUE", "WAIVED"},
        ("payment/payment_transaction", "transaction_type"): {"DISBURSEMENT", "REPAYMENT"},
        ("payment/payment_transaction", "transaction_status"): {"PENDING", "SUCCESS", "FAILED"},
    }
    for (table, column), allowed in domains.items():
        bad = {row[column] for row in tables[table] if row[column] not in allowed}
        require(not bad, f"{table}.{column}: values outside domain {sorted(bad)}")
    checks.append("Data Dictionary domain values")

    required_fields = {
        "partner_app/partner": {"partner_id", "partner_code", "partner_name", "partner_type", "status", "created_at"},
        "partner_app/campaign": {"campaign_id", "partner_id", "campaign_code", "campaign_name", "campaign_type", "channel", "start_date", "end_date", "status", "created_at"},
        "partner_app/customer_registration": {"registration_id", "partner_id", "campaign_id", "customer_id", "full_name", "phone_number", "citizen_id", "date_of_birth", "gender", "monthly_income", "requested_amount", "requested_term", "customer_type", "status", "created_at"},
        "partner_app/application_submission": {"submission_id", "registration_id", "request_id", "submit_status", "submitted_at", "created_at", "updated_at"},
        "cms/customer": {"customer_id", "customer_code", "citizen_id", "full_name", "date_of_birth", "gender", "phone_number", "customer_status", "created_at", "updated_at"},
        "los/loan_application": {"loan_application_id", "request_id", "registration_id", "customer_id", "los_application_no", "application_status_code", "product_code", "requested_amount", "requested_term", "submitted_at", "created_at", "updated_at"},
        "los/application_status_history": {"status_history_id", "loan_application_id", "status_sequence", "application_status_code", "changed_by", "changed_at"},
        "los/credit_assessment": {"credit_assessment_id", "loan_application_id", "score_model_code", "credit_score", "risk_level", "declared_income", "monthly_debt_obligation", "assessment_result", "assessed_at", "created_at", "updated_at"},
        "los/rule_evaluation": {"rule_evaluation_id", "loan_application_id", "rule_code", "rule_name", "rule_category", "evaluation_result", "decision_impact", "rule_version", "evaluated_at", "created_at"},
        "los/application_decision": {"application_decision_id", "loan_application_id", "decision_code", "decision_method", "decision_reason_code", "decided_by", "decided_at", "created_at", "updated_at"},
        "los/disbursement_request": {"disbursement_request_id", "loan_application_id", "application_decision_id", "request_no", "disbursement_amount", "beneficiary_account_no", "beneficiary_bank_code", "beneficiary_name", "request_status", "requested_at", "created_at", "updated_at"},
        "payment/loan_contract": {"contract_id", "contract_number", "payment_reference_id", "loan_application_id", "customer_id", "disbursement_request_no", "principal_amount", "term_months", "annual_interest_rate", "contract_date", "outstanding_principal", "contract_status", "created_at", "updated_at"},
        "payment/repayment_schedule": {"installment_id", "contract_id", "installment_number", "due_date", "principal_due", "interest_due", "total_due", "installment_status", "created_at", "updated_at"},
        "payment/payment_transaction": {"transaction_id", "transaction_reference", "contract_id", "transaction_type", "transaction_amount", "principal_amount", "interest_amount", "payment_method", "transaction_status", "transaction_at", "created_at", "updated_at"},
    }
    for table, columns in required_fields.items():
        for row_number, row in enumerate(tables[table], 2):
            blanks = sorted(column for column in columns if not row[column])
            require(not blanks, f"{table} row {row_number}: blank required fields {blanks}")
    checks.append("Data Dictionary NOT NULL constraints")

    fk_specs = (
        ("partner_app/campaign", "partner_id", "partner_app/partner"),
        ("partner_app/customer_registration", "partner_id", "partner_app/partner"),
        ("partner_app/customer_registration", "campaign_id", "partner_app/campaign"),
        ("partner_app/customer_registration", "customer_id", "cms/customer"),
        ("partner_app/application_submission", "registration_id", "partner_app/customer_registration"),
        ("los/loan_application", "registration_id", "partner_app/customer_registration"),
        ("los/loan_application", "customer_id", "cms/customer"),
        ("los/application_status_history", "loan_application_id", "los/loan_application"),
        ("los/credit_assessment", "loan_application_id", "los/loan_application"),
        ("los/rule_evaluation", "loan_application_id", "los/loan_application"),
        ("los/application_decision", "loan_application_id", "los/loan_application"),
        ("los/disbursement_request", "loan_application_id", "los/loan_application"),
        ("los/disbursement_request", "application_decision_id", "los/application_decision"),
        ("payment/loan_contract", "loan_application_id", "los/loan_application"),
        ("payment/loan_contract", "customer_id", "cms/customer"),
        ("payment/repayment_schedule", "contract_id", "payment/loan_contract"),
        ("payment/payment_transaction", "contract_id", "payment/loan_contract"),
    )
    for child, column, parent in fk_specs:
        bad = {row[column] for row in tables[child] if row[column] and row[column] not in ids[parent]}
        require(not bad, f"{child}.{column}: orphan references {sorted(bad)[:3]}")
        checks.append(f"FK {child}.{column} -> {parent}")

    installment_ids = ids["payment/repayment_schedule"]
    bad_installments = {r["installment_id"] for r in tables["payment/payment_transaction"] if r["installment_id"] and r["installment_id"] not in installment_ids}
    require(not bad_installments, "payment_transaction.installment_id: orphan references")

    registrations = {r["registration_id"]: r for r in tables["partner_app/customer_registration"]}
    submissions = {r["registration_id"]: r for r in tables["partner_app/application_submission"]}
    applications = {r["registration_id"]: r for r in tables["los/loan_application"]}
    customers = {r["customer_id"]: r for r in tables["cms/customer"]}
    for registration_id, registration in registrations.items():
        customer = customers[registration["customer_id"]]
        require(registration["citizen_id"] == customer["citizen_id"], f"registration {registration_id}: citizen_id differs from CMS")
        require(datetime.fromisoformat(customer["created_at"]) <= datetime.fromisoformat(registration["created_at"]), f"registration {registration_id}: CMS customer created after registration")
        if registration["status"] == "CANCELLED":
            require(registration_id not in submissions, f"cancelled registration {registration_id}: has a submission")
    registrations_by_customer: dict[str, list[dict[str, str]]] = defaultdict(list)
    for registration in registrations.values():
        registrations_by_customer[registration["customer_id"]].append(registration)
    for customer_id, rows in registrations_by_customer.items():
        rows.sort(key=lambda r: r["created_at"])
        cms_created = datetime.fromisoformat(customers[customer_id]["created_at"])
        for position, registration in enumerate(rows):
            if registration["customer_type"] == "NEW_TO_BANK":
                require(position == 0, f"customer {customer_id}: later registration marked NEW_TO_BANK")
                require(datetime.fromisoformat(registration["created_at"]) - cms_created <= timedelta(minutes=5), f"customer {customer_id}: NEW_TO_BANK not created near first registration")
            elif position > 0:
                require(registration["customer_type"] == "RELOAN", f"customer {customer_id}: repeated registration is not RELOAN")
    for registration_id, submission in submissions.items():
        registration = registrations[registration_id]
        require(datetime.fromisoformat(registration["created_at"]) <= datetime.fromisoformat(submission["submitted_at"]), f"submission {submission['submission_id']}: submitted before registration")
        if submission["submit_status"] == "SUCCESS":
            require(registration_id in applications, f"successful submission {submission['submission_id']}: missing LOS application")
            if registration_id in applications:
                application = applications[registration_id]
                require(application["request_id"] == submission["request_id"], f"submission {submission['submission_id']}: request_id differs in LOS")
                require(application["submitted_at"] == submission["submitted_at"], f"submission {submission['submission_id']}: submitted_at differs in LOS")
        else:
            require(registration_id not in applications, f"failed submission {submission['submission_id']}: created LOS application")
    checks.append("Partner App -> CMS -> LOS handoff")

    status_by_app: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in tables["los/application_status_history"]:
        status_by_app[row["loan_application_id"]].append(row)
    for app in tables["los/loan_application"]:
        history = sorted(status_by_app[app["loan_application_id"]], key=lambda r: int(r["status_sequence"]))
        require(bool(history), f"application {app['loan_application_id']}: missing status history")
        if history:
            require([int(r["status_sequence"]) for r in history] == list(range(1, len(history) + 1)), f"application {app['loan_application_id']}: non-contiguous status sequence")
            require(history[-1]["application_status_code"] == app["application_status_code"], f"application {app['loan_application_id']}: current status differs from latest history")
            require(all(datetime.fromisoformat(a["changed_at"]) <= datetime.fromisoformat(b["changed_at"]) for a, b in zip(history, history[1:])), f"application {app['loan_application_id']}: status timeline is not chronological")
    checks.append("LOS status history sequence and current-state reconciliation")

    assessments = tables["los/credit_assessment"]
    require(len({r["loan_application_id"] for r in assessments}) == len(assessments), "credit_assessment: more than one row per application")
    for row in assessments:
        declared = Decimal(row["declared_income"])
        verified = Decimal(row["verified_income"])
        debt = Decimal(row["monthly_debt_obligation"])
        expected = (debt / verified).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
        require(Decimal(row["debt_to_income_ratio"]) == expected, f"credit assessment {row['credit_assessment_id']}: incorrect DTI")
        app = next(a for a in tables["los/loan_application"] if a["loan_application_id"] == row["loan_application_id"])
        registration = registrations[app["registration_id"]]
        require(Decimal(registration["monthly_income"]) == declared, f"credit assessment {row['credit_assessment_id']}: declared income is not registration snapshot")
    checks.append("Credit assessment snapshot and DTI")

    rule_keys = [(r["loan_application_id"], r["rule_code"], r["rule_version"]) for r in tables["los/rule_evaluation"]]
    require(len(rule_keys) == len(set(rule_keys)), "rule_evaluation: duplicate application + rule_code + rule_version")
    rules_by_app: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in tables["los/rule_evaluation"]:
        rules_by_app[row["loan_application_id"]].append(row)
        if row["evaluation_result"] in {"FAIL", "REFER"}:
            require(bool(row["failure_reason"]), f"rule {row['rule_evaluation_id']}: FAIL/REFER without failure_reason")
    decisions = {r["loan_application_id"]: r for r in tables["los/application_decision"]}
    require(len(decisions) == len(tables["los/application_decision"]), "application_decision: more than one row per application")
    for app_id, decision in decisions.items():
        rules = rules_by_app.get(app_id, [])
        if decision["decision_code"] == "APPROVED":
            require(not any(r["decision_impact"] == "REJECT" and r["evaluation_result"] == "FAIL" for r in rules), f"approved application {app_id}: has rejecting failed rule")
            require(all((decision[c] for c in ("approved_amount", "approved_term", "annual_interest_rate"))), f"approved application {app_id}: missing approval terms")
        else:
            require(not any((decision[c] for c in ("approved_amount", "approved_term", "annual_interest_rate"))), f"non-approved application {app_id}: has approval terms")
    checks.append("Rule evaluation uniqueness and decision consistency")

    decisions_by_id = {r["application_decision_id"]: r for r in tables["los/application_decision"]}
    requests = tables["los/disbursement_request"]
    for request in requests:
        decision = decisions_by_id[request["application_decision_id"]]
        require(decision["decision_code"] == "APPROVED", f"disbursement request {request['request_no']}: decision is not APPROVED")
        require(Decimal(request["disbursement_amount"]) == Decimal(decision["approved_amount"]), f"disbursement request {request['request_no']}: amount differs from approved amount")
        if request["request_status"] == "ACCEPTED":
            require(bool(request["payment_reference_id"]), f"accepted request {request['request_no']}: missing payment_reference_id")
        if request["request_status"] in {"REJECTED", "FAILED"}:
            require(bool(request["failure_code"]), f"failed/rejected request {request['request_no']}: missing failure code")
    checks.append("Approved decision -> disbursement request")

    contracts = {r["contract_id"]: r for r in tables["payment/loan_contract"]}
    accepted_refs = {r["payment_reference_id"] for r in requests if r["request_status"] == "ACCEPTED"}
    for contract in contracts.values():
        require(contract["payment_reference_id"] in accepted_refs, f"contract {contract['contract_number']}: not linked to accepted request")
    schedules_by_contract: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in tables["payment/repayment_schedule"]:
        schedules_by_contract[row["contract_id"]].append(row)
        require(Decimal(row["total_due"]) == Decimal(row["principal_due"]) + Decimal(row["interest_due"]), f"installment {row['installment_id']}: total_due mismatch")
        require((row["installment_status"] == "PAID") == bool(row["paid_at"]), f"installment {row['installment_id']}: paid_at inconsistent with PAID status")
    success_repayments: dict[str, Decimal] = defaultdict(Decimal)
    for row in tables["payment/payment_transaction"]:
        require(Decimal(row["transaction_amount"]) == Decimal(row["principal_amount"]) + Decimal(row["interest_amount"]), f"transaction {row['transaction_reference']}: amount components mismatch")
        if row["transaction_type"] == "DISBURSEMENT":
            require(not row["installment_id"], f"disbursement {row['transaction_reference']}: installment_id must be blank")
            require(Decimal(row["interest_amount"]) == 0, f"disbursement {row['transaction_reference']}: interest must be zero")
        elif row["transaction_status"] == "SUCCESS":
            success_repayments[row["contract_id"]] += Decimal(row["principal_amount"])
    for contract_id, contract in contracts.items():
        schedules = sorted(schedules_by_contract.get(contract_id, []), key=lambda r: int(r["installment_number"]))
        if contract["contract_status"] == "PENDING_DISBURSEMENT":
            require(not contract["disbursement_date"] and not schedules, f"pending contract {contract['contract_number']}: has disbursement date or schedule")
        else:
            require(len(schedules) == int(contract["term_months"]), f"contract {contract['contract_number']}: schedule count differs from term")
            require(sum((Decimal(r["principal_due"]) for r in schedules), Decimal(0)) == Decimal(contract["principal_amount"]), f"contract {contract['contract_number']}: scheduled principal does not equal contract principal")
        expected_outstanding = Decimal(contract["principal_amount"]) - success_repayments[contract_id]
        require(Decimal(contract["outstanding_principal"]) == expected_outstanding, f"contract {contract['contract_number']}: outstanding principal mismatch")
        if contract["contract_status"] == "ACTIVE":
            require(expected_outstanding > 0, f"active contract {contract['contract_number']}: has no outstanding principal")
        if contract["contract_status"] == "CLOSED":
            require(expected_outstanding == 0 and all(r["installment_status"] == "PAID" for r in schedules), f"closed contract {contract['contract_number']}: not fully paid")
    checks.append("Contract schedule, transaction allocation and outstanding balance")

    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    expected_counts = {name: len(rows) for name, rows in tables.items()}
    require(manifest["row_counts"] == expected_counts, "manifest row_counts do not match CSV files")
    require(set(manifest["scenario_counts"]) == {"CANCELLED", "SUBMISSION_FAILED", "RECEIVED", "VALIDATING", "ASSESSMENT_FAIL", "RULE_REJECT", "MANUAL_REVIEW", "APPROVED_NO_DISBURSEMENT", "DISBURSEMENT_REJECTED", "PENDING_DISBURSEMENT", "ACTIVE_NO_REPAYMENT", "ACTIVE_PARTIAL", "ACTIVE_PAID", "CLOSED"}, "scenario coverage is incomplete")
    checks.append("Manifest row counts and scenario coverage")

    return {
        "status": "PASS" if not errors else "FAIL",
        "check_count": len(checks), "checks": checks, "error_count": len(errors), "errors": errors,
        "row_counts": expected_counts,
        "status_distribution": {
            "registration": dict(Counter(r["status"] for r in tables["partner_app/customer_registration"])),
            "loan_application": dict(Counter(r["application_status_code"] for r in tables["los/loan_application"])),
            "decision": dict(Counter(r["decision_code"] for r in tables["los/application_decision"])),
            "contract": dict(Counter(r["contract_status"] for r in tables["payment/loan_contract"])),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate generated Consumer Finance source data")
    parser.add_argument("--input", type=Path, default=Path("output/smoke"))
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = validate(args.input)
    report_path = args.report or args.input / "validation_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
