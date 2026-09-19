# Dharma Atlas｜佛典全球知识地图

> **The Global Map of Buddhist Texts, Transmission & Evidence**  
> 用现代人能理解的方式，把佛典的时间、地理、语言、版本、翻译、写本、人物、争议与证据链连接起来。

## 这个项目回答什么？

不是简单回答“哪一本才是真经”，而是把问题拆成可验证的证据链：

1. 这部作品在什么传统中出现？
2. 最早可见的实体写本/刻本是什么？
3. 有没有巴利、汉文、梵文、犍陀罗文、藏文等平行版本？
4. 不同版本哪里相同、哪里不同？
5. 是翻译差异，还是底本本来就不同？
6. 哪些判断是传统说法、哪些是学术共识、哪些仍有争议？
7. 原件/影像/校勘本今天在哪里可以看到？

## 三个核心产物

### 1. Infographic Map
位于 `docs/infographics/`：

- **01 — 2500 Years of Buddhist Texts**：佛典形成与传播时间线
- **02 — Transmission Geography**：传播 / 翻译 / 写本 / 馆藏地理图
- **03 — Textual Tradition Tree**：佛典传统与主要分支树
- **04 — Evidence Chain**：从“传统说法”到“可重建早期文本”的证据链
- **05 — Learning Map**：小白 / Explorer / Scholar 三种学习方式

### 2. HTML Website
入口：`docs/index.html`

网站结构：
- Start Here
- Timeline
- Geography
- Textual Tree
- Evidence
- Stories
- Learn
- Sources
- Search Lab

### 3. Research/Data Layer
位于 `data/`：
- `canon_master_map.json`
- `source_registry.json`
- `work_schema.json`

## 核心原则

### “最早可重建” ≠ “绝对真经”
佛教早期长期依靠口传。现代文献学能做的是比较多语言、多传统、多版本的证据，重建更早的文本层，而不是声称找到了“佛陀亲笔原稿”。

### Work ≠ Version
一个“作品”可以有多个版本、译本、抄本、刻本。数据层必须区分：
- Work：抽象作品
- Version：具体文本版本
- Witness：具体写本/刻本/实体见证

### Parallel ≠ Same
跨传统文本关系至少分：
- close parallel
- partial parallel
- resembling parallel
- translation
- recension
- quotation
- uncertain

## 第一批权威数字资源

| Resource | 重点 |
|---|---|
| CBETA | 汉文大藏经、T/X/J等经号、全文与校注 |
| SAT Daizōkyō Text Database | 《大正新脩大藏经》数字文本 |
| SuttaCentral | 早期佛典、多语言、平行经关系 |
| 84000 | 藏文 Kangyur/Tengyur 英译 |
| BDRC / BUDA | Work-Version-Person-Place、藏文与扫描资料 |
| Gāndhārī.org | 犍陀罗语佛教写本与语料 |
| International Dunhuang Programme | 敦煌/中亚写本 |
| NTU Buddhist Studies | 现代佛教学书目、论文与研究资料 |
| WorldCat | 全球实体馆藏定位 |

## Story-first 内容框架

第一季：**《真经到底去哪了？》**

1. 佛陀为什么没有留下一本书？
2. 没有纸和录音，几百个人怎么保存经文？
3. 为什么后来出现不同版本？
4. 地下为什么会出现两千年前的桦树皮写本？
5. 丝绸之路上的“国际翻译公司”
6. 鸠摩罗什为什么翻得这么好读？
7. 玄奘为什么一定要去印度？
8. 唐代译经场到底怎么工作？
9. 为什么有些印度原文失传，中文反而保存了？
10. 西藏为什么又保存了另一大套？
11. “伪经”到底是什么意思？
12. 今天学者怎么重建一个已经不存在的祖本？

## Status

**v0.2 — Canon Crosswalk / Explorer**
- [x] Repo architecture
- [x] 6 bilingual infographics
- [x] HTML single-page atlas
- [x] Initial canon/source schemas
- [x] 32 key text nodes (first crosswalk batch)
- [x] 20 concept → text learning entries
- [x] searchable Core Text Explorer
- [x] Season 1 / 12-episode story outline
- [x] source/ID verification ledger
- [ ] expand to 100 key texts
- [ ] 50 key people
- [ ] manuscript/library atlas
- [ ] full source ID crosswalk
- [ ] complete bilingual story episodes

---

**Repository:** `minyajing-rgb/Buddhist`  
**Product name:** **Dharma Atlas｜佛典全球知识地图**
