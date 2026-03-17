"""
translator_agent.py

Agent 2: Handles "信达雅" translation.
Generates the prompt for the LLM and handles the deterministic scrubbing.
"""

import sys
from common_utils import load_skill_content, load_readme_content, load_writing_style, deterministic_scrub

def build_translation_prompt(source_text, thoughts="", style="casual"):
    humanizer_rules = load_skill_content("humanizer-zh")
    subtranslator_rules = load_readme_content("subtranslator")
    writing_style, _ = load_writing_style()
    verbalizer_rules = load_readme_content("verbalizer")
    
    thoughts_header = f"> **译者导读**: {thoughts}\n\n" if thoughts else ""

    prompt = f"""
### ROLE
You are a Senior Tech Columnist and Professional Translator. 
You transform technical content into "Human-Native" Chinese.

### GUIDELINES (FOUR-FOLD GUARANTEE)
1. DE-AI FLAVOR: {humanizer_rules[:1500]}
2. NATIVE FLOW: {subtranslator_rules[:1500]}
3. PERSONAL STYLE: {writing_style[:1500]}
4. PERSONA & TONE: {verbalizer_rules[:1000]} (Target Style: {style})

### CRITICAL CONSTRAINTS (HARD RULES)
- NO long dashes (——). Use commas, colons or separate sentences.
- NO "translationese" (e.g., avoid "当...时", "被...", "不可或缺").
- NO repetitive sentence structures. Vary the pace.
- NO metadata modification (Keep Frontmatter intact).
- USE professional terminology (e.g., FDE, Agentic Infrastructure).
- PRESERVE structure: If the source uses bullet points or numbered lists, you MUST maintain that exact structure. Do NOT collapse lists into paragraphs.
- PRESERVE IMAGES: You MUST preserve all original markdown image tags `![alt](url)` exactly as they appear in the source text, maintaining their original structural positions.

### INPUT TEXT
{thoughts_header}{source_text}

### OUTPUT
Return ONLY the translated markdown content.
"""
    return prompt

def run_scrub(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    scrubbed = deterministic_scrub(text)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(scrubbed)
    print(f"Translator Agent: Deterministic scrub applied to {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translator_agent.py <file> [--prompt-only] [--thoughts '...'] [--style casual]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    prompt_only = False
    thoughts = ""
    style = "casual"
    
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "--prompt-only":
            prompt_only = True
        elif sys.argv[i] == "--thoughts" and i + 1 < len(sys.argv):
            thoughts = sys.argv[i+1]
        elif sys.argv[i] == "--style" and i + 1 < len(sys.argv):
            style = sys.argv[i+1]
            
    if prompt_only:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        print(build_translation_prompt(text, thoughts, style))
    else:
        run_scrub(input_file)
