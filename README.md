# 📈 DSA Core - AI 驱动量化分析终端

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-brightgreen)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![Lightweight-Charts](https://img.shields.io/badge/TradingView-Lightweight--Charts-blueviolet)

DSA Core 是一款集成了 **实时行情展示**、**AI 策略推理**、**持仓图像诊断** 以及 **舆情监测** 的一站式量化分析控制台。项目采用 Python FastAPI 作为后端核心引擎，前端借助 TradingView Lightweight Charts 打造极简、流畅且具科技感的暗黑风交易终端。

---

## 📸 终端预览

> 💡 *提示：建议上传您的项目实际截图至 `docs/assets/` 目录并替换以下图片链接。*

### 1. 核心看板与行情走势
![行情分析界面](docs/assets/dashboard.jpg)
*支持实时行情 K 线渲染、AI 深度逻辑诊断、核心入场/止损/目标位演算及实时舆情监测。*

### 2. AI 持仓识图诊断
![识图分析界面](docs/assets/vision_analysis.jpg)
*上传股票持仓/盘口截图，AI 引擎自动识别股票代码与成本，并实时输出加减仓策略。*

---

## ✨ 核心特性

- ⚡ **毫秒级 WebSockets 通信**：前端 UI 与后端实时保持长连接，实现 K 线数据与 AI 分析结论的无缝推送。
- 📊 **交互式 TradingView 图表**：基于 `lightweight-charts` 打造，完美支持自适应缩放与流畅的 K 线渲染。
- 🧠 **AI 大模型逻辑演算**：集成多模态 LLM，提供交易策略生成（包含建议入场价、配置权重、硬止损位及目标收益价）。
- 📷 **多模态持仓识图**：支持图片上传诊断，一键提取截图信息并给出针对性盘口分析。
- 🛡️ **高容错与网络自愈**：内置断线重连、数据清洗降级以及网络异常自动提示机制。
- 🚀 **一键极速启动**：提供开箱即用的 Python 启动引擎，无需繁琐的命令行配置。

---

## 🛠️ 技术栈

- **后端 (Backend)**: Python 3.10+, FastAPI, Uvicorn, WebSockets
- **前端 (Frontend)**: HTML5, Tailwind CSS, Lightweight Charts v4
- **AI 引擎 (AI Core)**: LangChain / Custom LLM Agent（支持多模态视觉）
- **数据接口 (Data Stream)**: Sina / Xueqiu Realtime Data API

---

## 📦 快速开始

### 1. 克隆项目与安装依赖

```bash
# 克隆仓库
git clone https://github.com/your-username/dsa_core.git
cd dsa_core

# 安装依赖项
pip install fastapi uvicorn python-multipart