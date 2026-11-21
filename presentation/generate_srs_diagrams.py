import os
import subprocess

OUT_DIR = 'presentation/srs_diagrams'
os.makedirs(OUT_DIR, exist_ok=True)
chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

def render_html_to_png(html_content, out_png, width=1400, height=850):
    html_path = os.path.join(OUT_DIR, 'temp_diagram.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    cmd = [
        chrome,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        f'--window-size={width},{height}',
        f'--screenshot={out_png}',
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"✓ Rendered {out_png} ({os.path.getsize(out_png)} bytes)")
    else:
        print(f"✗ Failed {out_png}: {res.stderr}")

# Diagram 1: Context-Level DFD (Level 0)
d1_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 40px; background: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  .title-bar { text-align: center; margin-bottom: 30px; }
  .title-bar h2 { margin: 0; color: #0F172A; font-size: 22px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
  .title-bar p { margin: 5px 0 0; color: #64748B; font-size: 13px; }
  .canvas { position: relative; width: 1200px; height: 600px; margin: 0 auto; background: #F8FAFC; border: 2px solid #E2E8F0; border-radius: 12px; }
  
  .entity { position: absolute; width: 180px; padding: 16px; background: #1E293B; color: #FFFFFF; border-radius: 8px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-left: 5px solid #38BDF8; }
  .entity h4 { margin: 0 0 6px; font-size: 14px; color: #38BDF8; text-transform: uppercase; }
  .entity p { margin: 0; font-size: 11px; color: #CBD5E1; line-height: 1.4; }
  
  .system-bubble { position: absolute; top: 180px; left: 450px; width: 300px; height: 240px; background: #0F172A; border: 4px solid #2563EB; border-radius: 50%; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; color: #FFFFFF; box-shadow: 0 10px 15px -3px rgba(37,99,235,0.25); }
  .system-bubble .proc-num { font-size: 14px; font-weight: 800; color: #38BDF8; border-bottom: 2px solid #38BDF8; padding-bottom: 2px; margin-bottom: 6px; }
  .system-bubble h3 { margin: 0 0 8px; font-size: 17px; font-weight: 700; max-width: 200px; }
  .system-bubble p { margin: 0; font-size: 11px; color: #94A3B8; max-width: 220px; line-height: 1.3; }

  /* Positions */
  #ent-officer { top: 60px; left: 40px; }
  #ent-supervisor { top: 380px; left: 40px; border-left-color: #10B981; }
  #ent-admin { top: 60px; right: 40px; border-left-color: #F59E0B; }
  #ent-readonly { top: 380px; right: 40px; border-left-color: #8B5CF6; }

  /* Flow labels */
  .flow-box { position: absolute; background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 4px; padding: 4px 8px; font-size: 10px; font-weight: 600; color: #1E293B; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
  svg.wires { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
</style>
</head>
<body>
<div class="title-bar">
  <h2>Figure 4.1.1: Context-Level Data Flow Diagram (Level 0 DFD)</h2>
  <p>System Boundaries, External Actor Interactions, and Core Forensic Information Inflows & Outflows</p>
</div>
<div class="canvas">
  <svg class="wires">
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#64748B" />
      </marker>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563EB" />
      </marker>
    </defs>
    <!-- Officer Flows -->
    <path d="M 230 110 L 460 230" fill="none" stroke="#2563EB" stroke-width="2" marker-end="url(#arrow-blue)" />
    <path d="M 460 260 L 230 140" fill="none" stroke="#64748B" stroke-width="1.5" stroke-dasharray="4" marker-end="url(#arrow)" />
    
    <!-- Supervisor Flows -->
    <path d="M 230 430 L 460 340" fill="none" stroke="#2563EB" stroke-width="2" marker-end="url(#arrow-blue)" />
    <path d="M 460 370 L 230 460" fill="none" stroke="#64748B" stroke-width="1.5" stroke-dasharray="4" marker-end="url(#arrow)" />

    <!-- Admin Flows -->
    <path d="M 970 110 L 740 230" fill="none" stroke="#2563EB" stroke-width="2" marker-end="url(#arrow-blue)" />
    <path d="M 740 260 L 970 140" fill="none" stroke="#64748B" stroke-width="1.5" stroke-dasharray="4" marker-end="url(#arrow)" />

    <!-- Auditor Flows -->
    <path d="M 970 430 L 740 340" fill="none" stroke="#2563EB" stroke-width="2" marker-end="url(#arrow-blue)" />
    <path d="M 740 370 L 970 460" fill="none" stroke="#64748B" stroke-width="1.5" stroke-dasharray="4" marker-end="url(#arrow)" />
  </svg>

  <!-- External Entities -->
  <div class="entity" id="ent-officer">
    <h4>Field Officer</h4>
    <p>Seizure documentation, presumptive testing, custody transfers, evidence upload</p>
  </div>
  <div class="entity" id="ent-supervisor">
    <h4 style="color:#10B981">Supervisor</h4>
    <p>Review queue, endorsement/corrections, case locking, official reporting</p>
  </div>
  <div class="entity" id="ent-admin">
    <h4 style="color:#F59E0B">Administrator</h4>
    <p>User provisioning, group roles, test kit catalog, security audits</p>
  </div>
  <div class="entity" id="ent-readonly">
    <h4 style="color:#A78BFA">Read-Only User</h4>
    <p>Compliance auditing, chain-of-custody verification, legal inspection</p>
  </div>

  <!-- Central System Bubble -->
  <div class="system-bubble">
    <span class="proc-num">0.0</span>
    <h3>FieldTest Companion</h3>
    <p>Digital Companion for Drug Field Testing & Forensic Custody Management Platform</p>
  </div>

  <!-- Flow Labels -->
  <div class="flow-box" style="top: 140px; left: 245px;">Cases, Samples, Test Events, Custody, Evidence &rarr;</div>
  <div class="flow-box" style="top: 200px; left: 235px;">&larr; Case Status, Validation Alerts, Receipts</div>

  <div class="flow-box" style="top: 365px; left: 230px;">Review Decision (Approve/Reject), Comments &rarr;</div>
  <div class="flow-box" style="top: 425px; left: 240px;">&larr; Submitted Dossiers, Forensic Summary Reports</div>

  <div class="flow-box" style="top: 140px; right: 230px;">&larr; User Provisioning, Group Permissions, Kit Catalog</div>
  <div class="flow-box" style="top: 200px; right: 240px;">System Audits, User Activity Logs &rarr;</div>

  <div class="flow-box" style="top: 365px; right: 240px;">&larr; Audit Queries, Compliance Search</div>
  <div class="flow-box" style="top: 425px; right: 230px;">Read-Only Dossiers, Custody Chains &rarr;</div>
</div>
</body>
</html>
"""
render_html_to_png(d1_html, os.path.join(OUT_DIR, 'dfd_context.png'), width=1300, height=750)

# Diagram 2: Level 1 DFD
d2_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 30px; background: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  .title-bar { text-align: center; margin-bottom: 25px; }
  .title-bar h2 { margin: 0; color: #0F172A; font-size: 22px; font-weight: 700; text-transform: uppercase; }
  .title-bar p { margin: 4px 0 0; color: #64748B; font-size: 13px; }
  
  .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; max-width: 1200px; margin: 0 auto; }
  .proc-card { background: #0F172A; color: white; border-radius: 8px; border: 1px solid #1E293B; border-top: 4px solid #2563EB; padding: 14px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
  .proc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
  .proc-num { background: #2563EB; color: white; font-size: 11px; font-weight: 800; padding: 2px 6px; border-radius: 4px; }
  .proc-name { font-size: 13px; font-weight: 700; color: #38BDF8; margin: 0; }
  .proc-desc { font-size: 10.5px; color: #CBD5E1; line-height: 1.35; margin: 0 0 10px; }
  .data-store { background: #1E293B; border-left: 3px solid #10B981; border-radius: 4px; padding: 6px 8px; font-size: 10px; color: #94A3B8; }
  .data-store strong { color: #34D399; }
</style>
</head>
<body>
<div class="title-bar">
  <h2>Figure 4.1.2: Level 1 Data Flow Diagram (Core System Processes & Data Stores)</h2>
  <p>Decomposition of FieldTest Companion into 8 Functional Processing Subsystems & Relational Repositories</p>
</div>
<div class="grid">
  <div class="proc-card">
    <div class="proc-header"><h3 class="proc-name">Auth & Access Control</h3><span class="proc-num">1.0</span></div>
    <p class="proc-desc">Validates user credentials, session cookies, and group-based roles (Officer, Supervisor, Admin, Auditor) via decorators.</p>
    <div class="data-store"><strong>D1: auth_user & auth_group</strong><br>User credentials, groups, role permissions</div>
  </div>
  <div class="proc-card">
    <div class="proc-header"><h3 class="proc-name">Case Management</h3><span class="proc-num">2.0</span></div>
    <p class="proc-desc">Performs CaseRecord CRUD, auto-generates sequential references (CASE-YYYY-XXXX), and handles lifecycle state changes.</p>
    <div class="data-store"><strong>D2: cases_caserecord</strong><br>Incident metadata, status, officer assignment</div>
  </div>
  <div class="proc-card">
    <div class="proc-header"><h3 class="proc-name">Sample Registration</h3><span class="proc-num">3.0</span></div>
    <p class="proc-desc">Registers physical seized specimens, auto-assigns SMP-YYYY-XXXX identifiers, enforces uniqueness, packaging, and tamper seals.</p>
    <div class="data-store"><strong>D3: cases_sample</strong><br>Physical description, seal #, condition, case FK</div>
  </div>
  <div class="proc-card">
    <div class="proc-header"><h3 class="proc-name">Presumptive Testing</h3><span class="proc-num">4.0</span></div>
    <p class="proc-desc">Documents reagent test events, verifies kit active status, validates kit expiration with mandatory notes, records sensory colors.</p>
    <div class="data-store"><strong>D4/D5: testkit & testevent</strong><br>Reagent catalog, lot numbers, test results</div>
  </div>
  <div class="proc-card" style="border-top-color:#10B981">
    <div class="proc-header"><h3 class="proc-name" style="color:#34D399">Custody Tracking</h3><span class="proc-num" style="background:#10B981">5.0</span></div>
    <p class="proc-desc">Maintains append-only chronological chain of custody, tracks transfer parties, storage locations, and flags out-of-sequence entries.</p>
    <div class="data-store"><strong>D6: custody_custodyevent</strong><br>From/to person, transfer type, seal verification</div>
  </div>
  <div class="proc-card" style="border-top-color:#10B981">
    <div class="proc-header"><h3 class="proc-name" style="color:#34D399">Evidence Vault</h3><span class="proc-num" style="background:#10B981">6.0</span></div>
    <p class="proc-desc">Validates uploaded evidence files (MIME type, extension, size limit), stores files privately, and enforces authenticated downloads.</p>
    <div class="data-store"><strong>D7: evidence_evidencefile</strong><br>Private media files, mime type, hash metadata</div>
  </div>
  <div class="proc-card" style="border-top-color:#F59E0B">
    <div class="proc-header"><h3 class="proc-name" style="color:#FBBF24">Supervisory Review</h3><span class="proc-num" style="background:#F59E0B">7.0</span></div>
    <p class="proc-desc">Routes submitted dossiers to supervisor queue, enforces mandatory review comments, processes approvals, and locks case records.</p>
    <div class="data-store"><strong>D8: reviews_reviewrecord</strong><br>Review decision, mandatory comments, timestamp</div>
  </div>
  <div class="proc-card" style="border-top-color:#8B5CF6">
    <div class="proc-header"><h3 class="proc-name" style="color:#C084FC">Security Audit Log</h3><span class="proc-num" style="background:#8B5CF6">8.0</span></div>
    <p class="proc-desc">Listens for system events, model modifications, authorization failures, and logins, writing immutable chronological audit records.</p>
    <div class="data-store"><strong>D9: auditlog_auditevent</strong><br>Actor, action, target entity, client IP address</div>
  </div>
</div>
</body>
</html>
"""
render_html_to_png(d2_html, os.path.join(OUT_DIR, 'dfd_level1.png'), width=1300, height=650)

# Diagram 3: System Architecture Diagram
d3_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 30px; background: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  .title-bar { text-align: center; margin-bottom: 25px; }
  .title-bar h2 { margin: 0; color: #0F172A; font-size: 22px; font-weight: 700; text-transform: uppercase; }
  .title-bar p { margin: 4px 0 0; color: #64748B; font-size: 13px; }
  
  .container { max-width: 1100px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px; }
  .tier { background: #0F172A; border-radius: 8px; border: 1px solid #334155; padding: 16px 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
  .tier-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E293B; padding-bottom: 8px; margin-bottom: 12px; }
  .tier-title { font-size: 14px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }
  .tier-badge { font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px; }
  
  .boxes { display: flex; gap: 12px; }
  .box { flex: 1; background: #1E293B; border-radius: 6px; padding: 10px 14px; border-left: 3px solid #38BDF8; }
  .box h4 { margin: 0 0 4px; font-size: 12px; color: #38BDF8; }
  .box p { margin: 0; font-size: 10.5px; color: #CBD5E1; line-height: 1.35; }

  .tier-1 { border-left: 6px solid #38BDF8; }
  .tier-1 .tier-title { color: #38BDF8; }
  .tier-1 .tier-badge { background: #0284C7; color: white; }

  .tier-2 { border-left: 6px solid #2563EB; }
  .tier-2 .tier-title { color: #60A5FA; }
  .tier-2 .tier-badge { background: #1D4ED8; color: white; }

  .tier-3 { border-left: 6px solid #10B981; }
  .tier-3 .tier-title { color: #34D399; }
  .tier-3 .tier-badge { background: #059669; color: white; }

  .tier-4 { border-left: 6px solid #F59E0B; }
  .tier-4 .tier-title { color: #FBBF24; }
  .tier-4 .tier-badge { background: #D97706; color: white; }
</style>
</head>
<body>
<div class="title-bar">
  <h2>Figure 4.1.3: Four-Tier MTV System Architecture Diagram</h2>
  <p>Layered Separation of Concerns: Presentation, Routing, Forensic Business Logic, and Data Persistence</p>
</div>
<div class="container">
  <!-- Tier 1 -->
  <div class="tier tier-1">
    <div class="tier-header">
      <span class="tier-title">Tier 1: Client & Presentation Interface Layer</span>
      <span class="tier-badge">Frontend Tier</span>
    </div>
    <div class="boxes">
      <div class="box">
        <h4>Responsive HTML5 & Bootstrap 5</h4>
        <p>Mobile-first operational layouts, cards, status badges, forms, and accessibility-compliant UI components.</p>
      </div>
      <div class="box">
        <h4>Django Template Language (DTL)</h4>
        <p>Base inheritance (base.html), contextual navigation, statutory disclaimer banners, and dynamic data rendering.</p>
      </div>
      <div class="box">
        <h4>Print & Export Engine</h4>
        <p>Court-ready CSS @media print styling and high-resolution PDF generation for official case summary reports.</p>
      </div>
    </div>
  </div>

  <!-- Tier 2 -->
  <div class="tier tier-2">
    <div class="tier-header">
      <span class="tier-title">Tier 2: Routing, Middleware & Controller Layer</span>
      <span class="tier-badge">Django MTV Controller</span>
    </div>
    <div class="boxes">
      <div class="box" style="border-left-color:#60A5FA">
        <h4>URL Routing & Dispatch</h4>
        <p>Root URL dispatcher (config/urls.py) directing traffic to 8 modular application route namespaces.</p>
      </div>
      <div class="box" style="border-left-color:#60A5FA">
        <h4>Class-Based & Functional Views</h4>
        <p>CRUD viewsets, search/filtering querysets, report views, and pagination logic across all applications.</p>
      </div>
      <div class="box" style="border-left-color:#60A5FA">
        <h4>Security Middleware</h4>
        <p>CSRF protection token validation, SessionMiddleware, AuthenticationMiddleware, and custom role decorators.</p>
      </div>
    </div>
  </div>

  <!-- Tier 3 -->
  <div class="tier tier-3">
    <div class="tier-header">
      <span class="tier-title">Tier 3: Business Logic & Forensic Validation Layer</span>
      <span class="tier-badge">Domain Service Tier</span>
    </div>
    <div class="boxes">
      <div class="box" style="border-left-color:#34D399">
        <h4>Form Clean & Integrity Guards</h4>
        <p>Unique case/sample code generators, incident date validation, kit expiry checks, and review comment requirements.</p>
      </div>
      <div class="box" style="border-left-color:#34D399">
        <h4>Custody & Sequence Engine</h4>
        <p>Chronological custody timeline verification, automatic retrospective out-of-sequence flags, and transfer validation.</p>
      </div>
      <div class="box" style="border-left-color:#34D399">
        <h4>Signals & Audit Event Dispatcher</h4>
        <p>Django post_save and custom signals silently emitting immutable audit trail entries with client IP addresses.</p>
      </div>
    </div>
  </div>

  <!-- Tier 4 -->
  <div class="tier tier-4">
    <div class="tier-header">
      <span class="tier-title">Tier 4: Data Persistence & Storage Layer</span>
      <span class="tier-badge">Persistence Tier</span>
    </div>
    <div class="boxes">
      <div class="box" style="border-left-color:#FBBF24">
        <h4>Django ORM & Query Engine</h4>
        <p>Parameterized SQL generation preventing injection attacks, atomic transaction blocks, and foreign-key integrity.</p>
      </div>
      <div class="box" style="border-left-color:#FBBF24">
        <h4>Relational Database (SQLite / Postgres)</h4>
        <p>Relational storage across 9 core tables with CASCADE, PROTECT, and SET_NULL referential rules.</p>
      </div>
      <div class="box" style="border-left-color:#FBBF24">
        <h4>Private Evidence Vault</h4>
        <p>Restricted file storage for photo/document evidence, served only via authenticated stream views.</p>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""
render_html_to_png(d3_html, os.path.join(OUT_DIR, 'system_architecture.png'), width=1300, height=800)

# Diagram 4: Entity-Relationship Diagram (ERD)
d4_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 25px; background: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  .title-bar { text-align: center; margin-bottom: 20px; }
  .title-bar h2 { margin: 0; color: #0F172A; font-size: 21px; font-weight: 700; text-transform: uppercase; }
  .title-bar p { margin: 4px 0 0; color: #64748B; font-size: 12px; }
  
  .canvas { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; max-width: 1250px; margin: 0 auto; }
  .entity-card { background: #0F172A; color: white; border-radius: 6px; border: 1px solid #1E293B; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); font-size: 10px; }
  .entity-header { background: #1E293B; padding: 6px 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #2563EB; }
  .entity-header h4 { margin: 0; font-size: 12px; font-weight: 700; color: #38BDF8; }
  .entity-header span { font-size: 9px; color: #94A3B8; text-transform: uppercase; }
  
  .fields { padding: 6px 10px; }
  .field-row { display: flex; justify-content: space-between; padding: 2px 0; border-bottom: 1px solid #1E293B; }
  .field-name { font-family: monospace; font-size: 9.5px; color: #E2E8F0; }
  .field-name strong { color: #F59E0B; }
  .field-name em { color: #38BDF8; font-style: normal; }
  .field-type { font-size: 8.5px; color: #94A3B8; }
  
  .rel-badge { margin: 4px 10px 8px; padding: 4px 6px; background: #1E293B; border-radius: 4px; font-size: 8.5px; color: #CBD5E1; border-left: 2px solid #10B981; }
</style>
</head>
<body>
<div class="title-bar">
  <h2>Figure 4.1.4: Complete Entity-Relationship (ER) Diagram</h2>
  <p>Relational Schema with Primary Keys (PK), Foreign Keys (FK), Data Types, and Referential Cardinality</p>
</div>
<div class="canvas">
  <!-- User -->
  <div class="entity-card">
    <div class="entity-header"><h4>auth.User</h4><span>Core Actor</span></div>
    <div class="fields">
      <div class="field-row"><span class="field-name"><strong>PK</strong> id</span><span class="field-type">AutoField</span></div>
      <div class="field-row"><span class="field-name">username</span><span class="field-type">CharField(150)</span></div>
      <div class="field-row"><span class="field-name">password</span><span class="field-type">CharField(128)</span></div>
      <div class="field-row"><span class="field-name">email, first/last_name</span><span class="field-type">CharField</span></div>
      <div class="field-row"><span class="field-name">is_staff, is_active</span><span class="field-type">BooleanField</span></div>
      <div class="field-row"><span class="field-name"><em>M:N</em> groups</span><span class="field-type">&rarr; auth.Group</span></div>
    </div>
    <div class="rel-badge">1:N with Cases, Samples, Tests, Custody, Reviews, Audits</div>
  </div>

  <!-- CaseRecord -->
  <div class="entity-card" style="border-top: 3px solid #2563EB;">
    <div class="entity-header" style="border-bottom-color:#2563EB"><h4>cases.CaseRecord</h4><span>Core Dossier</span></div>
    <div class="fields">
      <div class="field-row"><span class="field-name"><strong>PK</strong> id</span><span class="field-type">BigAutoField</span></div>
      <div class="field-row"><span class="field-name">case_reference</span><span class="field-type">CharField(32) [UNIQUE]</span></div>
      <div class="field-row"><span class="field-name">title, general_location</span><span class="field-type">CharField(255)</span></div>
      <div class="field-row"><span class="field-name">incident_datetime</span><span class="field-type">DateTimeField</span></div>
      <div class="field-row"><span class="field-name">status</span><span class="field-type">CharField(20) [CHOICES]</span></div>
      <div class="field-row"><span class="field-name"><em>FK</em> created_by, assigned_to</span><span class="field-type">&rarr; User (SET_NULL)</span></div>
    </div>
    <div class="rel-badge">1:N with Sample, EvidenceFile, ReviewRecord</div>
  </div>

  <!-- Sample -->
  <div class="entity-card" style="border-top: 3px solid #10B981;">
    <div class="entity-header" style="border-bottom-color:#10B981"><h4 style="color:#34D399">cases.Sample</h4><span>Physical Specimen</span></div>
    <div class="fields">
      <div class="field-row"><span class="field-name"><strong>PK</strong> id</span><span class="field-type">BigAutoField</span></div>
      <div class="field-row"><span class="field-name">sample_code</span><span class="field-type">CharField(32) [UNIQUE]</span></div>
      <div class="field-row"><span class="field-name"><em>FK</em> case</span><span class="field-type">&rarr; CaseRecord (CASCADE)</span></div>
      <div class="field-row"><span class="field-name">collected_at</span><span class="field-type">DateTimeField</span></div>
      <div class="field-row"><span class="field-name">packaging_reference</span><span class="field-type">CharField(100)</span></div>
      <div class="field-row"><span class="field-name">seal_reference</span><span class="field-type">CharField(100)</span></div>
      <div class="field-row"><span class="field-name">initial_condition</span><span class="field-type">CharField(100)</span></div>
    </div>
    <div class="rel-badge">1:N with TestEvent, CustodyEvent, EvidenceFile</div>
  </div>

  <!-- TestKit -->
  <div class="entity-card">
    <div class="entity-header"><h4>testing.TestKit</h4><span>Reagent Catalog</span></div>
    <div class="fields">
      <div class="field-row"><span class="field-name"><strong>PK</strong> id</span><span class="field-type">BigAutoField</span></div>
      <div class="field-row"><span class="field-name">name, manufacturer</span><span class="field-type">CharField(150)</span></div>
      <div class="field-row"><span class="field-name">category</span><span class="field-type">CharField(100)</span></div>
      <div class="field-row"><span class="field-name">catalogue_reference</span><span class="field-type">CharField(100)</span></div>
      <div class="field-row"><span class="field-name">active</span><span class="field-type">BooleanField (default=True)</span></div>
      <div class="field-row"><span class="field-name">general_safety_note</span><span class="field-type">TextField</span></div>
    </div>
    <div class="rel-badge">1:N with TestEvent (on_delete=PROTECT)</div>
  </div>

  <!-- TestEvent -->
  <div class="entity-card" style="border-top: 3px solid #38BDF8;">
    <div class="entity-header" style="border-bottom-color:#38BDF8"><h4 style="color:#38BDF8">testing.TestEvent</h4><span>Field Test Record</span></div>
    <div class="fields">
      <div class="field-row"><span class="field-name"><strong>PK</strong> id</span><span class="field-type">BigAutoField</span></div>
      <div class="field-row"><span class="field-name"><em>FK</em> sample</span><span class="field-type">&rarr; Sample (CASCADE)</span></div>
      <div class="field-row"><span class="field-name"><em>FK</em> kit</span><span class="field-type">&rarr; TestKit (PROTECT)</span></div>
      <div class="field-row"><span class="field-name">kit_lot_number</span><span class="field-type">CharField(100)</span></div>
      <div class="field-row"><span class="field-name">kit_expiry_date</span><span class="field-type">DateField</span></div>
      <div class="field-row"><span class="field-name">result_category</span><span class="field-type">CharField(30) [CHOICES]</span></div>
      <div class="field-row"><span class="field-name">observation_notes</span><span class="field-type">TextField</span></div>
      <div class="field-row"><span class="field-name">limitations_note</span><span class="field-type">TextField</span></div>
    </div>
    <div class="rel-badge">N:1 with Sample, N:1 with TestKit, N:1 with User</div>
  </div>

  <!-- CustodyEvent -->
  <div class="entity-card" style="border-top: 3px solid #10B981;">
    <div class="entity-header" style="border-bottom-color:#10B981"><h4 style="color:#34D399">custody.CustodyEvent</h4><span>Custody Ledger</span></div>
    <div class="fields">
      <div class="field-row"><span class="field-name"><strong>PK</strong> id</span><span class="field-type">BigAutoField</span></div>
      <div class="field-row"><span class="field-name"><em>FK</em> sample</span><span class="field-type">&rarr; Sample (CASCADE)</span></div>
      <div class="field-row"><span class="field-name">event_type</span><span class="field-type">CharField(30) [CHOICES]</span></div>
      <div class="field-row"><span class="field-name">event_at</span><span class="field-type">DateTimeField</span></div>
      <div class="field-row"><span class="field-name">from_person, to_person</span><span class="field-type">CharField(120)</span></div>
      <div class="field-row"><span class="field-name">location_reference</span><span class="field-type">CharField(150)</span></div>
      <div class="field-row"><span class="field-name">seal_reference</span><span class="field-type">CharField(100)</span></div>
      <div class="field-row"><span class="field-name">is_out_of_sequence</span><span class="field-type">BooleanField</span></div>
    </div>
    <div class="rel-badge">N:1 with Sample, N:1 with User (recorded_by)</div>
  </div>

  <!-- EvidenceFile -->
  <div class="entity-card">
    <div class="entity-header"><h4>evidence.EvidenceFile</h4><span>Secure Media Vault</span></div>
    <div class="fields">
      <div class="field-row"><span class="field-name"><strong>PK</strong> id</span><span class="field-type">BigAutoField</span></div>
      <div class="field-row"><span class="field-name"><em>FK</em> case</span><span class="field-type">&rarr; CaseRecord (CASCADE)</span></div>
      <div class="field-row"><span class="field-name"><em>FK</em> sample</span><span class="field-type">&rarr; Sample (NULL/CASCADE)</span></div>
      <div class="field-row"><span class="field-name">file</span><span class="field-type">FileField (private dir)</span></div>
      <div class="field-row"><span class="field-name">original_filename</span><span class="field-type">CharField(255)</span></div>
      <div class="field-row"><span class="field-name">content_type, file_size</span><span class="field-type">MIME / Integer</span></div>
    </div>
    <div class="rel-badge">N:1 with CaseRecord, N:1 with Sample, N:1 with User</div>
  </div>

  <!-- ReviewRecord -->
  <div class="entity-card" style="border-top: 3px solid #F59E0B;">
    <div class="entity-header" style="border-bottom-color:#F59E0B"><h4 style="color:#FBBF24">reviews.ReviewRecord</h4><span>Supervisor Sign-Off</span></div>
    <div class="fields">
      <div class="field-row"><span class="field-name"><strong>PK</strong> id</span><span class="field-type">BigAutoField</span></div>
      <div class="field-row"><span class="field-name"><em>FK</em> case</span><span class="field-type">&rarr; CaseRecord (CASCADE)</span></div>
      <div class="field-row"><span class="field-name"><em>FK</em> reviewer</span><span class="field-type">&rarr; User (PROTECT)</span></div>
      <div class="field-row"><span class="field-name">decision</span><span class="field-type">CharField(30) [CHOICES]</span></div>
      <div class="field-row"><span class="field-name">comment</span><span class="field-type">TextField (Mandatory)</span></div>
      <div class="field-row"><span class="field-name">reviewed_at</span><span class="field-type">DateTimeField</span></div>
    </div>
    <div class="rel-badge">N:1 with CaseRecord, N:1 with User (reviewer)</div>
  </div>

  <!-- AuditEvent -->
  <div class="entity-card" style="border-top: 3px solid #8B5CF6;">
    <div class="entity-header" style="border-bottom-color:#8B5CF6"><h4 style="color:#C084FC">auditlog.AuditEvent</h4><span>Immutable Trail</span></div>
    <div class="fields">
      <div class="field-row"><span class="field-name"><strong>PK</strong> id</span><span class="field-type">BigAutoField</span></div>
      <div class="field-row"><span class="field-name"><em>FK</em> actor</span><span class="field-type">&rarr; User (SET_NULL)</span></div>
      <div class="field-row"><span class="field-name">action</span><span class="field-type">CharField(50)</span></div>
      <div class="field-row"><span class="field-name">object_type, object_id</span><span class="field-type">CharField</span></div>
      <div class="field-row"><span class="field-name">summary</span><span class="field-type">TextField</span></div>
      <div class="field-row"><span class="field-name">ip_address</span><span class="field-type">GenericIPAddressField</span></div>
      <div class="field-row"><span class="field-name">timestamp</span><span class="field-type">DateTimeField</span></div>
    </div>
    <div class="rel-badge">Append-Only System Log; N:1 with User (actor)</div>
  </div>
</div>
</body>
</html>
"""
render_html_to_png(d4_html, os.path.join(OUT_DIR, 'erd_diagram.png'), width=1300, height=850)

# Diagram 5: Main Operational Workflow
d5_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 30px; background: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
  .title-bar { text-align: center; margin-bottom: 25px; }
  .title-bar h2 { margin: 0; color: #0F172A; font-size: 22px; font-weight: 700; text-transform: uppercase; }
  .title-bar p { margin: 4px 0 0; color: #64748B; font-size: 13px; }
  
  .flow-container { max-width: 1200px; margin: 0 auto; display: flex; flex-direction: column; gap: 14px; }
  .phase-row { display: flex; align-items: center; gap: 12px; }
  .phase-badge { width: 130px; background: #0F172A; color: white; padding: 8px 12px; border-radius: 6px; font-size: 11px; font-weight: 700; text-align: center; border-left: 4px solid #2563EB; flex-shrink: 0; }
  
  .steps-flex { display: flex; flex: 1; gap: 10px; }
  .step-card { flex: 1; background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 10px 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
  .step-num { font-size: 10px; font-weight: 800; color: #2563EB; margin-bottom: 2px; }
  .step-title { font-size: 12px; font-weight: 700; color: #0F172A; margin: 0 0 4px; }
  .step-desc { font-size: 10px; color: #475569; margin: 0; line-height: 1.35; }

  .decision-split { display: flex; flex: 1; gap: 12px; }
  .branch-card { flex: 1; border-radius: 6px; padding: 10px 12px; font-size: 10.5px; }
  .branch-reject { background: #FEF2F2; border: 1px solid #FCA5A5; color: #991B1B; }
  .branch-approve { background: #ECFDF5; border: 1px solid #6EE7B7; color: #065F46; }
</style>
</head>
<body>
<div class="title-bar">
  <h2>Figure 4.1.5: End-to-End Operational Lifecycle Workflow Diagram</h2>
  <p>Sequential Stages: Field Seizure, Reagent Testing, Chain of Custody, Supervisory Review, and Case Closure</p>
</div>
<div class="flow-container">
  <!-- Phase 1 -->
  <div class="phase-row">
    <div class="phase-badge">STAGE 1<br><span style="color:#38BDF8; font-size:9.5px;">FIELD SEIZURE</span></div>
    <div class="steps-flex">
      <div class="step-card">
        <div class="step-num">STEP 01</div>
        <div class="step-title">Officer Authentication</div>
        <p class="step-desc">Field Officer logs in via secure credentials; session created with Field Officer group permissions.</p>
      </div>
      <div class="step-card">
        <div class="step-num">STEP 02</div>
        <div class="step-title">Create Case Dossier</div>
        <p class="step-desc">Enters incident time, location, circumstances; system auto-assigns CASE-YYYY-XXXX (Status: Draft).</p>
      </div>
      <div class="step-card">
        <div class="step-num">STEP 03</div>
        <div class="step-title">Catalog Physical Samples</div>
        <p class="step-desc">Registers each specimen, auto-generates SMP-YYYY-XXXX, logs packaging and tamper seal IDs.</p>
      </div>
    </div>
  </div>

  <!-- Phase 2 -->
  <div class="phase-row">
    <div class="phase-badge" style="border-left-color:#10B981;">STAGE 2<br><span style="color:#34D399; font-size:9.5px;">TESTING & CUSTODY</span></div>
    <div class="steps-flex">
      <div class="step-card">
        <div class="step-num" style="color:#10B981">STEP 04</div>
        <div class="step-title">Record Field Test Event</div>
        <p class="step-desc">Selects active test kit, verifies expiry date, logs sensory color transition, records presumptive outcome.</p>
      </div>
      <div class="step-card">
        <div class="step-num" style="color:#10B981">STEP 05</div>
        <div class="step-title">Log Custody Transfers</div>
        <p class="step-desc">Appends chronological transfers from officer to evidence locker; flags retrospective entries.</p>
      </div>
      <div class="step-card">
        <div class="step-num" style="color:#10B981">STEP 06</div>
        <div class="step-title">Upload Evidence Files</div>
        <p class="step-desc">Uploads photos and documents (JPG, PNG, PDF &le; 10MB) into the protected private evidence vault.</p>
      </div>
    </div>
  </div>

  <!-- Phase 3 -->
  <div class="phase-row">
    <div class="phase-badge" style="border-left-color:#F59E0B;">STAGE 3<br><span style="color:#FBBF24; font-size:9.5px;">SUPERVISORY REVIEW</span></div>
    <div class="steps-flex">
      <div class="step-card" style="flex:0.8">
        <div class="step-num" style="color:#F59E0B">STEP 07</div>
        <div class="step-title">Submit Dossier</div>
        <p class="step-desc">Officer transitions case from Draft to Submitted; locks officer editing and alerts supervisor queue.</p>
      </div>
      <div class="decision-split">
        <div class="branch-card branch-reject">
          <strong>Decision A: Changes Requested</strong><br>
          Supervisor enters mandatory actionable feedback. Status shifts to "Changes requested". Case returns to Field Officer for correction.
        </div>
        <div class="branch-card branch-approve">
          <strong>Decision B: Endorsement / Approved</strong><br>
          Supervisor confirms protocol adherence. Status shifts to "Approved". Case is locked against modifications. Ready for official report export.
        </div>
      </div>
    </div>
  </div>

  <!-- Phase 4 -->
  <div class="phase-row">
    <div class="phase-badge" style="border-left-color:#8B5CF6;">STAGE 4<br><span style="color:#C084FC; font-size:9.5px;">REPORT & LAB</span></div>
    <div class="steps-flex">
      <div class="step-card">
        <div class="step-num" style="color:#8B5CF6">STEP 08</div>
        <div class="step-title">Generate Court-Ready Report</div>
        <p class="step-desc">Outputs official forensic case summary with dual-signature endorsement blocks and statutory disclaimers.</p>
      </div>
      <div class="step-card">
        <div class="step-num" style="color:#8B5CF6">STEP 09</div>
        <div class="step-title">Laboratory Transfer (GC-MS)</div>
        <p class="step-desc">Physical sample transferred to certified forensic toxicology laboratory for definitive confirmatory analysis.</p>
      </div>
      <div class="step-card">
        <div class="step-num" style="color:#8B5CF6">STEP 10</div>
        <div class="step-title">Immutable Audit Archival</div>
        <p class="step-desc">Complete lifecycle audit trail preserved indefinitely for judicial discovery and compliance audits.</p>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""
render_html_to_png(d5_html, os.path.join(OUT_DIR, 'workflow_diagram.png'), width=1300, height=750)
print("All 5 SRS diagrams rendered successfully!")
