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
