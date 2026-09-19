# Garden of Dharma｜官网交付与维护

日期：2026-09-19。用户要求：直接改官网、挂现有GitHub Pages，随后自行绑定域名；不要在前台暴露仓库或数据库入口。

## 本次设计

官网品牌：法藏花园 / Garden of Dharma；英文品牌副标Dharma Atlas。

明亮象牙白、暖金、莲粉与玉绿；莲池、花树、金色宝阁、石阶、栏杆、垂饰和拱形卡片。主场景是本项目原创的程序化矢量插画，渲染为PNG；不是用户历史参考图片的复制，也不声称历史现场复原。未检索到可用于本轮的历史参考图原件，因此依据已经确认的文字风格执行。

导航：主页、故事、经典、流转地图、人物、经藏宝阁、关于。中文英文以URL参数与切换按钮独立呈现。英文故事为单独编辑的完整阅读稿；六张既有图解保留中文图内文字，英文页面明确标注Chinese-language guide，不冒称整套图已翻译。原典名、书目题名与机构名称保留其来源语言。

## 代码与发布

- 访客界面源：`web/garden/`
- 访客数据投影：`scripts/build_garden.py`
- 原创场景渲染：`scripts/render_garden.py`
- 浏览器测试：`tests/garden_smoke.py`
- 网页归档：`docs/garden/`
- 唯一发布目录：`build/public/`
- 正式工作流：`.github/workflows/publish-atlas.yml`
- 实际部署和验收：`status/garden-deployment.json`、`status/garden-public-qa.json`（只在成功后写入）

入口与媒体路径使用相对URL，不锁死到项目路径或未来域名。此次没有设置CNAME、修改DNS、购买域名、修改仓库可见性或打开付费服务。

## 前台和研究资料的边界

前台没有GitHub链接、JSON导出、审计导出、源码展开、内部记录ID、原始研究对象、提交号或数据文件路径。公众需要的经典资料、进一步书目和机构来源仍可访问；不能为了隐藏仓库而移除必要的史料出处。

不是CSS隐藏：构建脚本使用字段白名单重新生成公众内容。发布只包含garden网页及其资产；旧的`review/`、`archive/`、根部release/deployment JSON与研究文件不被打包。Quantum子站按原目录保留。

**边界不能误述为保密：** 现有源仓库仍是公开的。访客看到的文字和浏览器必须获得的资源也是公开的。去掉站内链接、改用自定义域名、让旧研究网页返回404，都不能让公开仓库或已发布内容自动成为私密数据。需要真正私有时，应另行授权将研究层迁到私有仓库/受控后端，并确认现有账号与Pages方案；不可未经确认改变同仓库其他项目访问权。

## 回头绑定域名

用户尚未提供域名，本轮不猜域名、不改DNS。

绑定时在GitHub Pages设置配置已拥有的域名，并按GitHub官方说明配置DNS和HTTPS。子域名的CNAME通常指向账号的Pages主机名，而不是带路径的项目URL。是否使用根域名、www或子域名由用户明确；切勿仅添加仓库CNAME文件就宣称域名已绑定。

官方说明：https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

## 内容状态

网站发布与数据库研究并行；不宣称100部深度考证已完成。未确定的成书日期、版本等价、馆藏匹配继续保留读者可理解的说明。内容更新不应恢复旧的GitHub/原始数据入口。
