# 用户 Skills 索引

此文件用于按用途整理当前用户级 Codex skills，便于快速了解每个 skill 的触发场景和维护边界。

## 分类总览

| 分类 | 适用范围 | Skills |
| --- | --- | --- |
| 流程与安全类 | 任务编排、任务清单、编码安全、文本安全检查 | `auto-subagent-orchestrator`, `workspace-task-checklist`, `encoding-text-safety-v1` |
| Skill 管理类 | 查找、评估、安装可用 skill | `find-skills`, `personal-skill-installer` |
| 浏览器自动化类 | 真实浏览器操作、页面调试、截图和表单流验证 | `playwright` |
| 技术栈规范类 | FastAPI + Vue 全栈开发规范、新项目协作规范初始化 | `fastapi-vue-standard`, `new-fullstack-project` |
| 网页与产品设计类 | 高质量网页、落地页、仪表盘、前端体验设计 | `web-design-engineer` |
| 知识库检索类 | 本地资料、Markdown、PDF、Excel 检索问答 | `kb-retriever` |
| 视觉创作类 | 图像生成、网页视频、HyperFrames 制作、动画适配、registry 组件 | `gpt-image-2`, `hyperframes` |
| 任务总结类 | 将当前任务整理为桌面中文 Markdown 概要 | `summarize-task` |

## Skills 明细

### 流程与安全类

- `auto-subagent-orchestrator`
  - 用途：任务开始时判断是否适合拆分；一旦适合拆分，即视为已有用户长期授权，自动启动最小必要子节点。
  - 主进程职责：分配任务、跟踪集成、审查结果、处理兜底。
  - 注意：无需用户每次手动指定子节点；但高优先级系统/开发者/用户指令始终优先。

- `workspace-task-checklist`
  - 用途：任务开始时判断是否需要持久化任务清单；多步骤、跨文件、长任务、实现加验证、并行子任务或用户要求任务清单时，在当前工作区 `docs/task/` 创建中文 Markdown 清单。
  - 覆盖：初始化中文清单、更新单项状态、追加中文进展日志、记录本次任务修改的文件、标记任务完成，并通过 `docs/task/.current-task-checklist` 记录当前清单。
  - 注意：清单文件命名为 `YYYY-MM-DD-HH-MM-SS-任务名.md`；生成的任务文档正文使用中文；简单问答、单个命令、很小的单文件改动默认不创建；创建后只在真实状态变化或有成组文件变更时更新，不为每个细小命令刷写文档。

- `encoding-text-safety-v1`
  - 用途：创建或修改代码、配置、文档、提示词、注释、用户可见文本时，保证 UTF-8 文本安全。
  - 检查项：UTF-8 without BOM、`U+FFFD`、常见乱码片段。
  - 注意：编码修复应尽量与业务逻辑修改分开说明。

### Skill 管理类

- `find-skills`
  - 用途：当用户询问“有没有某种 skill”或想扩展能力时，帮助发现可安装的 skill。
  - 覆盖：按场景查找、判断是否适合安装、给出后续安装建议。
  - 注意：只负责发现和建议；真正安装时优先使用 `skill-installer` 系统 skill。

- `personal-skill-installer`
  - 用途：覆盖个人 Codex skills 的默认安装位置。
  - 覆盖：安装、列出、更新用户级 skills 时，默认目标目录为 `%USERPROFILE%\.agents\skills`。
  - 注意：每次安装或更新个人 skill 后，同步维护 `%USERPROFILE%\.agents\skills\README.md`。

### 浏览器自动化类

- `playwright`
  - 用途：通过 `playwright-cli` 或随 skill 提供的 wrapper 脚本，从终端驱动真实浏览器进行页面访问、快照、点击、表单填写、截图和 UI 流程调试。
  - 覆盖：CLI 命令参考、常见工作流、故障排查，以及脚本路径 `~/.agents/skills/playwright/scripts/playwright_cli.sh`。
  - 注意：使用元素引用前先获取页面 snapshot；目标副本已从 `.codex` 迁移到 `%USERPROFILE%\.agents\skills\playwright`，保留原 `.codex` 源目录不删除。

### 技术栈规范类

- `fastapi-vue-standard`
  - 用途：提供 FastAPI + Vue 全栈项目的通用编码规范。
  - 覆盖：数据建模、业务实现、API 设计、前端开发、权限控制、质量门禁。
  - 注意：代码修改后默认只检查变更文件语法；不要主动运行构建命令、开发服务、全量测试或联调验证，除非用户明确要求。

- `new-fullstack-project`
  - 用途：当用户发送“新建全栈项目”或要求初始化全栈项目协作规范时，在当前会话工作区创建前后端/docs 目录骨架和 `AGENTS.md`。
  - 覆盖：创建 `backend/`、`frontend/`、`docs/` 及常用子目录；从 skill 内置规范模板复制生成通用全栈项目协作说明，包含前后端分层、API、数据库、配置、后台任务、验证和迭代记录规范。
  - 注意：目录创建是幂等的；默认不覆盖已有 `AGENTS.md`，只有用户明确要求替换或覆盖时才使用 `--force`。

### 网页与产品设计类

- `web-design-engineer`
  - 用途：提升网页、落地页、仪表盘、原型、动画和数据可视化的设计质量。
  - 覆盖：信息架构、视觉层级、交互状态、响应式布局、设计审查。
  - 注意：适合“做一个页面/产品界面/仪表盘/高质量 Web UI”类任务，不等同于视频制作。

### 知识库检索类

- `kb-retriever`
  - 用途：从本地知识库目录检索资料并回答问题。
  - 覆盖：Markdown、PDF、Excel 等文件的分层索引导航和渐进式检索。
  - 注意：遇到 PDF/Excel 时先阅读 skill 内 references 的处理方法，再使用合适工具抽取内容。

### 视觉创作类

#### 图像生成

- `gpt-image-2`
  - 用途：面向 GPT Image 2 或 OpenAI 兼容图像接口进行图像生成、图像编辑和提示词设计。
  - 覆盖：海报、UI、产品图、信息图、学术图、架构图、漫画、头像、分镜、IP 周边等模板。
  - 注意：可在本地出图、交给宿主图像工具出图，或退化为高质量 prompt 顾问。

#### HyperFrames Unified Skill

- `hyperframes`
  - 用途：HyperFrames 唯一入口 skill，覆盖 HTML 视频组合、标题卡、字幕、转场、音频响应视觉、CLI、媒体预处理、registry、网站捕获、Remotion 迁移、web-video-presentation，以及动画适配器。
  - 覆盖：composition 编写、时间轴、媒体接入、字幕、转场、完整视频制作流程、`init`/`lint`/`inspect`/`preview`/`render`/`doctor`、TTS/转写/抠背景、registry 接线、网站转视频、Remotion 转换、口播稿演示、GSAP/Anime.js/CSS/WAAPI/Lottie/Three/Tailwind。
  - 注意：内部模块索引在 `hyperframes/modules/README.md`，按任务选择最小模块即可。

### 任务总结类

- `summarize-task`
  - 用途：当用户发送 `/总结任务` 或要求总结当前任务时，生成中文 Markdown 任务概要。
  - 输出：默认写入 `%USERPROFILE%\Desktop\task`，文件名使用当前日期和中文标题。
  - 注意：概要应记录目标、已创建内容、查看方式、取消/卸载方式、验证结果和注意事项。

## 维护规则

- 新增用户 skill 后，同步更新本索引。
- 分类优先按主要用途归入；如果一个 skill 跨多个用途，以最常触发的用途为主。
- 不建议把 skill 文件夹移动到分类子目录，避免影响 Codex 的 skill 发现机制。
- 若 skill 行为发生变化，应同步更新对应“用途”和“注意”说明。

## parallel-code-review-agent

- Category: code review workflow
- Trigger/use case: Use when you want one orchestrator agent to run multiple parallel code review agents and merge findings for a repository diff, PR, branch, commit range, or changed files.
- Maintenance notes: Update `parallel-code-review-agent/SKILL.md` when reviewer roles, severity rules, or output format should change.
