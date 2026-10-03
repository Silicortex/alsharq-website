# الشرق | Al Sharq — website

One-page link site for Al Sharq Store, Souq Al-Muradiyya, Old Damascus: WhatsApp, Instagram, Facebook and directions.
Plain HTML and CSS, no build step. Hosted on Vercel; every push to `main` redeploys.

## Before the first deploy — edit `index.html`
| What | Find | Replace with |
|---|---|---|
| WhatsApp Business number | `963XXXXXXXXX` | the number in international format, digits only (e.g. `9639…`) |
| Instagram / Facebook handle | `alsharq.damascus` | your handle, if you chose a different one |
| Shop location | `33.511354%2C36.305085` | the coordinates of the shop door (optional, later) |
| Site address | `alsharq-damascus.vercel.app` | your Vercel domain, if Vercel assigns a different one |

## Create the GitHub repo
```bash
cd alsharq-website
git init -b main && git add . && git commit -m "Al Sharq website"
gh repo create alsharq-website --private --source=. --push
```
(No GitHub CLI? Create an empty repo on github.com, then `git remote add origin <url> && git push -u origin main`.)

## Files
- `index.html` — the page (Arabic first, English second), meta tags and structured data
- `styles.css` — brand colours and layout
- `assets/` — logo, icons, social preview image
- `fonts/` — Reem Kufi and Readex Pro (SIL Open Font License, licences included)
