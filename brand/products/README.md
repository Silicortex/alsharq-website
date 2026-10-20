# Product pictures for business card v2

- `originals/` — the photos saved from Facebook. Kept on this computer only (git-ignored), because they are large.
- `cutouts/` — background removed, product only, transparent PNG. **These are what the card uses** (up to 3, in file-name order). The card currently shows `image2` (men's vest), `image5` (embroidered dress), `image6` (fur coat).

To change them:
```bash
pip install "rembg[cpu]" scipy -r brand/tools/requirements.txt     # rembg downloads a ~180 MB model on first run
python brand/tools/make_cutouts.py brand/products/originals/<photo>.png   # writes brand/products/cutouts/<photo>.png
python brand/tools/make_card_v2.py
```
- Check each cutout by eye: automatic removal can lose thin parts (it dropped the sleeves of the white dress, so that one is not used) and can keep logos, so crop leftovers out.
- Use original-size photos, not screenshots. Only use pictures you own or may reuse; this folder is public on GitHub (not on the website).
- They stand large along the left edge of the card, fading into the teal toward the text. With no files in `cutouts/`, that area stays empty.
