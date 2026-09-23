# 易涛的知识库

基于 Material for MkDocs 的公开学习与研究笔记，发布于 <https://11111tao.github.io/notes/>。

## 本地预览

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/mkdocs serve
```

## 新增笔记

1. 将 Markdown 文件放入 `docs/` 下对应主题目录。
2. 将图片放入 `docs/assets/images/`，在笔记中使用相对路径。
3. 新增普通笔记无需修改 `mkdocs.yml`；新增一级主题时更新首页知识地图。
4. 发布前运行下面的检查。

## 发布前检查

```bash
.venv/bin/python -m unittest tests/test_content_integrity.py -v
.venv/bin/mkdocs build --strict
```

推送到 `main` 后，GitHub Actions 会自动发布站点。
