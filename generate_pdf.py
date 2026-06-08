import os
import re
import base64
import requests
import markdown
from xhtml2pdf import pisa

def md_to_pdf(md_path, pdf_path):
    print(f"Reading Markdown file: {md_path}")
    # 1. Read Markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 2. Extract and download Mermaid diagrams
    mermaid_pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
    matches = list(mermaid_pattern.finditer(md_content))
    
    temp_images = []
    
    # Process from last to first so indices don't shift when replacing
    for i, match in enumerate(matches):
        mermaid_code = match.group(1).strip()
        print(f"Processing Mermaid diagram {i+1}...")
        
        # Base64 encode the code block for the mermaid.ink API
        b64_code = base64.b64encode(mermaid_code.encode("utf-8")).decode("utf-8")
        url = f"https://mermaid.ink/img/{b64_code}"
        
        # Download the rendered PNG image from the API
        try:
            r = requests.get(url, timeout=25)
            if r.status_code == 200:
                temp_filename = f"mermaid_temp_{i+1}.png"
                with open(temp_filename, 'wb') as img_f:
                    img_f.write(r.content)
                temp_images.append(temp_filename)
                
                # Replace the raw markdown code block with an HTML img tag
                img_tag = f'\n<p style="text-align: center; margin-top: 15pt; margin-bottom: 15pt;"><img src="{temp_filename}" style="width: 80%; max-width: 550px;" /></p>\n'
                md_content = md_content.replace(match.group(0), img_tag)
                print(f"Embedded Mermaid diagram {i+1} as local file {temp_filename}")
            else:
                print(f"Failed to fetch Mermaid diagram {i+1} from API: HTTP {r.status_code}")
        except Exception as e:
            print(f"Exception while fetching Mermaid diagram {i+1}: {e}")

    # 3. Convert Markdown to HTML (including tables and fenced code)
    print("Converting Markdown to HTML...")
    html_content = markdown.markdown(md_content, extensions=['extra'])
    
    # 4. Construct the complete HTML document with premium CSS styling for xhtml2pdf
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @page cover {{
        size: A4;
        margin: 3cm 2.5cm 3cm 2.5cm;
    }}
    @page main {{
        size: A4;
        margin: 2.5cm 2cm 2.5cm 2cm;
        @frame footer {{
            -pdf-frame-content: footer_content;
            left: 2cm; width: 17cm; top: 27.2cm; height: 1cm;
        }}
    }}
    
    body {{
        font-family: Helvetica, Arial, sans-serif;
        color: #333333;
        font-size: 10pt;
        line-height: 1.5;
    }}
    
    /* Cover Page Styling */
    .cover-page {{
        page-break-after: always;
        page: cover;
        text-align: center;
    }}
    .cover-title {{
        font-size: 28pt;
        color: #0F2C59;
        font-weight: bold;
        margin-top: 120pt;
        margin-bottom: 15pt;
    }}
    .cover-subtitle {{
        font-size: 13pt;
        color: #1A5F7A;
        margin-bottom: 80pt;
        line-height: 1.4;
    }}
    .cover-info {{
        font-size: 11pt;
        line-height: 1.8;
        margin-bottom: 120pt;
    }}
    
    /* Main Content Layout */
    .main-content {{
        page: main;
    }}
    
    h1 {{
        font-size: 18pt;
        color: #0F2C59;
        font-weight: bold;
        margin-top: 25pt;
        margin-bottom: 10pt;
        page-break-before: always;
        -pdf-keep-with-next: true;
    }}
    
    h1:first-of-type {{
        page-break-before: avoid;
    }}
    
    h2 {{
        font-size: 13pt;
        color: #1A5F7A;
        font-weight: bold;
        margin-top: 15pt;
        margin-bottom: 8pt;
        -pdf-keep-with-next: true;
    }}
    
    h3 {{
        font-size: 11pt;
        color: #57C5B6;
        font-weight: bold;
        margin-top: 12pt;
        margin-bottom: 6pt;
        -pdf-keep-with-next: true;
    }}
    
    p {{
        margin-bottom: 10pt;
        text-align: justify;
    }}
    
    ul, ol {{
        margin-bottom: 10pt;
        margin-left: 20pt;
    }}
    
    li {{
        margin-bottom: 4pt;
    }}
    
    blockquote {{
        border-left: 3px solid #0F2C59;
        background-color: #f0f4f8;
        padding: 8pt 12pt;
        margin: 10pt 0;
        font-style: italic;
    }}
    
    /* Tables styling */
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 15pt;
    }}
    th {{
        background-color: #0F2C59;
        color: #ffffff;
        font-size: 8.5pt;
        font-weight: bold;
        padding: 5pt;
        border: 1px solid #0F2C59;
        text-align: left;
    }}
    td {{
        border: 1px solid #dddddd;
        padding: 5pt;
        font-size: 8pt;
        vertical-align: top;
    }}
    
    /* Code styling */
    pre {{
        font-family: Courier, monospace;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 8pt;
        font-size: 7.5pt;
        margin-bottom: 10pt;
    }}
    code {{
        font-family: Courier, monospace;
        background-color: #f8f9fa;
        font-size: 8pt;
        padding: 1px 3px;
    }}
    
    /* Horizontal Rule */
    hr {{
        border: 0;
        border-top: 1px solid #cccccc;
        margin: 20pt 0;
    }}
</style>
</head>
<body>

<!-- Footer frame template -->
<div id="footer_content" style="text-align: right; font-size: 8pt; color: #777777; border-top: 1px solid #dddddd; padding-top: 5px;">
    Page <pdf:pagenumber /> of <pdf:pagecount />
</div>

<!-- Cover Page -->
<div class="cover-page">
    <div style="font-size: 14pt; font-weight: bold; color: #333333; margin-top: 20pt;">ASIA PACIFIC COLLEGE</div>
    <div style="font-size: 10pt; color: #666666;">School of Computing and Information Technology</div>
    
    <div class="cover-title">I-Travel</div>
    <div class="cover-subtitle">An Agentic Travel Planner for Personalized Itineraries<br>and Multi-Modal Trip Planning</div>
    
    <div class="cover-info">
        In partial fulfillment of the requirements<br>
        for the course in<br>
        <strong>Analytics & Artificial Intelligence (ANLYTC4)</strong>
    </div>
    
    <div style="font-size: 11pt; line-height: 1.6; text-align: left; margin-left: 80pt; margin-top: 50pt;">
        <strong>Documented by:</strong> Rylie Tengco (rtengco@student.apc.edu.ph)<br>
        <strong>Submitted to:</strong> Miss Rhea-Luz R. Valbuena<br>
        <strong>Academic Year:</strong> 2025-2026<br>
        <strong>Date:</strong> June 2026
    </div>
</div>

<!-- Main Body -->
<div class="main-content">
{html_content}
</div>

</body>
</html>
"""

    # 5. Clean up duplicate markdown metadata header from body block
    # Split by the first parsed <hr /> which corresponds to the first "---"
    content_parts = html_content.split('<hr />', 1)
    if len(content_parts) > 1:
        clean_html_content = content_parts[1].strip()
        full_html = full_html.replace(html_content, clean_html_content)

    # 6. Render HTML string directly to PDF
    print("Generating PDF...")
    with open(pdf_path, "wb") as pdf_f:
        pisa_status = pisa.CreatePDF(full_html, dest=pdf_f)
        
    # 7. Clean up temporary PNG files
    for temp_img in temp_images:
        try:
            if os.path.exists(temp_img):
                os.remove(temp_img)
                print(f"Cleaned up temporary file: {temp_img}")
        except Exception as e:
            print(f"Failed to remove temp file {temp_img}: {e}")
            
    if pisa_status.err:
        print("Error occurred while generating PDF!")
    else:
        print(f"PDF successfully generated at: {pdf_path}")

if __name__ == "__main__":
    md_to_pdf("I-Travel_Project_Report.md", "I-Travel_Project_Report.pdf")
