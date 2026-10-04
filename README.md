# الشرق | Al Sharq — website

One-page link site for Al Sharq Store, Souq Al-Muradiyya, Old Damascus: WhatsApp, Instagram, Facebook and directions.
Plain HTML and CSS, no build step.

- **Live site:** https://alsharq-damascus.vercel.app
- **Repo:** https://github.com/Silicortex/alsharq-website

## Deploying
Hosted on Vercel (project `alsharq-damascus`, framework "Other", no build command, output = repo root).
**Every push to `main` deploys to production automatically** — edit, commit, push, and the live site updates within seconds.

## Where to change things (`index.html`)
| What | Where | Notes |
|---|---|---|
| WhatsApp | `href="https://wa.me/963938695132?text=…"` | Number in international format, digits only. Keep the `?text=` part. |
| Phone in search data | `"telephone": "+963938695132"` in the JSON-LD `<script>` | Keep in sync with the WhatsApp number. |
| Instagram | `https://www.instagram.com/alsharq.damascus/` | Also appears in the JSON-LD `sameAs`. |
| Facebook | `https://www.facebook.com/alsharq.damascus` | Also appears in the JSON-LD `sameAs`. |
| Google Maps | `…/maps/search/?api=1&query=33.511363%2C36.305078` | Shop door, Plus Code `G864+G2W`. Also in JSON-LD `geo` and `hasMap`. |
| About text | `<section class="about">` | Two lines (Arabic, English): what the shop sells. |
| Call numbers | `<p class="calls">` in `<section class="info">` and the `telephone` list in the JSON-LD | Mobile 0933 917 095, landline 011 226 3552. Keep `tel:` links in international form. |
| Opening hours | last two `<p>` lines of `<section class="info">` | Also `openingHoursSpecification` in the JSON-LD. |
| Domain | `alsharq-damascus.vercel.app` | Used in canonical, `og:url`, `og:image` and the JSON-LD. Update everywhere if you add a custom domain. |

## Listings
Everywhere the shop's details live. When the phone, hours or address change, update each one:

| Where | Details |
|---|---|
| Website | This repo — https://alsharq-damascus.vercel.app (`index.html`) |
| Facebook | https://www.facebook.com/alsharq.damascus |
| Instagram | https://www.instagram.com/alsharq.damascus/ |
| WhatsApp Business | +963 938 695 132 |
| Opening hours | Daily 09:00–21:00 (`index.html` text and JSON-LD `openingHoursSpecification`) |
| OpenStreetMap | https://www.openstreetmap.org/node/14245692979 |
| Google Search Console | Verified. Keep the `google-site-verification` meta tag in `index.html`. |
| Google Business Profile | Not possible yet (Google blocks Syrian listings). Add when available. |
| Business card | `brand/print/`; rebuild with `brand/tools/make_card.py` |

## Files
- `index.html` — the page (Arabic first, English second), meta tags and structured data
- `styles.css` — brand colours, layout, animation
- `assets/` — logo, icons, social preview image
- `fonts/` — Reem Kufi and Readex Pro (SIL Open Font License, licences included)
- `vercel.json` — clean URLs and cache headers
