"""
wechat_publisher.py (Simplified)
"""
import sys
import os
import subprocess
import re

BAOYU_MD_TO_HTML = r"d:\cc\Library\Tools\baoyu-skills\skills\baoyu-markdown-to-html\scripts\main.ts"

def generate_wechat_assets(md_path):
    abs_md_path = os.path.abspath(md_path)
    cwd = os.path.dirname(abs_md_path)
    
    base_name = os.path.basename(abs_md_path).replace(".md", "")
    tmp_out = os.path.join(cwd, f"{base_name}_pub_log.txt")
    cmd = f'npx -y bun "{BAOYU_MD_TO_HTML}" "{abs_md_path}" --theme default > "{tmp_out}" 2>&1'
    print(f"Executing: {cmd}")
    subprocess.run(cmd, shell=True, cwd=cwd)
    
    # Expected HTML path
    html_path = abs_md_path.replace(".md", ".html")
    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found.")
        return

    print(f"HTML generated at {html_path}. Fixing image paths...")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Manual fix for known assets if metadata parsing failed
    # We use fallback paths relative to the current directory
    abs_cover = os.path.normpath(os.path.join(cwd, "assets", "cover.png"))
    abs_info = os.path.normpath(os.path.join(cwd, "assets", "infographic.png"))
    
    replacements = {
        "MDTOHTMLIMGPH_0": "file:///" + abs_cover.replace("\\", "/"),
        "MDTOHTMLIMGPH_1": "file:///" + abs_cover.replace("\\", "/"), 
        "MDTOHTMLIMGPH_2": "file:///" + abs_info.replace("\\", "/")
    }
    
    # Try to find more replacements in the log file
    if os.path.exists(tmp_out):
        try:
            with open(tmp_out, 'r', encoding='utf-8', errors='ignore') as f:
                logs = f.read()
            # Find JSON block reliably
            import json
            start_idx = logs.find('{')
            end_idx = logs.rfind('}')
            if start_idx != -1 and end_idx != -1:
                try:
                    data = json.loads(logs[start_idx:end_idx+1])
                    if "contentImages" in data:
                        for img in data["contentImages"]:
                            placeholder = img.get("placeholder")
                            local_path = img.get("localPath")
                            if placeholder and local_path:
                                abs_local = os.path.normpath(os.path.join(cwd, local_path))
                                web_path = "file:///" + abs_local.replace("\\", "/")
                                replacements[placeholder] = web_path
                    if "coverImage" in data:
                        abs_cover = os.path.normpath(os.path.join(cwd, data["coverImage"]))
                        replacements["MDTOHTMLIMGPH_0"] = "file:///" + abs_cover.replace("\\", "/")
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON from logs: {e}")
        except Exception as e:
            print(f"Error reading {tmp_out}: {e}")

    for placeholder, web_path in replacements.items():
        if placeholder in html_content:
            html_content = html_content.replace(placeholder, web_path)
            print(f"  Fixed {placeholder}")

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Done.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    generate_wechat_assets(sys.argv[1])
