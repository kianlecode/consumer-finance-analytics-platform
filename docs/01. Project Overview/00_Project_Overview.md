# Version 1.0

# Project Overview

## Project Vision

This project aims to build an end-to-end Analytics Engineering Platform that simulates the data ecosystem of a modern Consumer Finance company.

Rather than focusing solely on data transformation with dbt, the project reproduces a complete analytical platform including operational systems, data ingestion, Lakehouse storage, transformation, orchestration, and business analytics.

The platform is designed to resemble a real-world enterprise data environment while remaining fully deployable on a local machine using open-source technologies.

---

# Project Objectives

The project is designed to strengthen both Analytics Engineering and Data Engineering capabilities by covering the complete analytical lifecycle.

## Business Objectives

- Simulate the operational systems of a Consumer Finance company.
- Design realistic business processes and business rules.
- Generate business data that reflects real operational scenarios.
- Build an enterprise-style analytical platform.

## Technical Objectives

- Design enterprise data architecture.
- Build an end-to-end ELT pipeline.
- Implement Lakehouse architecture.
- Practice modern Data Modeling techniques.
- Implement dbt best practices.
- Apply Data Quality Testing.
- Orchestrate data pipelines using Apache Airflow.
- Develop business dashboards using Power BI.

---

# Business Domain

## Industry

Consumer Finance

## Business Scenario

Loan Origination through Partner Channels

The simulated company provides personal loan products through external partner applications such as digital wallets, fintech platforms, and merchant applications.

Customers submit loan applications through partner channels, which are processed by multiple operational systems responsible for customer management, loan origination, and payment processing.

---

# Architecture Vision

The project adopts a modern Lakehouse architecture that separates operational systems from analytical workloads.

The analytical platform consists of the following major layers:

- Source Systems
- Compute Layer
- Object Storage
- Lakehouse
- Transformation Layer
- Analytics Layer
- Orchestration Layer

The complete architecture is documented in the Technical Architecture document.

---

# Dataset Strategy

The project follows a Hybrid Dataset Strategy.

Instead of relying on a single dataset, multiple public datasets may be combined with generated data to build a realistic business environment.

## Principles

- Prefer public datasets whenever possible.
- Generate data only when suitable datasets are unavailable.
- Generated data must follow business rules.
- Generated data must remain internally consistent across systems.
- Every generated dataset should be explainable and reproducible.

---

# Technology Stack

| Layer | Technology | Purpose |
|--------|------------|---------|
| Programming Language | Python | Data generation and ingestion scripts |
| Source Database | PostgreSQL | Operational transactional database |
| Event Database | MongoDB | Customer activity and event tracking |
| Compute Engine | Apache Spark | Data ingestion and distributed processing |
| Object Storage | MinIO | S3-compatible storage for analytical datasets |
| Table Format | Delta Lake | ACID Lakehouse storage |
| Transformation | dbt Core | SQL-based ELT transformations |
| Orchestration | Apache Airflow | Workflow scheduling and orchestration |
| Analytics | Power BI | Reporting and dashboard visualization |
| Development | Docker Compose | Local deployment environment |
| Version Control | Git + GitHub | Source code management |

---

# Project Scope

Version 1 focuses on a single business domain.

Business Domain

```
Consumer Finance
        │
        ▼
Loan Origination
        │
        ▼
Partner Channel
        │
        ▼
Analytics Platform
```

The initial implementation covers:

- Customer registration
- Loan application
- Customer verification
- Loan assessment
- Loan contract generation
- Loan disbursement
- Loan repayment

Future versions may expand into additional financial products and business domains.

---

# Project Principles

## Principle 1

Build an enterprise-style Analytics Engineering Platform rather than a simple technology demo.

---

## Principle 2

Design before implementation.

Business architecture, source systems, data models, and technical architecture should be completed before development begins.

---

## Principle 3

Business drives data.

Every dataset should originate from a realistic business process.

---

## Principle 4

Technology serves architecture.

Technology choices should support architectural requirements rather than drive them.

---

## Principle 5

Maintain modularity.

Each layer of the platform should have a clear responsibility and remain loosely coupled with other layers.

---

## Principle 6

Document major design decisions.

Significant architectural and technical decisions should be recorded throughout the project lifecycle.

---

# Current Project Status

The project is currently in the Design Phase.

Completed:

- Project definition
- Business Architecture
- Logical Data Architecture
- Technical Architecture
- Initial implementation roadmap

Next phase:

- Source Database Design
- Data Generation Framework
- Docker Environment
- Spark Ingestion Pipeline

---

# Decision Log

| ID | Decision | Status |
|----|----------|--------|
| D001 | Consumer Finance selected as the business domain | ✅ |
| D002 | Build an end-to-end Analytics Engineering Platform | ✅ |
| D003 | Adopt a Hybrid Dataset Strategy | ✅ |
| D004 | Follow a Design-First approach | ✅ |
| D005 | PostgreSQL selected as the relational source database | ✅ |
| D006 | MongoDB selected for event data | ✅ |
| D007 | Adopt a Lakehouse architecture | ✅ |
| D008 | Apache Spark selected as the compute engine | ✅ |
| D009 | MinIO selected as the object storage | ✅ |
| D010 | Delta Lake selected as the table format | ✅ |
| D011 | dbt Core selected for transformations | ✅ |
| D012 | Apache Airflow selected for orchestration | ✅ |