# Material for MkDocs 公开知识库设计

## 背景与目标

当前“科研学习”目录包含 AI、实验室研究、Physical Intelligence、TDP Dataset、Crypto 等 Markdown 笔记及其图片。目标是将这些内容整理成一个公开、可搜索、可持续扩展的知识库，并发布到 `https://11111tao.github.io/notes/`。

现有个人站 `https://11111tao.github.io/` 继续使用 Hugo，承担个人介绍、正式文章和阶段性写作；新的 Material for MkDocs 站点承担长期知识沉淀。两者通过链接互相连接，不要求视觉风格一致。

成功标准：

- 所有现有笔记和图片都能正确公开显示。
- 知识库使用中文界面，正文保持原本的中文、英文或混合语言。
- 首页以知识地图呈现各主题入口。
- 新增普通笔记时无需手工维护导航。
- 本地可以预览并进行严格构建检查。
- 推送到 GitHub 后自动部署到 GitHub Pages。

## 技术方案

采用 Material for MkDocs，并使用 MkDocs 原生自动导航。`mkdocs.yml` 不声明完整的 `nav`，目录和页面会自动进入导航；这样新增普通笔记只需将 Markdown 文件放入对应目录。

首版只使用必要依赖和 Material 内置能力，不引入自动导航、博客、评论、统计或复杂标签插件。Python 依赖固定版本，保证本地和 CI 构建一致。

主题启用以下核心能力：

- 中文界面；
- 浅色与深色模式；
- 客户端全文搜索；
- 分层导航、面包屑和页面目录；
- 代码高亮与复制；
- 数学公式渲染；
- 常用 Material Markdown 扩展；
- 指向个人主页和 GitHub 仓库的入口。

## 信息架构

站点内容目录为：

```text
docs/
├── index.md
├── assets/
│   ├── images/
│   └── stylesheets/extra.css
├── AI/
│   ├── index.md
│   ├── Frameworks/
│   ├── Harness/
│   └── RSI/
├── Bai Lab/
│   └── index.md
├── Physical Intelligence/
│   └── index.md
├── TDP Dataset/
│   └── index.md
└── Crypto/
    └── index.md
```

首页使用 Material 卡片构成知识地图，为每个一级主题提供简介和入口。首页不显示需要人工维护的“最近更新”列表。每个一级主题拥有一个简短的 `index.md`，普通笔记由目录结构自动加入导航。只有新增一级主题时，才需要更新首页知识地图。

项目规范存放在 `docs/superpowers/specs/`，但通过 MkDocs 的排除规则从公开站点和自动导航中移除。

## 内容迁移规则

现有主题层级和正文内容保持不变，不改写作者的观点或表达。迁移只进行发布所需的机械性调整：

1. 将 Markdown 文件迁入 `docs/` 下对应主题目录。
2. 将现有图片集中迁入 `docs/assets/images/`。
3. 将 Obsidian 图片嵌入语法（如 `![[image.png]]`）转换为标准 Markdown 图片语法，并按页面所在层级生成正确的相对路径。
4. 为没有一级标题的笔记补充清晰标题。
5. 移除文件名中不适合 URL 的字符，并使用稳定、易读的文件名；页面展示标题不受 URL 文件名限制。
6. 保持外部链接、代码块、数学表达式和原有段落结构。

迁移后通过搜索确认不存在残留的 Obsidian 图片嵌入，并通过严格构建和页面检查确认图片路径有效。

## 图片与编辑约定

图片统一存放在 `docs/assets/images/`。Markdown 使用相对于当前页面文件的路径，例如：

```markdown
![说明](../../assets/images/example.png)
```

若继续使用 Obsidian 编辑，建议将附件目录设置为 `docs/assets/images`，将新链接格式设为相对路径，并使用标准 Markdown 链接而非 Wikilinks。这样拖入图片时由编辑器自动计算相对路径。

## 项目文件

仓库根目录包含：

- `mkdocs.yml`：站点、主题、扩展、搜索、数学公式与排除规则配置；
- `requirements.txt`：固定版本的 Python 构建依赖；
- `README.md`：本地预览、检查、发布和新增笔记说明；
- `.gitignore`：忽略构建输出、Python 缓存和本地环境；
- `.github/workflows/deploy.yml`：GitHub Pages 自动构建与部署；
- `docs/`：全部公开内容、资源和被排除的项目规范。

少量 CSS 仅用于知识地图卡片和必要的中文阅读体验调整，不大幅覆盖 Material 默认视觉设计。

## 开发与发布流程

本地工作流：

```bash
mkdocs serve
mkdocs build --strict
git add .
git commit -m "新增笔记：主题"
git push
```

GitHub Actions 在 `main` 分支更新后执行以下步骤：

1. 检出仓库；
2. 安装固定版本依赖；
3. 执行 `mkdocs build --strict`；
4. 上传生成的静态站点；
5. 使用 GitHub Pages 官方部署流程发布。

严格构建失败时停止部署，避免覆盖线上正常版本。仓库使用名称 `notes`，远程地址预期为 `11111tao/notes`，站点地址为 `https://11111tao.github.io/notes/`。

本地实现和校验全部通过后，再通过已登录的 GitHub CLI 创建公开仓库、设置远程地址并推送。GitHub Pages 使用 GitHub Actions 作为发布源。

## 错误处理与验证

实现阶段至少验证：

- `mkdocs build --strict` 成功；
- 自动导航包含所有公开 Markdown 页面；
- 首页知识地图链接均有效；
- 所有现有图片均能被构建结果引用；
- 不存在 `![[...]]` 形式的残留图片嵌入；
- 搜索索引包含中英文笔记内容；
- 数学公式和代码块正常渲染；
- 站点在 `/notes/` 子路径下生成正确链接；
- `docs/superpowers/specs/` 不出现在公开构建中；
- GitHub Actions 完成后，线上首页和至少一篇含图片的嵌套笔记可访问。

## 非目标与后续扩展

首版不包含博客时间线、评论、访问统计、复杂标签体系、自动生成最近更新或双向链接。未来笔记规模增长后，可以按实际需要引入标签页、自动导航插件、Git 修订时间或内容关系图，但这些功能不得增加当前日常发布的必要步骤。

个人 Hugo 站增加“笔记”入口属于互链的后续步骤；知识库首版会先提供返回个人主页的入口，不在此仓库中直接修改 Hugo 站点。
