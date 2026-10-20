# الشرق · Al Sharq — brand files

متجر الشرق، سوق المرادية، آخر سوق الحميدية، دمشق القديمة · Al Sharq Store, Souq Al-Muradiyya, Old Damascus

- Website: https://alsharq-damascus.vercel.app
- WhatsApp: +963 938 695 132 · https://wa.me/963938695132
- Calls: mobile 0933 917 095 · landline 011 226 3552 (card v1 and the website show both; card v2 shows the mobile only)
- Instagram / Facebook: @alsharq.damascus

## Files
| File | What | Use |
|---|---|---|
| `logo/alsharq-logo.png` | Full logo (symbol + الشرق + Al Sharq), transparent | Card front, sign, covers |
| `logo/alsharq-logo-on-teal.png` | Full logo on teal | Anywhere a ready image is needed |
| `logo/alsharq-symbol.png`, `logo/alsharq-symbol-on-teal.png` | Symbol only | Stickers, seals, small spaces |
| `logo/alsharq-profile-picture-with-name-1080.png` | Profile picture with the name | Facebook, Instagram, WhatsApp |
| `logo/alsharq-profile-picture-1080.png` | Profile picture, symbol only | Small avatars |
| `social/alsharq-facebook-cover-1640x624.jpg` | Facebook cover | Facebook page |
| `print/v1/alsharq-business-card-v1-print.pdf` | Business card version 1 (the printed one), 2 pages, 96 × 56 mm incl. 3 mm bleed | For the printer: double-sided, trim to 90 × 50 mm |
| `print/v2/alsharq-business-card-v2-print.pdf` | Business card version 2, ONE face (everything on the front: site teal with a faint star lattice, logo symbol top-right, name, offer, contacts with names, QR to the website, address), 96 × 56 mm incl. 3 mm bleed | For the printer: single-sided, trim to 90 × 50 mm |
| `print/v2/alsharq-business-card-v2-preview.png`, `print/v2/alsharq-business-card-v2.svg` | Version 2 preview, and the vector source | Checking; editing in CorelDraw or Illustrator |
| `print/v1/*-preview.png`, `print/v1/alsharq-business-card-v1-back.svg` | Version 1 previews, and the back as vector | Checking; editing in CorelDraw or Illustrator |
| `qr/alsharq-qr-website.*` | QR to the website | Card, sign, bags |
| `fonts/` | Reem Kufi (name, headlines), Readex Pro (all other text) | SIL Open Font License, licences included |

## Colours
| | Name | HEX | Use |
|---|---|---|---|
| قيشاني | Qishani teal | `#1F6A70` | Main ground |
| بازلت | Basalt | `#2A2826` | Text, dark ground |
| حجر مزّي | Mizzi stone | `#E8DDC7` | Logo lettering, warm paper |
| قمر الدين | Qamar al-Din | `#E37922` | The sun, one highlight |
| قمر الدين الغامق | Deep apricot | `#A9500F` | Accent text on white |

The logo's lettering is light: on white paper, place the logo on a teal block.

## Rebuild the business card (for example, a new phone number)
```bash
pip install -r tools/requirements.txt
python tools/make_card.py "+963 938 695 132" "0933 917 095" "011 226 3552"
```
The three numbers are: WhatsApp, mobile for calls, and the Damascus landline. The call numbers are also on the website (`index.html`).
This rewrites the files in `print/v1/` (the PDF, the back SVG and both previews). Text is converted to outlines, so the printer needs no fonts.

## Rebuild business card version 2 (one face, names beside the numbers)
```bash
pip install -r tools/requirements.txt
python tools/make_card_v2.py "+963 938 695 132" "0933 917 095" "" "عمر قطرميز" "يوسف قطرميز"
```
Arguments: WhatsApp number, mobile, landline, then the names shown beside the WhatsApp number and the mobile. Card v2 does not show the landline: pass `""` (or omit it) to leave it off, or give a number to add a third row labelled «أرضي». The names and numbers also have defaults at the top of `tools/make_card_v2.py`. Output goes to `print/v2/`: the PDF, the SVG and the preview. Add `--background` (anywhere in the command) for the background variant: the souq background image (`products/background/background-image.png`) behind the left half instead of the side lineup; its files end in `-v2-background-…`. Add `--mix` for the mixed variant: the background image across the whole card plus the three cutouts crisp in front with a soft shadow; its files end in `-v2-mix-…`. Product cutouts, shown large along the left edge, come from `products/cutouts/` (made by `tools/make_cutouts.py`, see `products/README.md`). Text is converted to outlines, so the printer needs no fonts. Version 1 is not changed by this script.

## Card versions
Each card design has its own folder under `print/`, and the version is in every file name so the printer cannot mix them up.

| Folder | Design | Built by |
|---|---|---|
| `print/v1/` | Two faces: teal front with logo and tagline, white back with QR and contacts. This is the printed card. | `tools/make_card.py` |
| `print/v2/` (three variants: side lineup, `-background`, `-mix`) | One face on the site's teal with a faint star lattice: logo symbol (no lettering) top-right, name and offer in stone, contacts with the people's names, QR to the website on a stone panel (top-left), product cutouts along the left edge, address. (Earlier drafts with a teal panel and with stone paper are in the git history.) | `tools/make_card_v2.py` |

For a new design, add `tools/make_card_v3.py` that writes to `print/v3/` and add a row here. Do not overwrite an older version.

## A4 print sheet
`python tools/make_sheet.py print/v2/alsharq-business-card-v2-mix-print.pdf` puts 8 copies of a card on one A4 page with crop marks at the 90 × 50 mm trim corners (`...-A4-sheet.pdf` and only the card dependencies). Print at 100% / "actual size", never "fit to page". Rebuild the sheet after every card change.

## Card v2 text colour
All card v2 text is metallic gold: a light-to-deep gradient (`#F6E4A6` to `#B98C34`, defined as `#gold` in `tools/make_card_v2.py`) with a soft dark shadow under every letter. A flat gold looked plain yellow and got lost on the photo. Text that should stay out of the gold treatment (the QR panel) is not affected. The QR panel stays stone so the code scans reliably.
