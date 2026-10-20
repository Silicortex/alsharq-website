# Product photos for business card v2

Put up to 4 product photos here (`.jpg`, `.jpeg`, `.png` or `.webp`), then rebuild the card:

```bash
pip install -r brand/tools/requirements.txt
python brand/tools/make_card_v2.py
```

- Files are used in name order (`1-...`, `2-...`). 1 photo fills the corner, 2 are stacked, 3 or 4 form a grid. Photos are centre-cropped to fit.
- Use the original, full-size photo, not a screenshot. Facebook shrinks pictures, so download from the photo's menu (Download) or use the camera originals. Print needs about 800 px or more on the short side.
- Only use photos you own or may reuse. This folder is public on GitHub (not on the website).
- With no photos here, the card keeps the top-left corner empty.
