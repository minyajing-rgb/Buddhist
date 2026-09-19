<!-- LIVE_PREVIEW_POLICY_START -->
## 当前公开预览：内容与网站并行更新

已上线：[https://minyajing-rgb.github.io/Buddhist/](https://minyajing-rgb.github.io/Buddhist/)。本次已核验真实HTTPS页面和浏览器交互。

用户于2026-09-19明确要求：已有内容先部署预览，研究和网站并行完善。此规则替代下文历史记录中“全部考证完成后再发布／官网未部署”的旧状态；学术证据仍须诚实标注。

发布结果见 `docs/public_deployment.json`，公网测试见 `data/public_beta_qa.json`。

本轮另核对18部的官方平行关系编码，旧重复分类目标133项，新映射重叠0项。仅指编码修正，不指独立完成全部经文校勘。

<!-- LIVE_PREVIEW_POLICY_END -->

# Dharma Atlas｜佛典全球知识地图

> 从一部经，读懂一个世界。  
> Story → Concept → Text → Version → Witness → Source.

这是面向小白、可以逐层进入专业证据的知识地图。底层数据库与上层教学分开维护；“作品已收录”“证据已核对”“网页可运行”“公网已部署”是四种不同状态。

## 直接进入本轮产物

|产物|入口|实际状态|
|---|---|---|
|完整交互研究版网站|[docs/review/index.html](docs/review/index.html)|七个模块；单文件包含数据和交互。GitHub文件页显示源码，不等于公网官网。|
|100份逐部审阅档案|[work-dossiers](docs/review/work-dossiers/)|每部有版本入口、编号、研究书目或明确缺口、完整结构化记录。|
|100部审阅版数据|[deep_crosswalk_100_v0.7.review.json](data/deep_crosswalk_100_v0.7.review.json)|保留旧标签与原记录；新增审阅字段，不伪造L3/L4完成。|
|实际质量与覆盖|[research_audit_v0.7.json](data/research_audit_v0.7.json)|机器统计和逐部缺口；不等于历史事实认证。|
|可复用研究Skill|[Global Knowledge Atlas](skills/global-knowledge-atlas/SKILL.md)|v1.1；跨学科生产流程、33张方法卡、适配模板和验收规则。|
|完整执行手册|[EXECUTION_PLAYBOOK_v1.1](skills/global-knowledge-atlas/references/EXECUTION_PLAYBOOK_v1.1.md)|问题→输入→操作→产物→门禁；HDS、学术、民间与KOL分开归因。|
|六张PNG图解|[review/assets](docs/review/assets/)|既有项目图解的PNG导出；教学示意，不是历史原件。|
|自动构建与ZIP|[Build complete research preview](../../actions/workflows/build-review.yml)|构建产物在每次成功运行的Artifacts；不自动部署官网。|

现有 `docs/index.html` 及旧网页均保留。本轮研究版使用 `docs/review/`，不覆盖此前页面。

## 本轮的真实进展

更新日期：2026-09-19。实际动态数字以审计文件为准。

|维度|本轮结果|口径|
|---|---:|---|
|代表性经论|100|基线已存在；本轮不是新增100部，也不是全部佛典。|
|逐部审阅档案|100|可展开内容与原始数据；不是100篇已完成学术考证。|
|权威元数据覆盖|60部 / 73条|固定来源commit；其中29条在该快照中属于目录占位。|
|关联书目记录|886条，关联18部|按作品内完整书目引用去重；跨作品全局标准化去重776条；包括版本资料和研究书目，不是已读论文数量。|
|补充独立阅读引导|68条|把后68部的通用占位段落换成具体阅读问题与比较提醒。|
|本轮具体作品—实物核对|2部|《金刚经》印本、《八千颂般若》写本；另校正犍陀罗卷轴实物信息。|
|带依据的时间事件|7|不同于28个地理总览节点。|
|人物 / 机构 / 来源平台|32 / 17 / 44|修正旧manifest里20个人物的错误总数。|
|可读故事 / 方法操作卡|12 / 33|故事供教学阅读；方法供跨学科迁移。|
|平行分类待核|18部|旧完整/近似关系列表存在重叠，保留原始分类并标出，不擅自判定。|

重要校正：剑桥《八千颂般若》彩绘写本的馆藏号为 **Add.1643**，纪年 **1015年**；**1139年后跋**是另一个事件。来源与定位见 [review_addendum_v0.7.json](data/review_addendum_v0.7.json)。不把写本年代当作作品成书年代。

## 官网研究版有什么

**开始探索**：问题引导、概念入口、学习路径、图解和真实覆盖统计。  
**故事剧场**：12集正文、上/下一集、阅读进度、导出。  
**100部经论**：中文/原文/编号搜索、传统与证据过滤、收藏、2–3部并排比较、完整详情、JSON导出。  
**时间地图**：按证据事件筛选年份；地理总览与现代馆藏单独分层；每个地点说明其角色。  
**人物**：32个人物及已登记的作者、译者与文本关系。  
**原件与馆藏**：24条实物/收藏记录、17家机构、明确访问路径、6张PNG图解和官方媒体外链。  
**研究室**：33方法卡、44来源平台、12研究问题、可见的QA与未完成事项。

正文与数据内嵌，可离线浏览；来源网站与官方视频需要联网。收藏和进度依赖浏览器允许本地存储；禁止存储时仅本次有效，可导出记录。没有假视频、假3D按钮或虚构实物影像。

## 如何本地打开与再生成

下载 `docs/review/index.html` 后用现代浏览器打开，或下载成功构建的ZIP。浏览器/企业策略禁用本地网页时，可在自己的开发环境使用静态服务器。

```bash
python -m pip install 'CairoSVG==2.8.2'
# Linux生成中文PNG需安装可用CJK字体；字体文件不随本项目交付。
python scripts/build_atlas.py
python scripts/finalize_review.py
python -m http.server 8000 --directory docs/review
```

完整输出：`build/Dharma-Atlas-v0.7.html`、`docs/review/index.html`、100份Markdown档案、审阅JSON、QA和输入文件SHA256清单。

权威资料更新需联网，且先校验CURRENT指向的schema：

```bash
python scripts/collect_authority_metadata.py --refresh
python scripts/repair_authority_bibliography.py
python scripts/build_atlas.py
python scripts/finalize_review.py
```

采集只保留身份/版本/书目等事实与来源定位，不重新发布84000的整部译文。来源仓库快照可能滞后于出版社现行网站；目录占位不能当成已出版译文。

## 可迁移到其他学科的Skill

入口：[skills/global-knowledge-atlas/SKILL.md](skills/global-knowledge-atlas/SKILL.md)。

流程覆盖：定义范围、利用已有数据库、多语言检索、引文追踪、文本/版本/实物辨析、年代与GIS、口述史与民间实践、数字社群与KOL溯源、实验与综述方法、争议整理、初学者教学、媒体授权和交付验收。

适配宗教/思想史、文学艺术、地方史民俗、自然科学、医疗疗愈研究、商业/游戏研究。换学科时替换实体、来源库、语言和证据门槛，不复制佛学结论。HDS来源用于语境化原则与研究入口；整套skill是本项目的综合设计，**不是哈佛认证、官方课程或合作项目**。

## 尚未通过的正式研究门禁

此前README的“100/100 L3”并不由逐部年代、书目与确切写本证据支持。本轮保留旧标签供diff，但不继续将它作为完成事实。

仍需完成：82部尚无条目级书目；100部的完整成书年代论证；更广的确切写本/刻本核对；18部平行分类冲突；作品与合集/传统边界；逐项学术争议和原文定位；外部访问与媒体权利复核。

六张信息图是教学示意。7个有依据的事件不等于完整历史事件库。网站能够运行不代表上述研究门禁已通过，仓库文件存在也不代表官网已公开部署。

## 版本与审计

基线由 [CURRENT.json](data/CURRENT.json) 管理。`v0.6`仍是保存的100部原始深层结构；`v0.7.review`是附加审阅，不破坏旧数据。

本轮修正了CURRENT曾指回v0.4旧schema的不一致，并增加工作流校验，防止旧结构导致权威证据被清空。研究版输出和正式发布状态分别登记。参见 [DATABASE_STATUS.md](DATABASE_STATUS.md)。
