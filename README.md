# 易涛的博士笔记

基于 Material for MkDocs 的公开学习笔记，发布于 <https://11111tao.github.io/notes/>。内容分为 PhD Journey、Courses、Papers、Concepts 和 Tools。`docs/` 也是公开笔记的 Obsidian Vault。

未发表课题的构想、组会记录、实验数据和结论应保存在另一个私人 Vault，不放入本仓库。这个仓库的 Git 历史也可能公开；仅从站点导航中隐藏文件不能保护其内容。

## 本地预览

```powershell
python -m pip install -r requirements.txt
python -m mkdocs serve
```

## 新增笔记

1. 将可公开的 Markdown 文件放入 `docs/` 下对应目录。月度回顾放在 PhD Journey；课程学习放在 Courses；已公开论文的阅读笔记放在 Papers；知识概念放在 Concepts；软件和工作流放在 Tools。
2. 将图片放入 `docs/assets/images/`，在笔记中使用相对路径。
3. 新增普通笔记无需修改 `mkdocs.yml`；新增一级主题时更新首页知识地图。
4. 发布前运行下面的检查。

## 发布前检查

```powershell
python -m mkdocs build --strict
python -m unittest tests/test_content_integrity.py -v
```

推送到 `main` 后，GitHub Actions 会自动发布站点。
