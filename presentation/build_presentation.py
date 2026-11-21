"""
FieldTest Companion - Professional Presentation Generator
Course: INT253 - Web Development in Python Using Django
Author: Ansh Sangwan
Generates FieldTest_Companion_Presentation.pptx (16:9 Widescreen, 15 Slides)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Initialize 16:9 Presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors
NAVY_BG = RGBColor(15, 23, 42)        # #0F172A
CARD_BG = RGBColor(30, 41, 59)        # #1E293B
CARD_BORDER = RGBColor(51, 65, 85)    # #334155
BLUE_ACCENT = RGBColor(37, 99, 235)   # #2563EB
BLUE_LIGHT = RGBColor(59, 130, 246)   # #3B82F6
CYAN_ACCENT = RGBColor(56, 189, 248)  # #38BDF8
TEXT_WHITE = RGBColor(255, 255, 255)
TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8
TEXT_LIGHT = RGBColor(203, 213, 225)  # #CBD5E1
SUCCESS_GREEN = RGBColor(16, 185, 129)# #10B981
WARNING_AMBER = RGBColor(245, 158, 11)# #F59E0B
DANGER_RED = RGBColor(239, 68, 68)    # #EF4444

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "presentation", "screenshots")

def set_slide_background(slide, color=NAVY_BG):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, title, category="INT253: WEB DEVELOPMENT IN PYTHON USING DJANGO"):
    # Category tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = CYAN_ACCENT

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.5), Inches(0.6))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

    # Divider line
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = CARD_BORDER
    div.line.fill.background()

def add_footer(slide, current_slide, total_slides=15):
    f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(8.0), Inches(0.3))
    tf_f = f_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "FieldTest Companion (DCDFT)  •  Ansh Sangwan  •  INT253 Final Viva"
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = TEXT_MUTED

    num_box = slide.shapes.add_textbox(Inches(11.5), Inches(7.05), Inches(1.0), Inches(0.3))
    tf_n = num_box.text_frame
    p_n = tf_n.paragraphs[0]
    p_n.alignment = PP_ALIGN.RIGHT
    p_n.text = f"{current_slide} / {total_slides}"
    p_n.font.size = Pt(9)
    p_n.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, title=None, bg_color=CARD_BG, border_color=CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()

    if title:
        t_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), Inches(0.4))
        tf = t_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

    return card

def add_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text.strip()


# ==============================================================================
# SLIDE 1: TITLE SLIDE
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)
set_slide_background(slide1)

# Subtle decorative background box
deco = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(11.733), Inches(5.1))
deco.fill.solid()
deco.fill.fore_color.rgb = RGBColor(20, 30, 48)
deco.line.color.rgb = CARD_BORDER
deco.line.width = Pt(1.5)

# Course badge
badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(1.7), Inches(5.2), Inches(0.42))
badge.fill.solid()
badge.fill.fore_color.rgb = BLUE_ACCENT
badge.line.fill.background()
tf_badge = badge.text_frame
p_b = tf_badge.paragraphs[0]
p_b.alignment = PP_ALIGN.CENTER
p_b.text = "INT253: WEB DEVELOPMENT IN PYTHON USING DJANGO"
p_b.font.size = Pt(11)
p_b.font.bold = True
p_b.font.color.rgb = TEXT_WHITE

# Main Title & Subtitle
tb_title = slide1.shapes.add_textbox(Inches(1.4), Inches(2.3), Inches(10.5), Inches(1.8))
tf_main = tb_title.text_frame
tf_main.word_wrap = True
p1 = tf_main.paragraphs[0]
p1.text = "FieldTest Companion"
p1.font.size = Pt(40)
p1.font.bold = True
p1.font.color.rgb = TEXT_WHITE

p2 = tf_main.add_paragraph()
p2.text = "Digital Companion for Drug Field Testing (DCDFT)"
p2.font.size = Pt(22)
p2.font.bold = True
p2.font.color.rgb = CYAN_ACCENT
p2.space_before = Pt(8)

p3 = tf_main.add_paragraph()
p3.text = "A full-stack forensic documentation system for presumptive test events, chain-of-custody tracking, and supervisor verification."
p3.font.size = Pt(13)
p3.font.color.rgb = TEXT_LIGHT
p3.space_before = Pt(12)

# Student Metadata Card
meta_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(4.5), Inches(5.2), Inches(1.3))
meta_card.fill.solid()
meta_card.fill.fore_color.rgb = CARD_BG
meta_card.line.color.rgb = CARD_BORDER
tf_meta = meta_card.text_frame
tf_meta.word_wrap = True
p_m1 = tf_meta.paragraphs[0]
p_m1.text = "STUDENT & SUBMISSION DETAILS"
p_m1.font.size = Pt(10)
p_m1.font.bold = True
p_m1.font.color.rgb = CYAN_ACCENT

p_m2 = tf_meta.add_paragraph()
p_m2.text = "Candidate Name: Ansh Sangwan"
p_m2.font.size = Pt(13)
p_m2.font.bold = True
p_m2.font.color.rgb = TEXT_WHITE
p_m2.space_before = Pt(4)

p_m3 = tf_meta.add_paragraph()
p_m3.text = "Project: drug_field_companion  •  Django 5.0.2 / Python 3.12"
p_m3.font.size = Pt(11)
p_m3.font.color.rgb = TEXT_MUTED

# Stack Badge Pills on Right
tech_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(4.5), Inches(5.0), Inches(1.3))
tech_card.fill.solid()
tech_card.fill.fore_color.rgb = CARD_BG
tech_card.line.color.rgb = CARD_BORDER
tf_tech = tech_card.text_frame
p_t1 = tf_tech.paragraphs[0]
p_t1.text = "SYSTEM HIGHLIGHTS"
p_t1.font.size = Pt(10)
p_t1.font.bold = True
p_t1.font.color.rgb = CYAN_ACCENT

p_t2 = tf_tech.add_paragraph()
p_t2.text = "• 8 Modular Django Apps  •  4-Role Access Control (RBAC)"
p_t2.font.size = Pt(11)
p_t2.font.color.rgb = TEXT_WHITE
p_t2.space_before = Pt(4)

p_t3 = tf_tech.add_paragraph()
p_t3.text = "• 20 Automated Tests Passed (AT-01 to AT-15)  •  Zero Failures"
p_t3.font.size = Pt(11)
p_t3.font.color.rgb = SUCCESS_GREEN

add_footer(slide1, 1)
add_speaker_notes(
    slide1,
    "Good morning, respected professors and examiner. My name is Ansh Sangwan, and today I am presenting my "
    "INT253 Django web application project titled FieldTest Companion – Digital Companion for Drug Field Testing. "
    "This web application serves as a comprehensive forensic documentation and workflow management platform for field officers, "
    "built entirely using Django 5 and Python 3.12 with clean role-based permissions, chain-of-custody tracking, and full automated testing."
)


# ==============================================================================
# SLIDE 2: INTRODUCTION & FORENSIC CONTEXT
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
set_slide_background(slide2)
add_header(slide2, "Introduction & Forensic Context", "Project Background")

# Left Column - What is Field Drug Testing & Scope
add_card(slide2, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.1), "Field Drug Testing & Digital Need")
left_tb = slide2.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.6), Inches(4.3))
tf_l = left_tb.text_frame
tf_l.word_wrap = True

def add_bullet(tf, title, desc, first=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.text = f"•  {title}: "
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    if not first:
        p.space_before = Pt(12)
    
    # Add regular description
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = TEXT_LIGHT

add_bullet(tf_l, "Presumptive Screening", "Field officers deploy colorimetric reagent kits and test strips during vehicular stops, border control, and scene inspections to quickly screen suspected materials.", True)
add_bullet(tf_l, "High Legal Stakes", "Every field test outcome directly impacts search warrants, detention, and forensic prosecution, requiring meticulous record-keeping from minute one.", False)
add_bullet(tf_l, "Paper-Based Vulnerability", "Conventional handwritten forms lead to lost notes, damaged papers, conflicting timestamps, and disputed evidence custody.", False)
add_bullet(tf_l, "Digital Companion Mission", "Provide an authoritative, role-governed web platform to standardize case data, enforce custody continuity, and produce audit-ready reports.", False)

# Right Column - Crucial Forensic Scope & Image
add_card(slide2, Inches(7.1), Inches(1.6), Inches(5.4), Inches(2.5), "Critical Safety & Forensic Scope", border_color=WARNING_AMBER)
scope_tb = slide2.shapes.add_textbox(Inches(7.3), Inches(2.2), Inches(5.0), Inches(1.8))
tf_s = scope_tb.text_frame
tf_s.word_wrap = True
ps1 = tf_s.paragraphs[0]
ps1.text = "⚠️ MANDATORY STATUTORY SCOPE NOTICE:"
ps1.font.size = Pt(11)
ps1.font.bold = True
ps1.font.color.rgb = WARNING_AMBER

ps2 = tf_s.add_paragraph()
ps2.text = "Field-test outcomes are presumptive screening results only. They do not establish the definitive identity of a substance. Confirmatory laboratory analysis (GC-MS / FTIR) is legally required."
ps2.font.size = Pt(11)
ps2.font.color.rgb = TEXT_WHITE
ps2.space_before = Pt(6)

ps3 = tf_s.add_paragraph()
ps3.text = "The platform stores descriptive metadata only—no chemical recipes, reagent formulas, or drug handling instructions are included."
ps3.font.size = Pt(10)
ps3.font.color.rgb = TEXT_MUTED
ps3.space_before = Pt(6)

# Right Column Lower Card - Landing Screenshot
add_card(slide2, Inches(7.1), Inches(4.3), Inches(5.4), Inches(2.4), "System Portal Overview")
landing_img = os.path.join(SCREENSHOTS_DIR, "landing.png")
if os.path.exists(landing_img):
    slide2.shapes.add_picture(landing_img, Inches(7.3), Inches(4.8), width=Inches(5.0), height=Inches(1.75))

add_footer(slide2, 2)
add_speaker_notes(
    slide2,
    "Field drug testing is conducted by authorized law enforcement personnel during field operations using presumptive test kits. "
    "A fundamental forensic concept in this project is that field tests are strictly presumptive screening outcomes—they never replace certified "
    "laboratory instrumentation such as GC-MS. Therefore, our Django application prominently displays persistent disclaimers across all screens and "
    "focuses entirely on structured administrative documentation and evidence traceability without providing chemical recipes."
)


# ==============================================================================
# SLIDE 3: PROBLEM STATEMENT & FLOWCHART
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
set_slide_background(slide3)
add_header(slide3, "Problem Statement: Challenges in Field Documentation", "Current Industry Challenges")

# Top 7 Problem Highlights
add_card(slide3, Inches(0.8), Inches(1.6), Inches(11.733), Inches(1.9), "Key Vulnerabilities in Conventional Field Drug Testing")
prob_tb = slide3.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(11.3), Inches(1.3))
tf_p = prob_tb.text_frame
tf_p.word_wrap = True

p_p1 = tf_p.paragraphs[0]
p_p1.text = "1. Paper Fragmentation: Notes scribbled on scene risk loss, water damage, or illegibility during court presentation."
p_p1.font.size = Pt(11)
p_p1.font.color.rgb = TEXT_LIGHT

p_p2 = tf_p.add_paragraph()
p_p2.text = "2. Chain-of-Custody Gaps: Transfers between officers and locker facilities lack verified timestamps and numbered seal tracking."
p_p2.font.size = Pt(11)
p_p2.font.color.rgb = TEXT_LIGHT
p_p2.space_before = Pt(4)

p_p3 = tf_p.add_paragraph()
p_p3.text = "3. Expired Kit Errors: Unnoticed deployment of expired test kits invalidates presumptive results in judicial hearings."
p_p3.font.size = Pt(11)
p_p3.font.color.rgb = TEXT_LIGHT
p_p3.space_before = Pt(4)

p_p4 = tf_p.add_paragraph()
p_p4.text = "4. Delayed Reviews & Manual Reports: Hand-compiling dossiers delays supervisor sign-offs and laboratory dispatch."
p_p4.font.size = Pt(11)
p_p4.font.color.rgb = TEXT_LIGHT
p_p4.space_before = Pt(4)

# Flowchart Card Below
add_card(slide3, Inches(0.8), Inches(3.7), Inches(11.733), Inches(3.0), "The Cascading Impact of Manual Documentation")

flow_steps = [
    ("Manual Documentation", "Handwritten on-scene notes & physical paperwork", DANGER_RED),
    ("Fragmented Records", "Dispersed logs across multiple notebooks & lockers", WARNING_AMBER),
    ("Tracking Difficulties", "Unclear specimen possession & seal status", WARNING_AMBER),
    ("Limited Traceability", "Lack of immutable audit trail & timestamp verification", DANGER_RED),
    ("Verification Failure", "Evidence challenged or dismissed in judicial review", DANGER_RED),
]

node_width = Inches(2.05)
node_height = Inches(1.6)
start_x = Inches(1.05)
y_pos = Inches(4.3)
spacing = Inches(2.35)

for i, (stitle, sdesc, scolor) in enumerate(flow_steps):
    x = start_x + (i * spacing)
    # Box
    box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y_pos, node_width, node_height)
    box.fill.solid()
    box.fill.fore_color.rgb = CARD_BG
    box.line.color.rgb = scolor
    box.line.width = Pt(1.5)
    
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"Step {i+1}"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = scolor
    
    p2 = tf.add_paragraph()
    p2.text = stitle
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = sdesc
    p3.font.size = Pt(9)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(4)

    # Arrow connector except last
    if i < len(flow_steps) - 1:
        arrow = slide3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x + node_width + Inches(0.05), y_pos + Inches(0.65), Inches(0.2), Inches(0.3))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = CYAN_ACCENT
        arrow.line.fill.background()

add_footer(slide3, 3)
add_speaker_notes(
    slide3,
    "The core problem we are addressing is the vulnerability of paper-based field drug records. "
    "As illustrated in the flowchart, manual notes lead to fragmented evidence logs, tracking ambiguity, and a compromised chain of custody. "
    "If an officer cannot prove who possessed a specimen at 10:15 AM or whether an intact seal was verified, the entire evidence package can be thrown out of court. "
    "FieldTest Companion was built to solve every single link in this breakdown."
)


# ==============================================================================
# SLIDE 4: PROPOSED SOLUTION & FEATURE MAP
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
set_slide_background(slide4)
add_header(slide4, "Proposed Solution: FieldTest Companion", "Solution Overview")

# 8 Features in a 4x2 Grid on Left / Center
features = [
    ("Digital Case Management", "Auto-generated CASE-YYYY-XXXX references with status state machines.", "bi-folder2"),
    ("Sample Registration", "Unique SMP-YYYY-XXXX codes, packaging types, and tamper-seal verification.", "bi-box-seam"),
    ("Field-Test Documentation", "Controlled 5-result categories, kit lot numbers, and expiry date validation.", "bi-flask"),
    ("Chain of Custody Ledger", "Append-only chronological handover ledger with out-of-sequence flags.", "bi-link-45deg"),
    ("Private Evidence Vault", "MIME/extension validated uploads with authenticated FileResponse delivery.", "bi-shield-lock"),
    ("Supervisor Review Gate", "Submitted queue requiring mandatory actionable review comments.", "bi-clipboard-check"),
    ("Print-Ready Summary Reports", "Official print-styled reports with specimen tables and dual signatures.", "bi-printer"),
    ("Role-Based Access (RBAC)", "Field Officer, Supervisor, Admin, and Auditor server-enforced controls.", "bi-people"),
]

card_w = Inches(3.65)
card_h = Inches(1.15)
xs = [Inches(0.8), Inches(4.7), Inches(8.6)]

for idx, (ftitle, fdesc, _) in enumerate(features[:6]):
    col = idx % 2
    row = idx // 2
    x = Inches(0.8) + (col * Inches(3.8))
    y = Inches(1.6) + (row * Inches(1.3))
    
    c = add_card(slide4, x, y, Inches(3.6), card_h, ftitle)
    tb = slide4.shapes.add_textbox(x + Inches(0.2), y + Inches(0.48), Inches(3.2), Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = fdesc
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_LIGHT

# Add Features 7 & 8 below
c7 = add_card(slide4, Inches(0.8), Inches(5.5), Inches(3.6), card_h, features[6][0])
tb7 = slide4.shapes.add_textbox(Inches(1.0), Inches(5.98), Inches(3.2), Inches(0.6))
tf7 = tb7.text_frame
tf7.word_wrap = True
tf7.paragraphs[0].text = features[6][1]
tf7.paragraphs[0].font.size = Pt(10)
tf7.paragraphs[0].font.color.rgb = TEXT_LIGHT

c8 = add_card(slide4, Inches(4.6), Inches(5.5), Inches(3.6), card_h, features[7][0])
tb8 = slide4.shapes.add_textbox(Inches(4.8), Inches(5.98), Inches(3.2), Inches(0.6))
tf8 = tb8.text_frame
tf8.word_wrap = True
tf8.paragraphs[0].text = features[7][1]
tf8.paragraphs[0].font.size = Pt(10)
tf8.paragraphs[0].font.color.rgb = TEXT_LIGHT

# Right Card - Embedded Real Dashboard Screenshot
add_card(slide4, Inches(8.4), Inches(1.6), Inches(4.133), Inches(5.05), "Live Application Dashboard")
dash_img = os.path.join(SCREENSHOTS_DIR, "dashboard.png")
if os.path.exists(dash_img):
    slide4.shapes.add_picture(dash_img, Inches(8.55), Inches(2.2), width=Inches(3.833), height=Inches(4.25))

add_footer(slide4, 4)
add_speaker_notes(
    slide4,
    "FieldTest Companion delivers a full-stack digital solution mapped across 8 core capabilities. "
    "Officers can register physical samples, document presumptive screening reactions, maintain unbroken custody timelines, "
    "and upload supporting photos directly into a private vault. As shown in the live dashboard screenshot on the right, "
    "operational KPIs, active cases, and pending reviews are presented in a clean, forensic navy interface built with Bootstrap 5 and custom CSS."
)


# ==============================================================================
# SLIDE 5: SYSTEM WORKFLOW FLOWCHART
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
set_slide_background(slide5)
add_header(slide5, "End-to-End Operational Workflow", "System Execution Flow")

add_card(slide5, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), "Field Case-to-Review Lifecycle Flowchart")

# Flowchart layout:
# Row 1: Field Officer Steps (Left to Right)
# Row 2: Submission & Supervisor Decision (Branching)

steps_r1 = [
    ("1. Officer Login", "Authenticate via secure session", BLUE_ACCENT),
    ("2. Create Case", "Auto-reference CASE-YYYY-XXXX", BLUE_ACCENT),
    ("3. Register Sample", "Record seal & physical condition", BLUE_ACCENT),
    ("4. Document Test", "Kit metadata, expiry check & result", BLUE_ACCENT),
    ("5. Log Custody", "Append-only handover & locker log", BLUE_ACCENT),
]

w_box = Inches(2.1)
h_box = Inches(1.4)
x_start = Inches(1.1)
y_r1 = Inches(2.2)

for i, (title, sub, col) in enumerate(steps_r1):
    x = x_start + (i * Inches(2.35))
    b = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y_r1, w_box, h_box)
    b.fill.solid()
    b.fill.fore_color.rgb = CARD_BG
    b.line.color.rgb = col
    b.line.width = Pt(1.5)
    
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(4)

    if i < len(steps_r1) - 1:
        arr = slide5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x + w_box + Inches(0.04), y_r1 + Inches(0.55), Inches(0.17), Inches(0.3))
        arr.fill.solid()
        arr.fill.fore_color.rgb = CYAN_ACCENT
        arr.line.fill.background()

# Down connector from Step 5 to Step 6
down_arr = slide5.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(10.5) + Inches(0.9), y_r1 + h_box + Inches(0.05), Inches(0.3), Inches(0.2))
down_arr.fill.solid()
down_arr.fill.fore_color.rgb = CYAN_ACCENT
down_arr.line.fill.background()

# Row 2: Submit -> Review -> Branches
# Step 6: Upload & Submit
b6 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(3.9), Inches(2.8), Inches(1.2))
b6.fill.solid()
b6.fill.fore_color.rgb = CARD_BG
b6.line.color.rgb = BLUE_ACCENT
b6.line.width = Pt(1.5)
tf6 = b6.text_frame
tf6.word_wrap = True
tf6.paragraphs[0].text = "6. Evidence & Submit"
tf6.paragraphs[0].font.size = Pt(11)
tf6.paragraphs[0].font.bold = True
tf6.paragraphs[0].font.color.rgb = TEXT_WHITE
p6_2 = tf6.add_paragraph()
p6_2.text = "Attach photos/PDFs. POST /submit locks editing & creates AuditEvent."
p6_2.font.size = Pt(9)
p6_2.font.color.rgb = TEXT_MUTED

# Left Arrow from Step 6 to Step 7 (Review Decision)
arr_left = slide5.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Inches(7.8), Inches(4.35), Inches(0.35), Inches(0.3))
arr_left.fill.solid()
arr_left.fill.fore_color.rgb = CYAN_ACCENT
arr_left.line.fill.background()

# Step 7: Supervisor Review Decision Diamond/Box
b7 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.0), Inches(3.9), Inches(2.6), Inches(1.2))
b7.fill.solid()
b7.fill.fore_color.rgb = CARD_BG
b7.line.color.rgb = WARNING_AMBER
b7.line.width = Pt(2)
tf7 = b7.text_frame
tf7.word_wrap = True
tf7.paragraphs[0].text = "7. Supervisor Decision"
tf7.paragraphs[0].font.size = Pt(11)
tf7.paragraphs[0].font.bold = True
tf7.paragraphs[0].font.color.rgb = WARNING_AMBER
p7_2 = tf7.add_paragraph()
p7_2.text = "Evaluate completeness, kit validity & custody sequence."
p7_2.font.size = Pt(9)
p7_2.font.color.rgb = TEXT_LIGHT

# Decision Branches (Left: Approved, Bottom/Left: Changes Requested)
# Branch A: Approved (Green)
b_app = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(3.9), Inches(3.5), Inches(1.2))
b_app.fill.solid()
b_app.fill.fore_color.rgb = RGBColor(6, 78, 59)
b_app.line.color.rgb = SUCCESS_GREEN
b_app.line.width = Pt(1.5)
tf_app = b_app.text_frame
tf_app.word_wrap = True
tf_app.paragraphs[0].text = "✓ APPROVED (Status: Approved)"
tf_app.paragraphs[0].font.size = Pt(11)
tf_app.paragraphs[0].font.bold = True
tf_app.paragraphs[0].font.color.rgb = TEXT_WHITE
p_app2 = tf_app.add_paragraph()
p_app2.text = "Locks case permanently. Authorizes official Print-Ready Case Report & laboratory dispatch."
p_app2.font.size = Pt(9)
p_app2.font.color.rgb = TEXT_LIGHT

arr_app = slide5.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Inches(4.7), Inches(4.35), Inches(0.2), Inches(0.3))
arr_app.fill.solid()
arr_app.fill.fore_color.rgb = SUCCESS_GREEN
arr_app.line.fill.background()

# Branch B: Changes Requested (Red) Below
b_chg = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.0), Inches(5.4), Inches(6.5), Inches(1.0))
b_chg.fill.solid()
b_chg.fill.fore_color.rgb = RGBColor(127, 29, 29)
b_chg.line.color.rgb = DANGER_RED
b_chg.line.width = Pt(1.5)
tf_chg = b_chg.text_frame
tf_chg.word_wrap = True
tf_chg.paragraphs[0].text = "↩ CHANGES REQUESTED (Mandatory Supervisory Comment Enforced)"
tf_chg.paragraphs[0].font.size = Pt(10)
tf_chg.paragraphs[0].font.bold = True
tf_chg.paragraphs[0].font.color.rgb = TEXT_WHITE
p_chg2 = tf_chg.add_paragraph()
p_chg2.text = "Case unlocks for officer correction. Officer remedies identified deficiency and resubmits for review."
p_chg2.font.size = Pt(9)
p_chg2.font.color.rgb = TEXT_LIGHT

add_footer(slide5, 5)
add_speaker_notes(
    slide5,
    "This slide illustrates the primary workflow from on-scene creation to supervisory sign-off. "
    "A Field Officer creates a case, secures samples, records presumptive results, and maintains the custody ledger. "
    "Submitting the case locks ordinary editing and triggers an audit event. The supervisor then reviews the complete record. "
    "If corrections are needed, a comment is strictly mandatory before returning the case. Once approved, the record is locked and can be exported as a forensic report."
)


# ==============================================================================
# SLIDE 6: USER ROLES & ACCESS CONTROL MATRIX
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
set_slide_background(slide6)
add_header(slide6, "User Roles & Permission Governance (RBAC)", "Role-Based Access Control")

roles = [
    (
        "Field Officer",
        BLUE_ACCENT,
        [
            ("Primary Purpose", "On-scene operational recording"),
            ("Create Cases", "Yes (Draft status)"),
            ("Register Samples", "Yes (Under assigned cases)"),
            ("Record Tests/Custody", "Yes (With validation checks)"),
            ("Submit Dossier", "Yes (Transfers to Supervisor)"),
            ("Approve Dossier", "No (Access Denied)"),
            ("User Management", "No (HTTP 403 Forbidden)"),
        ]
    ),
    (
        "Supervisor",
        WARNING_AMBER,
        [
            ("Primary Purpose", "Quality verification & oversight"),
            ("Create Cases", "Yes (Authorised)"),
            ("Register Samples", "Yes (Authorised)"),
            ("Record Tests/Custody", "Yes (Authorised)"),
            ("Submit Dossier", "Yes (Authorised)"),
            ("Approve Dossier", "Yes (Approve / Return)"),
            ("User Management", "No (HTTP 403 Forbidden)"),
        ]
    ),
    (
        "Administrator",
        DANGER_RED,
        [
            ("Primary Purpose", "System governance & credentialing"),
            ("Create Cases", "Yes (Full admin override)"),
            ("Register Samples", "Yes (Full admin override)"),
            ("Record Tests/Custody", "Yes (Full admin override)"),
            ("Submit Dossier", "No by default (Auditing rule)"),
            ("Approve Dossier", "No (Segregation of duties)"),
            ("User Management", "Yes (Full CRUD & Role Assign)"),
        ]
    ),
    (
        "Read-only User",
        TEXT_MUTED,
        [
            ("Primary Purpose", "Auditing & compliance inspection"),
            ("Create Cases", "No (Read-only access)"),
            ("Register Samples", "No (Read-only access)"),
            ("Record Tests/Custody", "No (Read-only access)"),
            ("Submit Dossier", "No (Read-only access)"),
            ("Approve Dossier", "No (Read-only access)"),
            ("User Management", "No (Read-only access)"),
        ]
    ),
]

col_w = Inches(2.78)
start_x = Inches(0.8)
for i, (rname, rcolor, rperms) in enumerate(roles):
    x = start_x + (i * Inches(2.98))
    # Card
    add_card(slide6, x, Inches(1.6), col_w, Inches(4.3), rname, border_color=rcolor)
    tb = slide6.shapes.add_textbox(x + Inches(0.15), Inches(2.15), col_w - Inches(0.3), Inches(3.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    for j, (pname, pval) in enumerate(rperms):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = f"{pname}:"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        if j > 0:
            p.space_before = Pt(5)
        
        run = p.add_run()
        run.text = f" {pval}"
        run.font.bold = False
        run.font.color.rgb = TEXT_WHITE if "Yes" in pval else (DANGER_RED if "No" in pval else TEXT_MUTED)

# Implementation Note Box Below
add_card(slide6, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.85), bg_color=CARD_BG, border_color=CARD_BORDER)
tb_note = slide6.shapes.add_textbox(Inches(1.0), Inches(6.12), Inches(11.3), Inches(0.7))
tf_n = tb_note.text_frame
tf_n.word_wrap = True
pn = tf_n.paragraphs[0]
pn.text = "Django Implementation Detail: "
pn.font.size = Pt(10)
pn.font.bold = True
pn.font.color.rgb = CYAN_ACCENT
rn = pn.add_run()
rn.text = "Role permissions are enforced server-side using Django Groups and custom view decorators (@role_required, @supervisor_required, @field_officer_required). Access is never merely hidden in HTML templates—unauthorized GET/POST requests trigger an immediate HTTP 403 PermissionDenied response."
rn.font.bold = False
rn.font.color.rgb = TEXT_LIGHT

add_footer(slide6, 6)
add_speaker_notes(
    slide6,
    "The application implements four distinct user roles using Django's built-in User and Group framework. "
    "A Field Officer records field data and submits cases; a Supervisor reviews and signs off; an Administrator manages users, "
    "test-kit catalogue metadata, and Django Admin; while a Read-only user can inspect records for audit compliance. "
    "Critically, these permissions are enforced in backend Python view decorators, ensuring that hiding buttons on the frontend is not the sole security layer."
)


# ==============================================================================
# SLIDE 7: SYSTEM ARCHITECTURE
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
set_slide_background(slide7)
add_header(slide7, "System Architecture & Request Lifecycle", "Technical Design")

# 4 Architectural Layers as Horizontal Tier Cards
tiers = [
    (
        "Tier 1: Presentation Layer",
        "HTML5  •  Bootstrap 5.3.3  •  Custom Forensic CSS  •  Responsive JavaScript",
        "Renders forensic dashboard, mobile-responsive sidebar, status badges, timelines, and printable case reports.",
        BLUE_ACCENT
    ),
    (
        "Tier 2: Application & Logic Layer",
        "Django URL Routing  •  View Handlers (FBVs/CBVs)  •  ModelForms  •  RBAC Decorators",
        "Processes HTTP GET/POST requests, enforces CSRF validation, validates business rules, and controls status transitions.",
        CYAN_ACCENT
    ),
    (
        "Tier 3: Modular Domain Apps",
        "8 Dedicated Django Apps (Core, Accounts, Cases, Testing, Custody, Evidence, Reviews, Audit)",
        "Decoupled business logic ensuring strict separation of concerns, isolated testing, and high maintainability.",
        BLUE_LIGHT
    ),
    (
        "Tier 4: Data & Persistence Layer",
        "Django ORM  •  SQLite Database  •  Private Evidence Vault Filesystem",
        "Enforces relational integrity, cascading rules (PROTECT / CASCADE), indexing, and authenticated file delivery.",
        SUCCESS_GREEN
    )
]

y_pos = Inches(1.6)
tier_h = Inches(1.15)
for i, (tname, tstack, tdesc, tcol) in enumerate(tiers):
    c = add_card(slide7, Inches(0.8), y_pos, Inches(11.733), tier_h, border_color=tcol)
    tb = slide7.shapes.add_textbox(Inches(1.0), y_pos + Inches(0.12), Inches(11.3), Inches(0.95))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = tname
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = tcol
    
    run_s = p1.add_run()
    run_s.text = f"   [{tstack}]"
    run_s.font.size = Pt(10)
    run_s.font.bold = False
    run_s.font.color.rgb = TEXT_MUTED
    
    p2 = tf.add_paragraph()
    p2.text = tdesc
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_LIGHT
    p2.space_before = Pt(4)
    
    # Down arrow between tiers
    if i < len(tiers) - 1:
        arr = slide7.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.4), y_pos + tier_h + Inches(0.02), Inches(0.5), Inches(0.16))
        arr.fill.solid()
        arr.fill.fore_color.rgb = CYAN_ACCENT
        arr.line.fill.background()
        
    y_pos += Inches(1.35)

add_footer(slide7, 7)
add_speaker_notes(
    slide7,
    "Here we see the 4-tier architectural design of FieldTest Companion following Django's Model-View-Template pattern. "
    "User requests enter Tier 1 through the browser, passing through Django's security middleware in Tier 2 for CSRF verification and role checking. "
    "The request is dispatched to one of the 8 modular applications in Tier 3, which executes the business logic. "
    "Finally, Tier 4 uses the Django ORM to communicate with SQLite and manages private file storage in the evidence vault."
)


# ==============================================================================
# SLIDE 8: DJANGO APPLICATION STRUCTURE (8 APPS)
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
set_slide_background(slide8)
add_header(slide8, "Modular Project Structure: 8 Django Applications", "Codebase Organization")

apps_data = [
    ("core", "Home, dashboard metrics, landing portal, custom error handlers (403, 404, 500), load_demo_data command."),
    ("accounts", "User login/logout, session management, role group assignment, and administrative user controls."),
    ("cases", "CaseRecord & Sample CRUD, unique reference generator, search & date filtering, print-friendly reports."),
    ("testing_records", "TestKit approved catalogue metadata, TestEvent documentation, kit expiry warning logic."),
    ("custody", "Chronological CustodyEvent ledger, handover tracking, seal integrity checks, out-of-sequence flags."),
    ("evidence", "Private evidence vault, server-side MIME & size validation, authenticated FileResponse streaming."),
    ("reviews", "Supervisor review queue, Approve / Return state transitions, mandatory actionable comment validation."),
    ("auditlog", "Immutable AuditEvent logging capturing actor, action, object_type, summary, and client IP."),
]

card_w = Inches(2.78)
card_h = Inches(2.1)

for idx, (aname, adesc) in enumerate(apps_data):
    col = idx % 4
    row = idx // 4
    x = Inches(0.8) + (col * Inches(2.98))
    y = Inches(1.6) + (row * Inches(2.3))
    
    add_card(slide8, x, y, col_w, card_h, f"app: {aname}")
    tb = slide8.shapes.add_textbox(x + Inches(0.15), y + Inches(0.55), col_w - Inches(0.3), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = adesc
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_LIGHT

# Why Modular Banner
add_card(slide8, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.65), bg_color=CARD_BG, border_color=BLUE_ACCENT)
tb_b = slide8.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.5))
tf_b = tb_b.text_frame
tf_b.word_wrap = True
pb = tf_b.paragraphs[0]
pb.text = "Architectural Advantage: "
pb.font.size = Pt(10)
pb.font.bold = True
pb.font.color.rgb = CYAN_ACCENT
rb = pb.add_run()
rb.text = "Decomposing the monolith into 8 domain apps prevents bloated models, simplifies automated unit testing, guarantees clear separation of concerns, and perfectly adheres to the INT253 syllabus standards."
rb.font.bold = False
rb.font.color.rgb = TEXT_LIGHT

add_footer(slide8, 8)
add_speaker_notes(
    slide8,
    "Rather than writing a monolithic application in a single folder, the project is structured into eight distinct Django apps. "
    "For example, custody is separated from testing_records, and evidence handling is kept independent from supervisory reviews. "
    "This modularity provides high maintainability, allows isolated automated unit testing for each feature, and demonstrates standard professional Django engineering."
)


# ==============================================================================
# SLIDE 9: DATABASE DESIGN & ENTITY RELATIONSHIP DIAGRAM (ERD)
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
set_slide_background(slide9)
add_header(slide9, "Database Schema & Entity Relationship Diagram (ERD)", "Data Architecture")

add_card(slide9, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1), "Relational Model Architecture (Django ORM & SQLite)")

# Models as structured boxes representing the exact schema in models.py
models_layout = [
    # (Title, Fields text, x, y, w, h, Border Color)
    (
        "User (auth.User)",
        "PK id (IntegerField)\n• username (CharField)\n• is_staff, is_active\n• groups (ManyToMany)",
        Inches(1.1), Inches(2.2), Inches(2.6), Inches(1.3), BLUE_ACCENT
    ),
    (
        "CaseRecord (cases)",
        "PK id (BigAutoField)\n• case_reference (Unique)\n• title, incident_datetime\n• status (Draft..Approved)\nFK created_by -> User\nFK assigned_to -> User",
        Inches(4.2), Inches(2.2), Inches(2.8), Inches(2.0), CYAN_ACCENT
    ),
    (
        "Sample (cases)",
        "PK id (BigAutoField)\n• sample_code (Unique)\n• collected_at, description\n• seal_reference, condition\nFK case -> CaseRecord\nFK created_by -> User",
        Inches(7.5), Inches(2.2), Inches(2.8), Inches(2.0), SUCCESS_GREEN
    ),
    (
        "TestKit (testing_records)",
        "PK id (BigAutoField)\n• name, manufacturer\n• catalogue_reference (Uniq)\n• active (BooleanField)\n• general_safety_note",
        Inches(10.6), Inches(2.2), Inches(1.7), Inches(1.8), WARNING_AMBER
    ),
    (
        "ReviewRecord (reviews)",
        "PK id (BigAutoField)\n• decision (Approve/Reject)\n• comment (TextField)\n• reviewed_at\nFK case -> CaseRecord\nFK reviewer -> User",
        Inches(1.1), Inches(4.5), Inches(2.6), Inches(1.7), WARNING_AMBER
    ),
    (
        "EvidenceFile (evidence)",
        "PK id (BigAutoField)\n• file (FileField - Vault)\n• original_filename, size\n• caption, uploaded_at\nFK case -> CaseRecord\nFK sample -> Sample (Opt)\nFK uploaded_by -> User",
        Inches(4.2), Inches(4.5), Inches(2.8), Inches(1.9), BLUE_LIGHT
    ),
    (
        "CustodyEvent (custody)",
        "PK id (BigAutoField)\n• event_type, event_at\n• from_person, to_person\n• seal_reference, location\n• is_out_of_sequence (Bool)\nFK sample -> Sample\nFK recorded_by -> User",
        Inches(7.5), Inches(4.5), Inches(2.8), Inches(2.0), DANGER_RED
    ),
    (
        "TestEvent (testing_records)",
        "PK id (BigAutoField)\n• result_category (Choices)\n• kit_lot_number, expiry\n• observation_notes\nFK sample -> Sample\nFK kit -> TestKit\nFK performed_by -> User",
        Inches(10.6), Inches(4.3), Inches(1.7), Inches(2.2), CYAN_ACCENT
    ),
]

for mtitle, mfields, mx, my, mw, mh, mcol in models_layout:
    mb = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mx, my, mw, mh)
    mb.fill.solid()
    mb.fill.fore_color.rgb = CARD_BG
    mb.line.color.rgb = mcol
    mb.line.width = Pt(1.5)
    
    tf = mb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = mtitle
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = mcol
    
    p2 = tf.add_paragraph()
    p2.text = mfields
    p2.font.size = Pt(8)
    p2.font.color.rgb = TEXT_LIGHT
    p2.space_before = Pt(3)

add_footer(slide9, 9)
add_speaker_notes(
    slide9,
    "The database design implements a robust relational schema with explicit constraints and cascading policies. "
    "A CaseRecord has a one-to-many relationship with physical Samples. Each Sample connects to multiple TestEvents and CustodyEvents. "
    "Crucially, ForeignKeys to User records use on_delete=PROTECT for operational personnel to prevent accidental or malicious deletion of forensic history. "
    "The schema was fully generated using Django migrations and operates seamlessly on SQLite."
)


# ==============================================================================
# SLIDE 10: CORE FUNCTIONAL MODULES
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
set_slide_background(slide10)
add_header(slide10, "Core Functional Modules: Case, Sample, Test & Custody", "Operational Implementation")

# 4 Quadrants: 2 Top, 2 Bottom
quadrants = [
    (
        "A. Case Management",
        "• Auto-generates sequential case reference (CASE-YYYY-XXXX).\n• Keyword search across reference, title, location, description.\n• Dynamic filtering by status and incident date range.\n• Server-side pagination (10 cases per page).\n• State machine locking preventing edits after submission.",
        Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.3),
        "case_list.png"
    ),
    (
        "B. Sample Management",
        "• Unique sequential sample codes (SMP-YYYY-XXXX).\n• Mandatory packaging, integrity seal, and condition capture.\n• Strict duplicate sample code prevention via form validation.\n• Automatically generates initial scene Collection custody event.\n• Linked specimen ledger tracking all related tests & custody.",
        Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.3),
        "sample_detail.png"
    ),
    (
        "C. Field-Test Documentation",
        "• Links to approved commercial TestKit catalogue entries.\n• Controlled 5-result categories (Presumptive pos/neg, etc.).\n• Server-side lot expiration safeguard requiring limitations note.\n• Objective sensory observation narrative capture.\n• Prominent persistent presumptive disclaimer on all views.",
        Inches(0.8), Inches(4.2), Inches(5.6), Inches(2.5),
        "test_event_form.png"
    ),
    (
        "D. Chain-of-Custody Tracking",
        "• Append-only chronological handover & storage tracking.\n• Records from/to parties, locker references, and verified seals.\n• Automatic out-of-sequence detection if retroactive date logged.\n• Visual vertical timeline with distinct state badges.\n• Protected deletion policy preserving historical evidentiary integrity.",
        Inches(6.8), Inches(4.2), Inches(5.7), Inches(2.5),
        "custody_timeline.png"
    ),
]

for qtitle, qdesc, qx, qy, qw, qh, qimg in quadrants:
    add_card(slide10, qx, qy, qw, qh, qtitle)
    tb = slide10.shapes.add_textbox(qx + Inches(0.2), qy + Inches(0.48), qw - Inches(2.1), qh - Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = qdesc
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_LIGHT

    # Small thumbnail screenshot in card
    img_path = os.path.join(SCREENSHOTS_DIR, qimg)
    if os.path.exists(img_path):
        slide10.shapes.add_picture(img_path, qx + qw - Inches(1.85), qy + Inches(0.48), width=Inches(1.7), height=Inches(1.6))

add_footer(slide10, 10)
add_speaker_notes(
    slide10,
    "This slide details the four foundational operational modules. "
    "In Case Management, cases receive automatically generated unique references and state machine locking. "
    "Sample registration enforces unique codes and seal numbers. In Field-Test Documentation, officers record presumptive outcomes with kit lot expiry checks. "
    "Finally, Chain of Custody provides an append-only timeline that flags any retroactive or out-of-sequence entries, ensuring full forensic transparency."
)


# ==============================================================================
# SLIDE 11: EVIDENCE, REVIEW & REPORTING
# ==============================================================================
slide11 = prs.slides.add_slide(blank_layout)
set_slide_background(slide11)
add_header(slide11, "Evidence Vault, Supervisor Review & Reporting", "Verification & Delivery")

# Left Column - Process Explanation
add_card(slide11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1), "Connected Forensic Verification Lifecycle")
tb_e = slide11.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.3))
tf_e = tb_e.text_frame
tf_e.word_wrap = True

add_bullet(tf_e, "1. Private Evidence Vault", "Secure upload validation strictly permitting .jpg, .jpeg, .png, and .pdf up to 10 MB. Files are stored in a private directory with no public URL access.", True)
add_bullet(tf_e, "2. Authenticated File Delivery", "Evidence is served exclusively through a permission-checked Django FileResponse endpoint verifying case access rights before streaming bytes.", False)
add_bullet(tf_e, "3. Supervisory Review Gate", "Submitted cases land in the supervisor review queue. Supervisors evaluate documentation completeness, test validity, and unbroken custody continuity.", False)
add_bullet(tf_e, "4. Mandatory Revision Comments", "If returning a case for corrections, the system enforces a descriptive comment detailing what must be amended before resubmission.", False)
add_bullet(tf_e, "5. Official Print-Ready Report", "Approved cases generate a print-styled forensic summary with dual-signature verification blocks, custody logs, and prominent disclaimers.", False)

# Right Column - Review & Report Screenshots
add_card(slide11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.4), "Supervisory Review Queue")
rev_img = os.path.join(SCREENSHOTS_DIR, "review_queue.png")
if os.path.exists(rev_img):
    slide11.shapes.add_picture(rev_img, Inches(7.0), Inches(2.1), width=Inches(5.3), height=Inches(1.75))

add_card(slide11, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.4), "Print-Ready Forensic Summary Report")
rep_img = os.path.join(SCREENSHOTS_DIR, "case_report.png")
if os.path.exists(rep_img):
    slide11.shapes.add_picture(rep_img, Inches(7.0), Inches(4.8), width=Inches(5.3), height=Inches(1.75))

add_footer(slide11, 11)
add_speaker_notes(
    slide11,
    "Evidence handling, review, and reporting form the final stage of the application workflow. "
    "Evidence files such as seal photographs are stored in a private vault and delivered only through authenticated Django FileResponse views. "
    "Supervisors access a dedicated review queue to approve cases or return them with mandatory written comments. "
    "Once approved, the system generates an official print-friendly report with embedded print CSS, complete custody tables, and signature blocks."
)


# ==============================================================================
# SLIDE 12: SECURITY & DATA INTEGRITY CONTROLS
# ==============================================================================
slide12 = prs.slides.add_slide(blank_layout)
set_slide_background(slide12)
add_header(slide12, "Security Architecture & Data Integrity Safeguards", "System Controls")

# 6 Security Cards in 2x3 layout
sec_cards = [
    (
        "Authentication & Hashing",
        "• Django built-in auth with PBKDF2 password hashing & SHA-256.\n• Session-based cookie authentication with HTTPOnly flags.\n• Inactive user account locking and secure logout via POST.",
        BLUE_ACCENT
    ),
    (
        "CSRF & Injection Defense",
        "• Django CsrfViewMiddleware enforced on all state mutations.\n• {% csrf_token %} required on every internal POST form.\n• Django ORM parameterization prevents SQL injection.",
        CYAN_ACCENT
    ),
    (
        "Server-Side Role Protection",
        "• Role decorators (@role_required, @supervisor_required).\n• Backend PermissionDenied (HTTP 403) exceptions.\n• Queryset scoping preventing unauthorized record exposure.",
        BLUE_LIGHT
    ),
    (
        "Private Media Vault",
        "• No public MEDIA_URL exposure for evidence files.\n• Strict server-side extension & MIME type whitelist.\n• Authenticated FileResponse stream with Content-Disposition.",
        SUCCESS_GREEN
    ),
    (
        "Immutable Audit Logging",
        "• Automated AuditEvent recorded on all key mutations.\n• Stores actor, action category, target entity, and client IP.\n• Django Admin prevents modification or deletion of audit logs.",
        WARNING_AMBER
    ),
    (
        "State Integrity & Disclaimers",
        "• State machine locks approved and submitted case records.\n• Append-only custody ledger flags out-of-sequence entries.\n• Mandatory statutory disclaimer on all forms and reports.",
        DANGER_RED
    ),
]

card_w = Inches(3.65)
card_h = Inches(2.2)

for idx, (stitle, sdesc, scol) in enumerate(sec_cards):
    col = idx % 3
    row = idx // 3
    x = Inches(0.8) + (col * Inches(3.95))
    y = Inches(1.6) + (row * Inches(2.45))
    
    add_card(slide12, x, y, card_w, card_h, stitle, border_color=scol)
    tb = slide12.shapes.add_textbox(x + Inches(0.18), y + Inches(0.55), card_w - Inches(0.36), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = sdesc
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_LIGHT

# Safety disclaimer footer note
add_card(slide12, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.65), bg_color=CARD_BG, border_color=CARD_BORDER)
tb_disc = slide12.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.5))
tf_d = tb_disc.text_frame
tf_d.word_wrap = True
pd = tf_d.paragraphs[0]
pd.text = "Educational Prototype Scope Note: "
pd.font.size = Pt(10)
pd.font.bold = True
pd.font.color.rgb = WARNING_AMBER
rd = pd.add_run()
rd.text = "This application is an academic software prototype developed for INT253. While engineered with industry best practices, real-world deployment requires departmental accreditation, formal cryptographic signing, and integration with certified forensic laboratories."
rd.font.bold = False
rd.font.color.rgb = TEXT_LIGHT

add_footer(slide12, 12)
add_speaker_notes(
    slide12,
    "Security is central to evidentiary data management. "
    "We implement Django's PBKDF2 password hashing, secure HTTPOnly session cookies, and mandatory CSRF tokens on every state-changing form. "
    "Server-side validation verifies file types and sizes before storing attachments in a private vault that cannot be accessed via direct URLs. "
    "Finally, all state changes are permanently traced in an append-only AuditEvent log."
)


# ==============================================================================
# SLIDE 13: TESTING & ACCEPTANCE VERIFICATION
# ==============================================================================
slide13 = prs.slides.add_slide(blank_layout)
set_slide_background(slide13)
add_header(slide13, "Automated Testing & Acceptance Verification", "Quality Assurance")

# Top Metrics Banner (4 KPI Blocks)
kpis = [
    ("20", "Automated Tests Executed", CYAN_ACCENT),
    ("20", "Test Assertions Passed", SUCCESS_GREEN),
    ("0", "Failures / 0 Errors", SUCCESS_GREEN),
    ("100%", "AT-01 to AT-15 Verified", BLUE_LIGHT),
]

kw = Inches(2.78)
for i, (knum, klbl, kcol) in enumerate(kpis):
    kx = Inches(0.8) + (i * Inches(2.98))
    b = add_card(slide13, kx, Inches(1.6), kw, Inches(1.15))
    tb = slide13.shapes.add_textbox(kx, Inches(1.7), kw, Inches(0.95))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = knum
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = kcol
    
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = klbl
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MUTED

# Acceptance Test Table on Left
add_card(slide13, Inches(0.8), Inches(3.0), Inches(6.8), Inches(3.9), "Acceptance Test Matrix (SRS v1.0 Coverage)")

tests_list = [
    ("AT-01", "Anonymous access to /dashboard/ redirects to login", "PASS"),
    ("AT-02", "Valid user login & secure POST logout lifecycle", "PASS"),
    ("AT-03", "Field Officer blocked from admin user management (403)", "PASS"),
    ("AT-04", "Case creation with missing required fields rejected", "PASS"),
    ("AT-05", "Duplicate sample code registration rejected", "PASS"),
    ("AT-06", "Test event recorded with presumptive disclaimer displayed", "PASS"),
    ("AT-07", "Unapproved test result choices rejected server-side", "PASS"),
    ("AT-08", "Case submit transitions status & logs audit event", "PASS"),
    ("AT-09", "Supervisor returning case without comment rejected", "PASS"),
    ("AT-10", "Supervisor approval transitions status to Approved", "PASS"),
    ("AT-11", "Custody events chronological order & sequence flags", "PASS"),
    ("AT-12", "Disallowed file (.exe) and oversized uploads rejected", "PASS"),
    ("AT-13", "Printable case report renders complete dossier & disclaimer", "PASS"),
    ("AT-14", "POST request without CSRF token rejected (HTTP 403)", "PASS"),
]

tb_tbl = slide13.shapes.add_textbox(Inches(0.95), Inches(3.45), Inches(6.5), Inches(3.3))
tf_tbl = tb_tbl.text_frame
tf_tbl.word_wrap = True

for idx, (tid, tdesc, tstatus) in enumerate(tests_list):
    p = tf_tbl.paragraphs[0] if idx == 0 else tf_tbl.add_paragraph()
    p.text = f"{tid}: "
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    
    run_d = p.add_run()
    run_d.text = f"{tdesc} "
    run_d.font.bold = False
    run_d.font.color.rgb = TEXT_LIGHT
    
    run_s = p.add_run()
    run_s.text = f"[{tstatus}]"
    run_s.font.bold = True
    run_s.font.color.rgb = SUCCESS_GREEN

# Terminal Execution Output Card on Right
add_card(slide13, Inches(7.8), Inches(3.0), Inches(4.733), Inches(3.9), "Actual Terminal Test Run Output")
tb_term = slide13.shapes.add_textbox(Inches(8.0), Inches(3.5), Inches(4.333), Inches(3.2))
tf_term = tb_term.text_frame
tf_term.word_wrap = True

term_lines = [
    ("$ python3 manage.py test", CYAN_ACCENT, True),
    ("Found 20 test(s).", TEXT_MUTED, False),
    ("Creating test database for alias 'default'...", TEXT_MUTED, False),
    ("System check identified no issues (0 silenced).", SUCCESS_GREEN, False),
    ("....................", TEXT_WHITE, True),
    ("--------------------------------------------------", CARD_BORDER, False),
    ("Ran 20 tests in 7.808s", TEXT_WHITE, True),
    ("", TEXT_WHITE, False),
    ("OK", SUCCESS_GREEN, True),
    ("Destroying test database for alias 'default'...", TEXT_MUTED, False),
    ("", TEXT_WHITE, False),
    ("$ python3 manage.py check", CYAN_ACCENT, True),
    ("System check identified no issues (0 silenced).", SUCCESS_GREEN, True),
]

for idx, (tline, tcolor, tbold) in enumerate(term_lines):
    p = tf_term.paragraphs[0] if idx == 0 else tf_term.add_paragraph()
    p.text = tline
    p.font.size = Pt(9.5)
    p.font.bold = tbold
    p.font.color.rgb = tcolor

add_footer(slide13, 13)
add_speaker_notes(
    slide13,
    "Quality assurance was verified through Django's automated test framework. "
    "We wrote and executed 20 automated tests covering all 15 acceptance criteria specified in the SRS, including authentication, "
    "role permissions, duplicate sample prevention, kit expiry checks, supervisor comment enforcement, and CSRF protection. "
    "As shown in the terminal output on the right, all 20 tests pass with zero failures and zero errors in 7.8 seconds."
)


# ==============================================================================
# SLIDE 14: COURSE OUTCOME MAPPING (INT253)
# ==============================================================================
slide14 = prs.slides.add_slide(blank_layout)
set_slide_background(slide14)
add_header(slide14, "Alignment with INT253 Course Outcomes", "Academic Syllabus Mapping")

cos = [
    (
        "CO1: Setup & Project Architecture",
        "Python 3.12 / Django 5.0.2 environment setup, modular 8-app architecture, config directory, virtual environment, and documented manage.py commands."
    ),
    (
        "CO2: Views, URLs & Error Handling",
        "Named URL patterns, path converters, clean GET/POST request handling, render/redirect patterns, and custom 403, 404, and 500 error templates."
    ),
    (
        "CO3: Django Template Language (DTL)",
        "Extensive template inheritance (base.html), block overrides, context variables, loops, conditional role-based navigation, and print stylesheets."
    ),
    (
        "CO4: Django Forms & Validation",
        "ModelForms for CaseRecord, Sample, TestEvent, CustodyEvent, ReviewRecord, and EvidenceFile with server-side validation, CSRF, and Post/Redirect/Get."
    ),
    (
        "CO5: ORM, Models & Administration",
        "ForeignKeys with PROTECT/CASCADE, unique constraints, date hierarchies, model clean() validation, database migrations, and complete Django Admin."
    ),
    (
        "CO6: Sessions, Auth & Permissions",
        "Django Authentication System, PBKDF2 hashing, session management, 4-role group permissions, and backend view decorators (@role_required)."
    ),
]

card_w = Inches(5.6)
card_h = Inches(1.5)

for idx, (cotitle, codesc) in enumerate(cos):
    col = idx % 2
    row = idx // 2
    x = Inches(0.8) + (col * Inches(6.1))
    y = Inches(1.6) + (row * Inches(1.7))
    
    add_card(slide14, x, y, card_w, card_h, cotitle, border_color=BLUE_ACCENT)
    tb = slide14.shapes.add_textbox(x + Inches(0.2), y + Inches(0.48), card_w - Inches(0.4), Inches(0.95))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = codesc
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_LIGHT

# Footer Summary
add_card(slide14, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.65), bg_color=CARD_BG, border_color=CARD_BORDER)
tb_cos = slide14.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.5))
tf_cos = tb_cos.text_frame
tf_cos.word_wrap = True
pcos = tf_cos.paragraphs[0]
pcos.text = "Syllabus Compliance: "
pcos.font.size = Pt(10)
pcos.font.bold = True
pcos.font.color.rgb = SUCCESS_GREEN
rcos = pcos.add_run()
rcos.text = "Every concept taught across Course Outcomes 1 to 6 in INT253 has been directly applied and verified in the FieldTest Companion codebase."
rcos.font.bold = False
rcos.font.color.rgb = TEXT_LIGHT

add_footer(slide14, 14)
add_speaker_notes(
    slide14,
    "This slide maps FieldTest Companion directly to the six course outcomes of INT253. "
    "CO1 is evidenced by our 8-app project architecture; CO2 by our URL routing and custom error handlers; "
    "CO3 by our base template inheritance; CO4 by our ModelForms and CSRF validation; "
    "CO5 by our relational ORM models and Django Admin; and CO6 by our session authentication and role decorators. "
    "The application serves as comprehensive practical evidence of mastery in Django web development."
)


# ==============================================================================
# SLIDE 15: CONCLUSION & FUTURE SCOPE
# ==============================================================================
slide15 = prs.slides.add_slide(blank_layout)
set_slide_background(slide15)
add_header(slide15, "Conclusion & Future Roadmap", "Summary & Next Steps")

# Left Column: Project Conclusion
add_card(slide15, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.4), "Project Summary & Outcomes")
tb_c = slide15.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(3.6))
tf_c = tb_c.text_frame
tf_c.word_wrap = True

add_bullet(tf_c, "Working Full-Stack Solution", "Successfully designed, developed, and tested a functional Django platform replacing paper notes with structured digital records.", True)
add_bullet(tf_c, "Forensic Integrity Preserved", "Enforces strict presumptive disclaimer boundaries, kit expiration warnings, and append-only custody chronology.", False)
add_bullet(tf_c, "Complete Review & Reports", "Empowers supervisors to review, return for corrections, or approve cases with print-ready summary reports.", False)
add_bullet(tf_c, "GitHub & Viva Ready", "Accompanied by comprehensive README, demo data loader, .gitignore, clean git commit history, and passing test suite.", False)

# Right Column: Future Roadmap
add_card(slide15, Inches(6.8), Inches(1.6), Inches(5.7), Inches(4.4), "Future Scope & Enhancements")
tb_f = slide15.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(3.6))
tf_f = tb_f.text_frame
tf_f.word_wrap = True

add_bullet(tf_f, "Cloud & Database Scaling", "Transition from development SQLite to a managed PostgreSQL cluster with automated backup and replication.", True)
add_bullet(tf_f, "Encrypted Object Vault", "Integrate AWS S3 / Google Cloud Storage private encrypted buckets with expiring signed URLs for evidence files.", False)
add_bullet(tf_f, "Automated PDF Generation", "Incorporate headless server-side PDF engines (e.g., WeasyPrint) for background PDF dispatch and email delivery.", False)
add_bullet(tf_f, "Forensic LIMS Integration", "Connect via secure REST APIs to certified Laboratory Information Management Systems (LIMS) for confirmatory tracking.", False)

# Thank You Banner at Bottom
ty_card = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.95))
ty_card.fill.solid()
ty_card.fill.fore_color.rgb = BLUE_ACCENT
ty_card.line.fill.background()
tf_ty = ty_card.text_frame
p_ty = tf_ty.paragraphs[0]
p_ty.alignment = PP_ALIGN.CENTER
p_ty.text = "Thank You! Questions & Viva Discussion"
p_ty.font.size = Pt(16)
p_ty.font.bold = True
p_ty.font.color.rgb = TEXT_WHITE

p_ty2 = tf_ty.add_paragraph()
p_ty2.alignment = PP_ALIGN.CENTER
p_ty2.text = "FieldTest Companion  •  Ansh Sangwan  •  INT253: Web Development in Python Using Django"
p_ty2.font.size = Pt(10)
p_ty2.font.color.rgb = TEXT_LIGHT

add_footer(slide15, 15)
add_speaker_notes(
    slide15,
    "In conclusion, FieldTest Companion successfully digitizes field drug testing records through a secure, modular, and role-governed Django application. "
    "It solves real-world issues of evidence traceability and chain-of-custody gaps while respecting academic safety constraints. "
    "For future work, the system can scale with PostgreSQL, encrypted cloud evidence vaults, and direct laboratory LIMS integration. "
    "Thank you for your time, and I am now ready for questions and viva discussion."
)

# Save PowerPoint
out_pptx = os.path.join(BASE_DIR, "FieldTest_Companion_Presentation.pptx")
prs.save(out_pptx)
print(f"✓ PowerPoint presentation successfully created: {out_pptx}")
