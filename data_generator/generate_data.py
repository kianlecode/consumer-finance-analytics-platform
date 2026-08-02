from __future__ import annotations

import argparse
import csv
import json
import random
import uuid
from calendar import monthrange
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


SEED = 20260801
AS_OF_DATE = date(2026, 7, 31)
NAMESPACE = uuid.UUID("1d96a8c2-b2ea-4b68-9134-4777c3d45cbc")

SCENARIOS = (
    "CANCELLED",
    "SUBMISSION_FAILED",
    "RECEIVED",
    "VALIDATING",
    "ASSESSMENT_FAIL",
    "RULE_REJECT",
    "MANUAL_REVIEW",
    "APPROVED_NO_DISBURSEMENT",
    "DISBURSEMENT_REJECTED",
    "PENDING_DISBURSEMENT",
    "ACTIVE_NO_REPAYMENT",
    "ACTIVE_PARTIAL",
    "ACTIVE_PAID",
    "CLOSED",
)

TABLE_FIELDS = {
    "partner_app/partner": ["partner_id", "partner_code", "partner_name", "partner_type", "status", "created_at", "updated_at"],
    "partner_app/campaign": ["campaign_id", "partner_id", "campaign_code", "campaign_name", "campaign_type", "channel", "start_date", "end_date", "budget", "status", "created_at", "updated_at"],
    "partner_app/customer_registration": ["registration_id", "partner_id", "campaign_id", "customer_id", "full_name", "phone_number", "citizen_id", "date_of_birth", "gender", "monthly_income", "requested_amount", "requested_term", "loan_purpose", "customer_type", "status", "created_at", "updated_at"],
    "partner_app/application_submission": ["submission_id", "registration_id", "request_id", "submit_status", "submitted_at", "los_reference_id", "error_code", "error_message", "created_at", "updated_at"],
    "cms/customer": ["customer_id", "customer_code", "citizen_id", "full_name", "date_of_birth", "gender", "phone_number", "customer_status", "created_at", "updated_at"],
    "los/loan_application": ["loan_application_id", "request_id", "registration_id", "customer_id", "los_application_no", "application_status_code", "product_code", "requested_amount", "requested_term", "loan_purpose", "submitted_at", "created_at", "updated_at"],
    "los/application_status_history": ["status_history_id", "loan_application_id", "status_sequence", "application_status_code", "status_reason", "changed_by", "changed_at"],
    "los/credit_assessment": ["credit_assessment_id", "loan_application_id", "score_model_code", "credit_score", "risk_level", "declared_income", "verified_income", "monthly_debt_obligation", "debt_to_income_ratio", "assessment_result", "assessed_at", "created_at", "updated_at"],
    "los/rule_evaluation": ["rule_evaluation_id", "loan_application_id", "rule_code", "rule_name", "rule_category", "input_value", "comparison_operator", "threshold_value", "evaluation_result", "decision_impact", "failure_reason", "rule_version", "evaluated_at", "created_at"],
    "los/application_decision": ["application_decision_id", "loan_application_id", "decision_code", "decision_method", "decision_reason_code", "decision_reason", "approved_amount", "approved_term", "annual_interest_rate", "decided_by", "decided_at", "created_at", "updated_at"],
    "los/disbursement_request": ["disbursement_request_id", "loan_application_id", "application_decision_id", "request_no", "disbursement_amount", "beneficiary_account_no", "beneficiary_bank_code", "beneficiary_name", "request_status", "payment_reference_id", "failure_code", "failure_message", "requested_at", "sent_at", "responded_at", "created_at", "updated_at"],
    "payment/loan_contract": ["contract_id", "contract_number", "payment_reference_id", "loan_application_id", "customer_id", "disbursement_request_no", "principal_amount", "term_months", "annual_interest_rate", "contract_date", "disbursement_date", "maturity_date", "outstanding_principal", "contract_status", "created_at", "updated_at"],
    "payment/repayment_schedule": ["installment_id", "contract_id", "installment_number", "due_date", "principal_due", "interest_due", "total_due", "installment_status", "paid_at", "created_at", "updated_at"],
    "payment/payment_transaction": ["transaction_id", "transaction_reference", "contract_id", "installment_id", "transaction_type", "transaction_amount", "principal_amount", "interest_amount", "payment_method", "transaction_status", "external_reference", "transaction_at", "created_at", "updated_at"],
}


def stable_uuid(kind: str, index: int | str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"{kind}:{index}"))


def money(value: Decimal | int | float | str) -> str:
    return str(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def rate(value: Decimal | str) -> str:
    return str(Decimal(str(value)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


def ts(value: datetime | None) -> str:
    return value.isoformat(sep=" ", timespec="seconds") if value else ""


def ds(value: date | None) -> str:
    return value.isoformat() if value else ""


def add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    return date(year, month, min(value.day, monthrange(year, month)[1]))


def age_on(dob: date, on_date: date) -> int:
    return on_date.year - dob.year - ((on_date.month, on_date.day) < (dob.month, dob.day))


def empty_tables() -> dict[str, list[dict[str, object]]]:
    return {name: [] for name in TABLE_FIELDS}


def generate_dataset(registration_count: int = 28, seed: int = SEED) -> tuple[dict[str, list[dict[str, object]]], dict[str, object]]:
    if registration_count < len(SCENARIOS):
        raise ValueError(f"registration_count must be at least {len(SCENARIOS)} to cover every smoke-test scenario")

    rng = random.Random(seed)
    tables = empty_tables()
    scenario_counts: dict[str, int] = defaultdict(int)

    partner_specs = [
        ("MOMO", "MoMo", "FINTECH"),
        ("ZALO", "Zalo", "FINTECH"),
        ("TIKI", "Tiki", "ECOMMERCE"),
    ]
    partner_ids: list[str] = []
    campaign_ids: list[str] = []
    for i, (code, name, partner_type) in enumerate(partner_specs, 1):
        partner_id = stable_uuid("partner", i)
        partner_ids.append(partner_id)
        created = datetime(2024, 12, i, 9, 0)
        tables["partner_app/partner"].append({
            "partner_id": partner_id, "partner_code": code, "partner_name": name,
            "partner_type": partner_type, "status": "ACTIVE", "created_at": ts(created), "updated_at": "",
        })
        for offset, (suffix, campaign_type, channel) in enumerate((("ALWAYS", "NORMAL", "APP"), ("PROMO", "PROMOTION", "WEB")), 1):
            campaign_no = (i - 1) * 2 + offset
            campaign_id = stable_uuid("campaign", campaign_no)
            campaign_ids.append(campaign_id)
            start = date(2025, 1, 1)
            end = date(2026, 12, 31)
            tables["partner_app/campaign"].append({
                "campaign_id": campaign_id, "partner_id": partner_id,
                "campaign_code": f"{code}_{suffix}_2025", "campaign_name": f"{name} {suffix.title()} Loan",
                "campaign_type": campaign_type, "channel": channel, "start_date": ds(start), "end_date": ds(end),
                "budget": money(0 if campaign_type == "NORMAL" else 500_000_000), "status": "ACTIVE",
                "created_at": ts(datetime(2024, 12, 15, 9, 0) + timedelta(days=campaign_no)), "updated_at": "",
            })

    first_names = ["An", "Bình", "Chi", "Dũng", "Giang", "Hà", "Hùng", "Lan", "Linh", "Minh", "Nam", "Nga", "Phúc", "Quân", "Thảo", "Trang", "Tuấn", "Vy", "Yến", "Khánh", "Long", "Mai"]
    family_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Đỗ", "Bùi"]
    customer_count = max(1, registration_count - max(2, registration_count // 5))
    customers: list[dict[str, object]] = []
    cms_rows_by_id: dict[str, dict[str, object]] = {}
    for i in range(customer_count):
        customer_id = stable_uuid("customer", i + 1)
        full_name = f"{family_names[i % len(family_names)]} {first_names[i % len(first_names)]}"
        dob = date(1986 + (i % 16), (i % 12) + 1, min(5 + i, 28))
        created = datetime(2024, 6, 1, 8, 0) + timedelta(days=i) if i < 6 else datetime(2025, 1, 1, 8, 0) + timedelta(days=i * 7)
        customer = {
            "customer_id": customer_id, "customer_code": f"CUS{i + 1:08d}", "citizen_id": f"001{(1980 + i) % 100:02d}{i + 1:07d}",
            "full_name": full_name, "date_of_birth": ds(dob), "gender": "MALE" if i % 2 == 0 else "FEMALE",
            "phone_number": f"09{(i % 8) + 1}{i + 1:07d}", "customer_status": "ACTIVE",
            "created_at": ts(created), "updated_at": ts(created),
        }
        customers.append(customer)
        cms_row = customer.copy()
        tables["cms/customer"].append(cms_row)
        cms_rows_by_id[customer_id] = cms_row

    prior_registration_count: dict[str, int] = defaultdict(int)

    for i in range(registration_count):
        scenario = SCENARIOS[i % len(SCENARIOS)]
        scenario_counts[scenario] += 1
        customer_index = i if i < customer_count else i - customer_count
        customer = customers[customer_index]
        registration_id = stable_uuid("registration", i + 1)
        cycle = i // len(SCENARIOS)
        if scenario == "CLOSED":
            created = datetime(2025, 1, 6, 9, 0) + timedelta(days=cycle * 30, minutes=i)
        elif scenario in {"ACTIVE_NO_REPAYMENT", "ACTIVE_PARTIAL", "ACTIVE_PAID"}:
            created = datetime(2026, 4, 1, 9, 0) + timedelta(days=cycle * 30 + (i % len(SCENARIOS)), minutes=i)
        else:
            created = datetime(2026, 1, 6, 9, 0) + timedelta(days=i * 5, minutes=i)
        partner_index = i % len(partner_ids)
        campaign_index = partner_index * 2 + (i % 2)
        if scenario == "CLOSED":
            requested_term = 6
        elif scenario in {"ACTIVE_NO_REPAYMENT", "ACTIVE_PARTIAL", "ACTIVE_PAID"}:
            requested_term = 36
        else:
            requested_term = (12, 24, 36)[i % 3]
        monthly_income = Decimal("7500000") if scenario == "RULE_REJECT" else Decimal(10_000_000 + (i % 9) * 2_000_000)
        requested_amount = Decimal(20_000_000 + (i % 6) * 10_000_000)
        preexisting = customer_index < 6
        customer_type = "RELOAN" if preexisting or prior_registration_count[str(customer["customer_id"])] else "NEW_TO_BANK"
        if customer_type == "NEW_TO_BANK":
            cms_created = created - timedelta(minutes=1)
            customer["created_at"] = ts(cms_created)
            customer["updated_at"] = ts(cms_created)
            cms_rows_by_id[str(customer["customer_id"])]["created_at"] = ts(cms_created)
            cms_rows_by_id[str(customer["customer_id"])]["updated_at"] = ts(cms_created)
        prior_registration_count[str(customer["customer_id"])] += 1
        registration_status = "CANCELLED" if scenario == "CANCELLED" else "SUBMITTED"
        registration = {
            "registration_id": registration_id, "partner_id": partner_ids[partner_index], "campaign_id": campaign_ids[campaign_index],
            "customer_id": customer["customer_id"], "full_name": customer["full_name"], "phone_number": customer["phone_number"],
            "citizen_id": customer["citizen_id"], "date_of_birth": customer["date_of_birth"], "gender": customer["gender"],
            "monthly_income": money(monthly_income), "requested_amount": money(requested_amount), "requested_term": requested_term,
            "loan_purpose": ("PERSONAL", "EDUCATION", "BUSINESS")[i % 3], "customer_type": customer_type,
            "status": registration_status, "created_at": ts(created), "updated_at": ts(created + timedelta(minutes=20)),
        }
        tables["partner_app/customer_registration"].append(registration)

        if scenario == "CANCELLED":
            continue

        submitted = created + timedelta(minutes=5)
        request_id = f"REQ{submitted:%Y%m%d}{i + 1:06d}"
        submission_id = stable_uuid("submission", i + 1)
        loan_application_id = stable_uuid("loan_application", i + 1)
        los_no = f"LOS{submitted:%Y%m%d}{i + 1:06d}"
        success = scenario != "SUBMISSION_FAILED"
        tables["partner_app/application_submission"].append({
            "submission_id": submission_id, "registration_id": registration_id, "request_id": request_id,
            "submit_status": "SUCCESS" if success else "FAILED", "submitted_at": ts(submitted),
            "los_reference_id": los_no if success else "", "error_code": "" if success else "LOS_TIMEOUT",
            "error_message": "" if success else "Connection timeout while submitting to LOS",
            "created_at": ts(submitted), "updated_at": ts(submitted + timedelta(seconds=10)),
        })
        if not success:
            continue

        current_status = {
            "RECEIVED": "RECEIVED", "VALIDATING": "VALIDATING", "ASSESSMENT_FAIL": "REJECTED",
            "RULE_REJECT": "REJECTED", "MANUAL_REVIEW": "MANUAL_REVIEW",
            "APPROVED_NO_DISBURSEMENT": "APPROVED",
        }.get(scenario, "DISBURSEMENT_REQUESTED")
        status_paths = {
            "RECEIVED": ["RECEIVED"],
            "VALIDATING": ["RECEIVED", "VALIDATING"],
            "ASSESSMENT_FAIL": ["RECEIVED", "VALIDATING", "CREDIT_ASSESSMENT", "REJECTED"],
            "RULE_REJECT": ["RECEIVED", "VALIDATING", "CREDIT_ASSESSMENT", "RULE_EVALUATION", "REJECTED"],
            "MANUAL_REVIEW": ["RECEIVED", "VALIDATING", "CREDIT_ASSESSMENT", "RULE_EVALUATION", "MANUAL_REVIEW"],
            "APPROVED_NO_DISBURSEMENT": ["RECEIVED", "VALIDATING", "CREDIT_ASSESSMENT", "RULE_EVALUATION", "APPROVED"],
        }
        path = status_paths.get(scenario, ["RECEIVED", "VALIDATING", "CREDIT_ASSESSMENT", "RULE_EVALUATION", "APPROVED", "DISBURSEMENT_REQUESTED"])
        final_changed = submitted
        for seq, status in enumerate(path, 1):
            changed = submitted + timedelta(minutes=seq)
            final_changed = changed
            actor = "UNDERWRITER" if status == "MANUAL_REVIEW" else ("SYSTEM" if status in {"RECEIVED", "VALIDATING"} else "LOS_ENGINE")
            tables["los/application_status_history"].append({
                "status_history_id": stable_uuid("status_history", f"{i + 1}:{seq}"), "loan_application_id": loan_application_id,
                "status_sequence": seq, "application_status_code": status, "status_reason": f"Application moved to {status}",
                "changed_by": actor, "changed_at": ts(changed),
            })
        tables["los/loan_application"].append({
            "loan_application_id": loan_application_id, "request_id": request_id, "registration_id": registration_id,
            "customer_id": customer["customer_id"], "los_application_no": los_no, "application_status_code": current_status,
            "product_code": "CASH_LOAN", "requested_amount": money(requested_amount), "requested_term": requested_term,
            "loan_purpose": registration["loan_purpose"], "submitted_at": ts(submitted),
            "created_at": ts(submitted + timedelta(seconds=2)), "updated_at": ts(final_changed),
        })

        if scenario in {"RECEIVED", "VALIDATING"}:
            continue

        verified_income = monthly_income * Decimal("0.90")
        debt = Decimal("2000000") if scenario != "MANUAL_REVIEW" else verified_income * Decimal("0.55")
        dti = debt / verified_income
        if scenario == "ASSESSMENT_FAIL":
            score, risk_level, assessment_result = 420, "VERY_HIGH", "FAIL"
        elif scenario == "MANUAL_REVIEW":
            score, risk_level, assessment_result = 590, "HIGH", "REFER"
        else:
            score, risk_level, assessment_result = 720 - (i % 5) * 15, "LOW" if i % 2 == 0 else "MEDIUM", "PASS"
        assessed_at = submitted + timedelta(minutes=3)
        tables["los/credit_assessment"].append({
            "credit_assessment_id": stable_uuid("credit_assessment", i + 1), "loan_application_id": loan_application_id,
            "score_model_code": "SCORE_V1", "credit_score": score, "risk_level": risk_level,
            "declared_income": money(monthly_income), "verified_income": money(verified_income),
            "monthly_debt_obligation": money(debt), "debt_to_income_ratio": rate(dti),
            "assessment_result": assessment_result, "assessed_at": ts(assessed_at),
            "created_at": ts(assessed_at), "updated_at": ts(assessed_at),
        })

        if scenario == "ASSESSMENT_FAIL":
            decision_code, reason_code, reason = "REJECTED", "CREDIT_SCORE_FAIL", "Credit assessment failed"
            approved_amount = approved_term = annual_rate = ""
        else:
            evaluated_at = submitted + timedelta(minutes=4)
            customer_age = age_on(date.fromisoformat(str(customer["date_of_birth"])), evaluated_at.date())
            rule_specs = [
                ("MIN_AGE", "Minimum age check", "ELIGIBILITY", str(customer_age), "GTE", "18", "PASS", "NONE", ""),
                ("MIN_INCOME", "Minimum income check", "CREDIT", money(monthly_income), "GTE", money(10_000_000),
                 "FAIL" if scenario == "RULE_REJECT" else "PASS", "REJECT" if scenario == "RULE_REJECT" else "NONE",
                 "Income below minimum threshold" if scenario == "RULE_REJECT" else ""),
                ("MAX_DTI", "Maximum debt-to-income check", "RISK", rate(dti), "LTE", "0.5000",
                 "REFER" if scenario == "MANUAL_REVIEW" else "PASS", "REFER" if scenario == "MANUAL_REVIEW" else "NONE",
                 "Debt-to-income ratio requires manual review" if scenario == "MANUAL_REVIEW" else ""),
            ]
            for rule_code, rule_name, category, input_value, operator, threshold, result, impact, failure_reason in rule_specs:
                tables["los/rule_evaluation"].append({
                    "rule_evaluation_id": stable_uuid("rule_evaluation", f"{i + 1}:{rule_code}:V1"),
                    "loan_application_id": loan_application_id, "rule_code": rule_code, "rule_name": rule_name,
                    "rule_category": category, "input_value": input_value, "comparison_operator": operator,
                    "threshold_value": threshold, "evaluation_result": result, "decision_impact": impact,
                    "failure_reason": failure_reason, "rule_version": "V1", "evaluated_at": ts(evaluated_at), "created_at": ts(evaluated_at),
                })
            if scenario == "RULE_REJECT":
                decision_code, reason_code, reason = "REJECTED", "MIN_INCOME_FAIL", "Mandatory income rule failed"
                approved_amount = approved_term = annual_rate = ""
            elif scenario == "MANUAL_REVIEW":
                decision_code, reason_code, reason = "MANUAL_REVIEW", "HIGH_DTI_REFER", "Application routed to underwriter"
                approved_amount = approved_term = annual_rate = ""
            else:
                decision_code, reason_code, reason = "APPROVED", "ELIGIBLE", "Credit assessment and mandatory rules passed"
                approved_amount = requested_amount * Decimal("0.80")
                approved_term = requested_term
                annual_rate = Decimal("0.2400") if risk_level == "MEDIUM" else Decimal("0.2000")

        decision_at = submitted + timedelta(minutes=5)
        decision_id = stable_uuid("application_decision", i + 1)
        tables["los/application_decision"].append({
            "application_decision_id": decision_id, "loan_application_id": loan_application_id,
            "decision_code": decision_code, "decision_method": "AUTO",
            "decision_reason_code": reason_code, "decision_reason": reason,
            "approved_amount": money(approved_amount) if approved_amount != "" else "",
            "approved_term": approved_term, "annual_interest_rate": rate(annual_rate) if annual_rate != "" else "",
            "decided_by": "LOS_ENGINE", "decided_at": ts(decision_at), "created_at": ts(decision_at), "updated_at": ts(decision_at),
        })
        if decision_code != "APPROVED" or scenario == "APPROVED_NO_DISBURSEMENT":
            continue

        requested_at = submitted + timedelta(minutes=6)
        request_no = f"DIS{requested_at:%Y%m%d}{i + 1:06d}"
        payment_ref = f"PAY{requested_at:%Y%m%d}{i + 1:06d}" if scenario != "DISBURSEMENT_REJECTED" else ""
        request_status = "REJECTED" if scenario == "DISBURSEMENT_REJECTED" else "ACCEPTED"
        tables["los/disbursement_request"].append({
            "disbursement_request_id": stable_uuid("disbursement_request", i + 1), "loan_application_id": loan_application_id,
            "application_decision_id": decision_id, "request_no": request_no, "disbursement_amount": money(approved_amount),
            "beneficiary_account_no": f"0123{i + 1:08d}", "beneficiary_bank_code": ("VCB", "TCB", "MBB")[i % 3],
            "beneficiary_name": str(customer["full_name"]).upper(), "request_status": request_status,
            "payment_reference_id": payment_ref, "failure_code": "INVALID_ACCOUNT" if request_status == "REJECTED" else "",
            "failure_message": "Beneficiary account is invalid" if request_status == "REJECTED" else "",
            "requested_at": ts(requested_at), "sent_at": ts(requested_at + timedelta(seconds=2)),
            "responded_at": ts(requested_at + timedelta(seconds=4)), "created_at": ts(requested_at),
            "updated_at": ts(requested_at + timedelta(seconds=4)),
        })
        if request_status != "ACCEPTED":
            continue

        contract_id = stable_uuid("contract", i + 1)
        contract_date = requested_at.date()
        disbursement_time = requested_at + timedelta(minutes=1)
        successful_disbursement = scenario != "PENDING_DISBURSEMENT"
        term = int(approved_term)
        principal = Decimal(approved_amount)
        schedule_rows: list[dict[str, object]] = []
        transaction_rows: list[dict[str, object]] = []
        outstanding = principal
        contract_updated = requested_at + timedelta(seconds=5)

        transaction_rows.append({
            "transaction_id": stable_uuid("transaction", f"{i + 1}:DISBURSEMENT"),
            "transaction_reference": f"TRX{disbursement_time:%Y%m%d}{i + 1:06d}D",
            "contract_id": contract_id, "installment_id": "", "transaction_type": "DISBURSEMENT",
            "transaction_amount": money(principal), "principal_amount": money(principal), "interest_amount": money(0),
            "payment_method": "BANK_TRANSFER", "transaction_status": "SUCCESS" if successful_disbursement else "PENDING",
            "external_reference": f"BANK{disbursement_time:%Y%m%d}{i + 1:06d}" if successful_disbursement else "",
            "transaction_at": ts(disbursement_time), "created_at": ts(disbursement_time), "updated_at": ts(disbursement_time),
        })

        maturity_date: date | None = None
        if successful_disbursement:
            monthly_rate = Decimal(annual_rate) / Decimal(12)
            base_principal = (principal / Decimal(term)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            opening = principal
            for installment_no in range(1, term + 1):
                due = add_months(disbursement_time.date(), installment_no)
                principal_due = opening if installment_no == term else base_principal
                interest_due = (opening * monthly_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                installment_id = stable_uuid("installment", f"{i + 1}:{installment_no}")
                status, paid_at = "PENDING", None
                paid_principal = Decimal(0)
                paid_interest = Decimal(0)
                if scenario == "ACTIVE_PARTIAL" and installment_no == 1 and due <= AS_OF_DATE:
                    status = "PARTIALLY_PAID"
                    paid_principal = (principal_due / 2).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    paid_interest = interest_due
                elif scenario in {"ACTIVE_PAID", "CLOSED"} and due <= AS_OF_DATE:
                    status = "PAID"
                    paid_principal, paid_interest = principal_due, interest_due
                    paid_at = datetime.combine(due, datetime.min.time()).replace(hour=9, minute=15)
                elif due <= AS_OF_DATE:
                    status = "OVERDUE"

                if paid_principal or paid_interest:
                    paid_time = paid_at or datetime.combine(due, datetime.min.time()).replace(hour=9, minute=15)
                    transaction_rows.append({
                        "transaction_id": stable_uuid("transaction", f"{i + 1}:REPAYMENT:{installment_no}"),
                        "transaction_reference": f"TRX{paid_time:%Y%m%d}{i + 1:06d}R{installment_no:02d}",
                        "contract_id": contract_id, "installment_id": installment_id, "transaction_type": "REPAYMENT",
                        "transaction_amount": money(paid_principal + paid_interest), "principal_amount": money(paid_principal),
                        "interest_amount": money(paid_interest), "payment_method": ("AUTO_DEBIT", "BANK_TRANSFER")[installment_no % 2],
                        "transaction_status": "SUCCESS", "external_reference": f"BANK{paid_time:%Y%m%d}{i + 1:06d}{installment_no:02d}",
                        "transaction_at": ts(paid_time), "created_at": ts(paid_time + timedelta(seconds=1)),
                        "updated_at": ts(paid_time + timedelta(seconds=2)),
                    })
                    outstanding -= paid_principal
                    contract_updated = max(contract_updated, paid_time)
                updated = paid_at or datetime.combine(min(due, AS_OF_DATE), datetime.min.time())
                schedule_rows.append({
                    "installment_id": installment_id, "contract_id": contract_id, "installment_number": installment_no,
                    "due_date": ds(due), "principal_due": money(principal_due), "interest_due": money(interest_due),
                    "total_due": money(principal_due + interest_due), "installment_status": status,
                    "paid_at": ts(paid_at), "created_at": ts(disbursement_time + timedelta(seconds=10)), "updated_at": ts(updated),
                })
                opening -= principal_due
            maturity_date = add_months(disbursement_time.date(), term)

        contract_status = "PENDING_DISBURSEMENT" if not successful_disbursement else ("CLOSED" if scenario == "CLOSED" else "ACTIVE")
        tables["payment/loan_contract"].append({
            "contract_id": contract_id, "contract_number": f"LN{contract_date:%Y%m}{i + 1:06d}",
            "payment_reference_id": payment_ref, "loan_application_id": loan_application_id,
            "customer_id": customer["customer_id"], "disbursement_request_no": request_no,
            "principal_amount": money(principal), "term_months": term, "annual_interest_rate": rate(annual_rate),
            "contract_date": ds(contract_date), "disbursement_date": ds(disbursement_time.date()) if successful_disbursement else "",
            "maturity_date": ds(maturity_date), "outstanding_principal": money(outstanding), "contract_status": contract_status,
            "created_at": ts(requested_at + timedelta(seconds=5)), "updated_at": ts(contract_updated),
        })
        tables["payment/repayment_schedule"].extend(schedule_rows)
        tables["payment/payment_transaction"].extend(transaction_rows)

    manifest = {
        "seed": seed, "as_of_date": ds(AS_OF_DATE), "registration_count": registration_count,
        "scenario_counts": dict(sorted(scenario_counts.items())),
        "row_counts": {name: len(rows) for name, rows in tables.items()},
        "excluded_tables": ["partner_app.customer_activity", "partner_app.notification_log"],
    }
    return tables, manifest


def write_dataset(tables: dict[str, list[dict[str, object]]], manifest: dict[str, object], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for table_name, rows in tables.items():
        system, table = table_name.split("/", 1)
        directory = output_dir / system
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / f"{table}.csv").open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=TABLE_FIELDS[table_name], extrasaction="raise")
            writer.writeheader()
            writer.writerows(rows)
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic source data for the Consumer Finance Analytics Platform")
    parser.add_argument("--registrations", type=int, default=28)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--output", type=Path, default=Path("output/smoke"))
    args = parser.parse_args()
    tables, manifest = generate_dataset(args.registrations, args.seed)
    write_dataset(tables, manifest, args.output)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
