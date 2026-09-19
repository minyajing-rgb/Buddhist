# QuriAtlas / 量子漫游 — 域名与部署交接

## 本次站点结构

- 主仓库：`minyajing-rgb/Buddhist`
- 量子站源码：`quantum/site/`
- 发布文件：`docs/quantum/index.html`
- 现有 Pages 公网路径：`https://minyajing-rgb.github.io/Buddhist/quantum/`
- 中文入口：末尾加 `?lang=zh`
- English entry: append `?lang=en`
- 原佛典网站继续位于共享站点根目录，没有改为量子站。

是否部署成功以 `.github/workflows/quantum-site.yml` 的公网内容校验和 `quantum/data/qa.v0.2.public.json` 为准，不能由目录存在推断。

## 方案 A：域名和托管都放到阿里云

将本项目生成的 `index.html` 放在一个独立静态站点的根目录，并把该站点的默认首页设置为 `index.html`。不要把整个 `Buddhist/docs` 作为只展示量子内容的站点根目录。

页面已包含 CSS、JavaScript、中英文内容和 SVG 图形，没有依赖 GitHub 原始文件地址或第三方 CDN 的运行资源，也没有后端服务。外部资料链接仍需要联网。选择实际承载服务后，以该服务控制台给出的域名绑定、DNS 记录和值、HTTPS 配置为准。

本次没有购买托管、创建阿里云资源、修改 DNS 或配置自定义域名。

## 方案 B：GitHub Pages 托管，阿里云管理 DNS

GitHub 官方流程是先在对应仓库 Settings → Pages 配置 Custom domain，再在 DNS 服务商添加对应记录。子域名的 CNAME 目标是 `minyajing-rgb.github.io`，不能包含 `https://`、`/Buddhist/` 或 `/quantum/`。

**注意路径：DNS 只选择主机，不选择网页目录。** 当前仓库根目录是佛典站；给整个仓库绑定域名，不会自动让量子子目录成为首页。

当一个独立域名需要直接打开量子首页时，使用独立的量子站发布根目录，例如单独 Pages 仓库，或者方案 A 的独立静态站点。不得为实现量子首页而擅自覆盖现有佛典首页。

不要在尚未创建并验证托管站点时添加通配符 DNS。域名、DNS 和 HTTPS 的最终状态应在绑定后单独验收。

## 上线验收

1. 域名 HTTPS 可访问且证书正常；打开正确量子页面。
2. `?lang=zh`、`?lang=en` 可直达；切换、刷新后保留语言。
3. 概念卡、4 个实验模型和地图 SVG 导出正常。
4. 手机端无横向裁切；控制按钮可以点击。
5. 老佛典站仍按原路径正常访问。

## Official references

- GitHub publishing sources: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub custom domains: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

Domain name and actual Aliyun hosting product have not yet been specified. Do not invent CNAME targets for an unselected hosting service.
