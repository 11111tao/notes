# Material for MkDocs Notes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the existing research notes into a public, automatically navigated Material for MkDocs knowledge base at `https://11111tao.github.io/notes/`.

**Architecture:** The repository root owns MkDocs configuration, pinned dependencies, tests, and a GitHub Pages workflow. Public content lives under `docs/`; MkDocs derives navigation from that directory, while the landing page and section index pages provide a curated knowledge map. A small standard-library integrity test validates migrated Markdown and assets before strict MkDocs builds and deployments.

**Tech Stack:** Python 3.12, Material for MkDocs 9.7.7, Python `unittest`, GitHub Actions, GitHub Pages

**Spec:** `docs/superpowers/specs/2026-09-22-material-mkdocs-notes-design.md`

## Global Constraints

- Publish from the public repository `11111tao/notes` to `https://11111tao.github.io/notes/`.
- Use a Chinese Material interface while preserving each note's original language and wording.
- Do not declare a complete `nav` in `mkdocs.yml`; ordinary notes must appear through native automatic navigation.
- Keep all public images in `docs/assets/images/` and reference them with document-relative Markdown paths.
- Exclude `docs/superpowers/` from the generated site and navigation.
- Pin `mkdocs-material==9.7.7`; do not add a navigation, blog, comments, analytics, tags, or backlinks plugin in the first release.
- Preserve note content except for titles, image-link conversion, and URL-safe filename changes required for publication.
- A failed content test or `mkdocs build --strict` must prevent deployment.

## Review Focus

- Nested notes must resolve `../` image links inside `docs/` without escaping the content tree; Task 2 adds a path-resolution test.
- Every migrated image reference must point to an existing file, including names that previously contained spaces or Chinese characters; Task 2 tests every local Markdown image target.
- Obsidian embeds must not survive migration; Task 2 scans every public Markdown page for `![[`.
- Project specs and plans must not leak into the public site; Task 3 verifies they are absent from `site/` after a strict build.
- Project Pages must work under `/notes/`, not only at the host root; Task 4 verifies `site_url`, generated canonical URLs, and the deployed URL.

---

### Task 1: Establish repository identity and the reproducible MkDocs foundation

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `mkdocs.yml`
- Create: `docs/index.md`
- Create: `docs/assets/javascripts/mathjax.js`
- Modify: Git repository-local configuration and the initial commit author

**Interfaces:**
- Consumes: approved design at `docs/superpowers/specs/2026-09-22-material-mkdocs-notes-design.md`
- Produces: a pinned Material installation, a valid MkDocs configuration, and a local Git identity associated with account `11111tao`

- [ ] **Step 1: Set a repository-local GitHub identity and repair the initial commit author**

```bash
git config user.name "Tao Yi"
git config user.email "148060325+11111tao@users.noreply.github.com"
git commit --amend --no-edit --reset-author
git show -s --format='%an <%ae>' HEAD
git add docs/superpowers/plans/2026-09-23-material-mkdocs-notes.md
git commit -m "docs: add Material for MkDocs implementation plan"
```

Expected: `Tao Yi <148060325+11111tao@users.noreply.github.com>`.

- [ ] **Step 2: Add pinned dependencies and local build exclusions**

Create `requirements.txt`:

```text
mkdocs-material==9.7.7
```

Create `.gitignore`:

```gitignore
.DS_Store
.venv/
.obsidian/
__pycache__/
*.py[cod]
site/
```

- [ ] **Step 3: Create the Material configuration**

Create `mkdocs.yml` with no `nav` key:

```yaml
site_name: 易涛的知识库
site_description: 易涛关于人工智能、科研与持续学习的公开笔记
site_url: https://11111tao.github.io/notes/
repo_url: https://github.com/11111tao/notes
repo_name: 11111tao/notes
edit_uri: edit/main/docs/

exclude_docs: |
  superpowers/

theme:
  name: material
  language: zh
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.sections
    - navigation.path
    - navigation.indexes
    - navigation.footer
    - content.code.copy
    - search.highlight
    - search.share
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: 切换至深色模式
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: 切换至浅色模式

plugins:
  - search:
      lang:
        - zh
        - en
  - typeset

markdown_extensions:
  - abbr
  - admonition
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true

extra_css:
  - assets/stylesheets/extra.css

extra_javascript:
  - assets/javascripts/mathjax.js
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

extra:
  social:
    - icon: fontawesome/solid/house
      link: https://11111tao.github.io/
      name: 个人主页
    - icon: fontawesome/brands/github
      link: https://github.com/11111tao
      name: GitHub
```

- [ ] **Step 4: Create the smallest buildable landing page and stylesheet placeholder**

Create `docs/index.md`:

```markdown
# 易涛的知识库

这里记录我在人工智能、科研与持续学习中的理解与实践。

[返回个人主页](https://11111tao.github.io/){ .md-button }
```

Create `docs/assets/stylesheets/extra.css`:

```css
:root {
  --notes-card-radius: 0.75rem;
}
```

Create `docs/assets/javascripts/mathjax.js`:

```javascript
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};

document$.subscribe(() => {
  MathJax.typesetPromise();
});
```

- [ ] **Step 5: Install and verify the foundation**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/mkdocs build --strict
```

Expected: build succeeds and creates `site/index.html` without warnings.

- [ ] **Step 6: Commit the foundation**

```bash
git add .gitignore requirements.txt mkdocs.yml docs/index.md docs/assets/stylesheets/extra.css docs/assets/javascripts/mathjax.js
git commit -m "build: add Material for MkDocs foundation"
```

### Task 2: Migrate notes and images with integrity tests

**Files:**
- Create: `tests/test_content_integrity.py`
- Move: eight existing Markdown notes into `docs/`
- Move: seven existing PNG images into `docs/assets/images/`
- Modify: migrated Markdown titles and image references

**Interfaces:**
- Consumes: `docs/` and the MkDocs configuration from Task 1
- Produces: `ContentIntegrityTests`, which validates public page titles, Obsidian syntax removal, safe local image paths, and expected migrated pages

- [ ] **Step 1: Write the content-integrity tests before moving content**

Create `tests/test_content_integrity.py`:

```python
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EXPECTED_PAGES = {
    "AI/Frameworks/cnn.md",
    "AI/Harness/how-agents-work.md",
    "AI/RSI/recursive-self-improvement.md",
    "Bai Lab/meeting-0920.md",
    "Bai Lab/mission-001-read-articles.md",
    "Crypto/diary-001.md",
    "Physical Intelligence/pi0.md",
    "TDP Dataset/0902-report-preparation.md",
}


def public_markdown_files():
    return [
        path
        for path in DOCS.rglob("*.md")
        if "superpowers" not in path.relative_to(DOCS).parts
    ]


class ContentIntegrityTests(unittest.TestCase):
    def test_expected_notes_were_migrated(self):
        actual = {str(path.relative_to(DOCS)) for path in public_markdown_files()}
        self.assertTrue(EXPECTED_PAGES <= actual)

    def test_every_public_page_has_h1(self):
        for path in public_markdown_files():
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertRegex(text, r"(?m)^# .+")

    def test_no_obsidian_embeds_remain(self):
        for path in public_markdown_files():
            with self.subTest(path=path):
                self.assertNotIn("![[", path.read_text(encoding="utf-8"))

    def test_local_images_exist_inside_docs(self):
        pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
        docs_root = DOCS.resolve()
        for path in public_markdown_files():
            text = path.read_text(encoding="utf-8")
            for raw_target in pattern.findall(text):
                target = raw_target.strip().strip("<>").split(" ", 1)[0]
                if target.startswith(("http://", "https://", "data:")):
                    continue
                resolved = (path.parent / target).resolve()
                with self.subTest(path=path, target=target):
                    self.assertTrue(resolved.is_relative_to(docs_root))
                    self.assertTrue(resolved.is_file())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and confirm the migration test fails**

```bash
.venv/bin/python -m unittest tests/test_content_integrity.py -v
```

Expected: `test_expected_notes_were_migrated` fails because the notes are still outside `docs/`.

- [ ] **Step 3: Move notes to stable URL-safe paths**

Use these exact mappings:

```text
AI/Frameworks/001 - CNN.md                         -> docs/AI/Frameworks/cnn.md
AI/Harness/Harness 001 - How does agent work?.md  -> docs/AI/Harness/how-agents-work.md
AI/RSI/RSI 001.md                                 -> docs/AI/RSI/recursive-self-improvement.md
Bai Lab/Meeting 0920.md                            -> docs/Bai Lab/meeting-0920.md
Bai Lab/Mission 001 Read Articles.md               -> docs/Bai Lab/mission-001-read-articles.md
Crypto/Diary 001.md                                -> docs/Crypto/diary-001.md
Physical Intelligence/PI0.md                       -> docs/Physical Intelligence/pi0.md
TDP Dataset/0902 汇报准备.md                        -> docs/TDP Dataset/0902-report-preparation.md
```

Create destination directories, then use `git add` after the move so Git records renames.

- [ ] **Step 4: Move image assets to stable names**

Use these exact mappings:

```text
Pasted image 20260922140116.png -> docs/assets/images/agent-harness-01.png
Pasted image 20260922140710.png -> docs/assets/images/agent-harness-02.png
Pasted image 20260922141321.png -> docs/assets/images/agent-harness-03.png
Pasted image 20260922141719.png -> docs/assets/images/agent-harness-04.png
Pasted image 20260922142503.png -> docs/assets/images/rsi-training-layers.png
Pasted image 20260922151300.png -> docs/assets/images/sia-results.png
截屏2026-09-22 16.40.09.png    -> docs/assets/images/tdp-workflow.png
```

- [ ] **Step 5: Add page titles and convert every Obsidian image embed**

Insert these H1 titles at the start of the corresponding pages:

```text
cnn.md                         -> # Convolutional Neural Networks
how-agents-work.md             -> # How Do AI Agents Work?
recursive-self-improvement.md  -> # Recursive Self-Improvement
meeting-0920.md                -> # Bai Lab Meeting — 09/20
mission-001-read-articles.md   -> # Mission 001 — Read Articles
diary-001.md                   -> # Crypto Diary 001
pi0.md                         -> # π0
0902-report-preparation.md     -> # 09/02 汇报准备
```

Replace the six Harness/RSI embeds with `../../assets/images/<new-name>.png`. Replace the TDP embed with `../assets/images/tdp-workflow.png`. Use meaningful alt text that describes the surrounding concept rather than the old filename.

- [ ] **Step 6: Run content and strict-build tests**

```bash
.venv/bin/python -m unittest tests/test_content_integrity.py -v
.venv/bin/mkdocs build --strict
rg -n --fixed-strings '![[' docs || true
```

Expected: all tests pass, MkDocs builds without warnings, and the search prints no matches.

- [ ] **Step 7: Commit the migrated content**

```bash
git add docs tests
git commit -m "content: migrate research notes and images"
```

### Task 3: Build the knowledge-map homepage and topic indexes

**Files:**
- Modify: `docs/index.md`
- Modify: `docs/assets/stylesheets/extra.css`
- Create: `docs/AI/index.md`
- Create: `docs/Bai Lab/index.md`
- Create: `docs/Physical Intelligence/index.md`
- Create: `docs/TDP Dataset/index.md`
- Create: `docs/Crypto/index.md`
- Modify: `tests/test_content_integrity.py`

**Interfaces:**
- Consumes: migrated page paths from Task 2
- Produces: stable topic landing URLs used by the homepage knowledge map

- [ ] **Step 1: Add tests for all knowledge-map destinations**

Add to `ContentIntegrityTests`:

```python
    def test_topic_indexes_exist(self):
        topic_indexes = [
            "AI/index.md",
            "Bai Lab/index.md",
            "Physical Intelligence/index.md",
            "TDP Dataset/index.md",
            "Crypto/index.md",
        ]
        for relative_path in topic_indexes:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((DOCS / relative_path).is_file())

    def test_project_docs_are_excluded_from_site(self):
        site = ROOT / "site"
        self.assertFalse((site / "superpowers").exists())
```

- [ ] **Step 2: Run the topic-index test and confirm it fails**

```bash
.venv/bin/python -m unittest tests.test_content_integrity.ContentIntegrityTests.test_topic_indexes_exist -v
```

Expected: failure because the five topic index pages do not exist.

- [ ] **Step 3: Create concise topic index pages**

Create each file with the specified heading and description:

```markdown
<!-- docs/AI/index.md -->
# 人工智能

记录神经网络、智能体工作机制与递归自我改进等主题。

<!-- docs/Bai Lab/index.md -->
# Bai Lab

实验室会议、研究任务与论文阅读记录。

<!-- docs/Physical Intelligence/index.md -->
# Physical Intelligence

关于具身智能、机器人学习与现实世界交互的笔记。

<!-- docs/TDP Dataset/index.md -->
# TDP Dataset

围绕材料数据、机器学习与汇报准备的研究记录。

<!-- docs/Crypto/index.md -->
# Crypto

对货币、区块链与加密生态的学习记录。
```

- [ ] **Step 4: Replace the landing page with a Material card grid**

Write `docs/index.md`:

```markdown
# 易涛的知识库

这里记录我在人工智能、科研与持续学习中的理解与实践。

[返回个人主页](https://11111tao.github.io/){ .md-button .md-button--primary }

## 知识地图

<div class="grid cards" markdown>

-   :material-brain: **人工智能**

    ---

    记录神经网络、智能体工作机制与递归自我改进等主题。

    [进入人工智能笔记](AI/)

-   :material-flask: **Bai Lab**

    ---

    实验室会议、研究任务与论文阅读记录。

    [进入实验室笔记](<Bai Lab/>)

-   :material-robot: **Physical Intelligence**

    ---

    关于具身智能、机器人学习与现实世界交互的笔记。

    [进入具身智能笔记](<Physical Intelligence/>)

-   :material-database: **TDP Dataset**

    ---

    围绕材料数据、机器学习与汇报准备的研究记录。

    [进入数据集笔记](<TDP Dataset/>)

-   :material-currency-btc: **Crypto**

    ---

    对货币、区块链与加密生态的学习记录。

    [进入 Crypto 笔记](Crypto/)

</div>
```

- [ ] **Step 5: Add focused card styling**

Extend `docs/assets/stylesheets/extra.css`:

```css
.md-typeset .grid.cards > ul > li {
  border-radius: var(--notes-card-radius);
  transition: border-color 160ms ease, transform 160ms ease;
}

.md-typeset .grid.cards > ul > li:hover {
  border-color: var(--md-accent-fg-color);
  transform: translateY(-2px);
}
```

- [ ] **Step 6: Build first, then test public-output exclusion**

```bash
.venv/bin/mkdocs build --strict
.venv/bin/python -m unittest tests/test_content_integrity.py -v
test ! -e site/superpowers
.venv/bin/python -c 'import json; data=json.load(open("site/search/search_index.json", encoding="utf-8")); text=str(data); assert "Recursive Self-Improvement" in text and "汇报准备" in text'
rg -n 'arithmatex|tex-mml-chtml' site/TDP\ Dataset/0902-report-preparation/index.html
```

Expected: strict build and all tests pass, project documents are absent, the search index contains English and Chinese content, and the formula page includes MathJax integration.

- [ ] **Step 7: Commit the knowledge map**

```bash
git add docs/index.md docs/assets/stylesheets/extra.css docs/*/index.md tests/test_content_integrity.py
git commit -m "feat: add knowledge map and topic indexes"
```

### Task 4: Add contributor documentation and GitHub Pages deployment

**Files:**
- Create: `README.md`
- Create: `.github/workflows/deploy.yml`

**Interfaces:**
- Consumes: the strict build and content tests from Tasks 1–3
- Produces: a documented local workflow and a Pages artifact named `github-pages`

- [ ] **Step 1: Create the GitHub Pages workflow**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy knowledge base

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write
  actions: read

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build-and-deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v5
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.12"
          cache: pip
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Test content
        run: python -m unittest tests/test_content_integrity.py -v
      - name: Build site
        run: mkdocs build --strict
      - name: Configure Pages
        uses: actions/configure-pages@v5
      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v5
        with:
          path: site
      - name: Deploy Pages
        id: deployment
        uses: actions/deploy-pages@v5
```

- [ ] **Step 2: Document the minimal authoring workflow**

Create `README.md` with these exact sections:

````markdown
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
````

- [ ] **Step 3: Validate workflow syntax and the full local release gate**

```bash
.venv/bin/python -c 'import yaml; yaml.safe_load(open(".github/workflows/deploy.yml", encoding="utf-8"))'
.venv/bin/python -m unittest tests/test_content_integrity.py -v
.venv/bin/mkdocs build --strict
git diff --check
```

Expected: YAML parses, all tests pass, the strict build succeeds, and `git diff --check` prints nothing.

- [ ] **Step 4: Commit deployment automation and documentation**

```bash
git add README.md .github/workflows/deploy.yml
git commit -m "ci: deploy knowledge base to GitHub Pages"
```

### Task 5: Publish the repository and verify the live site

**Files:**
- No new local files
- External state: public GitHub repository `11111tao/notes`, Pages configuration, Actions run, deployed site

**Interfaces:**
- Consumes: verified `main` branch and GitHub CLI account `11111tao`
- Produces: remote repository and live knowledge base URL

- [ ] **Step 1: Run the complete pre-publication verification**

```bash
gh auth status
git status --short --branch
.venv/bin/python -m unittest tests/test_content_integrity.py -v
.venv/bin/mkdocs build --strict
```

Expected: authenticated as `11111tao`, clean `main`, all tests pass, and strict build succeeds.

- [ ] **Step 2: Confirm the remote name is available, then create and push the public repository**

```bash
gh repo view 11111tao/notes
```

Expected before creation: a not-found response. Then run:

```bash
gh repo create 11111tao/notes --public --source=. --remote=origin --push --description "Public research and learning notes built with Material for MkDocs"
```

If the repository already exists and belongs to `11111tao`, add it as `origin` and push instead of creating a duplicate.

- [ ] **Step 3: Configure Pages for workflow deployment**

```bash
gh api --method POST repos/11111tao/notes/pages -f build_type=workflow
```

If GitHub reports that Pages already exists, verify instead:

```bash
gh api repos/11111tao/notes/pages --jq '{status: .status, build_type: .build_type, html_url: .html_url}'
```

Expected: `build_type` is `workflow` and `html_url` is `https://11111tao.github.io/notes/`.

- [ ] **Step 4: Watch the deployment workflow to completion**

```bash
gh run list --repo 11111tao/notes --workflow deploy.yml --limit 1
gh run watch --repo 11111tao/notes --exit-status
```

Expected: the latest `Deploy knowledge base` run concludes successfully.

- [ ] **Step 5: Verify the deployed root and one nested image-bearing page**

```bash
curl -fsS https://11111tao.github.io/notes/ | rg '易涛的知识库'
curl -fsS https://11111tao.github.io/notes/AI/Harness/how-agents-work/ | rg 'agent-harness-01.png'
```

Expected: both commands find the requested content.

- [ ] **Step 6: Report the live URL and the remaining Hugo backlink step**

Report `https://11111tao.github.io/notes/` as live. Note that adding a “笔记” link to the separate Hugo repository remains a small follow-up because this repository does not contain the Hugo source.
