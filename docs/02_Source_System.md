# Source Systems

## Overview

The Data Platform ingests data from four operational source systems. Each system is responsible for a specific business capability and owns its own operational data.

---

# 1. Partner App

## Purpose

The Partner App is the customer-facing channel where customers interact with loan products offered by the financial company.

## Responsibilities

- Display loan products
- Receive customer registrations
- Submit loan applications
- Record customer interaction events

## Generated Data

- Customer Activity
- Loan Registration
- Loan Application Submission

---

# 2. Loan Origination System (LOS)

## Purpose

The Loan Origination System (LOS) is the core business system responsible for managing the entire loan application lifecycle.

## Responsibilities

- Receive loan applications
- Validate application information
- Process loan applications
- Manage application status
- Generate loan contracts
- Approve or reject loan applications

## Generated Data

- Loan Application
- Application Status
- Loan Contract
- Loan Information
- Approval / Rejection Result

---

# 3. Customer Management System (CMS)

## Purpose

The Customer Management System (CMS) maintains customer master data used across business operations.

## Responsibilities

- Manage customer profiles
- Maintain KYC information
- Store demographic information
- Provide customer information for loan processing

## Generated Data

- Customer Profile
- Customer Information
- KYC Information

---

# 4. Payment System

## Purpose

The Payment System manages financial transactions throughout the loan lifecycle.

## Responsibilities

- Loan disbursement
- Repayment processing
- Payment transaction management

## Generated Data

- Disbursement
- Repayment
- Payment Transaction