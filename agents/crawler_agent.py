"""
Crawler Agent (Content Extractor)

Responsible for extracting raw text/markdown from URLs or local files.
Supports:
- URLs (Playwright -> Markdown)
- PDFs (pdfplumber/pypdf -> Text)
- Text/Markdown files (Direct read)
"""

import sys
import os
import datetime
from bs4 import BeautifulSoup, NavigableString
from playwright.sync_api import sync_playwright

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
    
    max_cols = max(len(row) for row in table_data)
    for row in table_data:
        while len(row) < max_cols:
            row.append('')
    
    lines = []
    lines.append("| " + " | ".join(table_data[0]) + " |")
    lines.append("| " + " | ".join(["---"] * max_cols) + " |")
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
    
    return "".join(html_to_markdown(child) for child in element.children)

def extract_from_url(url):
    """Extract content from URL. Uses fxtwitter for X posts, otherwise Defuddle CLI."""
    import subprocess
    import json
    import urllib.request
    
    today = datetime.date.today().strftime('%Y-%m-%d')
    md_content = ""
    title = f"Extracted from {url}"
    
    if "x.com/" in url or "twitter.com/" in url:
        print(f"Crawler Agent: Detected X/Twitter URL. Fetching via fxtwitter API...")
        api_url = url.replace("x.com", "api.fxtwitter.com").replace("twitter.com", "api.fxtwitter.com")
        try:
            req = urllib.request.Request(api_url, headers={'User-Agent': 'curl/7.68.0'})
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode('utf-8'))
            except Exception as e:
                print(f"Crawler Agent: urllib failed ({e}), falling back to curl via shell...")
                # Use shell=True for windows curl resolution, or fallback to saved file
                try:
                    result = subprocess.run(
                        f'curl.exe -s "{api_url}"',
                        capture_output=True,
                        text=True,
                        check=True,
                        shell=True
                    )
                    data = json.loads(result.stdout)
                except Exception as curl_err:
                    print(f"Crawler Agent: curl failed ({curl_err}), trying local tweet.json fallback...")
                    with open("tweet.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                
            if data.get("code") == 200 and "tweet" in data:
                tweet = data["tweet"]
                text = tweet.get("text", "")
                author = tweet.get("author", {}).get("name", "Unknown")
                
                md_content = f"**{author}**\n\n{text}\n\n"
                
                # Extract all media (images/videos)
                if "media" in tweet and "photos" in tweet["media"]:
                    for photo in tweet["media"]["photos"]:
                        md_content += f"![Image]({photo['url']})\n\n"
                        
                # Handle quote tweets or articles if they exist
                if "article" in tweet and "content" in tweet["article"]:
                    article = tweet["article"]
                    title = article.get("title", title)
                    cover_img = article.get("cover_media", {}).get("media_info", {}).get("original_img_url")
                    if cover_img:
                        md_content += f"![Cover]({cover_img})\n\n"
                    
                    # Create a lookup dictionary for all media entities attached to this article
                    media_dict = {}
                    entities_data = article.get("media_entities", {})
                    # sometimes it's a dict, sometimes list
                    if isinstance(entities_data, dict):
                        for k, v in entities_data.items():
                            if "media_info" in v and "original_img_url" in v["media_info"]:
                                media_dict[str(v.get("media_id", ""))] = v["media_info"]["original_img_url"]
                    elif isinstance(entities_data, list):
                        for v in entities_data:
                            if "media_info" in v and "original_img_url" in v["media_info"]:
                                media_dict[str(v.get("media_id", ""))] = v["media_info"]["original_img_url"]
                    
                    content_data = article["content"]
                    blocks = content_data.get("blocks", [])
                    entity_map_raw = content_data.get("entityMap", [])
                    entity_map = {}
                    if isinstance(entity_map_raw, list):
                        for item in entity_map_raw:
                            if "key" in item and "value" in item:
                                entity_map[str(item["key"])] = item["value"]
                    elif isinstance(entity_map_raw, dict):
                        entity_map = entity_map_raw
                    
                    for block in blocks:
                        b_text = block.get("text", "")
                        
                        # Check if this block contains an entity (like an image)
                        ranges = block.get("entityRanges", [])
                        if ranges:
                            for r in ranges:
                                e_key = str(r.get("key", ""))
                                if e_key in entity_map:
                                    entity_obj = entity_map[e_key]
                                    if entity_obj.get("type") == "MEDIA":
                                        try:
                                            media_id = str(entity_obj["data"]["mediaItems"][0]["mediaId"])
                                            if media_id in media_dict:
                                                # Print the image right where the block is
                                                md_content += f"![Article Image]({media_dict[media_id]})\n\n"
                                        except Exception as ex:
                                            print(f"Error extracting media id: {ex}")
                                            pass
                        
                        if b_text.strip():
                            # Render standard text
                            # (We could apply inline styles like Bold/Italic here based on inlineStyleRanges, 
                            # but simple text dump is typically enough for translation context)
                            
                            # Simple bold support
                            styles = block.get("inlineStyleRanges", [])
                            # For simplicity, if the whole block is mostly bold, make it bold
                            if any(s.get("style") == "Bold" and s.get("length", 0) > len(b_text) * 0.5 for s in styles):
                                md_content += f"**{b_text}**\n\n"
                            else:
                                md_content += f"{b_text}\n\n"
        except Exception as e:
            error_msg = f"Error fetching from fxtwitter: {e}"
            print(error_msg)
            return error_msg
            
    else:
        print(f"Crawler Agent: Navigating to {url} using Defuddle...")
        try:
            # Run defuddle parse <url> --md
            result = subprocess.run(
                ["defuddle", "parse", url, "--md"],
                capture_output=True,
                text=True,
                check=True,
                shell=True
            )
            md_content = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = f"Error loading URL with Defuddle: {e}\n{e.stderr}"
            print(error_msg)
            return error_msg
        except FileNotFoundError:
            error_msg = "Error: 'defuddle' command not found. Please install it with 'npm install -g defuddle'."
            print(error_msg)
            return error_msg
    
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
    
    print(f"Crawler Agent: Extracting from {filepath}...")
    
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

def run(target_input, output_file=None):
    if os.path.exists(target_input):
        res = extract_from_file(target_input)
    elif target_input.startswith("http"):
        res = extract_from_url(target_input)
    else:
        print("Error: Target not found and not a valid URL")
        sys.exit(1)
        
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(res)
        print(f"Crawler Agent: Output saved to {output_file}")
    else:
        print(res[:500] + "...")
    return res

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crawler_agent.py <url_or_file> [output_file]")
        sys.exit(1)
        
    target = sys.argv[1]
    outfile = sys.argv[2] if len(sys.argv) > 2 else None
    run(target, outfile)
