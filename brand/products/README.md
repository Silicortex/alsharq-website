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

## Background image (background and mix versions)
`background/background-image.png` is the one image used behind the card: an old souq scene (fabrics, lanterns, striped arches, mosque). The script crops a card-shaped band from it (a little below the centre) and fades it into the teal. Replace the file to change the background, any size, ideally 1500 px or more on the short side. `python brand/tools/make_card_v2.py --background` puts it behind the left half only; `--mix` puts it behind the whole card, with the `cutouts/` standing in front with a soft shadow. The default side-lineup version has no background photo.
