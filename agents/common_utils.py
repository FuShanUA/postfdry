"""
common_utils.py

Shared utilities for Postfdry agents.
"""

import os
import re

# Paths
AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
POSTFDRY_DIR = os.path.dirname(AGENTS_DIR)
TOOLS_DIR = os.path.dirname(POSTFDRY_DIR)
COMMON_DIR = os.path.join(TOOLS_DIR, "common")
ROOT_DIR = os.path.dirname(os.path.dirname(TOOLS_DIR)) # d:\cc

def load_skill_content(name):
    """Load SKILL.md for a given skill name."""
    path = os.path.join(TOOLS_DIR, name, "SKILL.md")
    if not os.path.exists(path):
        # Try one level up if not found (for agents/skills)
        path = os.path.join(ROOT_DIR, ".agents", "skills", name, "SKILL.md")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def load_readme_content(name):
    """Load README.md for a given skill name."""
    path = os.path.join(TOOLS_DIR, name, "README.md")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def load_style_guide():
    """Load HARD_CONSTRAINTS.md specific rules."""
    path = os.path.join(COMMON_DIR, "HARD_CONSTRAINTS.md")
    rules = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("|") and not line.startswith("| Rule") and not line.startswith("| description") and not line.startswith("|---"):
                    parts = [p.strip() for p in re.split(r'(?<!\\)\|', line) if p.strip()]
                    if len(parts) >= 2:
                        pattern = parts[1].strip('`').replace(r'\|', '|')
                        replacement = parts[2].strip('`').replace(r'\|', '|') if len(parts) > 2 else ""
                        rules.append((pattern, replacement))
    return rules


def load_writing_style():
    """Load WritingStyle rules and blacklist words."""
    content = load_skill_content("WritingStyle")
    if not content:
        content = load_readme_content("WritingStyle")
        
    blacklist = []
    # Extract blacklist words from patterns
    matches = re.findall(r'- \*\*.+?\*\*: (.+)', content)
    for m in matches:
        words = [w.strip() for w in m.split(',')]
        blacklist.extend(words)
    return content, blacklist

def deterministic_scrub(text):
    """Hard-fixes that MUST be applied regardless of LLM output."""
    
    lines = text.split('\n')
    processed_lines = []
    
    guide_rules = load_style_guide()
    # blacklist_words extraction is declarative for LLM, 
    # but could be used here for mechanical stripping if needed.
    # For now, we rely on guide_rules (HARD_CONSTRAINTS.md).
    
    in_metadata = True
    for line in lines:
        if in_metadata:
            if line.strip() == "" and len(processed_lines) > 0:
                in_metadata = False
            processed_lines.append(line)
            continue
            
        # Skip Markdown structures: images, links, headers, comments
        if line.startswith("#") or line.startswith("!") or line.startswith("<!--") or line.strip().startswith("- **"):
            processed_lines.append(line)
            continue
            
        for pattern, replacement in guide_rules:
            try:
                if pattern in ["!", "?", ":", ";"] and ("](" in line or "http" in line):
                    continue
                line = re.sub(pattern, replacement, line)
            except: pass
            
        processed_lines.append(line)
        
    return '\n'.join(processed_lines)
