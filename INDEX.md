# 用户 Skills 索引

此文件用于按用途整理当前用户级 Codex skills，便于快速了解每个 skill 的触发场景和维护边界。

## 分类总览

| 分类 | 适用范围 | Skills |
| --- | --- | --- |
| 流程与安全类 | 任务编排、编码安全、文本安全检查 | `auto-subagent-orchestrator`, `encoding-text-safety-v1` |
| Skill 管理类 | 查找、评估、安装可用 skill | `find-skills`, `personal-skill-installer` |
| 技术栈规范类 | FastAPI + Vue 全栈开发规范 | `fastapi-vue-standard` |
| 网页与产品设计类 | 高质量网页、落地页、仪表盘、前端体验设计 | `web-design-engineer` |
| 知识库检索类 | 本地资料、Markdown、PDF、Excel 检索问答 | `kb-retriever` |
| 视觉创作类 | 图像生成、网页视频、HyperFrames 制作、动画适配、registry 组件 | `gpt-image-2`, `hyperframes`, `hyperframes-cli`, `hyperframes-media`, `website-to-hyperframes`, `web-video-presentation`, `remotion-to-hyperframes`, `animejs`, `css-animations`, `gsap`, `lottie`, `tailwind`, `three`, `waapi`, `hyperframes-registry`, `contribute-catalog` |
| 任务总结类 | 将当前任务整理为桌面中文 Markdown 概要 | `summarize-task` |

## Skills 明细

### 流程与安全类

- `auto-subagent-orchestrator`
  - 用途：任务开始时判断是否适合拆分，并在规则允许时按需启动子节点。
  - 主进程职责：分配任务、跟踪集成、审查结果、处理兜底。
  - 注意：高优先级系统/开发者/用户指令始终优先。

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
  - 覆盖：安装、列出、更新用户级 skills 时，默认目标目录为 `C:\Users\16084\.agents\skills`。
  - 注意：每次安装或更新个人 skill 后，同步维护 `C:\Users\16084\.agents\skills\INDEX.md`。

### 技术栈规范类

- `fastapi-vue-standard`
  - 用途：提供 FastAPI + Vue 全栈项目的通用编码规范。
  - 覆盖：数据建模、业务实现、API 设计、前端开发、权限控制、质量门禁。
  - 注意：代码修改后默认只检查变更文件语法；不要主动运行构建命令、开发服务、全量测试或联调验证，除非用户明确要求。

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

#### HyperFrames 视频制作

- `hyperframes`
  - 用途：创建 HTML 视频组合、标题卡、字幕、转场、音频响应视觉和场景动画。
  - 覆盖：composition 编写、时间轴、媒体接入、字幕、转场、完整视频制作流程。
  - 注意：CLI 命令交给 `hyperframes-cli`；TTS、转写、抠背景交给 `hyperframes-media`。

- `hyperframes-cli`
  - 用途：运行 HyperFrames CLI 开发闭环。
  - 覆盖：`init`、`lint`、`inspect`、`preview`、`render`、`doctor`、环境排查。
  - 注意：资产预处理命令不归它处理，改用 `hyperframes-media`。

- `hyperframes-media`
  - 用途：为 HyperFrames 项目生成或处理媒体资产。
  - 覆盖：Kokoro TTS、Whisper 转写、u2net 背景移除。
  - 注意：首次运行相关命令可能下载模型。

- `website-to-hyperframes`
  - 用途：把现有网站捕获并改造成 HyperFrames 视频。
  - 覆盖：基于 URL 的产品展示、站点宣传片、产品导览、社交广告视频。
  - 注意：用户提供 URL 并要求做视频时优先触发。

- `web-video-presentation`
  - 用途：把文章、口播稿、课程或产品讲解做成点击驱动的 16:9 网页视频演示。
  - 覆盖：口播稿、outline、逐章开发、可选口播音频合成、录屏友好的交互节奏。
  - 注意：适合“网页做视频/动态 PPT 但不像 PPT/录屏教程”类任务。

- `remotion-to-hyperframes`
  - 用途：把已有 Remotion 组合迁移为 HyperFrames HTML 组合。
  - 覆盖：Remotion 源码结构判断、可迁移模式识别、不可迁移模式提示。
  - 注意：只有用户明确要求 port/convert/migrate Remotion 时使用。

#### HyperFrames 动画适配

- `animejs`
  - 用途：在 HyperFrames 中使用 Anime.js 动画和 timeline。
  - 注意：动画需要注册并支持确定性 seek。

- `css-animations`
  - 用途：在 HyperFrames 中使用 CSS keyframes、animation-delay、fill-mode 等 CSS 动画。
  - 注意：CSS-only motion 也要能被预览和渲染确定性定位。

- `gsap`
  - 用途：在 HyperFrames 中使用 GSAP 动画、timeline、easing、stagger 和性能模式。
  - 注意：优先使用可 seek、可复现的时间轴写法。

- `lottie`
  - 用途：在 HyperFrames 中嵌入 lottie-web JSON 或 `.lottie` 动画。
  - 注意：需要注册实例并保证 After Effects 导出动画可确定性 seek。

- `tailwind`
  - 用途：在 HyperFrames 组合里使用 Tailwind CSS v4.2 浏览器运行时。
  - 注意：适用于 `hyperframes init --tailwind` 项目及 v4 CSS-first token 调试。

- `three`
  - 用途：在 HyperFrames 中创建 Three.js/WebGL 场景、相机运动、shader 视觉。
  - 注意：WebGL canvas 需要响应 `hf-seek` 并在渲染中保持确定性。

- `waapi`
  - 用途：在 HyperFrames 中使用 Web Animations API。
  - 注意：`element.animate()`、`currentTime`、`KeyframeEffect` 等要支持确定性 seek。

#### HyperFrames Registry

- `hyperframes-registry`
  - 用途：安装并接线 HyperFrames registry 中的 blocks 和 components。
  - 覆盖：`hyperframes add`、安装位置、`index.html` 接线、`hyperframes.json` 维护。
  - 注意：只负责使用现有 registry 资源。

- `contribute-catalog`
  - 用途：向 HyperFrames 公共 catalog 新增 registry block 或 component，并准备上游 PR。
  - 覆盖：caption style、VFX block、transition、lower third、text effect、overlay、snippet。
  - 注意：只有用户明确要贡献公开 catalog 时使用。

### 任务总结类

- `summarize-task`
  - 用途：当用户发送 `/总结任务` 或要求总结当前任务时，生成中文 Markdown 任务概要。
  - 输出：默认写入 `C:\Users\16084\Desktop\task`，文件名使用当前日期和中文标题。
  - 注意：概要应记录目标、已创建内容、查看方式、取消/卸载方式、验证结果和注意事项。

## 维护规则

- 新增用户 skill 后，同步更新本索引。
- 分类优先按主要用途归入；如果一个 skill 跨多个用途，以最常触发的用途为主。
- 不建议把 skill 文件夹移动到分类子目录，避免影响 Codex 的 skill 发现机制。
- 若 skill 行为发生变化，应同步更新对应“用途”和“注意”说明。
