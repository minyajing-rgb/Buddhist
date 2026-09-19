---
name: global-knowledge-atlas
description: Build and maintain a source-traceable, story-first global knowledge atlas for any discipline. Use for comprehensive domain maps, canonical databases, crosswalks, timelines, geography, archive access, scholarly controversies, community/KOL research, beginner learning paths and research websites. Audit existing content before expansion; distinguish evidence coverage, functional implementation and publication.
metadata:
  version: "1.2"
  scope: cross-disciplinary
  output_mode: database-first
---

<!-- LIVING_RELEASE_OVERRIDE -->
> **发布规则 v1.2：** 当用户明确要求先预览、边研究边迭代时，先发布已可使用的内容，保留未知/争议/证据等级标签。研究完整性不得阻塞整站预览；功能、安全和隐私检查仍须通过。此条替代旧文中要求学术考证全部完成才允许任何公网预览的表述。每批采用“数据更新→自动构建→功能测试→预览发布→公网核验”，不以发布代替研究完成。



# Global Knowledge Atlas｜全球知识地图生产 Skill

## Mission

底层是有来源、可比较、可追溯的知识数据库；上层是小白能从故事、问题、地图、人物和实物逐层学习的产品。不是链接大全，不是一次长文，也不是只有漂亮外壳的网站。

所有学科都可复用生产流程，但不能复制其他学科的结论或证据标准。HDS相关原则必须有实际来源；本skill不代表哈佛认证或合作。

## 必须先读

1. 项目仓库的 CURRENT、状态台账和真实数据。统计而不是复述旧报告。
2. [执行手册 v1.1](references/EXECUTION_PLAYBOOK_v1.1.md)：33种方法操作卡、研究路线、6类学科迁移、质量门禁和启动指令。
3. [Harvard/HDS资源与归因](references/HARVARD_HDS_METHODS.md)。
4. [研究方法矩阵](references/RESEARCH_METHODS_MATRIX.md) 与 [方法目录](references/METHOD_CATALOG.json)。
5. [民间、社群与KOL](references/PUBLIC_COMMUNITY_KOL_METHODS.md)。
6. [跨学科适配模板](templates/DOMAIN_ADAPTER.md)、[Crosswalk schema](templates/CROSSWALK.schema.json)、[QA](templates/QA_GATE.md)。
7. 佛学项目加读 [Buddhist Studies adapter](adapters/BUDDHIST_STUDIES.md)。

若旧参考文件与v1.1执行手册在证据等级、发布状态上冲突，以v1.1更严格、明确的定义为准；保留旧版记录供diff。

## 标准执行顺序

### 1. 接手与冻结基线

读取默认分支；保存commit；检查是否有人已推进了任务。核对唯一ID、数量、空值、重复、关联、已完成资产和发布链接。不得把“32→100”历史目标当成当前仍只有32条。

### 2. 定义范围与主实体

写scope协议：对象单位、读者、地区、年代、语言、主流/少数分支、排除条件、证据阈值。以覆盖矩阵衡量完整性。100部代表经典不是完整大藏经；集合与子项不得混计。

### 3. 并行研究五条证据路线

- 学术：注释书目、论文、专著、校勘本、博士论文、反方研究。
- 档案/实物：目录、馆藏号、原件、影像、发现报告、收藏来源。
- 民间/实践：口述史、访谈、田野、地方文献、社区自述。
- 公众/KOL：视频、播客、公开讲座、论坛、传播链、常见误读。
- 数字方法：结构化语料、GIS、图谱、版本diff、计算辅助对照。

公众热度不是事实置信度。机构声望不能代替对具体论点的核验。实践者证言对于其经验是一手材料，不自动证明古代历史或干预疗效。

### 4. 来源与检索日志

为每次查询记录平台、关键词、语言、时间、过滤、纳排、零结果与权限限制。优先已存在的高质量语料和索引，不重复造库；利用他人的资料时保留来源和许可。不能把多次转发计作独立佐证。

### 5. Canonical entities与Crosswalk

核心实体：Work、Version、Witness/Object、Person、Organization、Place、Event、Concept、Claim、Source、BibliographyItem、MediaAsset、Collection。

每条关系给类型、方向、来源、定位、时间与审核状态。关系包括：version_of、translation_of、close_parallel、partial_parallel、resembling_parallel、quotation、adaptation、held_by、found_at、attributed_to、supports、contradicts、uncertain。

禁止 Work=Version=Witness、同名=同作、平行=完全相同、合集背景=某部经原件。

### 6. 年代与地图

分别记录传统日期、学术推定、译本日期、实体见证日期、现代出版日期、发现/购藏日期。日期使用区间、类型、依据与不确定性；未知保留未知。

地图分开显示叙事地、成书地、传播地、翻译地、发现地、现藏地、研究机构。现代图书馆不能随着古代年代滑块出现在“当时的传播地图”上。无时间证据的节点保留在“未定年/总览”层，不凭空分配年份。

### 7. 书目和争议

每条书目至少有题名、作者/编辑、年份或明确未知、出版载体、语言、稳定URL或标识、访问状态、关联论点与阅读状态。自动导入bibliography只代表目录元数据已取得，不代表读过论文。

争议逐项记录谁主张什么、依据何种版本/证据、主要反证、时间与限制。不要生成匿名“学界认为”；不要用两面各半伪装证据平衡。

### 8. 小白层与媒体

教学链：问题 → 故事 → 一个概念 → 时间/空间 → 具体文本或实物 → 我们知道什么 → 争议/未知 → 原始证据。

三种模式：Guided / Explorer / Scholar。显示层级可以不同，事实口径必须相同。媒体必须登记对象、作者、权利、使用方式、alt和实体关联。无视频/3D成品时禁止伪播放按钮。AI示意/复原不得冒充历史图像。

### 9. QA后生成与发布

先审计，再生成含全部数据的审阅构建；测试搜索、过滤、详情、对比、地图、阅读、来源与移动端。内容、权利或部署未通过时，不得称正式官网已完成/上线。

区分：source-archived / metadata-imported / scholar-reviewed / functional-preview / public-deployed。可以交付可运行研究预览，但必须公开其限制并保留正式发布门禁。

## 严格证据等级

- **L0**：发现线索。
- **L1**：作品级权威记录可回查。
- **L2**：多系统/跨版本关系已核对并标注类型。
- **L3**：L2 + 逐部年代依据 + 确切见证；无存世见证可用署名负面研究结论，而不是空值。
- **L4**：L3 + 可定位的paper/book书目、署名争议、反证和限制。

保留旧数据reported_level，另列assessed_level。没有证据不得自动升级。字段存在、HTTP200、目录编号、机构主页都不能独立认证L3。

## 质量门禁

A 覆盖：地区/语言/年代/流派/来源是否有系统遗漏。

B 身份：ID唯一、作品单位稳定、关系可解释、跨表引用不悬空。

C 内容：不是空字段、占位词、模板段落冒充逐部研究。

D 来源：主张可定位、转引可识别、已知断链显示、权威页与检索入口分开。

E 访问：线上何处读、版本是什么；线下原件由谁收藏、准确馆藏号与访问限制是什么。

F 争议：说话人/传统/时代清楚；不制造共识或等价关系。

G 权利/伦理：影像许可、脆弱社群、知情同意、隐私、健康/科学风险。

H 产品：真实数据驱动、渐进展示、无假按钮、键盘/手机可用、错误和空态可见。

I 发布：提供实际commit、测试报告和实际可访问产物；不把仓库文件链接当已部署官网。

## 当前仓库的执行工具

- `.github/workflows/atlas-quality.yml`：独立100部结构与证据缺口审计，并打包审阅产物。
- `scripts/collect_authority_metadata.py`：从指定权威仓库的固定commit导入元数据与书目事实；不转载全文。
- `.github/workflows/authority-import.yml`：运行导入，保留来源与导入状态。
- `scripts/build_atlas.py`（存在时）：从canonical manifest与显式补充层生成离线完整交互审阅版。

工具可迁移，佛学特定规则需换adapter。执行前检查文件实际存在，不能只因文档提到了路径就宣称已运行。

## 每批交付

变更摘要 + 新增/修正记录 + 来源/检索日志 + 维度级缺口 + QA + GitHub commit + 可运行产物（有则交付）+ 发布状态。

Done = 已归档的数据、来源、关系、访问链和相应QA；不是大纲、schema、链接总数或视觉稿。
