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
| Opening hours | commented block at the end of `<section class="info">` | Uncomment and edit when ready. |
| Domain | `alsharq-damascus.vercel.app` | Used in canonical, `og:url`, `og:image` and the JSON-LD. Update everywhere if you add a custom domain. |

## Files
- `index.html` — the page (Arabic first, English second), meta tags and structured data
- `styles.css` — brand colours, layout, animation
- `assets/` — logo, icons, social preview image
- `fonts/` — Reem Kufi and Readex Pro (SIL Open Font License, licences included)
- `vercel.json` — clean URLs and cache headers
