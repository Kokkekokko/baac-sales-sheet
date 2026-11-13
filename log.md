---
title: log
type: log
---

# Log

Append-only. Format: `## [YYYY-MM-DD] action | subject`

## [2026-11-11] ingest | initial build from 65 sales sheets
- Source: baac.or.th/help-center/document/sales-sheet, all 9 product tabs (two tabs paginated). สินเชื่อ and ประกัน had 0 documents.
- Copied PDFs to `raw/` and ran OCR on all of them (Tesseract 5.5, tha+eng, 300 dpi → `*.ocr.md`). PDF text layers were unusable because the Thai fonts have no ToUnicode map.
- Wrote 65 product pages and 7 category hubs. Agents read each PDF visually; the OCR text was a helper only.
- Wrote 18 concept pages, [[index]] and [[ปัญหาในเอกสารต้นฉบับ]].
- Renamed concept `A-Mobile` → [[BAAC Mobile]] (alias kept), because every source calls the app "BAAC Mobile".
- Added the new concept [[ประกันอุบัติเหตุที่แถมมากับเงินฝาก]].
- [[การคุ้มครองเงินฝาก]] is a stub: no source covers it.

## [2026-11-11] setup | connected olw (obsidian-llm-wiki 0.8.5)
- `olw init --existing`: added wiki.toml (language = th), .olw/, vault-schema.md, .gitignore, git repo.
- Added `.olw/make_olw_index.py` → wiki/index.md (91 entries), so `olw query` can see the nested pages.
- Added `status: published` to all pages. Quoted 3 titles containing ": " (their YAML was invalid). Removed the `\|` aliases in tables.
- `olw lint`: 100/100. LLM provider not configured yet (cloud provider chosen; needs an API key).

## [2026-11-12] config | olw provider → Claude Opus 5.5
- Global config (`%APPDATA%\olw\config.toml`): provider custom → https://api.anthropic.com/v1, model claude-opus-5-5, API key.
- Regenerated wiki.toml with a `[provider]` section. Kept language = th. Context hints set to 200K.
- Added `.olw/olw_claude.py` wrapper: olw's GET /models connection check needs the `anthropic-version` header. The installed package is not modified.
- Verified with `doctor` (reachable, model found) and a Thai test query (correct answer, 13 s).
