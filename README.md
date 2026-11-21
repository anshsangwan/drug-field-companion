# FieldTest Companion – Digital Companion for Drug Field Testing (DCDFT)

[![Django Version](https://img.shields.io/badge/Django-5.0.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Course](https://img.shields.io/badge/INT253-Web%20Dev%20in%20Python-orange?style=for-the-badge)](#alignment-with-int253-course-outcomes)
[![License](https://img.shields.io/badge/License-Academic%20Evaluation-blue?style=for-the-badge)](#)

---

> ### ⚠️ Mandatory Forensic Scope & Safety Disclaimer
> **This platform is an administrative record-keeping and workflow-traceability companion.**
> - Field-test outcomes documented within this application are **preliminary and presumptive screening results only**.
> - They **do not establish the definitive chemical identity** of any substance.
> - **Confirmatory laboratory analysis** by certified forensic spectrometry (e.g., GC-MS / FTIR) is legally and operationally required.
> - This software **strictly does NOT provide chemical recipes, reagent formulas, drug testing execution procedures, or automated substance identification**.
> - All demonstration records, suspect names, locations, and kit serials are entirely **fictional and synthetic**.

---

## 1. Project Overview

**FieldTest Companion (DCDFT)** is a full-stack Django web application engineered to replace fragmented manual paper logs and unstructured notes with a secure, auditable, and role-governed digital record system for field drug-testing operations.

Developed as a major assignment for **INT253: Web Development in Python Using Django**, this application models genuine chain-of-custody protocols, supervisor verification gates, private evidence vaults, and print-ready forensic summaries while maintaining strict compliance with academic safety standards.

---

## 2. Objectives

- **Digitize Field Documentation**: Streamline case creation, specimen registration, and sensory observations in real-time.
- **Assure Chain-of-Custody Integrity**: Provide an append-only chronological ledger tracking all specimen handovers, locker placements, and integrity seals.
- **Enforce Supervisory Verification**: Implement an auditable gate where supervisors can formally review, request mandatory revisions, or endorse final case documentation.
- **Secure Sensitive Evidence**: Safeguard photographic and documentary evidence in a private vault served strictly through authenticated endpoints.
- **Demonstrate Django Best Practices**: Exemplify Django Model-View-Template architecture, ORM relationships, forms validation, role-based decorators, CSRF protections, and automated testing suites.

---

## 3. Features

- **Role-Based Access Control (RBAC)**: Enforced across 4 distinct groups (`Field Officer`, `Supervisor`, `Administrator`, `Read-only User`) in backend views and queries.
- **Operational Metrics Dashboard**: Real-time KPI summary cards (Total Cases, Active Cases, Specimens Secured, Review Queue, Approved Cases, and Activity Feeds).
- **Unique Identification Generators**: Automated sequential generation of human-readable case references (`CASE-YYYY-XXXX`) and sample codes (`SMP-YYYY-XXXX`).
- **Controlled Presumptive Outcomes**: Controlled result classifications:
  - *Not performed*
  - *Inconclusive*
  - *Presumptive positive*
  - *Presumptive negative*
  - *Invalid / Kit issue*
- **Kit Expiration Safeguards**: Server-side validation checking kit batch expiration dates against execution timestamps, requiring explicit justification for overdue kits.
- **Chronological Custody Timeline**: Visual vertical ledger with automated flags for out-of-sequence retrospective entries.
- **Private Evidence Vault**: Secure upload validation (.jpg, .jpeg, .png, .pdf; max 10MB) with authenticated `FileResponse` delivery (no public static media URLs).
- **Supervisor Verification Workflow**: Multi-state workflow (`Draft` ➔ `Submitted` ➔ `Changes requested` ➔ `Approved` ➔ `Archived`) requiring mandatory supervisory feedback.
- **Print-Ready Case Summary Report**: Standardized, clean forensic report featuring embedded print CSS, seal verification tables, and supervisory endorsement signatures.
- **Immutable System Audit Trail**: Complete activity logging capturing actor, action classification, target object, client IP, and timestamps.

---

## 4. Technology Stack

- **Backend Framework**: Python 3.12 / Django 5.0.2
- **Database**: SQLite (local development / zero configuration)
- **Frontend / UI**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3.3, Bootstrap Icons
- **Template Engine**: Django Template Language (DTL)
- **Architecture**: Modular Django Monolith with 8 specialized applications
- **Version Control**: Git & GitHub-ready configuration

---

## 5. Project Architecture & Modular Applications

The codebase is organized into eight specialized, decoupled Django applications:

```
drug_field_companion/
├── manage.py
├── config/                  # Root project settings, URL routing, WSGI/ASGI
│   ├── settings.py          # Environment configuration, RBAC, private media
│   └── urls.py              # Root URL routing and custom error handlers (403, 404, 500)
├── core/                    # Landing page, dashboard metrics, demo command
│   ├── management/commands/ # Custom 'load_demo_data' command
│   └── views.py             # Role-aware dashboard & metrics calculation
├── accounts/                # Authentication, group definitions, access decorators
│   ├── decorators.py        # @role_required, @supervisor_required, @field_officer_required
│   ├── forms.py             # Custom styled login & user administration forms
│   └── views.py             # User lifecycle, role assignment, active toggles
├── cases/                   # CaseRecord & Sample models, CRUD, filtering, reports
│   ├── models.py            # Unique references, status state machines, permissions
│   ├── views.py             # List/detail views, sample registration, report generation
│   └── tests.py             # Automated test cases AT-04, AT-05, AT-08, AT-13, AT-14
├── testing_records/         # Approved kit catalogue & presumptive test events
│   ├── models.py            # TestKit catalogue, TestEvent model, safety disclaimers
│   └── forms.py             # Controlled result validation, kit expiration safeguards
├── custody/                 # Chronological chain-of-custody ledger
│   ├── models.py            # Append-only CustodyEvent model, sequence flags
│   └── views.py             # Custody event logging & visual timeline rendering
├── evidence/                # Private evidentiary file vault
│   ├── models.py            # EvidenceFile model, MIME/extension validators
│   └── views.py             # Authenticated file streaming endpoint
├── reviews/                 # Supervisor review & endorsement workflow
│   ├── models.py            # ReviewRecord model, mandatory comments validation
│   └── views.py             # Supervisory approval & revision queue
├── auditlog/                # Immutable chronological audit ledger
│   ├── models.py            # AuditEvent model
│   └── utils.py             # Reusable log_audit() helper
├── templates/               # Reusable DTL templates, base layout, and print reports
├── static/                  # Custom forensic stylesheet (styles.css) & JavaScript
└── media/                   # Private evidence vault (strictly excluded from Git)
```

---

## 6. Installation Instructions

### Prerequisites
- Python 3.11 or newer (`python3 --version`)
- pip (`python3 -m pip --version`)
- Git

### Clone the Repository
```bash
git clone https://github.com/your-username/drug_field_companion.git
cd drug_field_companion
```

---

## 7. Virtual Environment Setup

Create and activate an isolated virtual environment:

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (Command Prompt)
python -m venv .venv
.venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

## 8. Dependency Installation

Install all verified dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 9. Database Migrations

Apply the database migrations to initialize your local SQLite database:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 10. Superuser Creation

To create an initial Django Administrator account manually:

```bash
python manage.py createsuperuser
```
*(Enter your desired username, email, and password).*

---

## 11. Running the Application

Launch the local development server:

```bash
python manage.py runserver
```

Open your browser and navigate to:
**http://127.0.0.1:8000/**

---

## 12. Demo-Data Setup

To load safe, comprehensive, and realistic synthetic demo records (pre-configured users, approved kit catalogue entries, active cases, registered samples, test events, custody entries, and supervisor reviews), run:

```bash
python manage.py load_demo_data
```

### Pre-Configured Demo Accounts (Development & Evaluation)

| Role | Username | Password | Key Responsibilities |
| :--- | :--- | :--- | :--- |
| **Field Officer** | `officer_chen` | `DemoPass123!` | Create cases, register samples, record tests & custody, submit for review |
| **Supervisor** | `supervisor_ross` | `DemoPass123!` | Review pending cases, request corrections, approve documentation, view reports |
| **Administrator** | `admin_morales` | `DemoPass123!` | User management, role governance, kit catalogue, audit log, Django Admin |
| **Read-only User** | `auditor_taylor` | `DemoPass123!` | Inspection and compliance review of authorized records without modification |

> **Security Note:** Demo credentials are provided strictly for local development and academic evaluation. Never use default passwords in production.

---

## 13. Running Automated Tests

FieldTest Companion includes a comprehensive test suite validating all 15 scenarios (**AT-01 through AT-15**) defined in the Software Requirements Specification:

```bash
python manage.py test
```

### Acceptance Test Coverage Matrix

| Test ID | Scenario | Verified Behavior | Status |
| :--- | :--- | :--- | :---: |
| **AT-01** | Anonymous user opens `/dashboard/` | Redirects to login; no protected data displayed | **PASS** |
| **AT-02** | Valid user login and logout | Session initialized and terminated; protected routes locked | **PASS** |
| **AT-03** | Field Officer accesses User Management | Access denied (403 Permission Denied); no data mutation | **PASS** |
| **AT-04** | Create case with missing required field | Form re-renders with field-specific errors; no record saved | **PASS** |
| **AT-05** | Duplicate sample code registration | Second save is rejected with clean uniqueness validation | **PASS** |
| **AT-06** | Test event with allowed result category | Event linked to specimen; persistent disclaimer displayed | **PASS** |
| **AT-07** | Submit result outside defined categories | Server-side validation rejects unapproved choices | **PASS** |
| **AT-08** | Submit case for review | Status transitions to `Submitted`; audit event recorded | **PASS** |
| **AT-09** | Supervisor returns case without comment | Action rejected; mandatory comment required | **PASS** |
| **AT-10** | Supervisor approves submitted case | Status transitions to `Approved`; review history retained | **PASS** |
| **AT-11** | Add chronological custody events | Events rendered in sequence; out-of-sequence events flagged | **PASS** |
| **AT-12** | Upload disallowed or oversized files | Upload rejected; private files served only via auth endpoint | **PASS** |
| **AT-13** | Open case summary report | Contains case/sample/test/custody/review data & disclaimer | **PASS** |
| **AT-14** | Submit POST form without CSRF token | Django CSRF protection rejects request with HTTP 403 | **PASS** |
| **AT-15** | Run complete automated test suite | All 20 automated test assertions pass cleanly | **PASS** |

---

## 14. Screenshots & UI Walkthrough

*(Screenshots can be captured during demonstration)*

1. **Forensic Operations Dashboard**: Overview cards for active cases, pending reviews, quick action buttons, and recent audit activity.
2. **Case Dossier View**: Detailed case metadata, sample specimen list with status badges, and evidence manifest.
3. **Specimen Ledger & Test Documentation**: Presumptive result categories, kit lot numbers, and mandatory warning notices.
4. **Vertical Chain-of-Custody Timeline**: Step-by-step custody ledger with seal references and out-of-sequence flags.
5. **Supervisor Review Interface**: Decision controls (Approve vs. Request Corrections) with mandatory actionable comments.
6. **Print-Friendly Forensic Summary Report**: Official print-styled case summary with dual-signature sign-off blocks.

---

## 15. Known Limitations

1. **Local Filesystem Media Vault**: Evidence files are stored locally in `media/evidence_vault/`. In an enterprise production deployment, an encrypted private cloud object store (such as AWS S3 Private Bucket or Google Cloud Storage) with signed temporary URLs should be integrated.
2. **Browser-Based PDF Generation**: PDF generation is performed via the browser's native Print dialog (`window.print()`). Headless PDF engines (such as WeasyPrint) may be added if server-side PDF generation is required.
3. **Database Engine**: Configured by default for SQLite for academic simplicity. The codebase is fully compatible with PostgreSQL by configuring database environment variables.

---

## 16. Alignment with INT253 Course Outcomes

| Outcome | Syllabus Topic | Evidence in FieldTest Companion |
| :--- | :--- | :--- |
| **CO1** | Python/Django setup & project architecture | Modular 8-app structure, clean `settings.py`, virtual environment, migrations. |
| **CO2** | URL routing, views & HTTP error handling | Named URLs, path converters, GET/POST handlers, custom 403/404/500 handlers. |
| **CO3** | Django Template Language (DTL) | Reusable `base.html`, template inheritance, filters, loops, role-based nav blocks. |
| **CO4** | Django Forms & ModelForms | Server-side validation, Post/Redirect/Get pattern, CSRF tokens, custom widgets. |
| **CO5** | Django ORM, Models & Admin | ForeignKeys, cascading behaviors, unique constraints, date hierarchies, Django Admin. |
| **CO6** | Sessions, Auth & Permissions | Django Auth, session cookies, group-based access control, security headers. |

---

## 17. Publishing to GitHub

To push this repository to GitHub:

```bash
# 1. Initialize git repository
git init

# 2. Stage all project files (safe .gitignore prevents secret/database leaks)
git add .

# 3. Create initial commit
git commit -m "feat: complete FieldTest Companion application for INT253"

# 4. Link to your GitHub remote repository
git branch -M main
git remote add origin https://github.com/<your-username>/drug_field_companion.git

# 5. Push to GitHub
git push -u origin main
```
