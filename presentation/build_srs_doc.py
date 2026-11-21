import os
import sys
import docx
from presentation.srs_sections_front import (
    build_cover_page,
    build_revision_history,
    build_table_of_contents,
    build_section_1,
    build_section_2
)
from presentation.srs_sections_reqs import build_section_3
from presentation.srs_sections_models import (
    build_section_4,
    build_sections_5_to_11,
    build_appendices
)
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUTPUT_FILE = "Digital_Companion_for_Drug_Field_Testing_SRS.docx"

def initialize_srs_document():
    doc = docx.Document()
    
    # Page setup - Standard 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        section.different_first_page_header_footer = True
        
        # Header for normal pages (Right aligned)
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Digital Companion for Drug Field Testing (FieldTest Companion)")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.italic = True
        hrun.font.color.rgb = RGBColor(100, 116, 139)
        
        # Footer for normal pages (Left: Spec title, Right: Page number)
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        frun = fp.add_run("Software Requirements Specification\tPage ")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 116, 139)
        
        # Dynamic page number field
        fld = OxmlElement('w:fldSimple')
        fld.set(qn('w:instr'), 'PAGE')
        frun._r.append(fld)

    # Styles setup
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    return doc

def main():
    print(f"Generating Software Requirements Specification: {OUTPUT_FILE}...")
    doc = initialize_srs_document()
    
    print("1/7 Building Cover Page, Revision History, and Table of Contents...")
    build_cover_page(doc)
    build_revision_history(doc)
    build_table_of_contents(doc)
    
    print("2/7 Building Section 1: Introduction (Purpose, Scope, Definitions, References, Overview)...")
    build_section_1(doc)
    
    print("3/7 Building Section 2: General Description (Perspective, Functions, Users, Constraints, Dependencies)...")
    build_section_2(doc)
    
    print("4/7 Building Section 3: Specific Requirements (Interfaces, 16 Functional Reqs, Non-Functional, Design Constraints)...")
    build_section_3(doc)
    
    print("5/7 Building Section 4: Analysis Models (Level 0 DFD, Level 1 DFD, Architecture, ERD, Workflow)...")
    build_section_4(doc)
    
    print("6/7 Building Sections 5 to 11: GitHub, Deployment, and Institutional Proofs...")
    build_sections_5_to_11(doc)
    
    print("7/7 Building Appendices A.1 and A.2: Setup Guide & Test Verification Matrix...")
    build_appendices(doc)
    
    doc.save(OUTPUT_FILE)
    print(f"✓ Successfully generated {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE)} bytes)!")

if __name__ == "__main__":
    main()
