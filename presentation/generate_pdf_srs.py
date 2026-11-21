import os
import subprocess

HTML_OUT = "presentation/srs_document.html"
PDF_OUT = "Digital_Companion_for_Drug_Field_Testing_SRS.pdf"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def generate_pdf():
    # Read sections from our existing python modules or generate structured HTML
    from presentation.srs_sections_front import (
        build_cover_page, build_revision_history, build_table_of_contents,
        build_section_1, build_section_2
    )
    import docx
    
    # We can extract the content from our generated DOCX or construct HTML directly.
    # Constructing clean semantic HTML with CSS print stylesheet ensures beautiful PDF layout.
    doc = docx.Document("Digital_Companion_for_Drug_Field_Testing_SRS.docx")
    
    html_parts = []
    html_parts.append('''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Software Requirements Specification - FieldTest Companion</title>
<style>
  @page {
    size: letter portrait;
    margin: 1in;
    @top-right {
      content: "Digital Companion for Drug Field Testing (FieldTest Companion)";
      font-family: "Times New Roman", Times, serif;
      font-size: 8.5pt;
      font-style: italic;
      color: #64748B;
    }
    @bottom-left {
      content: "Software Requirements Specification";
      font-family: "Times New Roman", Times, serif;
      font-size: 8.5pt;
      color: #64748B;
    }
    @bottom-right {
      content: counter(page);
      font-family: "Times New Roman", Times, serif;
      font-size: 8.5pt;
      color: #64748B;
    }
  }

  body {
    font-family: "Times New Roman", Times, serif;
    font-size: 11pt;
    line-height: 1.25;
    color: #1E293B;
    margin: 0;
    padding: 0;
  }

  .cover-page {
    text-align: center;
    padding-top: 1.5in;
    page-break-after: always;
  }
  .cover-title {
    font-size: 24pt;
    font-weight: bold;
    color: #0F172A;
    margin-bottom: 25pt;
    line-height: 1.2;
  }
  .cover-subtitle {
    font-size: 17pt;
    font-weight: bold;
    color: #1E293B;
    margin-bottom: 30pt;
  }
  .cover-course {
    font-size: 13.5pt;
    font-weight: bold;
    color: #1E293B;
    margin-bottom: 30pt;
  }
  .cover-student {
    font-size: 13.5pt;
    font-weight: bold;
    color: #0F172A;
    margin-bottom: 45pt;
  }
  .cover-footer {
    font-size: 11.5pt;
    font-weight: bold;
    color: #475569;
    line-height: 1.4;
  }

  .page-break {
    page-break-after: always;
  }

  h1 {
    font-size: 14pt;
    font-weight: bold;
    color: #0F172A;
    margin-top: 18pt;
    margin-bottom: 8pt;
    page-break-after: avoid;
    border-bottom: 1.5pt solid #CBD5E1;
    padding-bottom: 3pt;
  }
  h2 {
    font-size: 12.5pt;
    font-weight: bold;
    color: #1E293B;
    margin-top: 14pt;
    margin-bottom: 6pt;
    page-break-after: avoid;
  }
  h3 {
    font-size: 11.5pt;
    font-weight: bold;
    color: #2563EB;
    margin-top: 10pt;
    margin-bottom: 4pt;
    page-break-after: avoid;
  }
  h4 {
    font-size: 11pt;
    font-weight: bold;
    color: #334155;
    margin-top: 8pt;
    margin-bottom: 3pt;
    page-break-after: avoid;
  }

  p {
    margin-top: 0;
    margin-bottom: 6pt;
    text-align: justify;
  }

  ul {
    margin-top: 0;
    margin-bottom: 6pt;
    padding-left: 20pt;
  }
  li {
    margin-bottom: 4pt;
    text-align: justify;
  }

  .callout {
    background-color: #F1F5F9;
    border-left: 4pt solid #2563EB;
    padding: 8pt 12pt;
    margin: 8pt 0 12pt 0;
    font-size: 10pt;
    page-break-inside: avoid;
  }
  .callout-title {
    font-weight: bold;
    color: #2563EB;
    margin-bottom: 3pt;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 8pt 0 12pt 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }
  th {
    background-color: #0F172A;
    color: #FFFFFF;
    font-weight: bold;
    text-align: left;
    padding: 6pt 8pt;
    border: 1pt solid #CBD5E1;
  }
  td {
    padding: 5pt 8pt;
    border: 1pt solid #CBD5E1;
    vertical-align: top;
  }
  tr:nth-child(even) td {
    background-color: #F8FAFC;
  }

  .diagram-container {
    text-align: center;
    margin: 12pt 0;
    page-break-inside: avoid;
  }
  .diagram-container img {
    max-width: 95%;
    height: auto;
    border: 1pt solid #CBD5E1;
    border-radius: 4pt;
  }
  .diagram-caption {
    font-size: 10pt;
    margin-top: 4pt;
    color: #334155;
  }
  .diagram-caption strong {
    color: #0F172A;
  }

  .toc-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 3pt;
    font-size: 10pt;
  }
  .toc-row.major {
    font-weight: bold;
    color: #0F172A;
    margin-top: 4pt;
  }
  .toc-dots {
    flex-grow: 1;
    border-bottom: 1pt dotted #94A3B8;
    margin: 0 5pt 3pt 5pt;
  }
</style>
</head>
<body>
''')

    # Convert DOCX structure to HTML cleanly
    # Or let's convert docx elements:
    in_table = False
    
    for element in doc.element.body:
        tag = element.tag.split('}')[-1]
        if tag == 'p':
            p_text = element.text.strip()
            if not p_text:
                continue
            
            # Check for headings
            p_xml = element.xml
            if "Digital Companion for Drug Field Testing" in p_text and "FieldTest Companion" in p_text and not html_parts[1:]:
                # Cover page title
                html_parts.append(f'''<div class="cover-page">
                    <div class="cover-title">Digital Companion for Drug Field Testing<br><span style="font-size:18pt; font-weight:normal; color:#2563EB;">(FieldTest Companion)</span></div>
                    <div class="cover-subtitle">Software Requirements Specification</div>
                    <div class="cover-course">Course Code: INT253<br>Course Name: Web Development in Python Using Django</div>
                    <div class="cover-student">Student Name: Ansh Sangwan<br>Student Registration Number: [INSERT REGISTRATION NUMBER]</div>
                    <div class="cover-footer">Prepared for<br>Continuous Assessment 3<br>Spring 2025</div>
                </div>''')
                continue
            elif "Software Requirements Specification" in p_text and len(p_text) < 40 and "cover-page" not in html_parts[-1]:
                continue
            elif "Course Code: INT253" in p_text:
                continue
            elif "Student Name: Ansh Sangwan" in p_text:
                continue
            elif "Continuous Assessment 3" in p_text:
                continue

            # Section headings
            if p_text.startswith("1. Introduction"):
                html_parts.append(f'<h1>{p_text}</h1>')
            elif p_text.startswith("2. General Description"):
                html_parts.append(f'<div class="page-break"></div><h1>{p_text}</h1>')
            elif p_text.startswith("3. Specific Requirements"):
                html_parts.append(f'<div class="page-break"></div><h1>{p_text}</h1>')
            elif p_text.startswith("4. Analysis Models"):
                html_parts.append(f'<div class="page-break"></div><h1>{p_text}</h1>')
            elif any(p_text.startswith(f"{i}. ") for i in ["5", "6", "7", "8", "9", "10", "11"]):
                html_parts.append(f'<h1>{p_text}</h1>')
            elif p_text.startswith("A. Appendices"):
                html_parts.append(f'<div class="page-break"></div><h1>{p_text}</h1>')
            elif p_text == "Revision History":
                html_parts.append(f'<h1>{p_text}</h1>')
            elif p_text == "Table of Contents":
                html_parts.append(f'<div class="page-break"></div><h1>{p_text}</h1>')
            elif any(p_text.startswith(f"{prefix} ") for prefix in ["1.1", "1.2", "1.3", "1.4", "1.5", "2.1", "2.2", "2.3", "2.4", "2.5", "3.1", "3.2", "3.5", "3.7", "3.9", "4.1", "A.1", "A.2"]):
                html_parts.append(f'<h2>{p_text}</h2>')
            elif any(p_text.startswith(f"{prefix} ") for prefix in ["3.1.1", "3.1.2", "3.1.3", "3.1.4", "3.5.1", "3.5.2", "3.5.3", "3.5.4", "3.5.5", "3.5.6", "4.1.1", "4.1.2", "4.1.3", "4.1.4", "4.1.5"]) or (p_text.startswith("3.2.") and p_text[5] == ' '):
                html_parts.append(f'<h3>{p_text}</h3>')
            elif any(p_text.startswith(f"3.2.{i}.") for i in range(1, 20)):
                html_parts.append(f'<p style="margin-left:8pt;"><strong>{p_text[:p_text.find(":")+1]}</strong>{p_text[p_text.find(":")+1:]}</p>')
            elif p_text.startswith("Figure "):
                colon_idx = p_text.find(":")
                html_parts.append(f'<div class="diagram-caption"><strong>{p_text[:colon_idx+1]}</strong><em>{p_text[colon_idx+1:]}</em></div>')
            elif "STATUTORY FORENSIC NOTICE" in p_text or "PLACEHOLDER" in p_text or "TAX REGISTRATION IDENTIFIER" in p_text:
                html_parts.append(f'<div class="callout"><div class="callout-title">{p_text}</div>')
            elif html_parts and html_parts[-1].startswith('<div class="callout">') and not html_parts[-1].endswith('</div>'):
                html_parts[-1] += f'<div style="font-style:italic;">{p_text}</div></div>'
            elif "\t" in p_text and any(ch.isdigit() for ch in p_text):
                # TOC line
                parts = p_text.split("\t")
                is_major = parts[0].strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "11.", "A."))
                html_parts.append(f'<div class="toc-row{" major" if is_major else ""}">'
                                  f'<span>{parts[0]}</span>'
                                  f'<span class="toc-dots"></span>'
                                  f'<span>{parts[1] if len(parts) > 1 else ""}</span></div>')
            elif p_text.startswith("• ") or "List Bullet" in p_xml:
                clean_bullet = p_text.lstrip("• ")
                html_parts.append(f'<ul><li>{clean_bullet}</li></ul>')
            else:
                html_parts.append(f'<p>{p_text}</p>')

        elif tag == 'tbl':
            # Convert docx table to HTML
            tbl_xml = element
            table_obj = [t for t in doc.tables if t._tbl == tbl_xml]
            if table_obj:
                t = table_obj[0]
                t_html = ['<table>']
                for r_idx, row in enumerate(t.rows):
                    t_html.append('<tr>')
                    for cell in row.cells:
                        tag_name = 'th' if r_idx == 0 else 'td'
                        t_html.append(f'<{tag_name}>{cell.text.strip()}</{tag_name}>')
                    t_html.append('</tr>')
                t_html.append('</table>')
                html_parts.append(''.join(t_html))

    # Insert images at appropriate diagram locations
    html_content = '\n'.join(html_parts)
    
    # Replace diagram captions with image + caption
    diagram_map = {
        "Figure 4.1.1:": ("presentation/srs_diagrams/dfd_context.png", "dfd_context"),
        "Figure 4.1.2:": ("presentation/srs_diagrams/dfd_level1.png", "dfd_level1"),
        "Figure 4.1.3:": ("presentation/srs_diagrams/system_architecture.png", "system_architecture"),
        "Figure 4.1.4:": ("presentation/srs_diagrams/erd_diagram.png", "erd_diagram"),
        "Figure 4.1.5:": ("presentation/srs_diagrams/workflow_diagram.png", "workflow_diagram")
    }

    for fig_key, (img_path, _) in diagram_map.items():
        abs_img_path = os.path.abspath(img_path)
        img_tag = f'<div class="diagram-container"><img src="file://{abs_img_path}"></div>'
        caption_target = f'<div class="diagram-caption"><strong>{fig_key}'
        if caption_target in html_content:
            html_content = html_content.replace(caption_target, f'{img_tag}\n{caption_target}')

    html_content += '\n</body>\n</html>'

    with open(HTML_OUT, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✓ Semantic HTML document written to: {HTML_OUT}")

    # Compile PDF via Chrome headless
    print(f"Compiling PDF via Google Chrome headless: {PDF_OUT}...")
    cmd = [
        CHROME_BIN,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--user-data-dir=presentation/chrome_profile',
        '--no-pdf-header-footer',
        f'--print-to-pdf={PDF_OUT}',
        os.path.abspath(HTML_OUT)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(PDF_OUT):
        print(f"✓ Successfully generated {PDF_OUT} ({os.path.getsize(PDF_OUT)} bytes)!")
    else:
        print(f"✗ Failed to generate PDF: {res.stderr}")

if __name__ == "__main__":
    generate_pdf()
