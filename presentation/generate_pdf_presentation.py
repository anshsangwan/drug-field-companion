"""
Generates high-fidelity HTML slide deck and compiles FieldTest_Companion_Presentation.pdf
using headless Google Chrome.
"""

import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "presentation", "screenshots")
HTML_OUT = os.path.join(BASE_DIR, "presentation", "slides.html")
PDF_OUT = os.path.join(BASE_DIR, "FieldTest_Companion_Presentation.pdf")
PROFILE_DIR = os.path.join(BASE_DIR, "presentation", "chrome_profile")
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Helper for absolute file URI for screenshots
def img_uri(name):
    p = os.path.join(SCREENSHOTS_DIR, name)
    return f"file://{p}" if os.path.exists(p) else ""

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>FieldTest Companion - Project Presentation</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  @page {{
    size: 13.333in 7.5in;
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: #090d16;
    color: #cbd5e1;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .slide {{
    width: 13.333in;
    height: 7.5in;
    max-width: 13.333in;
    max-height: 7.5in;
    position: relative;
    background-color: #0f172a;
    padding: 0.45in 0.8in 0.4in 0.8in;
    overflow: hidden;
    page-break-after: always;
    display: flex;
    flex-direction: column;
  }}

  /* Header */
  .slide-header {{
    border-bottom: 2px solid #334155;
    padding-bottom: 0.12in;
    margin-bottom: 0.22in;
    flex-shrink: 0;
  }}
  .category-tag {{
    font-size: 0.13in;
    font-weight: 700;
    text-transform: uppercase;
    color: #38bdf8;
    letter-spacing: 0.06em;
    margin-bottom: 0.04in;
  }}
  .slide-title {{
    font-size: 0.28in;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
  }}

  /* Footer */
  .slide-footer {{
    margin-top: auto;
    padding-top: 0.1in;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.12in;
    color: #64748b;
    border-top: 1px solid #1e293b;
    flex-shrink: 0;
  }}

  /* Cards & Grid Containers */
  .card {{
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 0.1in;
    padding: 0.18in 0.22in;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }}
  .card-title {{
    font-size: 0.16in;
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 0.08in;
    display: flex;
    align-items: center;
    gap: 0.08in;
  }}

  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.22in;
    flex-grow: 1;
  }}
  .grid-3 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.2in;
    flex-grow: 1;
  }}
  .grid-4 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 0.18in;
    flex-grow: 1;
  }}

  /* Typography */
  h1, h2, h3, h4 {{ color: #ffffff; }}
  p {{ font-size: 0.14in; line-height: 1.45; color: #cbd5e1; }}
  ul {{ list-style: none; }}
  li {{ font-size: 0.13in; line-height: 1.45; margin-bottom: 0.08in; color: #cbd5e1; }}
  li strong {{ color: #ffffff; }}
  code {{ font-family: 'JetBrains Mono', monospace; background: #0f172a; padding: 0.02in 0.05in; border-radius: 0.03in; color: #38bdf8; font-size: 0.12in; }}

  /* Badges */
  .badge {{
    display: inline-block;
    padding: 0.04in 0.08in;
    border-radius: 0.05in;
    font-size: 0.11in;
    font-weight: 700;
    text-transform: uppercase;
  }}
  .badge-blue {{ background: #2563eb; color: #ffffff; }}
  .badge-cyan {{ background: #0284c7; color: #ffffff; }}
  .badge-green {{ background: #059669; color: #ffffff; }}
  .badge-amber {{ background: #d97706; color: #ffffff; }}
  .badge-red {{ background: #dc2626; color: #ffffff; }}
  .badge-outline {{ border: 1px solid #475569; color: #94a3b8; }}

  /* Flowchart node */
  .flow-node {{
    background: #1e293b;
    border: 1.5px solid #38bdf8;
    border-radius: 0.08in;
    padding: 0.12in;
    text-align: center;
    position: relative;
  }}
  .flow-arrow {{
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.22in;
    color: #38bdf8;
    font-weight: bold;
  }}

  /* Image Container */
  .screenshot-box {{
    border-radius: 0.08in;
    overflow: hidden;
    border: 1px solid #334155;
    background: #0b0f19;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  }}
  .screenshot-box img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
</style>
</head>
<body>

<!-- SLIDE 1: TITLE SLIDE -->
<div class="slide" style="justify-content: center; align-items: center; background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);">
  <div style="background: rgba(30, 41, 59, 0.7); border: 2px solid #334155; border-radius: 0.16in; padding: 0.5in 0.8in; width: 11.5in; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
    <span class="badge badge-blue" style="font-size: 0.14in; padding: 0.06in 0.15in; margin-bottom: 0.2in;">INT253: WEB DEVELOPMENT IN PYTHON USING DJANGO</span>
    <h1 style="font-size: 0.52in; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.08in; color: #ffffff;">FieldTest Companion</h1>
    <h2 style="font-size: 0.26in; font-weight: 700; color: #38bdf8; margin-bottom: 0.25in;">Digital Companion for Drug Field Testing (DCDFT)</h2>
    <p style="font-size: 0.16in; color: #cbd5e1; max-width: 9.5in; margin: 0 auto 0.35in auto; line-height: 1.5;">
      A comprehensive forensic web platform providing structured case management, tamper-evident specimen registration, presumptive test documentation, append-only chain of custody, private evidence storage, and supervisory review workflows.
    </p>

    <div style="display: flex; justify-content: center; gap: 0.35in; text-align: left;">
      <div class="card" style="padding: 0.15in 0.25in; width: 4.5in;">
        <div style="font-size: 0.11in; font-weight: 700; color: #38bdf8; text-transform: uppercase;">Student & Course Metadata</div>
        <div style="font-size: 0.17in; font-weight: 700; color: #ffffff; margin-top: 0.04in;">Ansh Sangwan</div>
        <div style="font-size: 0.13in; color: #94a3b8; margin-top: 0.02in;">Course: INT253 • University Project Viva Evaluation</div>
      </div>
      <div class="card" style="padding: 0.15in 0.25in; width: 4.5in;">
        <div style="font-size: 0.11in; font-weight: 700; color: #38bdf8; text-transform: uppercase;">Technical Implementation</div>
        <div style="font-size: 0.15in; font-weight: 700; color: #ffffff; margin-top: 0.04in;">Django 5.0.2 • Python 3.12 • SQLite</div>
        <div style="font-size: 0.13in; color: #10b981; margin-top: 0.02in;">✓ 20 Automated Tests Passing (AT-01 to AT-15)</div>
      </div>
    </div>
  </div>
  <div class="slide-footer" style="width: 100%; position: absolute; bottom: 0.3in; left: 0; padding: 0 0.8in; border: none;">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>1 / 15</div>
  </div>
</div>

<!-- SLIDE 2: INTRODUCTION -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">Project Background & Operational Context</div>
    <div class="slide-title">Introduction to Field Drug Testing Documentation</div>
  </div>

  <div class="grid-2">
    <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
      <div>
        <div class="card-title">What is Field Drug Testing?</div>
        <p style="margin-bottom: 0.14in;">
          Field drug testing involves presumptive screening kits (colorimetric chemical ampoules and reagent test strips) deployed by authorized officers during roadside vehicle stops, seaport container inspections, and crime scene seizures.
        </p>

        <div class="card-title" style="margin-top: 0.15in;">Why Digital Documentation is Critical</div>
        <ul>
          <li><strong>Evidentiary Admissibility:</strong> A single missing timestamp or unverified seal can invalidate physical evidence in judicial proceedings.</li>
          <li><strong>Paper Vulnerability:</strong> Handwritten forms are prone to water damage, illegible handwriting, conflicting notes, and lost pages.</li>
          <li><strong>Institutional Accountability:</strong> Digital companions provide immutable audit logs, officer attribution, and mandatory supervisor review gates.</li>
        </ul>
      </div>

      <div style="background: rgba(245, 158, 11, 0.12); border-left: 4px solid #f59e0b; padding: 0.12in; border-radius: 0.05in;">
        <div style="font-size: 0.13in; font-weight: 700; color: #f59e0b; margin-bottom: 0.02in;">⚠️ MANDATORY FORENSIC SCOPE NOTICE</div>
        <div style="font-size: 0.115in; color: #fde68a;">
          Field-test outcomes are presumptive screening results only. They do not establish definitive chemical identity. Confirmatory laboratory analysis (GC-MS / FTIR) is legally required.
        </div>
      </div>
    </div>

    <div style="display: flex; flex-direction: column; gap: 0.18in;">
      <div class="card" style="flex: 1;">
        <div class="card-title">Portal Interface Overview</div>
        <p style="font-size: 0.12in; color: #94a3b8; margin-bottom: 0.08in;">
          Clean, authoritative landing interface communicating legal scope, role boundaries, and direct portal access.
        </p>
        <div class="screenshot-box" style="height: 3.2in;">
          <img src="{img_uri('landing.png')}" alt="Landing Portal">
        </div>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>2 / 15</div>
  </div>
</div>

<!-- SLIDE 3: PROBLEM STATEMENT -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">Problem Statement & Industry Gaps</div>
    <div class="slide-title">Vulnerabilities in Conventional Field Documentation</div>
  </div>

  <div class="card" style="margin-bottom: 0.22in; padding: 0.14in 0.2in;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.18in;">
      <div>
        <li style="margin-bottom: 0.06in;"><strong>1. Paper-Based Fragmentation:</strong> Notes spread across notebooks, loose forms, and locker logs.</li>
        <li style="margin-bottom: 0.06in;"><strong>2. Sample Traceability Gaps:</strong> Inability to verify which officer secured or transferred which bag.</li>
        <li style="margin-bottom: 0.06in;"><strong>3. Unnoticed Kit Expiration:</strong> Tests executed on expired lots invalidate legal admissibility.</li>
      </div>
      <div>
        <li style="margin-bottom: 0.06in;"><strong>4. Chain-of-Custody Breaches:</strong> Retrospective entries entered without sequence verification.</li>
        <li style="margin-bottom: 0.06in;"><strong>5. Delayed Supervisory Review:</strong> Hand-compiled dossiers delay lab submissions for days.</li>
        <li style="margin-bottom: 0.06in;"><strong>6. Unprotected Evidence Files:</strong> Scene photos shared over unsecured channels without access controls.</li>
      </div>
    </div>
  </div>

  <div class="card" style="flex-grow: 1; display: flex; flex-direction: column;">
    <div class="card-title" style="margin-bottom: 0.15in;">The Cascading Failure Flow of Manual Record-Keeping</div>

    <div style="display: flex; align-items: center; justify-content: space-between; flex-grow: 1; padding: 0 0.2in;">
      <div class="flow-node" style="width: 2.0in; border-color: #ef4444;">
        <span class="badge badge-red" style="margin-bottom: 0.05in;">Stage 1</span>
        <div style="font-size: 0.14in; font-weight: 700; color: #fff;">Manual Records</div>
        <div style="font-size: 0.11in; color: #94a3b8; margin-top: 0.04in;">Handwritten notes on scene during field arrests</div>
      </div>

      <div class="flow-arrow">➔</div>

      <div class="flow-node" style="width: 2.0in; border-color: #f59e0b;">
        <span class="badge badge-amber" style="margin-bottom: 0.05in;">Stage 2</span>
        <div style="font-size: 0.14in; font-weight: 700; color: #fff;">Fragmented Logs</div>
        <div style="font-size: 0.11in; color: #94a3b8; margin-top: 0.04in;">Dispersed logs across multiple patrol cars & lockers</div>
      </div>

      <div class="flow-arrow">➔</div>

      <div class="flow-node" style="width: 2.0in; border-color: #f59e0b;">
        <span class="badge badge-amber" style="margin-bottom: 0.05in;">Stage 3</span>
        <div style="font-size: 0.14in; font-weight: 700; color: #fff;">Tracking Gaps</div>
        <div style="font-size: 0.11in; color: #94a3b8; margin-top: 0.04in;">Unclear custody possession, missing seal numbers</div>
      </div>

      <div class="flow-arrow">➔</div>

      <div class="flow-node" style="width: 2.0in; border-color: #ef4444;">
        <span class="badge badge-red" style="margin-bottom: 0.05in;">Stage 4</span>
        <div style="font-size: 0.14in; font-weight: 700; color: #fff;">Zero Traceability</div>
        <div style="font-size: 0.11in; color: #94a3b8; margin-top: 0.04in;">Lack of audit trail; conflicting officer timestamps</div>
      </div>

      <div class="flow-arrow">➔</div>

      <div class="flow-node" style="width: 2.0in; border-color: #ef4444;">
        <span class="badge badge-red" style="margin-bottom: 0.05in;">Stage 5</span>
        <div style="font-size: 0.14in; font-weight: 700; color: #fff;">Case Dismissed</div>
        <div style="font-size: 0.11in; color: #94a3b8; margin-top: 0.04in;">Evidence suppressed in court due to broken custody</div>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>3 / 15</div>
  </div>
</div>

<!-- SLIDE 4: PROPOSED SOLUTION -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">Proposed Solution & Core Capabilities</div>
    <div class="slide-title">FieldTest Companion: Feature Map</div>
  </div>

  <div class="grid-2">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.15in;">
      <div class="card">
        <div class="card-title">📁 Case Management</div>
        <p style="font-size: 0.12in;">Auto-generated sequential <code>CASE-YYYY-XXXX</code> refs, status state machine, search and filters.</p>
      </div>
      <div class="card">
        <div class="card-title">🧪 Sample Registration</div>
        <p style="font-size: 0.12in;">Unique <code>SMP-YYYY-XXXX</code> codes, condition, tamper-seal tracking, duplicate prevention.</p>
      </div>
      <div class="card">
        <div class="card-title">🔬 Test Documentation</div>
        <p style="font-size: 0.12in;">Kit catalogue metadata, lot expiry validation, controlled 5-result presumptive categories.</p>
      </div>
      <div class="card">
        <div class="card-title">🔗 Chain of Custody</div>
        <p style="font-size: 0.12in;">Append-only transfer ledger, storage references, automated out-of-sequence flags.</p>
      </div>
      <div class="card">
        <div class="card-title">🛡️ Private Evidence Vault</div>
        <p style="font-size: 0.12in;">MIME/size validated image and PDF uploads served strictly via authenticated FileResponse.</p>
      </div>
      <div class="card">
        <div class="card-title">📋 Supervisor Review</div>
        <p style="font-size: 0.12in;">Dedicated queue, formal approvals, or revision requests with mandatory written comments.</p>
      </div>
      <div class="card">
        <div class="card-title">🖨️ Summary Reports</div>
        <p style="font-size: 0.12in;">Print-ready forensic summary reports with specimen ledgers and dual-signature blocks.</p>
      </div>
      <div class="card">
        <div class="card-title">👥 Role-Based Access</div>
        <p style="font-size: 0.12in;">Field Officer, Supervisor, Admin, and Read-only roles enforced in Python view decorators.</p>
      </div>
    </div>

    <div class="card" style="display: flex; flex-direction: column;">
      <div class="card-title">Live Application Dashboard Overview</div>
      <p style="font-size: 0.12in; color: #94a3b8; margin-bottom: 0.08in;">
        Centralized operational hub displaying case counts, active investigations, sample inventory, pending review queues, and real-time audit logs.
      </p>
      <div class="screenshot-box" style="flex-grow: 1;">
        <img src="{img_uri('dashboard.png')}" alt="Live Dashboard">
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>4 / 15</div>
  </div>
</div>

<!-- SLIDE 5: SYSTEM WORKFLOW -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">End-to-End System Execution Flow</div>
    <div class="slide-title">Case-to-Review Operational Workflow</div>
  </div>

  <div class="card" style="flex-grow: 1; padding: 0.25in; display: flex; flex-direction: column; justify-content: space-between;">
    <!-- Step Row 1 -->
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <div class="flow-node" style="width: 2.1in;">
        <div class="badge badge-blue" style="margin-bottom: 0.04in;">Step 1</div>
        <div style="font-size: 0.13in; font-weight: 700; color: #fff;">Field Officer Login</div>
        <div style="font-size: 0.105in; color: #94a3b8;">Auth via session cookies</div>
      </div>
      <div class="flow-arrow">➔</div>
      <div class="flow-node" style="width: 2.1in;">
        <div class="badge badge-blue" style="margin-bottom: 0.04in;">Step 2</div>
        <div style="font-size: 0.13in; font-weight: 700; color: #fff;">Create Case Record</div>
        <div style="font-size: 0.105in; color: #94a3b8;">Generates CASE-YYYY-XXXX</div>
      </div>
      <div class="flow-arrow">➔</div>
      <div class="flow-node" style="width: 2.1in;">
        <div class="badge badge-blue" style="margin-bottom: 0.04in;">Step 3</div>
        <div style="font-size: 0.13in; font-weight: 700; color: #fff;">Register Samples</div>
        <div style="font-size: 0.105in; color: #94a3b8;">Seal ref & initial condition</div>
      </div>
      <div class="flow-arrow">➔</div>
      <div class="flow-node" style="width: 2.1in;">
        <div class="badge badge-blue" style="margin-bottom: 0.04in;">Step 4</div>
        <div style="font-size: 0.13in; font-weight: 700; color: #fff;">Document Test Event</div>
        <div style="font-size: 0.105in; color: #94a3b8;">Kit lot, expiry & outcome</div>
      </div>
      <div class="flow-arrow">➔</div>
      <div class="flow-node" style="width: 2.1in;">
        <div class="badge badge-blue" style="margin-bottom: 0.04in;">Step 5</div>
        <div style="font-size: 0.13in; font-weight: 700; color: #fff;">Log Custody & Files</div>
        <div style="font-size: 0.105in; color: #94a3b8;">Transfers & photo vault</div>
      </div>
    </div>

    <!-- Connector down -->
    <div style="display: flex; justify-content: flex-end; padding-right: 0.9in; font-size: 0.2in; color: #38bdf8;">
      ↓
    </div>

    <!-- Step Row 2: Submit, Review & Decision Branches -->
    <div style="display: flex; align-items: center; justify-content: space-between;">
      <!-- Branch A: Approved -->
      <div class="flow-node" style="width: 3.2in; border-color: #10b981; background: rgba(16, 185, 129, 0.1);">
        <span class="badge badge-green" style="margin-bottom: 0.04in;">Branch A: Approved</span>
        <div style="font-size: 0.14in; font-weight: 800; color: #10b981;">Endorsement & Report</div>
        <div style="font-size: 0.11in; color: #cbd5e1; margin-top: 0.04in;">
          Case permanently locked. Authorizes Print-Ready Case Report & lab dispatch.
        </div>
      </div>

      <div class="flow-arrow" style="color: #10b981;">🡸 [Approved]</div>

      <!-- Decision Node -->
      <div class="flow-node" style="width: 3.0in; border-color: #f59e0b; border-width: 2px;">
        <span class="badge badge-amber" style="margin-bottom: 0.04in;">Step 7: Verification Gate</span>
        <div style="font-size: 0.15in; font-weight: 800; color: #f59e0b;">Supervisor Decision</div>
        <div style="font-size: 0.11in; color: #94a3b8; margin-top: 0.04in;">
          Examines test validity, lot dates & custody continuity.
        </div>
      </div>

      <div class="flow-arrow">🡸</div>

      <!-- Step 6 Submit -->
      <div class="flow-node" style="width: 2.8in; border-color: #2563eb;">
        <span class="badge badge-blue" style="margin-bottom: 0.04in;">Step 6: Submit Dossier</span>
        <div style="font-size: 0.14in; font-weight: 700; color: #fff;">POST /submit/</div>
        <div style="font-size: 0.11in; color: #94a3b8; margin-top: 0.04in;">
          Status ➔ Submitted. Locks officer editing.
        </div>
      </div>
    </div>

    <!-- Branch B: Changes Requested -->
    <div style="display: flex; justify-content: center; margin-top: 0.1in;">
      <div class="flow-node" style="width: 8.5in; border-color: #ef4444; background: rgba(239, 68, 68, 0.1); padding: 0.1in 0.2in;">
        <span class="badge badge-red" style="margin-right: 0.1in;">Branch B: Changes Requested</span>
        <strong style="color: #ffffff; font-size: 0.125in;">Mandatory Comment Enforced:</strong>
        <span style="font-size: 0.12in; color: #cbd5e1;"> Supervisor returns case with required actionable revision notes. Case unlocks for officer correction and resubmission.</span>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>5 / 15</div>
  </div>
</div>

<!-- SLIDE 6: USER ROLES & ACCESS CONTROL -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">Role-Based Access Control (RBAC)</div>
    <div class="slide-title">Four-Tier User Role Governance</div>
  </div>

  <div class="grid-4" style="margin-bottom: 0.2in;">
    <div class="card" style="border-color: #2563eb;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.1in;">
        <div style="font-size: 0.16in; font-weight: 700; color: #ffffff;">Field Officer</div>
        <span class="badge badge-blue">On-Scene</span>
      </div>
      <ul>
        <li>• Authenticate via username/pwd.</li>
        <li>• Create new case dossiers.</li>
        <li>• Register physical samples.</li>
        <li>• Document presumptive tests.</li>
        <li>• Maintain append-only custody.</li>
        <li>• Upload permitted evidence.</li>
        <li>• Submit cases for review.</li>
        <li><strong style="color:#ef4444;">✗ Cannot approve or edit locked cases.</strong></li>
      </ul>
    </div>

    <div class="card" style="border-color: #f59e0b;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.1in;">
        <div style="font-size: 0.16in; font-weight: 700; color: #ffffff;">Supervisor</div>
        <span class="badge badge-amber">Verification</span>
      </div>
      <ul>
        <li>• View assigned/submitted cases.</li>
        <li>• Access supervisory review queue.</li>
        <li>• Formally approve documentation.</li>
        <li>• Return cases with mandatory notes.</li>
        <li>• Access official summary reports.</li>
        <li>• Manage kit catalogue metadata.</li>
        <li>• Inspect case audit trails.</li>
        <li><strong style="color:#ef4444;">✗ Cannot manage user accounts.</strong></li>
      </ul>
    </div>

    <div class="card" style="border-color: #ef4444;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.1in;">
        <div style="font-size: 0.16in; font-weight: 700; color: #ffffff;">Administrator</div>
        <span class="badge badge-red">Governance</span>
      </div>
      <ul>
        <li>• Create & manage user credentials.</li>
        <li>• Assign Django groups & roles.</li>
        <li>• Activate or deactivate personnel.</li>
        <li>• Manage test-kit catalogue entries.</li>
        <li>• Inspect system-wide audit logs.</li>
        <li>• Full access to Django Admin.</li>
        <li>• Override case status if necessary.</li>
        <li><strong style="color:#10b981;">✓ Full administrative purview.</strong></li>
      </ul>
    </div>

    <div class="card" style="border-color: #64748b;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.1in;">
        <div style="font-size: 0.16in; font-weight: 700; color: #ffffff;">Read-only User</div>
        <span class="badge badge-outline">Auditing</span>
      </div>
      <ul>
        <li>• View permitted case records.</li>
        <li>• Inspect sample details & tests.</li>
        <li>• Review custody timeline.</li>
        <li>• View printable case reports.</li>
        <li>• Inspect authorized audit trails.</li>
        <li><strong style="color:#ef4444;">✗ Cannot create or edit cases.</strong></li>
        <li><strong style="color:#ef4444;">✗ Cannot record tests or custody.</strong></li>
        <li><strong style="color:#ef4444;">✗ Cannot approve or reject cases.</strong></li>
      </ul>
    </div>
  </div>

  <div class="card" style="padding: 0.12in 0.2in;">
    <div style="font-size: 0.13in; color: #38bdf8; font-weight: 700;">Backend Enforcement Mechanism:</div>
    <div style="font-size: 0.12in; color: #cbd5e1; margin-top: 0.03in;">
      Permissions are enforced at the view layer using Django Groups and Python decorators (<code>@role_required</code>, <code>@supervisor_required</code>, <code>@field_officer_required</code>). Unauthorized direct URL access immediately triggers an HTTP 403 <code>PermissionDenied</code> exception.
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>6 / 15</div>
  </div>
</div>

<!-- SLIDE 7: SYSTEM ARCHITECTURE -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">Full-Stack Technical Design</div>
    <div class="slide-title">Four-Tier System Architecture & Request Lifecycle</div>
  </div>

  <div style="display: flex; flex-direction: column; gap: 0.14in; flex-grow: 1;">
    <div class="card" style="border-left: 5px solid #2563eb; padding: 0.14in 0.2in;">
      <div style="display: flex; justify-content: space-between;">
        <div style="font-size: 0.15in; font-weight: 700; color: #ffffff;">1. Presentation Layer (Client Tier)</div>
        <span class="badge badge-blue">HTML5 • Bootstrap 5.3.3 • Forensic CSS • ES6 JS</span>
      </div>
      <p style="font-size: 0.125in; margin-top: 0.04in;">
        Renders responsive forensic interface, dark navy sidebar, live status badges, vertical custody timelines, and print-ready summary reports.
      </p>
    </div>

    <div style="text-align: center; color: #38bdf8; font-weight: bold; font-size: 0.18in; margin: -0.06in 0;">↓</div>

    <div class="card" style="border-left: 5px solid #0284c7; padding: 0.14in 0.2in;">
      <div style="display: flex; justify-content: space-between;">
        <div style="font-size: 0.15in; font-weight: 700; color: #ffffff;">2. Application & Logic Tier (Django Core)</div>
        <span class="badge badge-cyan">URL Routing • Views • Forms • Security Middleware</span>
      </div>
      <p style="font-size: 0.125in; margin-top: 0.04in;">
        Processes requests via named URL routes, executes GET/POST view logic, enforces CSRF token validation, runs ModelForms validation, and handles HTTP 403/404 errors.
      </p>
    </div>

    <div style="text-align: center; color: #38bdf8; font-weight: bold; font-size: 0.18in; margin: -0.06in 0;">↓</div>

    <div class="card" style="border-left: 5px solid #38bdf8; padding: 0.14in 0.2in;">
      <div style="display: flex; justify-content: space-between;">
        <div style="font-size: 0.15in; font-weight: 700; color: #ffffff;">3. Domain Application Services Tier</div>
        <span class="badge badge-outline">8 Decoupled Django Modular Apps</span>
      </div>
      <p style="font-size: 0.125in; margin-top: 0.04in;">
        Decoupled domain handlers: <code>core</code>, <code>accounts</code>, <code>cases</code>, <code>testing_records</code>, <code>custody</code>, <code>evidence</code>, <code>reviews</code>, and <code>auditlog</code>.
      </p>
    </div>

    <div style="text-align: center; color: #38bdf8; font-weight: bold; font-size: 0.18in; margin: -0.06in 0;">↓</div>

    <div class="card" style="border-left: 5px solid #10b981; padding: 0.14in 0.2in;">
      <div style="display: flex; justify-content: space-between;">
        <div style="font-size: 0.15in; font-weight: 700; color: #ffffff;">4. Data Persistence & File Vault Tier</div>
        <span class="badge badge-green">Django ORM • SQLite • Private Evidence Vault</span>
      </div>
      <p style="font-size: 0.125in; margin-top: 0.04in;">
        Relational SQLite database managed via ORM migrations with ForeignKeys (PROTECT / CASCADE). Evidence files stored securely in private filesystem directory (no public URLs).
      </p>
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>7 / 15</div>
  </div>
</div>

<!-- SLIDE 8: DJANGO APPLICATION STRUCTURE -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">Modular Architecture Breakdown</div>
    <div class="slide-title">Eight Specialized Django Applications</div>
  </div>

  <div class="grid-4" style="margin-bottom: 0.2in;">
    <div class="card">
      <div class="card-title">app: core</div>
      <p style="font-size: 0.115in;">Dashboard KPIs, landing portal, 403/404/500 handlers, and the <code>load_demo_data</code> management command.</p>
    </div>
    <div class="card">
      <div class="card-title">app: accounts</div>
      <p style="font-size: 0.115in;">Authentication, session handling, 4 RBAC groups, view decorators, and administrative user controls.</p>
    </div>
    <div class="card">
      <div class="card-title">app: cases</div>
      <p style="font-size: 0.115in;"><code>CaseRecord</code> & <code>Sample</code> models, sequential ref generator, search/filters, and report view.</p>
    </div>
    <div class="card">
      <div class="card-title">app: testing_records</div>
      <p style="font-size: 0.115in;"><code>TestKit</code> catalogue metadata, <code>TestEvent</code> logging, lot expiry validation & disclaimers.</p>
    </div>
    <div class="card">
      <div class="card-title">app: custody</div>
      <p style="font-size: 0.115in;"><code>CustodyEvent</code> append-only ledger, transfers, storage, and automated out-of-sequence flags.</p>
    </div>
    <div class="card">
      <div class="card-title">app: evidence</div>
      <p style="font-size: 0.115in;"><code>EvidenceFile</code> model, MIME whitelist, size checks, and authenticated FileResponse delivery.</p>
    </div>
    <div class="card">
      <div class="card-title">app: reviews</div>
      <p style="font-size: 0.115in;"><code>ReviewRecord</code> workflow, supervisory review queue, and mandatory actionable revision comments.</p>
    </div>
    <div class="card">
      <div class="card-title">app: auditlog</div>
      <p style="font-size: 0.115in;"><code>AuditEvent</code> immutable ledger tracking actor, action type, target object, client IP & timestamps.</p>
    </div>
  </div>

  <div class="card" style="padding: 0.15in 0.25in;">
    <div style="font-size: 0.13in; color: #38bdf8; font-weight: 700; margin-bottom: 0.04in;">Why Decompose into Eight Modular Apps?</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.2in; font-size: 0.12in; color: #cbd5e1;">
      <div><strong>Separation of Concerns:</strong> Isolates custody rules from testing documentation, avoiding bloated multi-thousand line files.</div>
      <div><strong>Independent Testing:</strong> Each application possesses dedicated unit tests, making automated test suites fast and deterministic.</div>
      <div><strong>High Reusability:</strong> The <code>auditlog</code> and <code>evidence</code> modules can be dropped into future forensic projects without modification.</div>
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>8 / 15</div>
  </div>
</div>

<!-- SLIDE 9: DATABASE DESIGN & ERD -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">Relational Database Modeling</div>
    <div class="slide-title">Entity Relationship Diagram (ERD) & Constraints</div>
  </div>

  <div class="card" style="flex-grow: 1; padding: 0.2in; display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 0.15in;">
    <!-- Column 1: Auth & Reviews -->
    <div style="display: flex; flex-direction: column; gap: 0.15in;">
      <div class="card" style="border-color: #2563eb; background: #0f172a;">
        <div style="font-size: 0.13in; font-weight: 700; color: #38bdf8;">User (auth.User)</div>
        <div style="font-size: 0.105in; color: #94a3b8; margin-top: 0.04in;">
          • PK id (Integer)<br>
          • username, email<br>
          • is_staff, is_active<br>
          • ManyToMany: groups
        </div>
      </div>
      <div class="card" style="border-color: #f59e0b; background: #0f172a;">
        <div style="font-size: 0.13in; font-weight: 700; color: #f59e0b;">ReviewRecord</div>
        <div style="font-size: 0.105in; color: #94a3b8; margin-top: 0.04in;">
          • PK id (BigAutoField)<br>
          • decision (Approved/Changes)<br>
          • comment (TextField)<br>
          • reviewed_at (DateTime)<br>
          • <strong style="color:#fff;">FK case -> CaseRecord</strong><br>
          • <strong style="color:#fff;">FK reviewer -> User</strong>
        </div>
      </div>
    </div>

    <!-- Column 2: CaseRecord & EvidenceFile -->
    <div style="display: flex; flex-direction: column; gap: 0.15in;">
      <div class="card" style="border-color: #0284c7; background: #0f172a;">
        <div style="font-size: 0.13in; font-weight: 700; color: #38bdf8;">CaseRecord</div>
        <div style="font-size: 0.105in; color: #94a3b8; margin-top: 0.04in;">
          • PK id (BigAutoField)<br>
          • <strong>case_reference (Unique)</strong><br>
          • title, incident_datetime<br>
          • general_location, description<br>
          • status (Draft..Approved)<br>
          • <strong style="color:#fff;">FK created_by -> User (PROTECT)</strong><br>
          • <strong style="color:#fff;">FK assigned_to -> User (SET_NULL)</strong>
        </div>
      </div>
      <div class="card" style="border-color: #38bdf8; background: #0f172a;">
        <div style="font-size: 0.13in; font-weight: 700; color: #38bdf8;">EvidenceFile</div>
        <div style="font-size: 0.105in; color: #94a3b8; margin-top: 0.04in;">
          • PK id (BigAutoField)<br>
          • file (FileField - Private Vault)<br>
          • original_filename, size<br>
          • content_type, caption<br>
          • <strong style="color:#fff;">FK case -> CaseRecord</strong><br>
          • <strong style="color:#fff;">FK sample -> Sample (Optional)</strong><br>
          • <strong style="color:#fff;">FK uploaded_by -> User</strong>
        </div>
      </div>
    </div>

    <!-- Column 3: Sample & CustodyEvent -->
    <div style="display: flex; flex-direction: column; gap: 0.15in;">
      <div class="card" style="border-color: #10b981; background: #0f172a;">
        <div style="font-size: 0.13in; font-weight: 700; color: #10b981;">Sample</div>
        <div style="font-size: 0.105in; color: #94a3b8; margin-top: 0.04in;">
          • PK id (BigAutoField)<br>
          • <strong>sample_code (Unique)</strong><br>
          • collected_at, description<br>
          • packaging_reference<br>
          • seal_reference, condition<br>
          • <strong style="color:#fff;">FK case -> CaseRecord (CASCADE)</strong><br>
          • <strong style="color:#fff;">FK created_by -> User</strong>
        </div>
      </div>
      <div class="card" style="border-color: #ef4444; background: #0f172a;">
        <div style="font-size: 0.13in; font-weight: 700; color: #ef4444;">CustodyEvent</div>
        <div style="font-size: 0.105in; color: #94a3b8; margin-top: 0.04in;">
          • PK id (BigAutoField)<br>
          • event_type, event_at<br>
          • from_person, to_person<br>
          • location_reference, seal_ref<br>
          • <strong>is_out_of_sequence (Boolean)</strong><br>
          • <strong style="color:#fff;">FK sample -> Sample</strong><br>
          • <strong style="color:#fff;">FK recorded_by -> User</strong>
        </div>
      </div>
    </div>

    <!-- Column 4: TestKit & TestEvent -->
    <div style="display: flex; flex-direction: column; gap: 0.15in;">
      <div class="card" style="border-color: #f59e0b; background: #0f172a;">
        <div style="font-size: 0.13in; font-weight: 700; color: #f59e0b;">TestKit</div>
        <div style="font-size: 0.105in; color: #94a3b8; margin-top: 0.04in;">
          • PK id (BigAutoField)<br>
          • name, manufacturer, category<br>
          • <strong>catalogue_reference (Unique)</strong><br>
          • active (Boolean)<br>
          • general_safety_note
        </div>
      </div>
      <div class="card" style="border-color: #0284c7; background: #0f172a;">
        <div style="font-size: 0.13in; font-weight: 700; color: #38bdf8;">TestEvent</div>
        <div style="font-size: 0.105in; color: #94a3b8; margin-top: 0.04in;">
          • PK id (BigAutoField)<br>
          • result_category (5 Choices)<br>
          • kit_lot_number, expiry_date<br>
          • performed_at, observations<br>
          • limitations_note<br>
          • <strong style="color:#fff;">FK sample -> Sample</strong><br>
          • <strong style="color:#fff;">FK kit -> TestKit (PROTECT)</strong><br>
          • <strong style="color:#fff;">FK performed_by -> User</strong>
        </div>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>9 / 15</div>
  </div>
</div>

<!-- SLIDE 10: CORE FUNCTIONAL MODULES -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">Implementation Details & Screenshots</div>
    <div class="slide-title">Core Operational Modules in Action</div>
  </div>

  <div class="grid-2">
    <!-- Module 1: Case Management -->
    <div class="card" style="display: flex; flex-direction: column;">
      <div class="card-title">1. Case Management & Filtering</div>
      <p style="font-size: 0.115in; margin-bottom: 0.06in;">
        Sequential case reference generator (<code>CASE-YYYY-XXXX</code>), keyword search, status dropdowns, and date range filters with server-side pagination.
      </p>
      <div class="screenshot-box" style="flex-grow: 1;">
        <img src="{img_uri('case_list.png')}" alt="Case List View">
      </div>
    </div>

    <!-- Module 2: Custody Timeline -->
    <div class="card" style="display: flex; flex-direction: column;">
      <div class="card-title">2. Chain-of-Custody Timeline</div>
      <p style="font-size: 0.115in; margin-bottom: 0.06in;">
        Append-only ledger showing chronological transfers, locker facilities, and verified seal numbers with automated out-of-sequence warning badges.
      </p>
      <div class="screenshot-box" style="flex-grow: 1;">
        <img src="{img_uri('custody_timeline.png')}" alt="Custody Timeline View">
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>10 / 15</div>
  </div>
</div>

<!-- SLIDE 11: EVIDENCE, REVIEW & REPORTING -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">Verification & Output Generation</div>
    <div class="slide-title">Evidence Vault, Supervisory Review & Case Reports</div>
  </div>

  <div class="grid-2">
    <!-- Supervisor Review Queue -->
    <div class="card" style="display: flex; flex-direction: column;">
      <div class="card-title">Supervisor Review Queue & Action</div>
      <p style="font-size: 0.115in; margin-bottom: 0.06in;">
        Supervisors review submitted cases. Form forces a mandatory comment before approving or requesting corrections.
      </p>
      <div class="screenshot-box" style="flex-grow: 1;">
        <img src="{img_uri('review_queue.png')}" alt="Supervisor Review Queue">
      </div>
    </div>

    <!-- Printable Report -->
    <div class="card" style="display: flex; flex-direction: column;">
      <div class="card-title">Print-Ready Forensic Summary Report</div>
      <p style="font-size: 0.115in; margin-bottom: 0.06in;">
        Standardized print stylesheet with specimen inventories, test outcome logs, custody tables, and dual-signature verification blocks.
      </p>
      <div class="screenshot-box" style="flex-grow: 1;">
        <img src="{img_uri('case_report.png')}" alt="Print-Ready Case Report">
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>11 / 15</div>
  </div>
</div>

<!-- SLIDE 12: SECURITY & DATA INTEGRITY -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">System Hardening & Controls</div>
    <div class="slide-title">Security Architecture & Data Integrity Controls</div>
  </div>

  <div class="grid-3" style="margin-bottom: 0.2in;">
    <div class="card" style="border-color: #2563eb;">
      <div class="card-title" style="color: #38bdf8;">Authentication & Hash</div>
      <p style="font-size: 0.12in;">
        • PBKDF2 password hashing with SHA-256.<br>
        • Django session framework with HTTPOnly cookies.<br>
        • Safe POST-only logout preventing CSRF session termination attacks.
      </p>
    </div>

    <div class="card" style="border-color: #0284c7;">
      <div class="card-title" style="color: #38bdf8;">Role Access Scoping</div>
      <p style="font-size: 0.12in;">
        • Backend view decorators (<code>@role_required</code>).<br>
        • Unauthorized requests trigger HTTP 403 <code>PermissionDenied</code>.<br>
        • Object-level ownership and role-scoped querysets.
      </p>
    </div>

    <div class="card" style="border-color: #38bdf8;">
      <div class="card-title" style="color: #38bdf8;">CSRF & Forms Security</div>
      <p style="font-size: 0.12in;">
        • <code>CsrfViewMiddleware</code> enforced across all views.<br>
        • <code>{{% csrf_token %}}</code> mandatory on every state-changing form.<br>
        • Tested and verified against unauthorized POST requests.
      </p>
    </div>

    <div class="card" style="border-color: #10b981;">
      <div class="card-title" style="color: #10b981;">Private Evidence Vault</div>
      <p style="font-size: 0.12in;">
        • Zero public URL access to uploaded media.<br>
        • Whitelist validation: <code>.jpg, .jpeg, .png, .pdf</code>.<br>
        • Authenticated <code>FileResponse</code> delivery with content headers.
      </p>
    </div>

    <div class="card" style="border-color: #f59e0b;">
      <div class="card-title" style="color: #f59e0b;">Chronological Integrity</div>
      <p style="font-size: 0.12in;">
        • Append-only custody ledger prevents silent history rewriting.<br>
        • Automatically flags retroactive out-of-sequence events.<br>
        • State machine locks approved dossiers from editing.
      </p>
    </div>

    <div class="card" style="border-color: #ef4444;">
      <div class="card-title" style="color: #ef4444;">Immutable Audit Logging</div>
      <p style="font-size: 0.12in;">
        • <code>AuditEvent</code> records actor, action, object ID, and client IP.<br>
        • Non-deletable and non-editable in Django Admin.<br>
        • Persistent forensic disclaimers on all forms and reports.
      </p>
    </div>
  </div>

  <div class="card" style="padding: 0.12in 0.2in;">
    <div style="font-size: 0.12in; color: #94a3b8;">
      <strong style="color: #f59e0b;">Academic Prototype Boundary:</strong> Designed as an educational proof-of-concept for INT253. Operational deployment with live criminal evidence would require departmental IT accreditation, cryptographic signing, and integration with certified forensic labs.
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>12 / 15</div>
  </div>
</div>

<!-- SLIDE 13: TESTING & VALIDATION -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">Quality Assurance & Verification</div>
    <div class="slide-title">Automated Testing & Acceptance Criteria (AT-01 to AT-15)</div>
  </div>

  <div class="grid-2">
    <!-- Acceptance Test Matrix -->
    <div class="card" style="display: flex; flex-direction: column;">
      <div class="card-title">SRS Acceptance Criteria (100% Passing)</div>
      <div style="font-size: 0.11in; display: flex; flex-direction: column; gap: 0.05in; flex-grow: 1;">
        <div><code>AT-01</code>: Anonymous user access redirects to login <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-02</code>: Valid user session login & secure POST logout <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-03</code>: Field Officer blocked from admin views (HTTP 403) <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-04</code>: Case creation with missing fields re-renders errors <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-05</code>: Duplicate sample code rejected with uniqueness error <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-06</code>: Test event records outcome & shows disclaimer <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-07</code>: Unapproved result choices rejected server-side <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-08</code>: Case submit changes status & logs AuditEvent <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-09</code>: Supervisor returning case without comment rejected <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-10</code>: Supervisor approval transitions status to Approved <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-11</code>: Custody events chronological order & sequence flags <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-12</code>: Disallowed / oversized files rejected; vault secured <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-13</code>: Case report contains complete dossier & disclaimer <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-14</code>: POST request without CSRF token rejected (HTTP 403) <strong style="color:#10b981;">[PASS]</strong></div>
        <div><code>AT-15</code>: Complete automated test suite runs with zero errors <strong style="color:#10b981;">[PASS]</strong></div>
      </div>
    </div>

    <!-- Terminal Output -->
    <div class="card" style="display: flex; flex-direction: column;">
      <div class="card-title">Live Test Suite Execution Output</div>
      <div class="card" style="background: #090d16; border-color: #334155; font-family: 'JetBrains Mono', monospace; font-size: 0.115in; padding: 0.15in; flex-grow: 1; color: #cbd5e1; line-height: 1.6;">
        <span style="color: #38bdf8;">$ python3 manage.py test</span><br>
        Found 20 test(s).<br>
        Creating test database for alias 'default'...<br>
        <span style="color: #10b981;">System check identified no issues (0 silenced).</span><br>
        <span style="color: #ffffff;">....................</span><br>
        --------------------------------------------------<br>
        Ran 20 tests in 7.808s<br><br>
        <span style="color: #10b981; font-weight: bold; font-size: 0.14in;">OK</span><br>
        Destroying test database for alias 'default'...<br><br>
        <span style="color: #38bdf8;">$ python3 manage.py check</span><br>
        <span style="color: #10b981;">System check identified no issues (0 silenced).</span>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>13 / 15</div>
  </div>
</div>

<!-- SLIDE 14: COURSE OUTCOME MAPPING -->
<div class="slide">
  <div class="slide-header">
    <div class="category-tag">INT253 Syllabus Compliance</div>
    <div class="slide-title">Mapping to INT253 Course Outcomes</div>
  </div>

  <div class="grid-2" style="flex-grow: 1;">
    <div style="display: flex; flex-direction: column; gap: 0.12in;">
      <div class="card" style="border-left: 4px solid #2563eb;">
        <div style="font-size: 0.13in; font-weight: 700; color: #38bdf8;">CO1: Python/Django Setup & Architecture</div>
        <p style="font-size: 0.115in; color: #cbd5e1;">Virtual environment configuration, modular 8-app layout, settings configuration, and clean <code>manage.py</code> management commands.</p>
      </div>

      <div class="card" style="border-left: 4px solid #0284c7;">
        <div style="font-size: 0.13in; font-weight: 700; color: #38bdf8;">CO2: URL Routing, Views & HTTP Error Handling</div>
        <p style="font-size: 0.115in; color: #cbd5e1;">Named URL patterns, path converters, clean GET/POST handlers, render/redirect flow, and custom 403, 404, and 500 error templates.</p>
      </div>

      <div class="card" style="border-left: 4px solid #38bdf8;">
        <div style="font-size: 0.13in; font-weight: 700; color: #38bdf8;">CO3: Django Template Language (DTL)</div>
        <p style="font-size: 0.115in; color: #cbd5e1;">Master <code>base.html</code> inheritance, block overrides, template variables, loops, conditional role-based menus, and print stylesheets.</p>
      </div>
    </div>

    <div style="display: flex; flex-direction: column; gap: 0.12in;">
      <div class="card" style="border-left: 4px solid #10b981;">
        <div style="font-size: 0.13in; font-weight: 700; color: #10b981;">CO4: Django Forms, Validation & CSRF</div>
        <p style="font-size: 0.115in; color: #cbd5e1;">ModelForms across all models, custom <code>clean()</code> validation, Post/Redirect/Get pattern, and CSRF token protection on all internal forms.</p>
      </div>

      <div class="card" style="border-left: 4px solid #f59e0b;">
        <div style="font-size: 0.13in; font-weight: 700; color: #f59e0b;">CO5: Django ORM, Models & Administration</div>
        <p style="font-size: 0.115in; color: #cbd5e1;">Relational models, ForeignKeys (PROTECT / CASCADE), migrations, unique constraints, and customized Django Admin with date hierarchies.</p>
      </div>

      <div class="card" style="border-left: 4px solid #ef4444;">
        <div style="font-size: 0.13in; font-weight: 700; color: #ef4444;">CO6: Sessions, Authentication & Permissions</div>
        <p style="font-size: 0.115in; color: #cbd5e1;">Django authentication system, PBKDF2 hashing, secure session management, role groups, and backend view decorators (<code>@role_required</code>).</p>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>14 / 15</div>
  </div>
</div>

<!-- SLIDE 15: CONCLUSION & FUTURE SCOPE -->
<div class="slide" style="justify-content: space-between;">
  <div class="slide-header">
    <div class="category-tag">Project Summary & Roadmap</div>
    <div class="slide-title">Conclusion & Future Scope</div>
  </div>

  <div class="grid-2" style="margin-bottom: 0.15in;">
    <div class="card">
      <div class="card-title">Project Summary & Key Achievements</div>
      <ul>
        <li><strong>Working Full-Stack Platform:</strong> Successfully built a production-grade Django application replacing vulnerable paper logs with structured digital dossiers.</li>
        <li><strong>Evidence Integrity:</strong> Preserves chain-of-custody continuity with append-only logs and retroactive sequence checks.</li>
        <li><strong>Supervisory Oversight:</strong> Enforces review accountability through mandatory written feedback before dossier approval.</li>
        <li><strong>Academic Rigor:</strong> 100% syllabus alignment for INT253 with 20 passing automated tests and zero warnings.</li>
      </ul>
    </div>

    <div class="card">
      <div class="card-title">Future Roadmap & Enterprise Scaling</div>
      <ul>
        <li><strong>Database Migration:</strong> Deploy managed PostgreSQL with automated replication and point-in-time recovery.</li>
        <li><strong>Encrypted Cloud Storage:</strong> Integrate AWS S3 / GCP private encrypted buckets with expiring signed URLs for evidence vault files.</li>
        <li><strong>Headless PDF Service:</strong> Incorporate WeasyPrint for automated server-side PDF generation and dispatch.</li>
        <li><strong>LIMS Integration:</strong> Connect via secure REST APIs to certified Laboratory Information Management Systems for confirmatory testing sync.</li>
      </ul>
    </div>
  </div>

  <div class="card" style="background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%); border: none; text-align: center; padding: 0.2in;">
    <h2 style="font-size: 0.26in; font-weight: 800; color: #ffffff; margin-bottom: 0.04in;">Thank You! Questions & Discussion</h2>
    <p style="font-size: 0.14in; color: #bfdbfe;">
      FieldTest Companion (DCDFT) • Ansh Sangwan • INT253 Final Viva Presentation
    </p>
  </div>

  <div class="slide-footer">
    <div>FieldTest Companion (DCDFT) • Ansh Sangwan</div>
    <div>15 / 15</div>
  </div>
</div>

</body>
</html>
"""

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✓ HTML slides written to: {HTML_OUT}")

# Render PDF using Google Chrome headless
cmd = [
    CHROME_BIN,
    "--headless=new",
    "--no-pdf-header-footer",
    f"--user-data-dir={PROFILE_DIR}",
    f"--print-to-pdf={PDF_OUT}",
    f"file://{HTML_OUT}"
]

print(f"Compiling PDF using Chrome headless: {PDF_OUT}...")
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if os.path.exists(PDF_OUT):
    size = os.path.getsize(PDF_OUT)
    print(f"✓ PDF successfully generated: {PDF_OUT} ({size} bytes)")
else:
    print(f"✗ Failed to generate PDF: {res.stderr}")
