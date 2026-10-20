# Product pictures for business card v2

- `originals/` — the photos saved from Facebook. Kept on this computer only (git-ignored), because they are large.
- `cutouts/` — background removed, product only, transparent PNG. **These are what the card uses** (up to 3, in file-name order). The side version of the card currently shows `image4` (folded fabrics), `image5` (embroidered dress), `image6` (fur coat). `image4` was cropped to the fabric stack before cutting; automatic cutouts can leave semi-transparent patches, so check them.

To change them:
```bash
pip install "rembg[cpu]" scipy -r brand/tools/requirements.txt     # rembg downloads a ~180 MB model on first run
python brand/tools/make_cutouts.py brand/products/originals/<photo>.png   # writes brand/products/cutouts/<photo>.png
python brand/tools/make_card_v2.py
```
- Check each cutout by eye: automatic removal can lose thin parts (it dropped the sleeves of the white dress, so that one is not used) and can keep logos, so crop leftovers out.
- Use original-size photos, not screenshots. Only use pictures you own or may reuse; this folder is public on GitHub (not on the website).
- They stand large along the left edge of the card, fading into the teal toward the text. With no files in `cutouts/`, that area stays empty.

## Background version
`background/` holds landscape crops (about 2.5:1, logos cropped out) used by the background variant of the card: `image4.jpg` (fabrics), `image8.jpg` (shirts), `image9.jpg` (vests). They are stacked down the left side, cross-faded into each other and faded into the teal toward the text. Build it with `python brand/tools/make_card_v2.py --background`. (`image8.png` is an exact duplicate of `image.png`, the shirts photo.)

## Mix version
`python brand/tools/make_card_v2.py --mix` uses both folders: the `background/` crops faded across the whole card, and the `cutouts/` standing in front with a soft shadow.
