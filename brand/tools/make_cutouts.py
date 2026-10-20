"""Usage: python tools/make_cutouts.py products/originals/photo1.png [photo2.png ...]
Removes the background of product photos and keeps only the main product (largest object), so logos or
watermarks in the picture are dropped. Writes transparent PNGs to products/cutouts/ (used by make_card_v2.py,
in file-name order). Extra requirement (large, only needed here): pip install "rembg[cpu]" scipy
The first run downloads the isnet-general-use model (~180 MB)."""
import sys, os
from PIL import Image
import numpy as np
from scipy import ndimage
from rembg import remove, new_session
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"..","products","cutouts"); os.makedirs(OUT,exist_ok=True)
sess=new_session("isnet-general-use")
for src in sys.argv[1:]:
    im=Image.open(src).convert("RGB"); cut=remove(im,session=sess).convert("RGBA")
    a=np.array(cut); mask=a[...,3]>40
    lab,n=ndimage.label(mask)
    if n:
        keep=lab==(1+int(np.argmax(ndimage.sum(mask,lab,range(1,n+1)))))
        keep=ndimage.binary_dilation(keep,iterations=3)
        a[...,3]=np.where(keep,a[...,3],0)
    cut=Image.fromarray(a); cut=cut.crop(cut.getbbox())
    name=os.path.splitext(os.path.basename(src))[0]+".png"; cut.save(os.path.join(OUT,name)); print(name,cut.size)
