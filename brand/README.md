# الشرق · Al Sharq — brand files

متجر الشرق، سوق المرادية، آخر سوق الحميدية، دمشق القديمة · Al Sharq Store, Souq Al-Muradiyya, Old Damascus

- Website: https://alsharq-damascus.vercel.app
- WhatsApp: +963 938 695 132 · https://wa.me/963938695132
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
| `print/alsharq-business-card-print.pdf` | Business card, 2 pages, 96 × 56 mm incl. 3 mm bleed | For the printer: double-sided, trim to 90 × 50 mm |
| `print/*-preview.png`, `print/alsharq-business-card-back.svg` | Previews, and the back as vector | Checking; editing in CorelDraw or Illustrator |
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
python tools/make_card.py "+963 938 695 132"
```
This rewrites `print/alsharq-business-card-print.pdf`, the back SVG and both previews. Text is converted to outlines, so the printer needs no fonts.
