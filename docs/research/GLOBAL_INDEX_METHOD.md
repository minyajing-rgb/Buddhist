# GLOBAL INDEX METHOD｜怎么找一部佛典、版本、原件

> 这不是“列一堆网站”。每次查询都走同一条可复核路径。

## 0. 先问清楚你找的是什么

同一个中文经名可能指：
- 一个 **Work**（抽象作品）；
- 某个 **Version / recension**（具体传统版本）；
- 某个 **Translation**；
- 某件 **Witness**（写本、刻本、碑铭、经板）；
- 某个 **Collection**（大藏经、文集、部类）。

先分层，后面才不会把“相似文本”误当“同一本”。

## 1. 中文佛典：先走 CBETA / SAT

**路径**
1. 中文经名 → CBETA
2. 记录 T / X / J 等编号
3. SAT 交叉确认《大正藏》位置
4. 看译者、卷数、异译
5. 再去 SuttaCentral / 84000 / Sanskrit sources 找平行版本

**适合**：汉译经、论、律、注疏、历代藏经。

## 2. 早期佛典：先走 SuttaCentral

**路径**
1. Pāli / English / Chinese title
2. 锁定 DN / MN / SN / AN / Khp / Snp 等ID
3. 打开 parallels
4. 看汉阿含、梵文残片、藏文对应
5. 再转 Gandhari / manuscript catalog 查实体证据

**注意**：parallel 不等于 identical。

## 3. 藏文佛典：84000 + BDRC + Adarshah

- **84000**：Toh编号、英译、Kangyur/Tengyur结构。
- **BDRC/BUDA**：Work / Version / scans / 具体版刻。
- **Adarshah**：藏文电子文本路线。

## 4. 梵文佛典：GRETIL + DSBC + NGMCP

- **GRETIL**：大量梵文电子文本。
- **DSBC**：梵文佛教经典与尼泊尔手稿资源。
- **NGMCP**：尼泊尔18万余件微缩手稿的目录工程，适合追具体 manuscript / microfilm。

## 5. 犍陀罗与中亚：Gandhari + IDP

- **Gandhari.org**：Gāndhārī corpus / manuscript / inscription / bibliography。
- **IDP**：敦煌、中亚写本跨馆整合。
- BnF Pelliot / British Library Stein 等馆藏再做实体定位。

## 6. 东南亚贝叶经

### Sri Lanka
National Library of Sri Lanka → palm-leaf collection → Pāli/Sinhala/Sanskrit。

### Thailand
National Library Ancient Manuscript DB + D-Library：
- palm leaf
- inscriptions
- Thai folding books
- item-level registration number

### Myanmar
National Library of Myanmar：
- Buddhist Literature Digital Collection
- Palm-leaf Manuscript Digital Collection
- Rare Books

## 7. 韩国与日本

### Korea
Dongguk University KABC：
- integrated Tripitaka
- Korean Buddhist Complete Works
- Koryŏ canon related resources
- images / catalog records

实体见证：Haeinsa Tripitaka Koreana woodblocks。

### Japan
SAT + NDL + INBUDS：
- Taishō text
- Japanese scholarship
- digitized old books
- remote photoduplication / in-person use

## 8. 蒙古

National Library of Mongolia：
1. e-catalog 搜藏文/蒙古文题名
2. 看是否标电子版本
3. 对应 BDRC 查数字扫描
4. 无数字版则记录 call number 联系馆方

## 9. 如果网上没有全文

统一走：

```
Title / ID
→ WorldCat / national catalog
→ institution catalog
→ shelfmark / call number
→ digitized? yes: read online
→ no: request scan / photoduplication
→ restricted/fragile: reading-room appointment
→ compare with parallel/version databases
```

## 10. 每次研究必须留下这些字段

- canonical_title
- aliases
- language
- tradition
- Work ID
- Version ID
- canonical IDs
- direct URLs
- witness / shelfmark
- holding institution
- chronology
- relation type
- bibliography
- confidence
- last_verified_at

这样整个数据库以后可以自动生成 Map、Timeline、Compare、Story，而不是重新人工整理。
