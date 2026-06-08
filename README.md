# PostOS - 智能化专家级出版工作流平台 (Standalone 2.0)

智能化、去 AI 味的专家级公众号出版与译介工作流平台。本仓库已完全剥离封装，克隆即可独立开箱即用。

---

## 💻 安装说明

### 🍎 macOS 用户安装

打开终端 (Terminal)，进入项目根目录，依次运行：

```bash
# 1. 运行一键式环境安装与配置脚本（全自动创建虚拟环境、安装依赖及爬虫浏览器）
./setup.sh

# 2. 启动 PostOS GUI 交互界面
.venv/bin/python scripts/postos_gui.py
```

---

### 🪟 Windows 用户安装

打开命令提示符 (CMD) 或 PowerShell，进入项目根目录，依次运行：

```cmd
:: 1. 双击或在命令行运行 Windows 一键安装批处理文件
setup.bat

:: 2. 启动 PostOS GUI 交互界面
.venv\Scripts\python scripts\postos_gui.py
```

---

## ⚙️ 统一 API Key 密钥配置

首次使用时，请直接在 GUI 界面最上方的配置栏中选择对应厂商，输入你的 API Key 并点击 **「保存 Key」**。
系统会自动在本地创建并同步维护 `.env` 文件。你输入的密钥会以遮罩星号安全显示，后续运行任务时无需重复配置。

---

## 📄 PDF 模板自定义说明

当前仓库的 `assets/templates/federation/` 目录下默认包含的 `cover.pdf`（封面）、`inside.pdf`（正文背景）和 `back.pdf`（封底）均为**样例模板**。

如需制作和使用自己专属的 PDF 模板，请按以下步骤操作：

1. **准备模板 PDF 文件**：
   - 准备好包含特定设计元素、Logo 和页边距背景的三个 PDF 页面（尺寸建议为标准 A4：595 x 842 pt）。
   - **封面** (`cover.pdf`)：用于覆盖第一页，其中需要预留标题和发布机构/时间的空白文字输入区域。
   - **正文背景** (`inside.pdf`)：将自动作为所有正文页的背景底层。
   - **封底** (`back.pdf`)：将自动拼接到 PDF 最后一页作为尾页。
2. **替换模板文件**：
   - 将这三个文件重命名并覆盖放置到 `assets/templates/federation/` 目录下对应的同名文件。
3. **调整标题及元数据渲染位置**：
   - 若新封面的标题定位区域与样例不同，可编辑 `config/styler_federation.json` 配置文件。
   - 修改其中 `title`、`publisher`、`date` 的 `pos` 坐标范围 `[x0, y0, x1, y1]`，以此精准定位渲染文字的锚点位置。

