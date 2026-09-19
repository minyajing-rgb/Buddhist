# CONTENT QA GATE｜内容完整性验收

> 原则：以后**只有通过本页 QA 的内容才能标记 DONE**。Outline / title / empty card 都不能叫“完成”。

## A. Database Coverage

### Online Sources
- [x] 汉文佛典：CBETA / SAT
- [x] 早期佛典：SuttaCentral / Pāli Tipiṭaka / PTS
- [x] 藏文：84000 / BDRC / Adarshah
- [x] 梵文：GRETIL / DSBC
- [x] 犍陀罗：Gandhari.org / EBMP
- [x] 敦煌/中亚：IDP / BnF Pelliot / NLC
- [x] 学术论文：NTU DLBS / INBUDS
- [x] 规范数据：DILA Authority
- [x] 全球馆藏定位：WorldCat
- [x] 多语文本对齐/数字人文：BuddhaNexus / OpenPecha
- [ ] 韩国数字大藏经专库：待下一轮官方入口核验
- [ ] 东南亚国家级巴利写本目录：待下一轮扩展

### Offline / Physical Holdings
- [x] British Library
- [x] BnF
- [x] Library of Congress
- [x] Cambridge University Library
- [x] Harvard-Yenching
- [x] National Diet Library
- [x] National Library of China
- [x] National Central Library (Taiwan)
- [x] Haeinsa / Tripitaka Koreana
- [x] University of Washington / EBMP
- [x] Bodleian
- [x] BDRC partner network
- [ ] Nepal National Archives / major Newar Buddhist manuscript repositories
- [ ] Sri Lanka national/temple Pāli manuscript repositories
- [ ] Myanmar/Thailand national manuscript repositories
- [ ] Mongolia national/monastic Tibetan collections

## B. Per-record Minimum Fields

每个 **Source** 至少：
- [ ] 中英文名
- [ ] URL
- [ ] authority_level
- [ ] access
- [ ] languages
- [ ] traditions
- [ ] content_types
- [ ] strengths
- [ ] limitations
- [ ] how to query
- [ ] verified_from

每个 **Library** 至少：
- [ ] 城市/国家
- [ ] strength
- [ ] online-first path
- [ ] onsite trigger
- [ ] access steps
- [ ] official source URL

每个 **Text Work** 至少：
- [ ] canonical title set
- [ ] tradition
- [ ] IDs where verified
- [ ] relation type
- [ ] chronology status
- [ ] source links
- [ ] bibliography status
- [ ] evidence confidence

## C. User-facing Content Gate

任何学习页面不能只有提纲。最低标准：
- [ ] 300–800字大众解释
- [ ] 1个故事/人物钩子
- [ ] 1个timeline节点
- [ ] 1个geography节点
- [ ] 2个以上primary/authority source links
- [ ] 1个“争议/不知道”框
- [ ] 1个“继续深挖”入口

## D. Visual Gate

- [ ] 白色基底
- [ ] 海军蓝文字 + 少量暖金 + 轻紫/青绿辅助
- [ ] 不做厚重“宗教寺庙风”
- [ ] 地图写实但克制
- [ ] 图主格式 PNG/JPG，不以SVG作为用户主入口
- [ ] 所有成品图进入 docs/assets/img/
- [ ] 每张图有source/alt/title metadata

## E. Definition of Done

**DONE = data exists + source verified + user-facing explanation exists + QA checked.**

以下都不能称完成：
- 只有标题
- 只有outline
- 只有一张图
- 只有JSON schema没有data
- 有data但没有source
- 有网页卡片但点进去是空的
