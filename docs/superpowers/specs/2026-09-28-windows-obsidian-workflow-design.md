# Windows 与 Obsidian 笔记工作流设计

## 背景与目标

笔记仓库已从 macOS 迁移到 Windows，并继续使用 Material for MkDocs 与 GitHub Pages 发布。日常写作使用 Obsidian；发布前由 Codex 整理附件、验证站点、提交并推送。

成功标准：

- 仓库位于 `D:\notes`，Obsidian Vault 为 `D:\notes\docs`。
- 新附件统一保存在 `docs/assets/images/`。
- Obsidian 生成标准 Markdown 相对链接，不使用 Wikilinks。
- Obsidian 的本机配置不进入 Git。
- 本地内容测试和 `mkdocs build --strict` 均能通过。
- 推送到 `main` 后沿用现有 GitHub Actions 自动部署。

## 本地目录与工具

- Git 仓库根目录：`D:\notes`
- Obsidian Vault：`D:\notes\docs`
- Python 虚拟环境：`D:\notes\.venv`
- 附件目录：`D:\notes\docs\assets\images`
- MkDocs 配置：`D:\notes\mkdocs.yml`

不引入 Obsidian Git 插件，也不增加新的发布服务。Git、构建与发布仍以仓库现有工具链为准。

## Obsidian 配置

在 `docs/.obsidian/app.json` 中使用以下本机设置：

- 附件目录为 `assets/images`；
- 新链接格式为相对路径；
- 关闭 Wikilinks，生成标准 Markdown 链接。

仓库现有 `.gitignore` 已忽略 `.obsidian/`，因此这些偏好只影响本机，不改变公开站点或其他设备。

## 编辑与附件流程

用户在 Obsidian 中创建或修改 `docs/` 下的 Markdown 文件。拖入图片时，Obsidian 将文件保存到 `assets/images/`，并根据当前笔记深度写入相对链接。

发布前，Codex 执行机械性整理：

1. 检查新增和修改的 Markdown 文件；
2. 将遗漏或散落的附件移动到 `docs/assets/images/`；
3. 修正图片相对路径并补充有意义的替代文本；
4. 检查是否残留 Obsidian 嵌入语法或失效的本地图片链接；
5. 不主动改写笔记观点与正文内容。

## 预览、验证与发布

首次设置时在仓库根目录创建 `.venv`，安装 `requirements.txt` 中锁定的依赖。本地预览从仓库根目录运行 MkDocs，并通过浏览器访问本地地址。

每次发布依次执行：

1. 查看 Git 差异，确认发布范围；
2. 运行 `python -m unittest tests/test_content_integrity.py -v`；
3. 运行 `mkdocs build --strict`；
4. 检查 Git 差异与未跟踪附件；
5. 创建描述本次笔记变更的提交；
6. 推送到 `origin/main`；
7. 确认 GitHub Actions 部署成功，并抽查线上页面及图片。

测试或严格构建失败时停止提交或推送，先修复内容与路径问题。推送需要当前 Windows Git 已具备仓库写入凭据；若没有，则在首次发布时完成 GitHub 身份验证。

## 边界与后续扩展

首阶段不安装 Obsidian Git 插件、不自动定时提交、不改变现有 GitHub Pages 工作流，也不把 `.obsidian` 配置纳入版本控制。若日后需要一键预览或发布，再根据实际重复操作增加 PowerShell 脚本。
