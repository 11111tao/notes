# PhD Notes Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the public notes site into a five-section PhD learning journal and render homepage Material icons correctly.

**Architecture:** Keep `docs/` as the public Obsidian Vault and MkDocs source. Organize published Markdown by purpose, move existing reusable content without rewriting its claims, and keep unpublished research in a separate Vault outside this repository. Update the existing integrity checks for the new tree.

**Tech Stack:** Material for MkDocs 9.7.7, Markdown, Python 3.13 `unittest`, PowerShell on Windows. Use the installed `python` and `python -m mkdocs`; this checkout has no `.venv`.

**Spec:** `docs/superpowers/specs/2026-09-29-phd-notes-reorganization-design.md`

## Global Constraints

- Public entries: `PhD Journey`, `Courses`, `Papers`, `Concepts`, `Tools`.
- `Courses` starts with 化工数学; do not invent course-note content.
- `Papers` holds public-paper reading notes, one paper per page; preserve current prose, citations, and `tdp-workflow.png`.
- Unpublished project ideas, experiments, results, meeting details, and collaborator information stay out of this Git repository.
- Remove TDP Dataset, Physical Intelligence, Crypto, and the Bai Lab meeting record, including their existing uncommitted changes, as authorized by the user.
- Preserve the existing uncommitted Bai Lab paper-note content while moving it.
- Historical `docs/superpowers/` files stay excluded from MkDocs and are not rewritten.
- Do local verification; do not push or publish as part of this plan.

## Review Focus

- A moved paper image with a stale relative path should fail the existing local-image test; check it in Task 2.
- A moved home or section link with a stale relative path should fail the existing local-link test; check it in Task 2.
- An old public section left behind should fail the retired-section test; check it in Task 2.
- A literal `:material-...:` shortcode in generated home HTML should fail the icon test; check it in Task 1.
- A private meeting note copied into a new public section should fail the public-boundary test; check it in Task 2.

---

### Task 1: Render homepage Material icons

**Files:**
- Modify: `mkdocs.yml`
- Modify: `tests/test_content_integrity.py`

**Interfaces:**
- Consumes: existing `mkdocs build --strict` and `site/index.html`.
- Produces: generated home HTML with SVG icons instead of literal `:material-...:` shortcodes.

- [ ] **Step 1: Add `test_homepage_icons_render_as_svg`** to `tests/test_content_integrity.py`; read `site/index.html`, assert it contains `class="twemoji"` or equivalent Material SVG markup, and assert it lacks the literal `:material-brain:` shortcode.
- [ ] **Step 2: Run `python -m mkdocs build --strict` and `python -m unittest tests/test_content_integrity.py -v`**; expect the new icon test to fail.
- [ ] **Step 3: Add `pymdownx.emoji` to `mkdocs.yml`** with `emoji_index: !!python/name:material.extensions.emoji.twemoji` and `emoji_generator: !!python/name:material.extensions.emoji.to_svg`.
- [ ] **Step 4: Run `python -m mkdocs build --strict` and `python -m unittest tests/test_content_integrity.py -v`**; expect the icon test to pass and no icon shortcode in `site/index.html`.
- [ ] **Step 5: Commit only `mkdocs.yml` and `tests/test_content_integrity.py`** with message `fix: render homepage Material icons`.

### Task 2: Migrate and prune public notes

**Files:**
- Create: `docs/PhD Journey/index.md`, `docs/Courses/index.md`, `docs/Courses/chemical-engineering-mathematics/index.md`, `docs/Papers/index.md`, `docs/Concepts/index.md`, `docs/Tools/index.md`
- Move: `docs/Bai Lab/mission-001-read-articles.md` content to `docs/Papers/machine-learning-driven-impact-resistance.md` and `docs/Papers/machine-learning-enabled-materials-design.md`
- Move: `docs/AI/Frameworks/cnn.md` to `docs/Concepts/machine-learning/cnn.md`; `docs/AI/Harness/how-agents-work.md` to `docs/Concepts/agents/how-agents-work.md`; `docs/AI/RSI/recursive-self-improvement.md` to `docs/Concepts/agents/recursive-self-improvement.md`
- Delete: public Markdown under `docs/TDP Dataset/`, `docs/Physical Intelligence/`, `docs/Crypto/`, and the remaining `docs/Bai Lab/`; delete unreferenced `docs/assets/images/` files only after checking references
- Modify: `docs/index.md`, `README.md`, `tests/test_content_integrity.py`

**Interfaces:**
- Consumes: current Markdown content and the `docs/assets/images/` image library.
- Produces: five valid top-level pages and source links, one public-paper page per paper, no retired public pages.

- [ ] **Step 1: Capture the current working-tree text** of the Bai Lab paper note and list all its image targets. Confirm existing `Bai Lab`, `Crypto` modifications before deletion, and keep the paper prose unchanged during moves.
- [ ] **Step 2: Update integrity tests**: replace `EXPECTED_PAGES` and topic indexes with the new paths; add `test_retired_public_sections_absent` for the removed directories and `test_public_boundary` checking no public page is titled `Bai Lab Meeting` or contains the existing meeting-note marker `Kai Li's focus`.
- [ ] **Step 3: Run the updated tests** against the old tree; expect failures for missing new pages and present retired pages.
- [ ] **Step 4: Create the five section indexes and the 化工数学 entry.** Explain each section's scope in short Chinese prose. Split the two cited public papers into distinct `Papers` pages without changing their claims; retain the short second-paper stub if that is all the source contains.
- [ ] **Step 5: Move the three AI concept pages** to clear `Concepts` subfolders, adjusting relative image links. Remove the old topic pages and any retired images with no remaining references.
- [ ] **Step 6: Replace the homepage cards and update README** for the five sections and public/private authoring rule. Keep Material icon shortcodes now supported by Task 1; choose valid icons for every new card.
- [ ] **Step 7: Run `python -m mkdocs build --strict` and `python -m unittest tests/test_content_integrity.py -v`**; expect all checks to pass. Inspect `site/index.html` for five cards and SVG icons, inspect the Papers pages for the retained image, and confirm retired page directories are absent from `site/`.
- [ ] **Step 8: Review `git diff` and `git status --short`** for preserved paper content, deleted retired pages, and no new private research details. Commit only the intended migration files with message `docs: reorganize public PhD notes`.

## Self-review

- Spec coverage: five sections, migration, deletions, public boundary, icon fix, tests, and local-only completion are assigned above.
- Relative links and assets are covered by existing tests after updated paths; generated output is checked after a fresh build.
- Task 1 and Task 2 each have a failing check, implementation, passing check, and focused commit.
