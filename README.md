# Consumer Finance Analytics Platform

> An end-to-end data and analytics engineering project that simulates a modern data platform for the Consumer Finance domain.

## Project Overview

Consumer Finance Analytics Platform is a personal learning project designed to simulate how data is generated, processed, modeled and served in a consumer finance organization.

Instead of starting from a prepared dataset, the project begins by designing and simulating operational source systems. Data generated from these systems will then be ingested, transformed and served through a modern analytics platform.

The project follows the complete data lifecycle:

```text
Operational Source Systems
            │
            ▼
      Data Generation
            │
            ▼
       Data Ingestion
            │
            ▼
       Data Lakehouse
            │
            ▼
 Transformation & Modeling
            │
            ▼
 Analytics & Visualization
```

The project is primarily designed to develop practical Analytics Engineering skills while building a foundation for future Data Engineering work.

---

## Objectives

- Design realistic source systems for the Consumer Finance domain.
- Simulate operational data and business processes.
- Build reproducible ingestion and ELT pipelines.
- Implement a layered lakehouse architecture.
- Design scalable analytical data models.
- Apply data quality checks and incremental processing.
- Orchestrate end-to-end data workflows.
- Build business-ready datasets and Power BI dashboards.
- Practice technical documentation, Git and GitHub workflows.

---

## Business Domain

**Consumer Finance / Digital Lending**

The project simulates the lifecycle of a consumer loan application:

```text
Customer Acquisition
        │
        ▼
Loan Application
        │
        ▼
Credit Assessment
        │
        ▼
Business Rule Evaluation
        │
        ▼
Approval / Rejection
        │
        ▼
Disbursement
        │
        ▼
Analytics
```

---

## Architecture

```text
┌─────────────────────────────────────┐
│         Operational Systems         │
│                                     │
│  Partner App                        │
│  Loan Origination System            │
│  Customer Management System         │
│  Payment System                     │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│        Data Generation Layer        │
│                Python               │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│          Data Ingestion Layer       │
│          Python / Apache Spark      │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│            Data Lakehouse           │
│                                     │
│       MinIO + Delta Lake            │
│       Bronze → Silver → Gold        │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│       Transformation & Modeling     │
│          Spark SQL / dbt Core       │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│       Analytics & Visualization     │
│               Power BI              │
└─────────────────────────────────────┘
```

---

## Tech Stack

| Category | Technology |
|---|---|
| Programming | Python |
| Operational Databases | PostgreSQL, MongoDB |
| Containerization | Docker |
| Object Storage | MinIO |
| Data Lakehouse | Delta Lake |
| File Format | Parquet |
| Processing Engine | Apache Spark / Spark SQL |
| Transformation | dbt Core |
| Orchestration | Apache Airflow |
| Visualization | Power BI |
| Version Control | Git and GitHub |

The technology stack may be adjusted during implementation based on project complexity and learning objectives.

---

## Planned Analytics Use Cases

- Loan application funnel.
- Approval and rejection analysis.
- Credit score and risk analysis.
- Processing time and SLA monitoring.
- Business rule failure analysis.
- Partner and campaign performance.
- Requested versus approved loan amount.
- Disbursement performance.
- Customer and loan portfolio analysis.

---

## Current Status

The project is currently in the **Operational Source System Design Phase**.

Completed:

- Project scope and architecture.
- Implementation and learning roadmap.
- Partner App business and data design.
- Loan Origination System business and data design.

In progress:

- Remaining operational source-system design.
- Cross-system business and data relationships.

---

## Roadmap

- [x] Define project scope and architecture.
- [x] Design Partner App.
- [x] Design Loan Origination System.
- [ ] Design remaining operational systems.
- [ ] Implement source databases with Docker.
- [ ] Build Python data generators.
- [ ] Build data ingestion pipelines.
- [ ] Build Bronze, Silver and Gold layers.
- [ ] Implement dbt models and data quality tests.
- [ ] Add Airflow orchestration.
- [ ] Build Power BI dashboards.
- [ ] Complete end-to-end documentation and demonstration.

---

## Repository Status

This repository is under active development.

The current focus is on designing consistent operational systems and business data flows before starting the technical implementation.
