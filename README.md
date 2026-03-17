# Postfdry 自动化编辑工作流 (Postfdry-OS)

Postfdry 是一个强大的 7 智能体（7-Agent）虚拟编辑部流水线，旨在将任何 URL、文本、PDF 或文件转换为精美、经过全面“去 AI 味”和本地化处理的专业文章，并最终输出为排版精良的 Markdown、HTML（完美适配微信公众号）或 PDF。

## 🌟 核心理念与架构

该项目采用多智能体协同流水线架构，涵盖内容抓取、翻译、重写、校验、人设润色到最终排版生成的全链路：

1. **Agent 1: 爬虫与内容抓取 (Crawler Agent)**
   - 自动识别并解析常规网页、PDF、DOCX 等文件格式。
   - **特色功能**：由于 X.com/Twitter 对 Readability 爬虫深度混淆，本爬虫直接对接 `fxtwitter` API，精准抓取推文中的所有配图和视频，并在 Markdown 中**原地保留图片结构和正确位置**。同时支持 `Defuddle` CLI 的本地网页解析。
2. **Agent 2: 翻译与母语化 (Translator Agent)**
   - 针对英文文章和长文案，将其翻译成“人类母语风格”的顺畅中文。
   - 严格保证所有原文内嵌的图表（Markdown 图片标签）不丢失且位置不变。
3. **Agent 3: 深度重写与提炼 (Rewriter Agent)**
   - 基于提取或翻译的内容，进行深度改写和结构化提炼。
   - 去除“AI 味”，增强通读性和易用性。
4. **Agent 4/5: 风格化与审核 (Style & Review Agents)** 
   - 强约束打磨语感，确保输出内容符合特定的组织传讯或专业媒体口吻（基于 `HARD_CONSTRAINTS`）。
5. **Agent 6: PDF 打包与生成 (PDF Agent)**
   - 结合主题排版（Theme Factory），将重写后的绝佳内容渲染为 PDF 报告/白皮书。
6. **Agent 7: 微信公众号排版发布 (WeChat Publisher)**
   - 一键将 Markdown 转换为带原生微信排版和 CSS 样式的 HTML 片段，直接处理剪贴板样式复制，并确保源文章中的图片（含推文多图等）精准挂载。

## 🚀 核心亮点

- **自动保持多图排版**: 这是在处理 X.com 长推文时的杀手锏功能。无论原文结构多复杂，原配图都能被正确映射回重写的中文长文中。
- **本地防拥堵与并行处理**: 多个微信排版脚本允许同时并发生成 HTML 而不相互锁定日志文件。
- **灵活的落地方案**: 基于底层大语言模型能力构建，可热插拔式切换各类 LLM 后端。

## 🛠 安装与使用指南

**1. 前置依赖**
确保你已安装了 Python 3 和 Node.js 环境，并安装相关的模块包：
```bash
# Python 依赖
pip install -r requirements.txt 

# 安装 defuddle 及 baoyu 相关 markdown 渲染工具 (按全局方式)
npm install -g @kepano/defuddle
```

**2. 核心调用示例**
所有脚本位于 `agents/` 目录下，直接调用对应的 Python 脚本即可串联测试：

例如，要提取一篇 Twitter 文章并生成 Markdown：
```bash
python agents/crawler_agent.py "https://x.com/julienbek/status/2029680516568600933" original_material.md
```

后续调用翻译及排版模块：
```bash
# 翻译
python agents/translator_agent.py original_material.md
# 生成微信 HTML
python agents/wechat_publisher.py translated_article.md
```

## 📂 项目结构

- `/agents`: 核心的 7 个 Python 智能体脚本（爬虫、翻译、重写、排版等）。
- `SKILL.md`: 配合大语言模型智能体（如 Obsidian/Claude 的自建 Agent 系统）使用的自动化指令定义文件。
- `/scripts`: 各类辅助 Bash/PowerShell 脚本。
- `README.md`: 本项目说明。

## 🤝 贡献与反馈

欢迎提交 Issue 和 Pull Request，我们致力于打造出最好用的个人/企业全自动信息消化分发一体化平台。
