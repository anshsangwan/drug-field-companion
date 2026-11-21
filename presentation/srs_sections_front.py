import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from presentation.srs_style_helpers import (
    add_heading_1, add_heading_2, add_heading_3, add_heading_4,
    add_paragraph, add_bullet, add_callout, format_table,
    NAVY, SLATE, MUTED, BLUE
)

def build_cover_page(doc):
    # Blank paragraphs to center vertically
    for _ in range(4):
        p_blank = doc.add_paragraph()
        p_blank.paragraph_format.space_before = Pt(0)
        p_blank.paragraph_format.space_after = Pt(0)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_after = Pt(28)
    r_proj = p_proj.add_run("Digital Companion for Drug Field Testing\n(FieldTest Companion)")
    r_proj.font.name = "Times New Roman"
    r_proj.font.size = Pt(22)
    r_proj.font.bold = True
    r_proj.font.color.rgb = NAVY

    p_srs = doc.add_paragraph()
    p_srs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_srs.paragraph_format.space_after = Pt(28)
    r_srs = p_srs.add_run("Software Requirements Specification")
    r_srs.font.name = "Times New Roman"
    r_srs.font.size = Pt(17)
    r_srs.font.bold = True
    r_srs.font.color.rgb = SLATE

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(28)
    r_code = p_course.add_run("Course Code: INT253\n")
    r_code.font.name = "Times New Roman"
    r_code.font.size = Pt(13.5)
    r_code.font.bold = True
    r_code.font.color.rgb = SLATE
    r_cname = p_course.add_run("Course Name: Web Development in Python Using Django")
    r_cname.font.name = "Times New Roman"
    r_cname.font.size = Pt(13)
    r_cname.font.bold = True
    r_cname.font.color.rgb = SLATE

    p_student = doc.add_paragraph()
    p_student.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_student.paragraph_format.space_after = Pt(28)
    r_name = p_student.add_run("Student Name: Ansh Sangwan\n")
    r_name.font.name = "Times New Roman"
    r_name.font.size = Pt(13.5)
    r_name.font.bold = True
    r_name.font.color.rgb = NAVY
    r_reg = p_student.add_run("Student Registration Number: [INSERT REGISTRATION NUMBER]")
    r_reg.font.name = "Times New Roman"
    r_reg.font.size = Pt(12)
    r_reg.font.bold = True
    r_reg.font.color.rgb = SLATE

    for _ in range(4):
        p_blank = doc.add_paragraph()
        p_blank.paragraph_format.space_before = Pt(0)
        p_blank.paragraph_format.space_after = Pt(0)

    p_prep = doc.add_paragraph()
    p_prep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_prep.paragraph_format.space_after = Pt(4)
    r_prep = p_prep.add_run("Prepared for\nContinuous Assessment 3\nSpring 2025")
    r_prep.font.name = "Times New Roman"
    r_prep.font.size = Pt(11.5)
    r_prep.font.bold = True
    r_prep.font.color.rgb = SLATE

    doc.add_page_break()

def build_revision_history(doc):
    add_heading_1(doc, "Revision History")
    add_paragraph(doc, "The following document revision history tracks formal iterations, amendments, and engineering refinements made to this Software Requirements Specification across its development lifecycle.")

    table = doc.add_table(rows=4, cols=4)
    headers = ["Version", "Date", "Author", "Description of Changes"]
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
    
    rows_data = [
        ("1.0", "2025-05-10", "Ansh Sangwan", "Initial baseline draft; formalization of 8-app modular architecture, MTV pattern, and core user roles."),
        ("1.1", "2025-05-18", "Ansh Sangwan", "Added presumptive colorimetric test documentation, reagent expiry validation guards, and append-only chain of custody ledger."),
        ("1.2", "2025-05-24", "Ansh Sangwan", "Incorporated supervisory two-person review workflow, case lockdown logic, court-ready printable reporting, and 20 automated tests.")
    ]
    for r_idx, data in enumerate(rows_data):
        for c_idx, val in enumerate(data):
            table.rows[r_idx + 1].cells[c_idx].text = val

    format_table(table, [Inches(0.8), Inches(1.1), Inches(1.3), Inches(3.3)])
    doc.add_page_break()

def build_table_of_contents(doc):
    add_heading_1(doc, "Table of Contents")
    add_paragraph(doc, "The table of contents reflects the structural hierarchy, section numbering, and appendices defined by the official project specification format.")

    toc_items = [
        ("1. INTRODUCTION", "1", True),
        ("  1.1 Purpose", "1", False),
        ("  1.2 Scope", "1", False),
        ("  1.3 Definitions, Acronyms, and Abbreviations", "2", False),
        ("  1.4 References", "3", False),
        ("  1.5 Overview", "4", False),
        ("2. GENERAL DESCRIPTION", "4", True),
        ("  2.1 Product Perspective", "4", False),
        ("  2.2 Product Functions", "5", False),
        ("  2.3 User Characteristics", "6", False),
        ("  2.4 General Constraints", "7", False),
        ("  2.5 Assumptions and Dependencies", "8", False),
        ("3. SPECIFIC REQUIREMENTS", "8", True),
        ("  3.1 External Interface Requirements", "8", False),
        ("    3.1.1 User Interfaces", "8", False),
        ("    3.1.2 Hardware Interfaces", "9", False),
        ("    3.1.3 Software Interfaces", "9", False),
        ("    3.1.4 Communications Interfaces", "10", False),
        ("  3.2 Functional Requirements", "10", False),
        ("    3.2.1 User Authentication and Session Management", "10", False),
        ("    3.2.2 Role-Based Access Control and Authorization", "11", False),
        ("    3.2.3 Case Record Registration and Management", "12", False),
        ("    3.2.4 Automated Case Reference Identifier Generation", "13", False),
        ("    3.2.5 Physical Seizure Sample Cataloging and Validation", "14", False),
        ("    3.2.6 Colorimetric Test Kit Catalog Management", "15", False),
        ("    3.2.7 Test Kit Expiration Validation and Justification", "16", False),
        ("    3.2.8 Presumptive Field-Test Event Documentation", "17", False),
        ("    3.2.9 Chronological Append-Only Chain of Custody Ledger", "18", False),
        ("    3.2.10 Evidence File Vault and Restricted Download Access", "19", False),
        ("    3.2.11 Supervisory Review Queue and Decision Workflow", "20", False),
        ("    3.2.12 Revision Request and Re-submission Workflow", "21", False),
        ("    3.2.13 Case Record Lockdown and Immutability Safeguards", "22", False),
        ("    3.2.14 Case Search, Multi-Criteria Filtering, and Pagination", "23", False),
        ("    3.2.15 Court-Ready Forensic Case Report Generation", "24", False),
        ("    3.2.16 Centralized Security Audit Logging and Event Tracking", "25", False),
        ("  3.5 Non-Functional Requirements", "26", False),
        ("    3.5.1 Performance", "26", False),
        ("    3.5.2 Reliability", "26", False),
        ("    3.5.3 Availability", "27", False),
        ("    3.5.4 Security", "27", False),
        ("    3.5.5 Maintainability", "28", False),
        ("    3.5.6 Portability", "28", False),
        ("  3.7 Design Constraints", "29", False),
        ("  3.9 Other Requirements", "29", False),
        ("4. ANALYSIS MODELS", "30", True),
        ("  4.1 Data Flow Diagrams (DFD)", "30", False),
        ("    4.1.1 Context-Level Data Flow Diagram (Level 0 DFD)", "30", False),
        ("    4.1.2 Level 1 Data Flow Diagram (Core Processes & Stores)", "31", False),
        ("    4.1.3 Four-Tier MTV System Architecture Diagram", "32", False),
        ("    4.1.4 Complete Entity-Relationship (ER) Diagram", "33", False),
        ("    4.1.5 End-to-End Operational Lifecycle Workflow Diagram", "34", False),
        ("5. GITHUB LINK", "35", True),
        ("6. DEPLOYED LINK", "35", True),
        ("7. CLIENT APPROVAL PROOF", "36", True),
        ("8. CLIENT LOCATION PROOF", "36", True),
        ("9. TRANSACTION ID PROOF", "37", True),
        ("10. EMAIL ACKNOWLEDGEMENT", "37", True),
        ("11. GST No.", "38", True),
        ("A. APPENDICES", "38", True),
        ("  A.1 Appendix 1: Project Setup and Execution Instructions", "38", False),
        ("  A.2 Appendix 2: Automated Test Suite Verification Matrix", "40", False),
    ]

    for title, page_str, is_major in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(3) if is_major else Pt(1)
        p.paragraph_format.space_after = Pt(3) if is_major else Pt(1)
        
        # Add tab stop at 6.5 inches with dotted leader
        tab_stops = p.paragraph_format.tab_stops
        tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        run_title = p.add_run(title)
        run_title.font.name = 'Times New Roman'
        run_title.font.size = Pt(10.5 if is_major else 10)
        run_title.font.bold = is_major
        run_title.font.color.rgb = NAVY if is_major else SLATE
        
        run_tab = p.add_run(f"\t{page_str}")
        run_tab.font.name = 'Times New Roman'
        run_tab.font.size = Pt(10.5 if is_major else 10)
        run_tab.font.bold = is_major
        run_tab.font.color.rgb = NAVY if is_major else SLATE

    doc.add_page_break()

def build_section_1(doc):
    add_heading_1(doc, "1. Introduction")
    add_paragraph(doc, "The introduction to this Software Requirements Specification (SRS) provides an authoritative, comprehensive overview of the digital platform named FieldTest Companion – Digital Companion for Drug Field Testing. Engineered as a robust full-stack web application utilizing Python and the Django framework, this specification details the functional capabilities, forensic integrity controls, external interfaces, non-functional quality attributes, and analysis models governing the system. This document is authored to provide software engineers, forensic compliance specialists, and academic evaluators with complete technical criteria to inspect, verify, and validate the software against the requirements of INT253: Web Development in Python Using Django.")

    add_heading_2(doc, "1.1 Purpose")
    add_paragraph(doc, "The primary purpose of this SRS document is to define the exact software requirements, data relationships, access-control policies, and legal-compliance boundaries for FieldTest Companion. The target audience for this document includes academic evaluators and course instructors evaluating university course project submissions, full-stack Python/Django software developers maintaining or extending the codebase, forensic quality assurance auditors examining evidentiary traceability, and law enforcement agency administrators assessing digital companion deployment.")

    add_heading_2(doc, "1.2 Scope")
    add_paragraph(doc, "This subsection formally demarcates the operational and legal scope of the software product:", bold_prefix="System Identification & Demarcation: ")
    add_bullet(doc, "Digital Companion for Drug Field Testing (Engineering Code: FieldTest Companion, Django Package: drug_field_companion).", bold_prefix="(1) Product Name: ")
    add_bullet(doc, "The application captures, catalogs, and manages seized narcotics cases; generates unique sequential reference codes; documents presumptive colorimetric test kit results; enforces kit expiration rules; records an unbroken chronological chain-of-custody ledger; provides a secure private evidence file vault; and enforces a mandatory two-person supervisory review workflow before generating court-admissible forensic summary reports.", bold_prefix="(2) System Capabilities: ")
    add_bullet(doc, "FieldTest Companion does not perform automated molecular identification, does not interpret raw spectrometry data, does not replace certified forensic toxicology laboratories, and does not provide operational recipes or instructions for chemical reagent synthesis.", bold_prefix="(3) Explicit Negative Scope: ")
    
    add_callout(doc, 
        "\"Field-test outcomes are presumptive screening results only. They do not establish the definitive identity of a substance. Confirmatory laboratory analysis is required.\"\n"
        "This statutory notice is systematically rendered across all user interfaces, field-entry forms, and official printable case reports in accordance with international forensic standards.",
        title="MANDATORY FORENSIC DISCLAIMER ENFORCEMENT"
    )

    add_paragraph(doc, "The application of FieldTest Companion resolves critical vulnerabilities inherent in conventional law enforcement field testing. By replacing handwritten notebooks with structured digital records, the platform eliminates illegible test documentation, enforces tamper seal recording, guarantees chronological chain-of-custody visibility, and ensures that preliminary screening evidence cannot be filed in judicial proceedings without explicit supervisory concurrence.", bold_prefix="Application & Benefits: ")

    add_heading_2(doc, "1.3 Definitions, Acronyms, and Abbreviations")
    add_paragraph(doc, "To facilitate unequivocal interpretation of the requirements, the specialized forensic, legal, and software engineering terms utilized throughout this SRS are defined below.")

    table = doc.add_table(rows=11, cols=3)
    headers = ["Term / Acronym", "Full Expression", "Operational & Forensic Definition"]
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
    
    terms = [
        ("SRS", "Software Requirements Specification", "A formal engineering document describing the behavior, features, and constraints of a software system."),
        ("MTV", "Model-Template-View", "Django architectural design pattern separating relational schema (Model), user presentation (Template), and business logic controller (View)."),
        ("RBAC", "Role-Based Access Control", "Security mechanism restricting system operations based on assigned organizational roles (Field Officer, Supervisor, Admin, Read-only)."),
        ("Presumptive Test", "Preliminary Chemical Color Test", "Qualitative colorimetric screening test establishing reasonable suspicion of a controlled substance; non-definitive in judicial proof."),
        ("Confirmatory Test", "Definitive Instrumental Analysis", "Unequivocal molecular identification performed by certified laboratories using Gas Chromatography-Mass Spectrometry (GC-MS)."),
        ("Chain of Custody", "Evidentiary Transfer Ledger", "Chronological documentation tracking the custody, transfer, analysis, and disposition of physical evidence under legal rules of evidence."),
        ("Out-of-Sequence", "Retrospective Entry Flag", "System safeguard identifying when a custody transfer event is recorded with an earlier timestamp than existing logged events."),
        ("Two-Person Rule", "Supervisory Separation of Duty", "Evidentiary protocol prohibiting the arresting or testing officer from approving their own case dossier without supervisor endorsement."),
        ("ORM", "Object-Relational Mapping", "Django abstraction translating relational database tables and foreign keys into Python class objects, preventing SQL injection."),
        ("CSRF", "Cross-Site Request Forgery", "Web security protection injecting cryptographic tokens into state-changing HTTP POST requests to prevent unauthorized cross-origin execution.")
    ]
    for r_idx, (t, f, d) in enumerate(terms):
        table.rows[r_idx + 1].cells[0].text = t
        table.rows[r_idx + 1].cells[1].text = f
        table.rows[r_idx + 1].cells[2].text = d

    format_table(table, [Inches(1.2), Inches(1.8), Inches(3.5)])

    add_heading_2(doc, "1.4 References")
    add_paragraph(doc, "The functional requirements and technical implementation described herein reference the authoritative standards, libraries, and legal guidelines listed below:")

    ref_table = doc.add_table(rows=6, cols=3)
    ref_headers = ["Document / Standard Title", "Publishing Body / Organization", "Standard Reference / Official URI"]
    for i, h in enumerate(ref_headers):
        ref_table.rows[0].cells[i].text = h
    
    refs = [
        ("Django Framework Documentation (v5.x)", "Django Software Foundation", "https://docs.djangoproject.com/en/5.0/"),
        ("Python Standard Library Reference (v3.12)", "Python Software Foundation", "https://docs.python.org/3.12/"),
        ("Color Test Reagents/Kits for Drugs of Abuse (NIJ Standard 0604.01)", "National Institute of Justice (U.S. DOJ)", "https://www.ojp.gov/pdffiles1/nij/183258.pdf"),
        ("Federal Rules of Evidence (Rule 901: Authenticating Evidence)", "Legal Information Institute (Cornell Law)", "https://www.law.cornell.edu/rules/fre/rule_901"),
        ("General Requirements for Competence of Testing Labs (ISO/IEC 17025)", "International Organization for Standardization", "https://www.iso.org/standard/67198.html")
    ]
    for r_idx, (tit, pub, uri) in enumerate(refs):
        ref_table.rows[r_idx + 1].cells[0].text = tit
        ref_table.rows[r_idx + 1].cells[1].text = pub
        ref_table.rows[r_idx + 1].cells[2].text = uri

    format_table(ref_table, [Inches(2.2), Inches(1.8), Inches(2.5)])

    add_heading_2(doc, "1.5 Overview")
    add_paragraph(doc, "The remainder of this specification is structured into authoritative sections aligned with the official report format:")
    add_bullet(doc, "Section 2 provides the General Description, detailing product perspective, functions, user characteristics, general constraints, and operational dependencies.", bold_prefix="General Description: ")
    add_bullet(doc, "Section 3 delivers Specific Requirements, detailing external interfaces, 16 individual functional requirements with complete input/processing/output/error specifications, and measurable non-functional requirements.", bold_prefix="Specific Requirements: ")
    add_bullet(doc, "Section 4 presents Analysis Models, including Level 0 and Level 1 Data Flow Diagrams, 4-tier MTV system architecture, complete relational entity-relationship diagrams, and operational workflows.", bold_prefix="Analysis Models: ")
    add_bullet(doc, "Sections 5 through 11 document project hosting, deployment links, institutional proofs, transaction records, and tax identifiers.", bold_prefix="Project Proofs: ")
    add_bullet(doc, "Appendices A.1 and A.2 provide environment configuration instructions and the automated test verification matrix demonstrating 100% test pass rates.", bold_prefix="Appendices: ")

    doc.add_page_break()

def build_section_2(doc):
    add_heading_1(doc, "2. General Description")
    add_paragraph(doc, "This section describes the overarching operational context, general factors, domain characteristics, and environmental constraints that govern FieldTest Companion. It establishes the conceptual foundation necessary to interpret the granular technical requirements articulated in Section 3.")

    add_heading_2(doc, "2.1 Product Perspective")
    add_paragraph(doc, "FieldTest Companion is a standalone, self-contained web platform engineered specifically for field investigation units, law enforcement precincts, and forensic liaison offices. Within the broader criminal justice information ecosystem, FieldTest Companion occupies the critical operational window between crime scene substance seizure and formal intake by an accredited forensic toxicology laboratory.")
    add_paragraph(doc, "Historically, this operational window relied entirely on handwritten field notebooks and physical evidence tags. FieldTest Companion digitizes this boundary layer by interfacing with field officers via modern web browsers on mobile devices, tablets, and laptops. While the system operates as an autonomous web application with its own relational database, it produces standardized data exports and court-ready forensic summary reports designed for seamless downstream ingest into state Laboratory Information Management Systems (LIMS).")

    add_heading_2(doc, "2.2 Product Functions")
    add_paragraph(doc, "The primary functions delivered by FieldTest Companion are modularized across 8 decoupled Django applications:")
    add_bullet(doc, "Centralized operational dashboard providing real-time metrics on active investigations, pending supervisory reviews, recent seizures, and quick-action navigation.", bold_prefix="1. Core Portal (core): ")
    add_bullet(doc, "Authentication, group role management (Field Officer, Supervisor, Administrator, Read-only User), and secure profile administration.", bold_prefix="2. Identity Management (accounts): ")
    add_bullet(doc, "Comprehensive incident cataloging, sequential reference generation (CASE-YYYY-XXXX), multi-criteria filtering, and sample management.", bold_prefix="3. Case & Dossier CRUD (cases): ")
    add_bullet(doc, "Physical specimen registration (SMP-YYYY-XXXX), tamper seal verification, packaging documentation, and initial condition assessment.", bold_prefix="4. Specimen Inventory (cases): ")
    add_bullet(doc, "Presumptive reagent kit catalog, lot number and expiration tracking, sensory color observation recording, and controlled result categorization.", bold_prefix="5. Field Testing Engine (testing_records): ")
    add_bullet(doc, "Append-only chronological custody ledger tracking physical possession transfers, storage lockers, and automated out-of-sequence retrospective flags.", bold_prefix="6. Chain of Custody (custody): ")
    add_bullet(doc, "Private evidence repository supporting photo and PDF attachments with MIME-type and size validation, accessible exclusively via authenticated streaming endpoints.", bold_prefix="7. Secure Evidence Vault (evidence): ")
    add_bullet(doc, "Two-person supervisory review queue, mandatory actionable feedback validation, approval/revision state machines, and permanent case record locking.", bold_prefix="8. Supervisory Governance (reviews): ")
    add_bullet(doc, "Silent chronological tracking of user authentication, case modifications, authorization denials, and system administrative actions with client IP capture.", bold_prefix="9. Security Audit Log (auditlog): ")

    add_heading_2(doc, "2.3 User Characteristics")
    add_paragraph(doc, "The platform is designed to accommodate four distinct user personas, each possessing defined operational responsibilities, technical skill levels, and authorization scopes:")

    user_table = doc.add_table(rows=5, cols=3)
    user_headers = ["User Role", "Operational Context & Technical Literacy", "System Authorization Scope"]
    for i, h in enumerate(user_headers):
        user_table.rows[0].cells[i].text = h
    
    users = [
        ("Field Officer", "Patrol officers and narcotics detectives operating in field cruisers, mobile command posts, and inspection stations. Basic to intermediate computer literacy; requires streamlined, high-contrast, mobile-friendly forms.", "Create cases; register physical samples; record field-test events; initiate custody transfers; upload evidence photos; submit cases for review. Prohibited from approving own cases or managing user accounts."),
        ("Supervisor", "Sergeants, lieutenants, and senior investigative leads operating in precinct offices. Intermediate technical literacy; requires rapid summary inspection, revision tools, and reporting utilities.", "Full inspection of precinct cases; access supervisory review queue; issue formal approvals; return cases with mandatory revision remarks; lock/unlock cases; generate official court-ready reports."),
        ("Administrator", "Agency IT specialists and system administrators. Advanced technical literacy; proficient in user provisioning, group permissions, and system maintenance.", "User account creation and role assignment; activate/deactivate accounts; manage test kit catalog entries; configure precinct parameters; inspect system-wide audit logs."),
        ("Read-Only User", "Compliance auditors, internal affairs investigators, prosecutors, and legal defense representatives. Intermediate legal literacy; requires uninhibited search and inspection capabilities without modification permissions.", "Read-only global inspection across cases, samples, test events, custody ledgers, evidence files, and security audit logs. Strictly prohibited from creating, updating, or deleting any data.")
    ]
    for r_idx, (role, ctx, scope) in enumerate(users):
        user_table.rows[r_idx + 1].cells[0].text = role
        user_table.rows[r_idx + 1].cells[1].text = ctx
        user_table.rows[r_idx + 1].cells[2].text = scope

    format_table(user_table, [Inches(1.2), Inches(2.0), Inches(3.3)])

    add_heading_2(doc, "2.4 General Constraints")
    add_paragraph(doc, "The design and implementation of FieldTest Companion are governed by several foundational constraints:")
    add_bullet(doc, "In strict adherence to safety standards and legal mandates, the application prohibits chemical formulation recipes, reagent manufacturing guidelines, and automated positive/negative chemical determinations. All field test outcomes must be labeled presumptive screening results.", bold_prefix="Statutory Forensic Constraints: ")
    add_bullet(doc, "Under the Two-Person Integrity Principle, the user who creates a case or records a test event is strictly prohibited from approving that case. Supervisory approval requires an independent authenticated user belonging to the Supervisor role group.", bold_prefix="Two-Person Integrity Rule: ")
    add_bullet(doc, "The software is engineered exclusively in Python 3.12 utilizing the Django 5.x framework, relying on Django's built-in Model-Template-View architectural patterns without external third-party proprietary frameworks.", bold_prefix="Architectural Framework Constraints: ")
    add_bullet(doc, "All evidence files must be saved outside the web root in private media directories and served solely through streaming views requiring active user session validation.", bold_prefix="Evidentiary Storage Restrictions: ")
    add_bullet(doc, "The interface must conform to responsive web standards (HTML5/CSS3/Bootstrap 5) and operate seamlessly across modern browsers (Google Chrome, Apple Safari, Mozilla Firefox, Microsoft Edge) without client-side native plugin dependencies.", bold_prefix="Client Browser Compatibility: ")

    add_heading_2(doc, "2.5 Assumptions and Dependencies")
    add_paragraph(doc, "The operational validity and runtime performance of FieldTest Companion assume the following technical dependencies:")
    add_bullet(doc, "The server environment maintains an active Python 3.10+ execution environment with the Django framework and required dependencies installed as defined in requirements.txt.", bold_prefix="Python Runtime: ")
    add_bullet(doc, "The application utilizes SQLite 3 for local development and automated testing, and supports PostgreSQL 14+ for enterprise production deployment via Django ORM configuration.", bold_prefix="Relational Persistence: ")
    add_bullet(doc, "The host operating system must grant read and write filesystem permissions to the dedicated media/evidence directory for secure evidence document storage.", bold_prefix="Filesystem Storage Permissions: ")
    add_bullet(doc, "System clocks on the application host must be synchronized via Network Time Protocol (NTP) to guarantee chronological timestamp integrity for chain of custody and audit records.", bold_prefix="Time Synchronization: ")
    add_bullet(doc, "Field devices require TCP/IP network connectivity via mobile data (4G/5G) or Wi-Fi to synchronize field records with the central Django server.", bold_prefix="Network Infrastructure: ")

    doc.add_page_break()
