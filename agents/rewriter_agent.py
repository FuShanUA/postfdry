"""
rewriter_agent.py

Agent 3: Handles depth-enhancing rewriting.
Generates the prompt for the Rewrite LLM and handles the deterministic scrubbing.
"""

import sys
from common_utils import load_skill_content, load_readme_content, load_writing_style, deterministic_scrub

def build_rewriting_prompt(source_text, thoughts="", style="intellectual", intent="面向国内 B 端读者提供数据管理领域的深度见解，强调落地实践。"):
    humanizer_rules = load_skill_content("humanizer-zh")
    writing_style, _ = load_writing_style()
    verbalizer_rules = load_readme_content("verbalizer")
    
    prompt = f"""
### ROLE
你是一名数据治理语境下的资深研究者。你不仅对全球数据技术趋势有深刻见解，更熟悉中国国内的政策环境（如数据要素、数据资产、DCMM 贯标、可信数据空间等）。

### TASK
请根据原文内容，结合下方提供的【作者/宣发意图】，以资深专家的视角“改写”生成一篇高水平的技术深度观察文章。

### INTENT (作者意图)
{intent}

### WRITING STRATEGY
1. **结构化页头**：文章开头必须包含以下格式的标题和作者信息：
    # [引人入胜的中文新标题]
    作者：数据治理研究院
2. **开头引入 (The Hook)**：结合国内 AI 或数据建设热点引出话题，形式要像同事间分享深度见解，避免空洞。并在开头适当增加译者导读性质的评论。
3. **正文改写 (Completeness First)**：
    - **必须涵盖原文的所有核心点位**。即便为了逻辑连贯进行了整合，也绝对不能遗漏原文中任何一个点的核心内涵。
    - **深度融合**：在原文框架内适当补充与营销/宣发意图相关的分析与国内现状的印证，使文章贴近本土语境。
    - **保留图像**：必须在改写后的相应位置，完整保留原文中所有的 Markdown 图片标签（如 `![原图](链接)`），绝对不得删减或修改图片链接。
4. **专家风范 (Expert Style)**：
    - **严控翻译腔**：严禁出现“这不仅是...更是...”、“不仅仅是...而且是...”等西化结构。禁止使用“不是...而是...”（请用“并非...，而是...”替代）。
    - **严禁英文残留**：正文中禁止出现括号里的英文原词（如：`数据质量（Data Quality）`），除非是极其通用的技术缩写（AI, API, POC）。请直接使用贴切的中文。
    - **文字洗练**：去除所有废话和 AI 式的修饰词。
    - **应用积累模式**：遵循以下风格要点：{writing_style[:1000]}
5. **结尾总结 (The Three-Part Finale)**：
    文章最后必须包含以下三个板块，结构清晰：
    - **【核心要点提炼】**：用 Bullet Points 简洁明了地总结全文核心洞察。
    - **【原文金句摘录】**：挑选 3-5 句原文最具洞见的句子，并**必须将其翻译为极具冲击力的中文金句**（严禁保留英文原文）。每句话控制在 25 字以内。
    - **【国内落地启示】**：针对国内企业数据部门、数字化管理者、数科公司或技术供应商提出具体、可操作的启示。
6. **结构化页脚**：
    在全文最后，使用独立的一行添加以下作者简介和原文信息，格式如下：
    *作者简介：数据治理研究院。文章原标题：[此处填写原文英文标题]*

### GUIDELINES
- DE-AI FLAVOR: {humanizer_rules[:1000]}
- PERSONA & TONE: {verbalizer_rules[:500]} (Target Style: {style})
- **禁止废话**：除了要求的部分，不要有任何多余的开场白或结束语。
- **人称控制**：除必要主观判断外，尽量将观点融入叙述，读起来像一篇连贯的独立观察。

### EDITORS THOUGHTS
{thoughts if thoughts else "（无额外思考，按专业视角自由发挥）"}

### INPUT TEXT (ORIGINAL)
{source_text}

### OUTPUT
直接返回改写后的 Markdown 内容。
"""
    return prompt

def run_scrub(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    scrubbed = deterministic_scrub(text)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(scrubbed)
    print(f"Rewriter Agent: Deterministic scrub applied to {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rewriter_agent.py <file> [--prompt-only] [--thoughts '...'] [--style intellectual] [--intent '...']")
        sys.exit(1)
        
    input_file = sys.argv[1]
    prompt_only = False
    thoughts = ""
    style = "intellectual"
    intent = "面向国内 B 端读者提供数据管理领域的深度见解，强调落地实践。"
    
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "--prompt-only":
            prompt_only = True
        elif sys.argv[i] == "--thoughts" and i + 1 < len(sys.argv):
            thoughts = sys.argv[i+1]
        elif sys.argv[i] == "--style" and i + 1 < len(sys.argv):
            style = sys.argv[i+1]
        elif sys.argv[i] == "--intent" and i + 1 < len(sys.argv):
            intent = sys.argv[i+1]
            
    if prompt_only:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        print(build_rewriting_prompt(text, thoughts, style, intent))
    else:
        run_scrub(input_file)
