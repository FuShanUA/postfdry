---
name: postfdry
description: Transform content (URL/Text/PDF/File) into polished, humanized, and illustrated articles. Operates as a 7-Agent virtual editorial team (Postfdry-OS).
---

# Postfdry-OS (Article Deep Polish Editorial Team)

A comprehensive content transformation workflow that orchestrates **extraction**, **translation**, **humanization**, **illustration**, and **multi-format publishing** (PDF & WeChat).

This skill operates as a virtual 7-Agent team. As the Antigravity Orchestrator, you must coordinate these agents to produce the final output.

## The 7-Agent Team

### Agent 1: Content Crawler (内容爬取)
- **Role**: Extracts raw text from URLs, PDFs, or local files.
- **Input**: Original URL or File Path.
- **Output**: `original_material.md`
- **Execution**: `python Library/Tools/postfdry/agents/crawler_agent.py <input> D:\cc\Projects\<project_name>\original_material.md`

### Agent 2: Translator (专业翻译)
- **Role**: Translates source to "信达雅" commercial Chinese, applying strict writing style rules and terminology constraints.
- **Input**: `original_material.md`
- **Output**: `translated_article.md`
- **Execution**: 
  1. `python Library/Tools/postfdry/agents/translator_agent.py <original_material.md> --prompt-only > prompt.md`
  2. Use LLM to generate the translation based on the prompt, save to `translated_article.md`
  3. `python Library/Tools/postfdry/agents/translator_agent.py D:\cc\Projects\<project_name>\translated_article.md` (Applies deterministic scrub)

### Agent 3: Rewriter (深度改写)
- **Role**: Acts as a Senior Industry Researcher. Rewrites the article for the domestic B2B audience, adding marketing intent, industry insights, and a 3-part structured conclusion.
- **Input**: `original_material.md` + Intent description.
- **Output**: `rewritten_article.md`
- **Execution**:
  1. `python Library/Tools/postfdry/agents/rewriter_agent.py <original_material.md> --prompt-only --intent "..." > prompt.md`
  2. Use LLM to generate the rewrite based on the prompt, save to `rewritten_article.md`
  3. `python Library/Tools/postfdry/agents/rewriter_agent.py D:\cc\Projects\<project_name>\rewritten_article.md` (Applies deterministic scrub)

### Agent 4: Cover Illustrator (头图设计)
- **Role**: Parses the translated or rewritten article to generate a professional 16:9 warm-toned business cover.
- **Input**: `translated_article.md` or `rewritten_article.md`
- **Output**: Generates a prompt for `assets/cover.png`
- **Execution**: 
  1. `python Library/Tools/postfdry/agents/cover_illustrator.py <md_file>` -> Outputs Prompt
  2. Call `baoyu-image-gen` using the prompted text: `npx -y bun d:\cc\Library\Tools\baoyu-skills\skills\baoyu-image-gen\scripts\main.ts --prompt "..." --image "assets\cover.png" --ar 16:9`

### Agent 5: Infographic Illustrator (插图设计)
- **Role**: Visualizes the core trends or complex logic into a 16:9 infographic.
- **Input**: `rewritten_article.md` (or specific complex sections)
- **Output**: Generates a prompt for `assets/infographic.png`
- **Execution**:
  1. `python Library/Tools/postfdry/agents/infographic_illustrator.py <md_file>` -> Outputs Prompt
  2. Call `baoyu-image-gen` using the prompted text: `npx -y bun d:\cc\Library\Tools\baoyu-skills\skills\baoyu-image-gen\scripts\main.ts --prompt "..." --image "assets\infographic.png" --ar 16:9`

### Agent 6: PDF Publisher (译介资料排版)
- **Role**: Merges the faithful translation and cover image into a professional PDF using enterprise templates.
- **Input**: `assets/cover.png` + `translated_article.md`
- **Output**: `publish/Translated_Document.pdf`
- **Execution**: `python Library/Tools/postfdry/agents/pdf_publisher.py <translated_article.md>`

### Agent 7: WeChat Publisher (公众号排版)
- **Role**: Assembles the deep rewrite, cover, and infographics into WeChat-compatible Markdown & HTML.
- **Input**: `assets/cover.png` + `rewritten_article.md` + `assets/*_infographic.png`
- **Output**: `publish/WeChat_Article.html`
- **Execution**: `python Library/Tools/postfdry/agents/wechat_publisher.py <rewritten_article.md> <cover.png>`

---

## Two Core Operating Modes (双元工作流)

As the Orchestrator, you must manage the pipeline in `D:\cc\Projects\<project_name>\` by choosing ONE of the following two modes based on the user's request.

### Mode 1: Translation Mode (翻译模式)
Used for creating faithful, professional internal reading materials.
1.  **Parse**: Run **Agent 1 (Crawler)** on the source URL/file to get `original_material.md`.
2.  **Translate**: Run **Agent 2 (Translator)** to generate the "信达雅" `translated_article.md` (remember to run the deterministic scrub script post-LLM).
3.  **Cover**: Run **Agent 4 (Cover Illustrator)** to generate the 16:9 prompt based on the translation, then call `baoyu-image-gen` to render `assets/cover.png`.
4.  **PDF Assembly**: Run **Agent 6 (PDF Publisher)** using the translation and cover to assemble `publish/Translated_Document.pdf`.

### Mode 2: Rewriting Mode (改写模式)
Used for creating deep, localized marketing content for public distribution (like WeChat).
1.  **Parse**: Run **Agent 1 (Crawler)** on the source URL/file to get `original_material.md`.
2.  **Rewrite**: Run **Agent 3 (Rewriter)** to generate the deep insights `rewritten_article.md` (remember to run the deterministic scrub script post-LLM).
3.  **Cover**: Run **Agent 4 (Cover Illustrator)** to generate the 16:9 prompt based on the rewritten text, then call `baoyu-image-gen` to render `assets/cover.png`.
4.  **Infographic**: Run **Agent 5 (Infographic Illustrator)** to generate the 16:9 prompt for infographics, then call `baoyu-image-gen` to render `assets/infographic_*.png`.
5.  **WeChat Assembly**: Run **Agent 7 (WeChat Publisher)** using the rewrite, cover, and infographics to assemble the final HTML draft.

### Mode 3: Sync Mode (同步模式)
Used to generate both internal PDF and external WeChat documents simultaneously, leveraging parallel execution.
1. **Parse**: Run **Agent 1 (Crawler)** to extract `original_material.md`.
2. **Translate & Rewrite (Parallel)**:
   - Run **Agent 2 (Translator)** for `translated_article.md`.
   - Run **Agent 3 (Rewriter)** for `rewritten_article.md`.
3. **Illustrate (Parallel)**:
   - Run **Agent 4 (Cover Illustrator)** to generate `assets/cover.png` (using `translated_article.md` or `rewritten_article.md`).
   - Run **Agent 5 (Infographic Illustrator)** to generate `assets/infographic_*.png` (using `rewritten_article.md`).
4. **Publish (Parallel)**:
   - Run **Agent 6 (PDF Publisher)** using Translation + Cover.
   - Run **Agent 7 (WeChat Publisher)** using Rewrite + Cover + Infographic.

Make sure to ALWAYS run the "Deterministic Scrub" step via the Agent scripts after the LLM generates `translated` or `rewritten` content before proceeding to image generation or publishing.

## Dependencies
- `WritingStyle`, `humanizer-zh`, `subtranslator`, `verbalizer`
- `HARD_CONSTRAINTS.md`
- `baoyu-markdown-to-html` and `baoyu-image-gen`
