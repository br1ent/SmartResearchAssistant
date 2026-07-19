# AceResearch 研思

> 基于 LangGraph 多 Agent 协作的深度研究平台

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AceResearch 是一个基于大语言模型的智能研究平台，通过多个 AI Agent 协作自动完成从规划、搜索到撰写报告的全流程深度研究。同时支持智能对话、联网搜索、个人知识库检索等多种交互模式。

<!-- ![截图](./docs/screenshot.png) -->

## 核心特性

- **多 Agent 协作** — Planner、Researcher、Analyst、Writer、Reviewer 五个 Agent 自动协作完成深度研究
- **研究流水线** — 主题规划 → 并行搜索 → 综合分析 → 报告撰写 → 质量审查（最多 2 次），全流程自动化
- **RAG 知识库** — 上传个人文档，向量检索 + 重排序精准回答文档相关问题，与联网搜索完全隔离
- **流式对话** — SSE 实时推送，用户即时看到 AI 回复内容
- **记忆系统** — 闲聊和知识库对话各自拥有独立记忆，提升长对话体验
- **暗色模式** — 支持亮色/暗色主题切换，偏好自动持久化到 localStorage

## 快速开始

### 前置条件

- Python 3.11+
- Node.js ^22.18.0 或 >=24.12.0
- MySQL 8.0+
- DeepSeek API Key（必须）
- Tavily API Key（必须，联网搜索用）

### 克隆仓库

```bash
git clone https://github.com/your-username/AceResearch.git
cd AceResearch
```

### 后端安装

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r ../requirements.txt
```

### 前端安装

```bash
cd frontend
npm install
```

### 配置环境变量

在 `backend/` 目录下创建 `.env` 文件：

```env
# 数据库
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=smart_research

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256

# DeepSeek
DEEPSEEK_API_KEY=your-deepseek-api-key

# Tavily（联网搜索）
TAVILY_API_KEY=your-tavily-api-key
```

> 完整环境变量列表见下方 [环境变量](#环境变量) 章节。

### 启动服务

**启动后端**（自动创建数据库表）：

```bash
cd backend
uvicorn main:app --reload --port 8000
```

**启动前端**（开发模式）：

```bash
cd frontend
npm run dev
```

访问 http://localhost:5173 即可使用。

### 生产部署

```bash
cd frontend
npm run build
```

构建产物在 `frontend/dist/`，后端会自动托管静态文件，访问 http://localhost:8000 即可。

## 功能概览

| 功能 | 说明 |
|---|---|
| 闲聊模式 | DeepSeek 大模型 + Tool Calling（联网搜索、天气查询、实时时间） |
| 研究模式 | 五 Agent 协作（每个话题独立隔离），自动规划、搜索、撰写、审查报告 |
| 个人文档检索 | PDF/TXT/MD/DOCX 上传，向量检索 + 重排序，纯文档内问答 |
| 实时进度反馈 | WebSocket 推送研究进度，可视化展示每个 Agent 的工作状态 |
| 主题切换 | 暗色/亮色模式，偏好自动持久化到 localStorage，无闪烁 |

## 系统架构

```
┌─────────────────────────────────────────────────────┐
│                  前端 (Vue 3)                         │
│   DaisyUI 5 + Tailwind CSS 4 + Pinia + Vue Router   │
├─────────────────────────────────────────────────────┤
│             SSE / WebSocket / REST                   │
├─────────────────────────────────────────────────────┤
│                 后端 (FastAPI)                        │
├───────────┬─────────────────┬───────────────────────┤
│  闲聊模式  │    研究模式       │   个人文档检索         │
│ ChatGraph │ PlanningWorkflow │   ChatGraph + RAG     │
│ + ReAct   │ + ExecutionWf.   │   (仅 KB Tools)       │
├───────────┴─────────────────┴───────────────────────┤
│              LangGraph (Agent 状态编排)               │
├─────────────────────────────────────────────────────┤
│    MySQL (SQLAlchemy ORM)   │  ChromaDB (向量数据库)  │
└─────────────────────────────────────────────────────┘
```

## 技术栈

**前端**

| 技术 | 版本 | 用途 |
|---|---|---|
| Vue 3 | ^3.5 | 渐进式前端框架 |
| Vite | ^8.0 | 构建工具，热更新 |
| Tailwind CSS | 4.x | 原子化 CSS |
| DaisyUI | 5.x | 组件库，主题系统 |
| Pinia | ^3.0 | 状态管理 |
| Vue Router | ^5.0 | 路由管理 |
| Lucide Vue | ^1.24 | 图标库 |
| Croppie | ^2.6 | 头像裁剪 |
| Axios | ^1.18 | HTTP 客户端 |

**后端**

| 技术 | 用途 |
|---|---|
| FastAPI | Web 框架，自动 OpenAPI 文档 |
| SQLAlchemy 2.0 | ORM，异步会话管理 |
| PyMySQL | MySQL 驱动 |
| LangGraph | 多 Agent 有状态编排 |
| LangChain | ChatOpenAI 流式调用，Tool Calling |
| ChromaDB | 向量数据库 |
| python-jose | JWT 签发和解码 |
| passlib + bcrypt | 密码哈希 |
| WebSocket | 实时推送研究进度 |
| SSE | 流式对话输出 |

**AI / 搜索服务**

| 服务 | 用途 |
|---|---|
| DeepSeek (V4 Flash) | LLM 推理，OpenAI 兼容接口 |
| Tavily Search API | 联网搜索 |
| 阿里云百炼 text-embedding-v4 | 文本向量化（1024 维） |
| 阿里云百炼 qwen3-rerank | 重排序，提升检索精度 |
| 和风天气 QWeather v7 | 城市查询 + 实时天气 |

## 项目结构

```
AceResearch/
├── backend/
│   ├── agents/
│   │   ├── chat/                 # 闲聊 Agent（ChatGraph + ReAct）
│   │   ├── research/             # 研究 Agent（Planning + Execution）
│   │   └── memory/               # 记忆提取 Agent
│   ├── services/                 # 业务逻辑层
│   ├── routers/                  # FastAPI 路由（REST + WebSocket）
│   ├── models/                   # SQLAlchemy ORM 模型
│   ├── schemas/                  # Pydantic 请求/响应 schema
│   ├── config/                   # 配置（数据库、Agent、提示词）
│   ├── utils/                    # 工具（JWT、WebSocket 管理）
│   └── main.py                   # 应用入口
├── frontend/
│   └── src/
│       ├── views/                # 页面组件
│       ├── stores/               # Pinia 状态管理
│       ├── components/           # 通用组件
│       ├── router/               # 路由配置
│       ├── js/                   # 工具函数（HTTP、主题）
│       └── css/                  # 样式入口
├── requirements.txt
└── README.md
```

## API 路由

**认证**

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/user/register` | 注册 |
| POST | `/api/user/login` | 登录，返回 JWT |
| POST | `/api/user/reset-password` | 重置密码 |
| GET | `/api/user/info` | 获取用户信息 |
| PUT | `/api/user/profile` | 更新个人资料 |
| POST | `/api/user/avatar` | 上传头像 |

**对话**

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/chat/conversations` | 获取对话列表 |
| DELETE | `/api/chat/conversations/{id}` | 删除对话 |
| GET | `/api/chat/conversations/{id}/messages` | 获取消息历史 |
| GET | `/api/chat/conversations/{id}/report` | 获取研究报告 |
| POST | `/api/chat/send` | 发起研究（WebSocket 推送进度） |
| POST | `/api/chat/send/stream` | 闲聊流式输出（SSE） |

**研究**

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/chat/research/confirm` | 确认方案，开始执行 |
| POST | `/api/chat/research/revise` | 修改方案，重新规划 |

**知识库**

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/kb/documents` | 文档列表 |
| POST | `/api/kb/documents/upload` | 上传文档（PDF/TXT/MD/DOCX） |
| DELETE | `/api/kb/documents/{id}` | 删除文档 |

**报告**

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/reports/` | 报告列表 |
| GET | `/api/reports/{id}` | 报告详情 |
| DELETE | `/api/reports/{id}` | 删除报告 |

## 环境变量

| 变量 | 说明 | 默认值 | 必填 |
|---|---|---|---|
| `DB_HOST` | MySQL 地址 | `localhost` | 是 |
| `DB_PORT` | MySQL 端口 | `3306` | 是 |
| `DB_USER` | MySQL 用户名 | `root` | 是 |
| `DB_PASSWORD` | MySQL 密码 | - | 是 |
| `DB_NAME` | 数据库名 | `smart_research` | 是 |
| `SECRET_KEY` | JWT 密钥 | - | 是 |
| `ALGORITHM` | JWT 算法 | `HS256` | 否 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token 过期时间（分钟） | `30` | 否 |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | - | 是 |
| `DEEPSEEK_BASE_URL` | DeepSeek API 地址 | `https://api.deepseek.com/v1` | 否 |
| `DEEPSEEK_MODEL` | 模型名 | `deepseek-v4-flash` | 否 |
| `DEEPSEEK_MAX_TOKENS` | 最大输出 token 数 | `8192` | 否 |
| `TAVILY_API_KEY` | Tavily 搜索 API Key | - | 是 |
| `EMBEDDING_API_KEY` | 阿里云百炼 DashScope API Key | - | 知识库需要 |
| `QWEATHER_API_HOST` | 和风天气 API Host | - | 否 |
| `QWEATHER_API_KEY` | 和风天气 API Key | - | 否 |

> 更多可选变量见 `backend/config/` 下的配置文件。

## 数据模型

**MySQL 表**

| 表名 | 说明 | 关键字段 |
|---|---|---|
| `users` | 用户 | id, username, email, password_hash, photo, memory |
| `conversations` | 对话会话 | id, user_id, title, mode(chat/research/knowledge) |
| `messages` | 消息记录 | id, conversation_id, role, content, msg_type |
| `reports` | 研究报告 | id, conversation_id, title, content, status |
| `knowledge_documents` | 上传的文档 | id, user_id, title, file_type, status |
| `agent_prompts` | Agent 提示词 | id, mode, stage, content |

**ChromaDB Collection**

每个用户独立一个 collection（`user_{id}_kb`），存储文档分块的 1024 维向量，支持 top-k 检索 + 重排序。

## 许可证

MIT License
