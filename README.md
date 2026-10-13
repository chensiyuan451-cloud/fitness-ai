# fitness-ai 🏋️

> 一个「健身训练记录系统」，并逐步演进为 **AI 私教 Agent**。
> 个人学习 + 求职作品集项目：Python 后端（FastAPI）+ MySQL + Redis + Docker + 大模型应用开发。

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/zh/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)](https://dev.mysql.com/doc/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/docs/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://docs.docker.com/compose/)

---

## 一、项目简介

`fitness-ai` 用来解决一个很实际的问题：**去健身房练了半年，但完全不知道自己有没有进步。**

它要做的三件事：

1. **记录**：把「今天练了什么动作、多少组、每组多少次、多重」结构化地记下来，而不是记在备忘录里。
2. **分析**：统计训练容量（组数 × 次数 × 重量）、周训练量趋势、部位分布，用排行榜看出自己的薄弱项。
3. **指导（AI 私教）**：把训练历史交给大模型，自动生成**训练周报**、给出**下次训练建议**、回答「我深蹲为什么上不去重量」这类问题。

### 功能规划

| 阶段 | 功能 | 状态 |
|---|---|---|
| v0.1 | 命令行训练记录工具，数据存 JSON | ⏳ 第 1 周 |
| v0.2 | MySQL 四张表（用户 / 动作 / 训练 / 组）建模 + 数据迁移 | ⏳ 第 2 周 |
| v0.3 | FastAPI 训练记录 API：注册登录（JWT）+ 训练记录增删改查 | ⏳ 第 3 周 |
| v0.4 | Redis 排行榜（本周训练量 Top）、热门接口缓存、接口限流、日志、pytest | ⏳ 第 4 周 |
| v0.5 | Docker Compose 一键启动 + Nginx 反向代理 + 部署到云服务器公网可访问 | ⏳ 第 5 周 |
| v0.6 | 接入 DeepSeek / 通义千问 API，「AI 周报」+ 流式输出 | ⏳ 第 6 周 |
| v1.0 | AI 私教 Agent：多轮对话 + 工具调用（查训练数据）+ 训练计划生成 | 🎯 后续 |

---

## 二、技术栈

| 分类 | 选型 | 用途 |
|---|---|---|
| 语言 | Python 3.12 | 主力开发语言 |
| Web 框架 | FastAPI + Uvicorn | 提供 RESTful API，自带 Swagger 文档 |
| 数据校验 | Pydantic v2 | 请求/响应模型与参数校验 |
| ORM | SQLAlchemy 2.x | 操作 MySQL，避免手写 SQL 拼接 |
| 数据库 | MySQL 8.0 | 存用户、动作、训练、组等结构化数据 |
| 缓存 | Redis 7 | 缓存热点接口、限流、ZSET 做训练量排行榜 |
| 认证 | JWT (python-jose / PyJWT) + bcrypt | 用户注册登录与接口鉴权 |
| 测试 | pytest + httpx | 接口自动化测试 |
| 日志 | loguru / logging | 结构化日志，方便排查问题 |
| 容器化 | Docker + Docker Compose | 本地一键起 MySQL/Redis，也用于部署 |
| 反向代理 | Nginx | 生产环境反向代理 + HTTPS |
| 大模型 | DeepSeek API / 通义千问 API（OpenAI 兼容格式） | AI 周报、训练建议、AI 私教对话 |
| 工具链 | uv、Git、GitHub Actions（后续） | 依赖管理、版本管理、CI |

---

## 三、目录结构

```
fitness-ai/
├── app/                    # 应用代码（业务逻辑都写在这里）
│   └── main.py             # FastAPI 入口
├── tests/                  # pytest 测试代码
├── docs/                   # 文档：学习计划、环境报告、接口设计
├── scripts/                # 脚本：数据迁移、初始化、备份
├── docker/                 # Docker 相关配置（初始化 SQL 等）
│   └── init/init.sql
├── docker-compose.yml      # MySQL 8.0 + Redis 7 本地环境
├── .env.example            # 环境变量模板（只放变量名，不放真实值）
├── .gitignore              # 忽略 .env / .venv / *.pdf / private/
├── requirements.txt        # 依赖清单
└── README.md
```

---

## 四、快速开始

```bash
# 1. 克隆项目
git clone git@github.com:<你的用户名>/fitness-ai.git
cd fitness-ai

# 2. 复制环境变量模板并填写自己的密码
copy .env.example .env

# 3. 用 uv 创建虚拟环境并安装依赖
uv venv --python 3.12
uv pip install -r requirements.txt

# 4. 启动 MySQL + Redis
docker compose up -d

# 5. 启动开发服务器
uv run uvicorn app.main:app --reload --port 8000
```

打开 <http://127.0.0.1:8000/docs> 可以看到自动生成的接口文档。

---

## 五、开发路线图

| 周次 | 日期 | 主题 | 交付物 |
|---|---|---|---|
| 第 0 周 | 10/14 – 10/18 | 环境搭建、GitHub 连接、旧项目整理、简历 v1 | 环境报告、简历 v1、仓库初始化 |
| 第 1 周 | 10/19 – 10/25 | Python 核心（数据结构 / 函数 / 类 / 异常 / 文件 / 模块 / 类型注解） | 命令行训练记录工具（JSON 存储） |
| 第 2 周 | 10/26 – 11/01 | MySQL（CRUD / 多表连接 / 索引 / 事务）+ Git 分支 + Linux 命令 | 四张表设计 + 数据迁移脚本 |
| 第 3 周 | 11/02 – 11/08 | FastAPI + Pydantic + SQLAlchemy + JWT | 训练记录 API v1（注册登录 + 增删改查） |
| 第 4 周 | 11/09 – 11/15 | Redis（缓存 / 限流 / ZSET 排行榜）+ 日志 + pytest | 本周训练量排行榜、接口缓存、核心测试 |
| 第 5 周 | 11/16 – 11/22 | Docker、docker-compose、Nginx | 部署到云服务器，公网可访问 |
| 第 6 周 | 11/23 – 11/30 | DeepSeek / 通义千问 API、Prompt、流式输出 | 「AI 周报」功能、简历 v2 |

详细到每一天的计划见 [`docs/学习计划.md`](docs/学习计划.md)。

---

## 六、安全约定（重要）

- ✅ 所有密码、密钥只写在 **`.env`** 里，`.env` 已被 `.gitignore` 忽略。
- ✅ 仓库里只保留 `.env.example`，里面**只有变量名，没有真实值**。
- ❌ 绝不把 API Key、数据库密码、简历、手机号提交到 GitHub。
- ❌ 绝不提交 `.venv/`、`*.pdf`、`private/`、`resume/`。

如果有一天你**不小心**提交了密钥：

```bash
git rm --cached .env
# 然后立刻去对应平台把那个 Key 作废并重新生成（历史提交里的密钥永远算已泄露）
```

---

## 七、License

学习项目，暂未指定开源协议。
