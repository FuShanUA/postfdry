"""
extractor.py

Unified content extractor for Postfdry.
Supports:
- URLs (Playwright -> Markdown)
- PDFs (pdfplumber/pypdf -> Text)
- Text/Markdown files (Direct read)
"""

import sys
import os
import re
import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup, NavigableString, Tag

def process_table(table_element):
    """Convert HTML table to proper Markdown table."""
    rows = table_element.find_all('tr')
    if not rows:
        return ""
    
    table_data = []
    for row in rows:
        cells = row.find_all(['th', 'td'])
        row_data = [cell.get_text(strip=True).replace('|', '\\|') for cell in cells]
        table_data.append(row_data)
    
    if not table_data:
        return ""
    
    # Determine column widths
    max_cols = max(len(row) for row in table_data)
    # Pad rows to have equal columns
    for row in table_data:
        while len(row) < max_cols:
            row.append('')
    
    # Build markdown
    lines = []
    # Header row
    lines.append("| " + " | ".join(table_data[0]) + " |")
    # Separator
    lines.append("| " + " | ".join(["---"] * max_cols) + " |")
    # Data rows
    for row in table_data[1:]:
        lines.append("| " + " | ".join(row) + " |")
    
    return "\n\n" + "\n".join(lines) + "\n\n"


def html_to_markdown(element):
    """Recursively convert HTML element to Markdown."""
    if element is None:
        return ""
    
    if isinstance(element, NavigableString):
        text = str(element).strip()
        return text if text else ""
    
    tag_name = element.name.lower()
    
    if tag_name == 'br':
        return "\n"
    
    if tag_name == 'p':
        return "\n\n" + "".join(html_to_markdown(child) for child in element.children) + "\n\n"
    
    if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        level = int(tag_name[1])
        return f"\n\n{'#' * level} " + "".join(html_to_markdown(child) for child in element.children) + "\n\n"
        
    if tag_name == 'a':
        text = "".join(html_to_markdown(child) for child in element.children)
        href = element.get('href', '')
        return f"[{text}]({href})" if href else text
    
    if tag_name in ['strong', 'b']:
        return f"**{''.join(html_to_markdown(child) for child in element.children)}**"
        
    if tag_name in ['em', 'i']:
        return f"*{''.join(html_to_markdown(child) for child in element.children)}*"
        
    if tag_name == 'ul':
        content = ""
        for child in element.children:
            if child.name == 'li':
                content += f"\n- {''.join(html_to_markdown(c) for c in child.children).strip()}"
        return content + "\n"
        
    if tag_name == 'ol':
        content = ""
        for i, child in enumerate(element.find_all('li', recursive=False)):
            content += f"\n{i+1}. {''.join(html_to_markdown(c) for c in child.children).strip()}"
        return content + "\n"
        
    if tag_name == 'table':
        return process_table(element)
        
    if tag_name == 'img':
        alt = element.get('alt', 'Image')
        src = element.get('src', '')
        return f"![{alt}]({src})"
    
    # Default: traverse children
    return "".join(html_to_markdown(child) for child in element.children)

def extract_from_url(url):
    """Extract content from URL using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"Navigating to {url}...")
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=60000)
            
            # Basic ungating attempt
            page.evaluate("""() => {
                const overlays = document.querySelectorAll('.c-gated-content__overlay, .hs-form-gated, .modal, .popup');
                overlays.forEach(el => el.remove());
                window.scrollTo(0, document.body.scrollHeight);
            }""")
            page.wait_for_timeout(2000)
            content = page.content()
        except Exception as e:
            print(f"Error loading URL: {e}")
            browser.close()
            return f"Error loading URL: {e}"
        finally:
            browser.close()
        
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title.string if soup.title else "No Title"
    
    article = soup.find('article')
    if not article:
        selectors = ['main', 'div.content', 'div.article-body', 'body']
        for sel in selectors:
            article = soup.select_one(sel)
            if article: break
            
    md_content = html_to_markdown(article)
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    return f"""Title: {title}
Date: {today}
Source: Web
EngTitle: {title}
Url: {url}

{md_content}"""

def extract_from_file(filepath):
    """Extract content from local file."""
    ext = os.path.splitext(filepath)[1].lower()
    filename = os.path.basename(filepath)
    content = ""
    
    if ext == '.pdf':
        try:
            import pdfplumber
            with pdfplumber.open(filepath) as pdf:
                content = "\n\n".join([p.extract_text() or "" for p in pdf.pages])
        except ImportError:
            try:
                from pypdf import PdfReader
                reader = PdfReader(filepath)
                content = "\n\n".join([p.extract_text() for p in reader.pages])
            except ImportError:
                return "Error: Neither pdfplumber nor pypdf installed."
                
    elif ext in ['.txt', '.md']:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

    elif ext == '.docx':
        try:
            import docx
            doc = docx.Document(filepath)
            content = "\n\n".join([p.text for p in doc.paragraphs])
        except ImportError:
            return "Error: python-docx not installed."
            
    else:
        return f"Unsupported format: {ext}"
        
    today = datetime.date.today().strftime('%Y-%m-%d')
    return f"""Title: {filename}
Date: {today}
Source: File
EngTitle: {filename}
Url: {filepath}

{content}"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <url_or_file> [output_file]")
        sys.exit(1)
        
    target = sys.argv[1]
    outfile = sys.argv[2] if len(sys.argv) > 2 else None
    
    if os.path.exists(target):
        res = extract_from_file(target)
    elif target.startswith("http"):
        res = extract_from_url(target)
    else:
        print("Error: Target not found and not a valid URL")
        sys.exit(1)
        
    if outfile:
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(res)
        print(f"Saved to {outfile}")
    else:
        print(res[:500] + "...")
