"""
illustrator.py - Postfdry Illustration Prompt Generator

Analyzes the Executive Summary in result.md and generates high-quality 
prompts for infographics using the established style and logic.
"""

import sys
import os
import re

def extract_key_points(md_path):
    """Extract all core points from the article body (headers)."""
    if not os.path.exists(md_path):
        return None
        
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract numbered headers (e.g., "1. XXX")
    points = re.findall(r'^###\s*(\d+\..*?)$', content, re.M)
    
    # If not found, try any level 3 headers
    if not points:
        points = re.findall(r'^###\s*(.*?)$', content, re.M)
        
    return points[:10]

def generate_cover_prompt(points, title_cn, title_en):
    """Refined cover prompt: Warm style, 16:9, 3-4 key points labels."""
    labels = "1. 组织觉醒, 2. AI-Ready 数据, 3. 生产力优先, 4. Agent 可观测性"
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
    
    prompt = f"""[Warm Widescreen Cover]
PROMPT: A 16:9 widescreen professional illustration for '{title_cn}'. 
STYLE: {style_desc}
"""
    return prompt

def generate_infographic_prompt(points, title_cn, title_en):
    """Comprehensive 10-point 'Total Map' in the same warm style."""
    if not points:
        return "Error: No points found for infographic."
        
    points_list = ", ".join([f"{p}" for p in points])
    
    style_desc = (
        "A comprehensive 'Strategic Landscape' infographic mapping all 10 key article trends. 16:9 Widescreen aspect ratio. "
        "LAYOUT: A structured central-hub or grid layout visualizing 10 distinct trends. "
        "STYLE: Clean tech-consulting roadmap. Professional and minimal. Use subtle connector lines. "
        "COLORS: Bright Cream background (#FDF5E6) with Warm Amber and Soft Rust accents to match the cover. "
        "TEXT: All 10 labels in Simplified Chinese must be clearly legible: " + points_list + ". "
        "NO icons or very minimal geometric dots. High clarity is the absolute priority."
    )
    
    prompt = f"""[Total Strategy Map - 10 points]
PROMPT: A 16:9 widescreen infographic for '{title_cn}'.
{style_desc}
"""
    return prompt

def main():
    if len(sys.argv) < 2:
        print("Usage: python illustrator.py <result.md>")
        sys.exit(1)
        
    md_path = sys.argv[1]
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_cn_match = re.search(r'^Title:\s*(.+)$', content, re.M)
    title_en_match = re.search(r'^EngTitle:\s*(.+)$', content, re.M)
    
    title_cn = title_cn_match.group(1).strip() if title_cn_match else "Untitled"
    title_en = title_en_match.group(1).strip() if title_en_match else "Untitled"
    
    points = extract_key_points(md_path)
    
    print("\n" + "="*40)
    print("ASSET 1: ARTICLE COVER (头图)")
    print("="*40)
    print(generate_cover_prompt(points, title_cn, title_en))
    print("\n[INSTRUCTION] Use baoyu-image-gen via terminal to generate the cover. You MUST pass --ar 16:9. Example:")
    print("npx -y bun d:\\cc\\Library\\Tools\\baoyu-skills\\skills\\baoyu-image-gen\\scripts\\main.ts --prompt \"...\" --image \"D:\\cc\\Projects\\<project_name>\\assets\\cover.png\" --ar 16:9")
    
    print("\n" + "="*40)
    print("ASSET 2: CONTENT INFOGRAPHIC (信息图)")
    print("="*40)
    if points:
        print(generate_infographic_prompt(points, title_cn, title_en))
        print("\n[INSTRUCTION] Use baoyu-image-gen via terminal to generate the infographic. You MUST pass --ar 16:9. Example:")
        print("npx -y bun d:\\cc\\Library\\Tools\\baoyu-skills\\skills\\baoyu-image-gen\\scripts\\main.ts --prompt \"...\" --image \"D:\\cc\\Projects\\<project_name>\\assets\\infographic_zh.png\" --ar 16:9")
    else:
        print("Executive Summary not found. Skipping infographic.")

if __name__ == "__main__":
    main()
