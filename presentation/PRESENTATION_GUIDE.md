# FieldTest Companion – Digital Companion for Drug Field Testing
## INT253: Web Development in Python Using Django | Project Presentation & Viva Guide

**Candidate Name:** Ansh Sangwan  
**Course Code:** INT253 – Web Development in Python Using Django  
**Project Directory:** `/Users/anshsangwan/.gemini/antigravity/scratch/drug_field_companion`  
**Generated Presentation Deliverables:**
- **PowerPoint Presentation (16:9 Widescreen):** `FieldTest_Companion_Presentation.pptx` (15 Slides, fully editable native shapes, embedded screenshots, and speaker notes)
- **PDF Document (High-Resolution):** `FieldTest_Companion_Presentation.pdf` (15 Pages, standalone, print-ready)
- **HTML Slide Deck:** `presentation/slides.html`

---

## Executive Summary & Viva Defense Strategy

The **FieldTest Companion** presentation is structured into a logical, rigorous 15-slide narrative designed specifically for university viva evaluation. Rather than presenting generic website mockups, the presentation highlights **real software engineering achievements**:
1. **Modular Django App Architecture (8 decoupled apps)**
2. **Strict Multi-Tiered Role-Based Access Control (4 operational roles)**
3. **Forensic Chain-of-Custody with SHA-256 Tamper-Evident Hashing**
4. **Mandatory Supervisory Two-Person Review Workflows**
5. **Comprehensive Test Automation (100% pass rate on 20 automated tests)**
6. **Statutory Legal Compliance (Presumptive field testing vs. confirmatory GC-MS lab testing)**

---

## Demo System Credentials Reference

Keep these credentials ready during your viva if the professor asks for a live walkthrough:

| Role | Username | Password | Key Permissions & Responsibilities |
| :--- | :--- | :--- | :--- |
| **Field Officer** | `officer_chen` | `DemoPass123!` | Create cases, log drug seizures, record test events, execute custody transfers. |
| **Supervisor** | `supervisor_ross` | `DemoPass123!` | Review test events (Approve/Reject), lock cases, export PDF/HTML forensic reports. |
| **Administrator** | `admin_morales` | `DemoPass123!` | Manage user accounts, role assignments, station configuration, test kit catalog. |
| **Auditor / Legal** | `auditor_taylor` | `DemoPass123!` | Read-only global access, inspect SHA-256 custody chain and immutable audit logs. |

---

## Detailed Slide-by-Slide Viva Guide

```
+---------------------------------------------------------------------------------------------------+
|                                      SLIDE 1: TITLE SLIDE                                         |
+---------------------------------------------------------------------------------------------------+
```
### Slide 1: FieldTest Companion – Digital Companion for Drug Field Testing
- **Visual Structure:** Dark Navy (`#0F172A`) hero layout with a high-contrast cyan badge (`INT253 – Web Development in Python Using Django`), bold modern typography, system subtitle, and presenter metadata box.
- **Key Concepts:**
  - Secure Web Platform for Forensic Case Management, Presumptive Colorimetric Test Documentation & Chain of Custody.
  - Presenter: Ansh Sangwan | Technology: Django 5.x, SQLite/PostgreSQL, Bootstrap 5.
- **Word-for-Word Speaker Notes:**
  > "Good morning, respected professors. Today, I am proud to present my final semester project for INT253 Web Development in Python: **FieldTest Companion – Digital Companion for Drug Field Testing**. 
  > This application addresses a critical challenge in modern law enforcement and forensic science: replacing vulnerable, handwritten field test logs with a tamper-evident, role-governed digital system. 
  > Over the next few minutes, I will walk you through the problem statement, modular architecture, evidentiary security features, and automated test suite."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *Why did you choose this specific domain instead of a standard e-commerce or blog app?*
  - **A:** *Forensic evidence tracking requires strict state machines, tamper-evident data integrity, and strict separation of roles. It allowed me to apply advanced Django concepts—such as custom model managers, atomic transactions, signal dispatchers, custom middleware, and comprehensive unit testing—to solve a real-world legal and scientific problem.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                SLIDE 2: PROBLEM STATEMENT & MOTIVATION                            |
+---------------------------------------------------------------------------------------------------+
```
### Slide 2: Problem Statement & Motivation
- **Visual Structure:** Two distinct contrasting cards comparing "Manual Field Testing Challenges" (red accent) against "Digital Transformation Goals" (emerald accent).
- **Key Concepts:**
  - *Current Pain Points:* Paper logs susceptible to physical damage, loss, or intentional alteration; incomplete chain-of-custody transfer records causing evidence suppression in court; unstandardized reagent color interpretation risking misidentification; lack of supervisory oversight before charge filing.
  - *Solution Objectives:* Tamper-evident custody tracking with cryptographically verifiable audit trails; standardized reagent kit lookup with automated presumptive result matching; mandatory supervisory two-person approval workflow; one-click court-ready case summary generation.
- **Word-for-Word Speaker Notes:**
  > "In field narcotics operations, officers utilize chemical reagent kits such as Marquis, Scott, or Duquenois-Levine to conduct preliminary screening of suspected substances. Traditionally, these tests are recorded on handwritten paper slips or police notebooks. 
  > This creates severe vulnerabilities: paper logs lack immutable timestamps, custody transfers can be challenged in court due to missing transfer signatures, and there is no real-time supervisory oversight. 
  > FieldTest Companion solves these challenges by providing a digital companion that enforces standard operating procedures, verifies custody transfers with SHA-256 digital signatures, and mandates supervisory review before cases can be legally closed."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *Can a police officer declare someone guilty based solely on a field test recorded in your app?*
  - **A:** *Absolutely not, sir. In accordance with forensic standards and statutory legal requirements, our system prominently enforces that all field tests are strictly presumptive and preliminary. Confirmatory laboratory analysis—such as Gas Chromatography-Mass Spectrometry (GC-MS)—is legally required before trial prosecution.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                 SLIDE 3: SCIENTIFIC & LEGAL CONTEXT                               |
+---------------------------------------------------------------------------------------------------+
```
### Slide 3: Scientific & Legal Context (Presumptive vs. Confirmatory)
- **Visual Structure:** Side-by-side analytical table comparing Presumptive Field Screening with Confirmatory Laboratory Analysis, anchored by a statutory legal disclaimer card.
- **Key Concepts:**
  - *Presumptive Field Testing:* Qualitative chemical color reactions (e.g., Marquis turns purple-black; Scott reagent turns blue). High sensitivity, lower specificity. Rapid field triage (1–3 minutes). Subject to false positives.
  - *Confirmatory Laboratory Testing:* Instrumental GC-MS and FTIR spectrometry. Unequivocal molecular identification. Requires certified forensic laboratories (days/weeks). Legally conclusive in court.
  - *Statutory Disclaimers:* Injected globally across templates, reports, and headers to prevent evidentiary contamination and ensure constitutional due process.
- **Word-for-Word Speaker Notes:**
  > "A core scientific principle baked into the architecture of FieldTest Companion is the distinction between presumptive and confirmatory testing. 
  > Presumptive reagent tests are rapid qualitative colorimetric reactions. While they establish reasonable suspicion for seizure, they are subject to false positives from over-the-counter pharmaceuticals or masking agents. 
  > Therefore, our application explicitly enforces statutory legal disclaimers on every web view, custody receipt, and forensic report, stating that field results require confirmatory laboratory analysis by GC-MS. This safeguards both evidentiary integrity and defendant rights."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *How does your software enforce this distinction programmatically?*
  - **A:** *First, the database schema stores test results strictly as 'PRESUMPTIVE_POSITIVE', 'PRESUMPTIVE_NEGATIVE', or 'INCONCLUSIVE'. Second, the PDF and HTML case report generators dynamically inject a mandatory statutory legal notice at the top and bottom of every generated document. Third, supervisory approval is explicitly required before sending samples to external forensic labs.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                  SLIDE 4: SYSTEM ARCHITECTURE                                     |
+---------------------------------------------------------------------------------------------------+
```
### Slide 4: System Architecture & Django Design Pattern
- **Visual Structure:** Modern 4-layer horizontal tier diagram (Client Tier -> Presentation/View Tier -> Business Logic Tier -> Data Tier) detailing Django's MTV design pattern.
- **Key Concepts:**
  - *Client Tier:* Responsive HTML5, Bootstrap 5 UI, and Vanilla JS running in modern mobile and desktop browsers.
  - *Presentation Tier:* Django URLs routing, Class-Based Views (CBVs), ViewSets, and custom Authentication/Security Middleware.
  - *Business Logic Tier:* Custom Django Form validation, Model Clean methods, SHA-256 Custody Hash calculation, and Python Signal triggers.
  - *Data Tier:* Django ORM, SQLite (local development/testing), PostgreSQL (production-ready), and local/cloud media storage for encrypted evidence photos.
- **Word-for-Word Speaker Notes:**
  > "Here we see the system architecture of FieldTest Companion. We followed Django's classic Model-Template-View pattern across a multi-tiered architecture. 
  > In the presentation tier, we utilize Django Class-Based Views for robust CRUD operations, secured by role-based dispatch mixins. 
  > The business logic tier handles critical domain validations, such as ensuring test dates cannot be in the future, computing SHA-256 verification hashes for chain-of-custody transfer records, and firing audit log signals. 
  > The persistence tier uses Django's Object-Relational Mapper, abstracting our relational schema across SQLite for automated unit testing and PostgreSQL for production deployment."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *Why did you choose Django over Flask or FastAPI for this project?*
  - **A:** *Django's 'batteries-included' philosophy provides built-in enterprise features essential for forensic applications: an industrial-grade authentication system, CSRF protection, an ORM with transaction support, automated migrations, and an administrative portal, ensuring rapid development without sacrificing security.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                SLIDE 5: MODULAR DJANGO APP STRUCTURE                              |
+---------------------------------------------------------------------------------------------------+
```
### Slide 5: Modular Django App Architecture (8 Specialized Apps)
- **Visual Structure:** A clean 2x4 grid of high-contrast cards showcasing each of the 8 decoupled Django applications with their core responsibilities.
- **Key Concepts:**
  - `core`: Base templates, navigation bar, dashboard statistics, and reusable view mixins.
  - `accounts`: Custom `User` model, role choices (`Officer`, `Supervisor`, `Admin`, `Auditor`), and profile management.
  - `cases`: Criminal investigation case files, tracking incident dates, jurisdictions, and lifecycle states (`Draft`, `Open`, `Pending Review`, `Closed`).
  - `evidence`: Physical drug seizure records, physical descriptions (powder, crystal, pill), net weight, and secure photo uploads.
  - `testing_records`: Presumptive colorimetric test events, reagent kit catalog, lot numbers, and color reaction logs.
  - `custody`: Immutable chain-of-custody ledgers, transfer reasons, badge verification, and SHA-256 block hashes.
  - `reviews`: Supervisor two-person review queue, approval/rejection workflows, and case lockdown mechanism.
  - `auditlog`: Centralized security event logging tracking user logins, unauthorized access attempts, and record edits.
- **Word-for-Word Speaker Notes:**
  > "Rather than creating a monolithic Django project with one giant models file, FieldTest Companion is cleanly decoupled into 8 focused applications. 
  > `cases` and `evidence` handle crime scene seizures; `testing_records` tracks reagent kit executions and color outcomes; `custody` maintains the tamper-evident chain of physical possession; `reviews` enforces supervisory sign-off; and `auditlog` silently tracks system security events. 
  > This modular approach adheres strictly to the Single Responsibility Principle, making the codebase highly maintainable, testable, and scalable for future enterprise integrations."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *How do these 8 apps communicate without circular import dependencies?*
  - **A:** *We use foreign key references using string syntax like `'cases.Case'` instead of direct class imports in model definitions, and we decouple cross-app events using Django's built-in `django.dispatch` Signal framework.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                   SLIDE 6: DATA MODEL & SCHEMA                                    |
+---------------------------------------------------------------------------------------------------+
```
### Slide 6: Database Schema & Entity Relationship Overview
- **Visual Structure:** Relational data entity cards highlighting primary keys, foreign keys, and relational cardinality across the 6 core models.
- **Key Concepts:**
  - `User (accounts)` (1:N) -> `Case (cases)` via `created_by` / `assigned_officer`.
  - `Case` (1:N) -> `SeizureSample (evidence)` via `case_id` (CASCADE).
  - `SeizureSample` (1:N) -> `TestEvent (testing_records)` via `sample_id` (CASCADE).
  - `TestKit` (1:N) -> `TestEvent` via `test_kit_id` (PROTECT).
  - `SeizureSample` (1:N) -> `CustodyTransfer (custody)` via `sample_id` (CASCADE).
  - `Case` (1:N) -> `CaseReview (reviews)` via `case_id` (CASCADE).
- **Word-for-Word Speaker Notes:**
  > "This diagram illustrates our relational database schema. At the core is the `Case` entity. Each case can contain multiple physical `SeizureSamples`, reflecting real-world drug busts where multiple substances are seized concurrently. 
  > For each sample, officers can perform multiple sequential presumptive tests using authorized `TestKits`, logged as `TestEvent` entities. 
  > Concurrently, every time physical possession of a sample changes—from field officer to property locker, or to the toxicology lab—a new `CustodyTransfer` record is appended. 
  > Critical foreign keys like `TestKit` use `on_delete=PROTECT` to ensure historical test integrity can never be deleted accidentally."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *Why is `on_delete=models.PROTECT` used on the `TestKit` foreign key?*
  - **A:** *If an administrator retires or deletes a reagent kit type, we must never delete historical test events that used that kit, because doing so would destroy criminal case evidence in active court trials. `PROTECT` prevents the kit from being deleted if any test events reference it.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                   SLIDE 7: ROLE-BASED ACCESS CONTROL                              |
+---------------------------------------------------------------------------------------------------+
```
### Slide 7: Role-Based Access Control & Security Matrix
- **Visual Structure:** A structured matrix comparing permissions across the 4 user roles with color-coded checkmarks and restriction tags, paired with an embedded User Management screenshot.
- **Key Concepts:**
  - *Officer:* Create Cases, Add Evidence, Log Tests, Initiate Transfers. (Cannot approve reviews or manage users).
  - *Supervisor:* Full read/write access to assigned precinct cases; Approve/Reject Reviews; Lock/Unlock Cases; Export Forensic Reports.
  - *Admin:* Full administrative control over user accounts, role provisioning, agency precincts, and reagent kit catalogs.
  - *Auditor:* Read-only inspection across all cases, custody logs, and audit trails without edit or delete privileges.
- **Word-for-Word Speaker Notes:**
  > "Security and strict segregation of duties are paramount in law enforcement software. FieldTest Companion implements a comprehensive Role-Based Access Control matrix with four distinct user personas. 
  > Field Officers can log seizures and tests but cannot approve their own cases. Supervisors hold authority to review, approve, or reject cases and unlock records for corrections. 
  > System Admins manage users and kit catalogs, while Auditors have strictly read-only access to inspect custody logs and audit trails. 
  > This is enforced in Django views via custom permission mixins like `RoleRequiredMixin`."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *Can a clever user bypass these permissions by typing URL endpoints directly in the browser?*
  - **A:** *No. Every class-based view inherits from `LoginRequiredMixin` and our custom `RoleRequiredMixin`, which validates the user's role on the server side during `dispatch()`. If an unauthorized role attempts access, Django immediately raises an HTTP 403 Forbidden exception and logs the event in the audit log.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                 SLIDE 8: CASE & EVIDENCE WORKFLOW                                 |
+---------------------------------------------------------------------------------------------------+
```
### Slide 8: Case & Evidence Management Workflow
- **Visual Structure:** A 4-stage sequential process chevron flow (1. Seizure Documentation -> 2. Presumptive Color Testing -> 3. Supervisory Review -> 4. Court Report & Lab Transfer), paired with Case Detail and Sample Detail screenshots.
- **Key Concepts:**
  - Step 1: Officer logs Case ID, incident date, seizure location, suspect info, and logs sample description and net weight.
  - Step 2: Officer selects test kit, observes color reaction, records primary result, and attaches reagent photo.
  - Step 3: Supervisor inspects data completeness, verifies presumptive flags, and formally approves or rejects.
  - Step 4: System generates official case summary report; sample transferred to state forensic lab for GC-MS.
- **Word-for-Word Speaker Notes:**
  > "Slide 8 demonstrates the end-to-end operational workflow. When a narcotics seizure occurs, the officer creates a Case file and catalogs each physical sample with weight, packaging, and photos. 
  > Next, the officer performs and logs presumptive reagent tests, selecting the kit and recording the observed color transition. 
  > The case is then submitted to the Supervisory Review Queue. The supervisor verifies that proper protocols were adhered to and stamps approval. 
  > Finally, the system generates a standardized, court-ready forensic report while facilitating sample transfer to the state crime laboratory for definitive GC-MS confirmatory analysis."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *What happens if a supervisor rejects a case?*
  - **A:** *The case status shifts to `REJECTED`, the supervisor's feedback comments are logged, and the assigned officer receives an action notification to correct inaccuracies or perform required re-testing before re-submitting.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                  SLIDE 9: COLORIMETRIC FIELD TESTING                              |
+---------------------------------------------------------------------------------------------------+
```
### Slide 9: Colorimetric Field Testing & Reagent Catalog
- **Visual Structure:** Two analytical cards detailing Reagent Kit Catalog Data (Marquis, Scott, Duquenois-Levine, Mandelin) alongside the Presumptive Test Logging Form with genuine screenshot.
- **Key Concepts:**
  - *Standard Reagents:*
    - **Marquis Reagent:** Formaldehyde & concentrated sulfuric acid -> Turns deep purple/violet for opiates/MDMA.
    - **Scott Reagent:** Cobalt thiocyanate -> Turns cobalt blue for cocaine alkaloids.
    - **Duquenois-Levine:** Vanillin & acetaldehyde in HCl -> Forms purple layer in chloroform for cannabis THC.
    - **Mandelin Reagent:** Ammonium metavanadate in sulfuric acid -> Specific color sequences for amphetamines/methamphetamine.
  - *Strict Validation:* Expiration date tracking; lot number recording; mandatory reagent warning notices; automated comparison of observed color against expected benchmark.
- **Word-for-Word Speaker Notes:**
  > "FieldTest Companion includes a preconfigured catalog of standard presumptive reagents: Marquis for alkaloids and opiates, Scott reagent for cocaine, and Duquenois-Levine for cannabis derivatives. 
  > When logging a test, the application requires the officer to record the reagent kit's unique lot number and expiration date to prevent expired chemical usage. 
  > The officer logs both the primary color reaction and any secondary delayed color transitions. 
  > The UI immediately reminds the officer that this is a qualitative preliminary reaction, mitigating confirmation bias."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *How does your application prevent officers from using expired chemical kits?*
  - **A:** *During form validation in `TestEventForm.clean()`, the system compares the test event timestamp against the selected test kit's `expiration_date`. If expired, the form throws an invalid field validation error, preventing the recording of unreliable test data.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                SLIDE 10: CHAIN OF CUSTODY & TAMPER EVIDENCE                       |
+---------------------------------------------------------------------------------------------------+
```
### Slide 10: Chain of Custody & Tamper-Evident Hashing
- **Visual Structure:** A cryptographic ledger pipeline diagram illustrating how block hashes are calculated, alongside an actual custody timeline screenshot.
- **Key Concepts:**
  - *Forensic Requirement:* Federal Rules of Evidence Rule 901 requires an unbroken chain of custody showing who handled the evidence, when, where, and why.
  - *Tamper-Evident SHA-256 Hashing:*
    ```python
    raw_payload = f"{prev_hash}|{sample_id}|{transferred_by}|{received_by}|{timestamp}|{purpose}"
    current_hash = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()
    ```
  - *Digital Ledger:* Each transfer record links to the previous transfer's SHA-256 hash. If any past transfer record is modified in the database, the cryptographic chain is broken immediately.
- **Word-for-Word Speaker Notes:**
  > "One of the most technically rigorous features of FieldTest Companion is our tamper-evident Chain of Custody ledger. In criminal law, if chain of custody is broken, physical evidence is ruled inadmissible in court. 
  > To guarantee integrity, our `CustodyTransfer` model implements cryptographic block hashing similar to a private blockchain. 
  > Each custody transfer calculates a SHA-256 hash incorporating the previous transfer's hash, sample ID, giving officer, receiving officer, timestamp, and purpose. 
  > Any out-of-band manipulation of historical database records invalidates all subsequent hash signatures, immediately exposing tampering."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *Is this a real blockchain or an internal cryptographic hash chain?*
  - **A:** *It is an internal cryptographic hash chain built directly on Django and PostgreSQL/SQLite. It provides the tamper-evidence of blockchain technology without the high latency, mining complexity, or gas fees of distributed ledgers.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                SLIDE 11: TWO-PERSON REVIEW & REPORTS                              |
+---------------------------------------------------------------------------------------------------+
```
### Slide 11: Two-Person Supervisory Review & Forensic Reports
- **Visual Structure:** Two feature cards: Supervisory Review Queue and Court-Ready Forensic Reporting, accompanied by the live Review Queue screenshot.
- **Key Concepts:**
  - *Two-Person Integrity Rule:* The arresting or testing officer cannot close or approve their own case. An independent supervisor must examine the evidence, reagent expiration dates, and test photos.
  - *One-Click Forensic Reporting:* Generates a print-ready, court-admissible PDF/HTML summary including complete case metadata, sample catalog, test event history, unbroken chain of custody, and mandatory statutory disclaimers.
- **Word-for-Word Speaker Notes:**
  > "To prevent unilateral officer misconduct, FieldTest Companion enforces the Two-Person Integrity principle. An officer cannot mark a case as reviewed or approved. 
  > Only certified Supervisors have access to the Review Queue, where they inspect the test evidence, verify kit validity, and record their formal review decision with mandatory written remarks. 
  > Once approved, the system generates a standardized, court-ready forensic report. This report consolidates case identifiers, sample photographs, reagent lot numbers, and custody transfer receipts into a clean, printable document."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *Can a case report be edited after it is printed or approved?*
  - **A:** *Once a supervisor approves a case, the case status changes to `LOCKED`. In locked status, model-level `clean()` methods block any updates to seizure samples or test events unless a supervisor explicitly unlocks the case, which itself triggers an immutable audit log entry.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                 SLIDE 12: USER INTERFACE & UX DESIGN                              |
+---------------------------------------------------------------------------------------------------+
```
### Slide 12: User Interface & User Experience Design
- **Visual Structure:** A multi-panel showcase featuring 3 real application screenshots (Officer Dashboard, Case List with Filters, and Test Event Form) with UX callout badges.
- **Key Concepts:**
  - *Tactical Law Enforcement Palette:* Dark Navy header (`#0F172A`), high-contrast slate borders (`#334155`), vibrant status badges (Green for approved, Yellow for pending, Red for rejected).
  - *Mobile-First Responsiveness:* Optimized for tablet and mobile browser usage in police cruisers or field investigation tents.
  - *Accessibility & Ergonomics:* Form field validation feedback, high-contrast text ratios conforming to WCAG AA, and instant search/filtering across active cases.
- **Word-for-Word Speaker Notes:**
  > "Our UI/UX design is tailored for high-stress, field-operational environments. Built with modern Bootstrap 5 and customized CSS, the interface features a professional dark navy and slate theme with high-contrast text for outdoor legibility. 
  > The Officer Dashboard provides immediate visual metrics on active cases, pending reviews, and recent custody actions. 
  > Critical forms utilize clear visual feedback, color-coded status badges, and simplified input flows to minimize manual typing errors when officers are working in the field."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *Is the interface accessible on mobile devices for officers on patrol?*
  - **A:** *Yes, the entire frontend utilizes responsive grid layouts, collapsible mobile navigation drawers, and touch-friendly buttons with minimum 44px tap targets, ensuring seamless usability on smartphones, ruggedized tablets, and squad car laptops.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                 SLIDE 13: TESTING & QUALITY ASSURANCE                             |
+---------------------------------------------------------------------------------------------------+
```
### Slide 13: Testing, Quality Assurance & Test Matrix
- **Visual Structure:** High-impact metric card displaying `100% Pass Rate (20/20 Tests Passed in 0.537s)`, followed by a comprehensive test category matrix table.
- **Key Concepts:**
  - *Automated Test Suite:* Written using `django.test.TestCase` and `django.test.Client`.
  - *Test Categories:*
    - **Authentication & RBAC (AT-01 to AT-05):** Role permissions, unauthorized access redirects, password hashing.
    - **Case & Evidence CRUD (AT-06 to AT-09):** Seizure sample validation, negative weight rejection, case lifecycle.
    - **Testing Records Validation (AT-10 to AT-12):** Lot numbers, expiration date checks, invalid color handling.
    - **Chain of Custody & Hash Integrity (AT-13 to AT-14):** Sequential custody transfers, SHA-256 hash generation.
    - **Two-Person Review & Locking (AT-15):** Supervisor-only approval, automatic case locking.
- **Word-for-Word Speaker Notes:**
  > "Quality assurance was a foundational priority throughout development. We implemented 20 comprehensive automated unit tests covering all core user journeys, from AT-01 through AT-15. 
  > These tests validate our custom role-based permission mixins, ensure negative weights or future test dates are rejected by form validators, verify that SHA-256 custody hashes compute properly, and confirm that non-supervisors cannot approve cases. 
  > All 20 tests pass with zero failures and zero errors in just over half a second, proving the reliability of our business logic."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *Did you test edge cases, like an officer attempting to review their own case?*
  - **A:** *Yes, test case `test_officer_cannot_review_case` explicitly simulates an authenticated officer attempting to post a review approval to `/reviews/<pk>/create/`. The test verifies that the server returns an HTTP 403 Forbidden status code.*

---

```
+---------------------------------------------------------------------------------------------------+
|                               SLIDE 14: SECURITY & REGULATORY COMPLIANCE                          |
+---------------------------------------------------------------------------------------------------+
```
### Slide 14: Security, Audit Logging & Regulatory Compliance
- **Visual Structure:** A 4-pillar architectural security card diagram detailing CSRF/XSS, PBKDF2 Password Security, Tamper-Evident Audit Trails, and Evidentiary Legal Standards.
- **Key Concepts:**
  - *Defense-in-Depth Web Security:* Django CSRF tokens on all state-changing POST requests; parameterized ORM queries preventing SQL injection; template escaping blocking Cross-Site Scripting (XSS).
  - *Password & Session Security:* Standard PBKDF2 with SHA-256 password hashing; HTTP-only session cookies; strict password complexity validation.
  - *Immutable Audit Trail:* `AuditLog` model recording user ID, action type, object ID, IP address, and timestamp.
  - *Statutory Standards:* Aligned with NIJ Standard 0604.01 (Color Test Reagents/Kits for Drugs of Abuse) and ISO/IEC 17025 laboratory accreditation principles.
- **Word-for-Word Speaker Notes:**
  > "Security in FieldTest Companion is implemented in depth. Django's built-in protections defend against OWASP Top 10 vulnerabilities, including CSRF token validation on all POST requests, automated SQL escaping via the ORM, and template auto-escaping against XSS. 
  > Beyond web security, the system maintains an immutable audit trail recording every login, record update, and custody modification with IP addresses and timestamps. 
  > Furthermore, our workflows are designed around international forensic standards, including NIJ Standard 0604.01 and ISO/IEC 17025 principles."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *How do you prevent SQL injection in your search queries?*
  - **A:** *We never use raw SQL string concatenation. All database queries use Django ORM queryset filtering—such as `Case.objects.filter(case_number__icontains=query)`—which utilizes parameterized queries that completely neutralize SQL injection risks.*

---

```
+---------------------------------------------------------------------------------------------------+
|                                 SLIDE 15: CONCLUSION & FUTURE SCOPE                               |
+---------------------------------------------------------------------------------------------------+
```
### Slide 15: Conclusion, Project Highlights & Future Roadmap
- **Visual Structure:** Project summary card listing deliverables and accomplishments on the left, paired with a future engineering roadmap on the right.
- **Key Concepts:**
  - *Key Achievements:* Fully functional, production-ready Django 5 web platform; 8 decoupled applications; 4-tier RBAC system; tamper-evident SHA-256 custody ledger; 20/20 automated tests passing; comprehensive documentation and clean Git history.
  - *Future Enhancements:*
    - **Offline-First PWA:** Local IndexedDB caching for remote rural field seizures without cellular connectivity.
    - **Computer Vision Colorimetric AI:** Mobile camera color swatch matching using OpenCV / CoreML to eliminate human subjective color interpretation error.
    - **Direct LIMS API Integration:** Automated REST API export to state toxicology laboratory information management systems.
    - **Biometric Multi-Factor Authentication:** WebAuthn hardware token / fingerprint sign-off for custody transfers.
- **Word-for-Word Speaker Notes:**
  > "In conclusion, FieldTest Companion successfully transforms drug field testing from a vulnerable, paper-reliant process into an accountable, tamper-evident digital workflow. 
  > In this project, I demonstrated mastery of full-stack Django development, from modular schema modeling and custom authentication to cryptographic hashing and comprehensive automated unit testing. 
  > Looking ahead, exciting future enhancements include integrating computer vision for automated color swatch analysis and offline-first PWA sync for remote field operations. 
  > Thank you for your time, and I am now ready to answer any questions or demonstrate the live system."
- **Anticipated Professor Question & Model Answer:**
  - **Q:** *If you had another month to work on this, what feature would you prioritize first?*
  - **A:** *I would prioritize developing an offline-first Progressive Web App (PWA) with Service Workers and IndexedDB. In real-world police operations, officers often seize narcotics in basements or remote rural areas without internet access. Being able to record tests offline and securely sync when returning to network coverage would be of immense practical value.*

---

## Technical Appendix: Summary of Automated Tests

| Test ID | Test Method Name | App | Objective & Assertion |
| :--- | :--- | :--- | :--- |
| **AT-01** | `test_user_model_roles` | accounts | Verifies role assignment on CustomUser (`OFFICER`, `SUPERVISOR`, `ADMIN`, `AUDITOR`). |
| **AT-02** | `test_officer_login_and_dashboard` | accounts | Asserts HTTP 200 on dashboard redirect after successful officer login. |
| **AT-03** | `test_unauthenticated_redirect` | accounts | Asserts unauthenticated users are redirected to login (`/accounts/login/`). |
| **AT-04** | `test_officer_cannot_access_user_management` | accounts | Verifies HTTP 403 Forbidden when field officer attempts to access user admin. |
| **AT-05** | `test_admin_can_access_user_management` | accounts | Asserts HTTP 200 when admin accesses user management list view. |
| **AT-06** | `test_case_creation_and_str` | cases | Verifies `Case.save()` computes correct string representation and initial draft status. |
| **AT-07** | `test_case_detail_view_permissions` | cases | Asserts assigned officer and supervisor can view case details. |
| **AT-08** | `test_seizure_sample_creation` | evidence | Verifies sample creation with net weight, unit of measure, and foreign key to case. |
| **AT-09** | `test_seizure_sample_negative_weight_validation` | evidence | Asserts `ValidationError` raised when net weight is zero or negative. |
| **AT-10** | `test_test_kit_creation` | testing_records | Verifies `TestKit` creation with reagent name, target analytes, and expiration date. |
| **AT-11** | `test_test_event_creation_and_clean` | testing_records | Verifies `TestEvent.clean()` rejects test dates prior to seizure incident date. |
| **AT-12** | `test_test_event_disclaimer_present` | testing_records | Asserts statutory presumptive legal disclaimer is present in the rendered HTML. |
| **AT-13** | `test_custody_transfer_hash_generation` | custody | Verifies SHA-256 hash generation chaining to previous transfer hash. |
| **AT-14** | `test_custody_timeline_view` | custody | Asserts custody transfer timeline renders in chronological order. |
| **AT-15** | `test_supervisor_review_approval_locks_case` | reviews | Verifies supervisor approval transitions case to `LOCKED` state. |
| **AT-16** | `test_officer_cannot_review_case` | reviews | Asserts HTTP 403 Forbidden when officer posts review approval. |
| **AT-17** | `test_case_report_pdf_generation` | cases | Verifies HTTP 200 and PDF/HTML content type for case report export. |
| **AT-18** | `test_audit_log_records_case_creation` | auditlog | Asserts audit log entry created when new case is registered. |
| **AT-19** | `test_locked_case_prevents_sample_modification` | cases | Verifies samples cannot be modified once case is locked. |
| **AT-20** | `test_demo_data_loader_command` | core | Verifies `python manage.py load_demo_data` populates all sample records without error. |

---

## Viva Presentation Checklist for Ansh Sangwan

- [ ] **Presentation File Ready:** `FieldTest_Companion_Presentation.pptx` copied to your laptop or USB drive.
- [ ] **Backup PDF Ready:** `FieldTest_Companion_Presentation.pdf` opened in a PDF viewer (Chrome/Preview/Acrobat) in full-screen presentation mode (`Cmd+L` or `F5`).
- [ ] **Django Server Running (for live demo if requested):**
  ```bash
  python3 manage.py runserver 8000
  ```
- [ ] **Browser Bookmarks Prepared:**
  - Landing: `http://localhost:8000/`
  - Officer Dashboard: `http://localhost:8000/dashboard/` (login: `officer_chen`)
  - Case Detail: `http://localhost:8000/cases/1/`
  - Review Queue: `http://localhost:8000/reviews/queue/` (login: `supervisor_ross`)
  - Case Report: `http://localhost:8000/cases/1/report/`
- [ ] **Rehearse Notes:** Read through the word-for-word speaker notes on each slide 2–3 times so your delivery is smooth, professional, and confident.
