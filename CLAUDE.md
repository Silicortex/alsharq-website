# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

One-page, Arabic-first (RTL) link site for Al Sharq, a shop in Souq Al-Muradiyya, Old Damascus. Plain HTML + CSS, no JS, no build step, no tests, no linter. Live at https://alsharq-damascus.vercel.app. The git root is this folder (not its parent).

## Commands

- Preview locally: `python3 -m http.server 8765` in the repo root, then open http://localhost:8765/. Use a server, not `file://`: `index.html` references `/styles.css`, `/fonts/...` and `/assets/...` with root-absolute paths.
- Deploy: `git push origin main`. The Vercel project `alsharq-damascus` is connected to `Silicortex/alsharq-website`, and each push to `main` goes to production in seconds. There is no preview-branch workflow in use.
- Vercel work goes through the `vercel` CLI (logged in as the account that owns the team). The Vercel MCP connection cannot see this project (404/403), so don't rely on it.
- Rebuild the printed business card (needs Python deps): `pip install -r brand/tools/requirements.txt && python brand/tools/make_card.py "<new number>"`.

## Architecture

- `index.html` is the whole site, with `<head>` meta, JSON-LD and the four buttons. `styles.css` holds all styling and animation. `vercel.json` sets clean URLs and cache headers for `/assets/` and `/fonts/`.
- Fonts are self-hosted in `fonts/` (Reem Kufi for display, Readex Pro for text) and preloaded in `<head>`. Brand colours live as CSS variables in `:root` (teal `#1F6A70`, basalt, stone, apricot).
- `brand/` (logos, QR, print files, fonts, `tools/make_card.py`) lives in GitHub but is **excluded from the deployed site by `.vercelignore`**. `/brand/...` must return 404 live. Don't link to it from the page.
- `.vercel/` and `.env*` are git-ignored; they exist locally from `vercel link`.

## Data that is duplicated and must stay in sync

When any of these change, update every location, then push:

- **Phone/WhatsApp**: the `wa.me/<digits>?text=...` href (keep the `?text=` part) and `"telephone": "+<digits>"` in the JSON-LD in `index.html`, plus `README.md` (the table of editable values), `brand/README.md`, and the card (`make_card.py "<number>"`, which regenerates the PDF, back SVG and previews in `brand/print/`).
- **Instagram/Facebook handle** (`alsharq.damascus`): the two button hrefs and `sameAs` in the JSON-LD, plus `brand/README.md`. `HANDLE` and `URL` are hard-coded constants in `brand/tools/make_card.py` (the QR encodes `URL`), so edit them there and rebuild the card.
- **Domain** (`alsharq-damascus.vercel.app`): canonical, `og:url`, `og:image`, and the JSON-LD `url`, `logo` and `image`. Also in `README.md`, `brand/README.md` and `make_card.py` (the QR).
- **Map coordinates** `33.511363, 36.305078`: the Google Maps button href (`lat%2Clng`) and JSON-LD `geo` and `hasMap`. Shop door, Plus Code `G864+G2W`; the visible Plus Code text in `.info .plus` must match.

## Listings (keep in sync with the site)

Shop details also live outside this repo; when the phone, hours or address change, update these too:

- Facebook https://www.facebook.com/alsharq.damascus and Instagram https://www.instagram.com/alsharq.damascus/
- WhatsApp Business: +963 938 695 132
- Opening hours: daily 09:00–21:00 (visible text in `index.html` and JSON-LD `openingHoursSpecification`)
- OpenStreetMap: node link not added yet (add it here once it exists)
- Google Search Console: verified; keep the `google-site-verification` meta tag in `index.html`
- Google Business Profile: not possible yet (Google blocks Syrian listings); add when available
- Business card: `brand/print/`, rebuilt with `brand/tools/make_card.py`

## Gotchas

- Keep all Arabic text, the English line under it, and the `lang="en" dir="ltr"` attributes on English spans. The page is `dir="rtl"`, so "start" means right.
- The sunburst and grain are decorative pseudo-elements. The grain (`body::after`) is deliberately `position: absolute` and limited to the hero, not `fixed`, so scrolling stays cheap on old phones. Keep it that way.
- `overflow-x: clip` on `html` and `body` is required: the 780px sunburst would otherwise overflow to the left in RTL and shift the page.
- Small text must stay full-strength stone on teal (no `opacity` on `.tagline-en` or `.footer p`).
- The repo is **public** because Vercel's Hobby plan cannot connect a private organization repo. Per-deployment `*.vercel.app` URLs sit behind Vercel login (302). Only the production alias is public, which is intended.
- Verify a deploy with `curl -s -o /dev/null -w '%{http_code}'` against `/`, `/styles.css`, both `/fonts/*.woff2` and the four `/assets/*` files (all 200).
