"""
cover_illustrator.py

Agent 4: Generates the specialized prompt for rendering a 16:9 article cover.
"""

import sys
import os
import re

def extract_key_points(md_path):
    if not os.path.exists(md_path):
        return None
        
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    points = re.findall(r'^###\s*(\d+\..*?)$', content, re.M)
    if not points:
        points = re.findall(r'^###\s*(.*?)$', content, re.M)
    return points[:10]

def generate_cover_prompt(points, title_cn):
    labels = "1. 组织觉醒, 2. AI-Ready 数据, 3. 生产力优先, 4. Agent 可观测性" # default fallback
    if points and len(points) >= 4:
        labels = ", ".join([p.split('：')[0] if '：' in p else p for p in points[:4]])

    style_desc = (
        "Minimalist professional technical illustration for a premium business journal cover. 16:9 Widescreen aspect ratio. "
        "COLORS: Warm professional palette: Deep Amber (#FFBF00) and Terracotta (#E2725B) accents on a clean, bright Cream background (#FDF5E6). "
        "LAYOUT: A large, elegant central metaphor of a 'Solid Foundation' or a 'Lighthouse' guiding through a data ocean. "
        "STYLE: Clean flat vector art with geometric precision. Generous breathable white space. High-end aesthetic. "
        "TEXT: Large Simplified Chinese labels embedded in the illustration for: " + labels + ". "
        "NO dark themes, NO icon-spam. Aim for clarity and prestige."
    )
    
    prompt = f"[Warm Widescreen Cover] PROMPT: A 16:9 widescreen professional illustration for '{title_cn}'. STYLE: {style_desc}"
    return prompt

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cover_illustrator.py <result.md>")
        sys.exit(1)
        
    md_path = sys.argv[1]
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_cn_match = re.search(r'^Title:\s*(.+)$', content, re.M)
    title_cn = title_cn_match.group(1).strip() if title_cn_match else "Untitled"
    
    points = extract_key_points(md_path)
    
    print(generate_cover_prompt(points, title_cn))
