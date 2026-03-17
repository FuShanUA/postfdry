"""
infographic_illustrator.py

Agent 5: Generates the specialized prompt for rendering a 16:9 infographic.
"""

import sys
import os
import re
from cover_illustrator import extract_key_points

def generate_infographic_prompt(points, title_cn):
    if not points:
        return ""
        
    points_list = ", ".join([f"{p}" for p in points])
    
    style_desc = (
        "A 16:9 widescreen detailed infographic for '" + title_cn + "'. "
        "LAYOUT: A sophisticated business strategic landscape or roadmap. 10 clear nodes for the 10 trends. "
        "STYLE: High-end 2.5D isometric illustration style or glassmorphism business aesthetic. "
        "Vibrant but professional. Use rich gradients and elegant micro-shadows. "
        "ELEMENTS: Each trend node should have a small, intuitive 3D icon. Use flowing connector lines with glowing accents. "
        "COLORS: Sophisticated palette: Warm Terracotta, Deep Indigo, and Muted Gold on a very clean tech-white or light-grey background. "
        "TEXT: All 10 labels in Simplified Chinese must be sharp, bold, and center-stage: " + points_list + ". "
        "OVERALL FEEL: Premium, complex, and highly visual. Not a simple bullet list. A data visual masterpiece."
    )
    
    prompt = f"[Total Strategy Map] PROMPT: A 16:9 widescreen infographic for '{title_cn}'. {style_desc}"
    return prompt

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python infographic_illustrator.py <result.md>")
        sys.exit(1)
        
    md_path = sys.argv[1]
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_cn_match = re.search(r'^Title:\s*(.+)$', content, re.M)
    title_cn = title_cn_match.group(1).strip() if title_cn_match else "Untitled"
    
    points = extract_key_points(md_path)
    prompt = generate_infographic_prompt(points, title_cn)
    
    if prompt:
        print(prompt)
    else:
        print("Error: No points found for infographic.")
