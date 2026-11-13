# BAAC Sales Sheet Wiki — schema

This is an Obsidian vault built as an **LLM wiki**: an LLM reads immutable sources in `raw/` and keeps a
cross-linked markdown knowledge base in `wiki/`. People read the wiki; the LLM writes and maintains it.

## Layers

| Path | What | Who edits |
|---|---|---|
| `raw/<NN_หมวด>/*.pdf` | BAAC (ธ.ก.ส.) product sales sheets, downloaded from baac.or.th/help-center/document/sales-sheet | nobody (immutable) |
| `raw/<NN_หมวด>/*.ocr.md` | Tesseract OCR of each PDF (tha+eng). Helper only — tables are often garbled | regenerated, never hand-edited |
| `raw/index.csv` | title, file, original URL for every PDF | download script |
| `wiki/products/<หมวด>/<ชื่อผลิตภัณฑ์>.md` | one page per sales sheet | LLM |
| `wiki/categories/<หมวด>.md` | one hub per site category, with comparison table | LLM |
| `wiki/concepts/<แนวคิด>.md` | cross-cutting topics (tax, fees, deposit protection…) | LLM |
| `index.md` | entry point, links every page | LLM |
| `log.md` | append-only change log (`## [YYYY-MM-DD] action | subject`) | LLM |

## Rules

1. **The PDF is the source of truth.** Read the PDF itself (visually); use the `.ocr.md` only to speed up reading.
   When the two disagree, the PDF wins. Never invent numbers. If a field is not in the document, write `ไม่ระบุในเอกสาร`.
2. Write content in **Thai** (the sources' language). Keep English product names / codes in `aliases`.
3. Cite page numbers for facts: `(หน้า 2)`. Every product page ends with a link to its PDF.
4. Link generously with `[[wikilinks]]`: product → its category hub, product → concepts, related products ↔ each other.
5. Use only the canonical concept names below for links (so pages connect). New concepts are fine — add them to this list.
6. Dates in documents are Buddhist Era (พ.ศ.). Keep them as written; optionally add ค.ศ. in parentheses.
7. When updating: re-read the source, edit the page, update category hub + `index.md`, append to `log.md`.

## Category hubs (canonical names)

`[[สลากออมทรัพย์]]` · `[[เงินฝาก]]` · `[[บัตร]]` · `[[เงินฝากสงเคราะห์ชีวิต]]` · `[[บริการ]]` · `[[บริการต่างประเทศ]]` · `[[มาตรการภาครัฐ]]`
(สินเชื่อ and ประกัน tabs had 0 documents on the site as of 2026-11-11.)

## Canonical concepts

`[[ภาษีดอกเบี้ยเงินฝาก]]` · `[[ค่าธรรมเนียม]]` · `[[การคุ้มครองเงินฝาก]]` · `[[ผลตอบแทนเฉลี่ยต่อปี]]` ·
`[[การถอนหรือไถ่ถอนก่อนครบกำหนด]]` · `[[กรณีผู้ฝากเสียชีวิต]]` · `[[BAAC Mobile]]` (alias A-Mobile) · `[[การรับรางวัลสลาก]]` ·
`[[ความคุ้มครองประกันภัยที่แถมมากับบัตร]]` · `[[อัตราแลกเปลี่ยน]]` · `[[เลตเตอร์ออฟเครดิต (LC)]]` ·
`[[การเรียกเก็บเงินตามเอกสาร (Bill for Collection)]]` · `[[การโอนเงินต่างประเทศ]]` · `[[MRTA และ MLTA]]` ·
`[[การลดหย่อนภาษีเงินได้]]` · `[[ช่องทางติดต่อและร้องเรียน]]` · `[[ความเสี่ยงของผลิตภัณฑ์]]` · `[[ประกันอุบัติเหตุที่แถมมากับเงินฝาก]]`

## Product page template

```markdown
---
title: <ชื่อผลิตภัณฑ์ตามเอกสาร>
aliases: [<English name>, <รหัสโครงการ/ชื่อย่อ>]
type: product
category: "[[<หมวด hub>]]"
product_code: <รหัสโครงการ หรือ ไม่ระบุในเอกสาร>
offer_period: <ระยะเวลาเสนอขาย/รับฝาก ถ้ามี>
source: "[[raw/<NN_หมวด>/<file>.pdf]]"
source_url: <url from raw/index.csv>
tags: [baac, sales-sheet, <category-en>]
updated: YYYY-MM-DD
---

# <ชื่อผลิตภัณฑ์>

> [!summary] สรุป
> 2–4 sentences: what it is, who it is for, the headline numbers.

## ข้อมูลสำคัญ
| หัวข้อ | รายละเอียด |
|---|---|
(eligibility, minimum/maximum, term, rate/return/prize, fees, tax, channels … whatever the sheet has)

## <sections that fit the product: อัตราดอกเบี้ย / รางวัล / ค่าธรรมเนียม / ความคุ้มครอง / เงื่อนไข …>

## ข้อควรระวัง
(risks, penalties, early-withdrawal rules, exclusions)

## ที่เกี่ยวข้อง
- หมวด: [[<hub>]]
- แนวคิด: [[...]]
- ผลิตภัณฑ์ใกล้เคียง: [[...]]

## แหล่งที่มา
- Sales sheet: ![[raw/<NN_หมวด>/<file>.pdf]]  (embed) · [ต้นฉบับบนเว็บไซต์](<source_url>)
```

## Category hub template

Frontmatter `type: category`. Sections: overview, comparison table of every product in the category
(name link + the 3–5 columns that matter most for that category), how to choose, related concepts.

## olw (obsidian-llm-wiki) integration

The vault is also an olw vault (`wiki.toml`, `.olw/`, `vault-schema.md`, git repo). Mode: **query + maintain only**.
The pages here were written by the process above, not by `olw compile`.

- Use: `olw query "..."` (add `--save` to keep the answer in `wiki/queries/`), `olw lint`, `olw maintain`, `olw status`.
- Avoid on this vault: `olw ingest` / `olw compile` / `olw run` on `raw/`. They would re-synthesise all 65 OCR files into duplicate flat pages.
- **Never** run `olw clean`: it deletes `wiki/`.
- `wiki/index.md` is olw's page catalogue, and `olw query` picks pages from it. olw's own index generator only scans the top level of `wiki/`.
  So after adding or renaming pages, or after any olw command that rewrites it (ingest, compile, approve, review), regenerate it with
  `python -I .olw/make_olw_index.py`. The human entry point stays `index.md` in the vault root.
- Every wiki page needs `status: published` in its frontmatter (olw lint requires it).
- Quote YAML values that contain `: `.
- In tables, link with plain `[[Page]]`, not `[[Page\|alias]]`: olw's link checker can't read the escaped pipe.
- LLM: Claude Opus 5.5 (`claude-opus-5-5`) through Anthropic's OpenAI-compatible endpoint (`provider = custom`, `https://api.anthropic.com/v1`).
  The API key lives only in `%APPDATA%\olw\config.toml`. **Run olw as `python .olw/olw_claude.py <command>`**, not plain `olw`:
  the wrapper adds the `anthropic-version` header that olw's connection check needs. Plain `olw` reports "Cannot reach custom" for any command that calls the API.
  Plain `olw lint` and `olw status` work fine. JSON mode returns HTTP 400 on this endpoint; olw retries without it automatically.
