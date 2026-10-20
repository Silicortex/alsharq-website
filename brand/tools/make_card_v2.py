"""Usage: python tools/make_card_v2.py "<WhatsApp>" "<mobile>" "<landline>" ["<WhatsApp contact name>" "<mobile contact name>"]
       e.g. python tools/make_card_v2.py "+963 938 695 132" "0933 917 095" "011 226 3552"
Al Sharq business card, version 2: ONE face, 96x56 mm incl. 3 mm bleed (trim 90x50 mm), outlined text.
Layout: site teal ground with a faint star lattice; logo symbol (no lettering) top-right, straight on the teal;
name, offer and tagline; contacts with the people's names; QR (to the website) on a stone panel, top-left; address.
Optional product cutouts (transparent PNGs from tools/make_cutouts.py) in brand/products/cutouts/, up to 3 by file name, stand large along the left edge, fading into the teal toward the text (QR top-left).
Icons: WhatsApp glyph from Simple Icons (CC0); handset from Material Design Icons (Apache-2.0)."""
import sys, os, base64, io, glob
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from tp import shape, static_font
import qrcode, cairosvg
from PIL import Image
from pypdf import PdfReader, PdfWriter
BG_MODE="--background" in sys.argv; sys.argv=[a for a in sys.argv if a!="--background"]   # variant: faded product photos behind the left half
MIX_MODE="--mix" in sys.argv; sys.argv=[a for a in sys.argv if a!="--mix"]               # variant: faded photos over the whole card + crisp products in front
SFX="-background" if BG_MODE else ("-mix" if MIX_MODE else "")
PHONE=sys.argv[1] if len(sys.argv)>1 else "+963 938 695 132"   # WhatsApp
CALL =sys.argv[2] if len(sys.argv)>2 else "0933 917 095"        # mobile
LAND =sys.argv[3] if len(sys.argv)>3 else "011 226 3552"        # Damascus landline
NAME_WA =sys.argv[4] if len(sys.argv)>4 else "عمر قطرميز"        # person behind the WhatsApp number
NAME_MOB=sys.argv[5] if len(sys.argv)>5 else "يوسف قطرميز"       # person behind the mobile number
LAND_LABEL="أرضي"                                                # landline has no person, so a plain label
HANDLE="@alsharq.damascus"; URL="https://alsharq-damascus.vercel.app"; OUT=os.path.join(HERE,"..")
BAS,STONE,TEAL,QAMAR="#2A2826","#E8DDC7","#1F6A70","#E37922"
WA_PATH="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"
CALL_PATH="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"

RK7=static_font("ReemKufi-Variable.ttf",700); RK6=static_font("ReemKufi-Variable.ttf",600); R4=static_font("ReadexPro-Variable.ttf",400); R5=static_font("ReadexPro-Variable.ttf",500); R6=static_font("ReadexPro-Variable.ttf",600)
def width(font,t,size): return shape(font,t,size)["width"]
def run(font,t,size,fill,x0,base):
    r=shape(font,t,size); return f'<path transform="translate({x0:.3f} {base:.3f})" fill="{fill}" d="{r["d"]}"/>'
def right(font,t,size,fill,xr,base): return run(font,t,size,fill,xr-width(font,t,size),base)
def center(font,t,size,fill,xc,base): return run(font,t,size,fill,xc-width(font,t,size)/2,base)
def fit(font,t,size,maxw):
    w=width(font,t,size); return size if w<=maxw else size*maxw/w

q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=0); q.add_data(URL); q.make(fit=True); M=q.get_matrix(); n=len(M)
def qr_rects(x,y,size,fill):
    c=size/n; return "".join(f'<rect x="{x+j*c:.3f}" y="{y+i*c:.3f}" width="{c+0.02:.3f}" height="{c+0.02:.3f}" fill="{fill}"/>' for i,row in enumerate(M) for j,v in enumerate(row) if v)

W,H=362.835,211.654; R=W-26; LEFT=26.0
body=[]
# ---- ground: the site's teal with a faint eight-point star lattice
body.append(f'<defs><pattern id="lat" width="44" height="44" patternUnits="userSpaceOnUse"><g fill="none" stroke="{STONE}" stroke-opacity=".10" stroke-width=".6"><rect x="11" y="11" width="22" height="22"/><rect x="11" y="11" width="22" height="22" transform="rotate(45 22 22)"/><circle cx="22" cy="22" r="15.6"/></g></pattern></defs>')
body.append(f'<rect width="{W}" height="{H}" fill="{TEAL}"/><rect width="{W}" height="{H}" fill="url(#lat)"/>')
# ---- logo symbol (no lettering), straight on the teal, top-right
sym=open(os.path.join(OUT,"logo","alsharq-symbol.png"),"rb").read(); sw,sh=Image.open(io.BytesIO(sym)).size
SH=68.0; SW=SH*sw/sh; SX=R-SW; SY=22.0
body.append(f'<image x="{SX:.3f}" y="{SY}" width="{SW:.3f}" height="{SH}" xlink:href="data:image/png;base64,{base64.b64encode(sym).decode()}"/>')
# ---- optional product cutouts: a large lineup on the left edge, bottom-aligned, fading into the teal toward the text
CUTS=sorted(glob.glob(os.path.join(os.environ.get("CARD_PRODUCTS_DIR",os.path.join(OUT,"products","cutouts")),"*.png")))[:3]
if BG_MODE or MIX_MODE:
    import numpy as np
    BGP=sorted(glob.glob(os.path.join(OUT,"products","background","*.jpg")))[:3]
    BW=(W if MIX_MODE else 190.0); S=3.2; th=H/max(1,len(BGP)); OVL=12.0; cv=Image.new("RGBA",(round(BW*S),round(H*S)),(0,0,0,0))
    for bi,bf in enumerate(BGP):                                       # tiles overlap and cross-fade, so there are no hard seams
        y0=max(0.0,bi*th-OVL); y1=min(H,(bi+1)*th+OVL); tw,tt=round(BW*S),round((y1-y0)*S)
        im=Image.open(bf).convert("RGB"); r=min(im.width/tw,im.height/tt); cw,ch=tw*r,tt*r
        im=im.crop((round((im.width-cw)/2),round((im.height-ch)/2),round((im.width+cw)/2),round((im.height+ch)/2))).resize((tw,tt),Image.LANCZOS).convert("RGBA")
        ys=(np.arange(tt)/S)[:,None]; fade=np.ones((tt,1))
        if bi>0: fade=np.minimum(fade,np.clip(ys/(2*OVL),0,1))
        if bi<len(BGP)-1: fade=np.minimum(fade,np.clip(((y1-y0)-ys)/(2*OVL),0,1))
        t=np.array(im); t[...,3]=(255*fade[:,0:1].repeat(tw,1)).astype(np.uint8)
        cv.alpha_composite(Image.fromarray(t),(0,round(y0*S)))
    a=np.array(cv); xs=(np.arange(a.shape[1])/S)[None,:]
    if MIX_MODE: a[...,3]=(a[...,3]*(0.30-0.20*xs/W)).astype(np.uint8)         # whole card: 30% at the left edge down to 10% at the right
    else: a[...,3]=(a[...,3]*0.55*np.clip((BW-xs)/(BW-70),0,1)).astype(np.uint8)   # 55% at the left edge, solid teal again by x=190
    b=io.BytesIO(); Image.fromarray(a).save(b,"PNG")
    body.append(f'<image x="0" y="0" width="{BW}" height="{H:.3f}" xlink:href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/>')
    if BG_MODE: CUTS=[]
BAND_Y=167.0
body.append(f'<rect x="0" y="{BAND_Y}" width="{W}" height="{H-BAND_Y:.2f}" fill="#174F54"/><rect x="0" y="{BAND_Y}" width="{W}" height=".8" fill="{STONE}" fill-opacity=".35"/>')
if CUTS:
    import numpy as np
    S=3.2; CW,CH=150.0,H; FEET=193.0; PH=(112.0 if MIX_MODE else 104.0)                       # canvas width, items height, feet line (inside the trim)
    MAXW,OV=((52.0,14.0) if MIX_MODE else (60.0,8.0)); cv=Image.new("RGBA",(round(CW*S),round(CH*S)),(0,0,0,0)); cx0=14.0
    for f in CUTS:
        im=Image.open(f).convert("RGBA"); sc=min(PH/im.height,MAXW/im.width); w,h=im.width*sc,im.height*sc
        im=im.resize((max(1,round(w*S)),max(1,round(h*S))),Image.LANCZOS)
        cv.alpha_composite(im,(round(cx0*S),round((FEET-h)*S))); cx0+=w-OV
    a=np.array(cv); xs=(np.arange(a.shape[1])/S)[None,:]
    if not MIX_MODE:
        ramp=np.clip((142-xs)/(142-106),0,1)                           # solid until x=106, gone by x=142
        a[...,3]=(a[...,3]*ramp).astype(np.uint8)
    cv=Image.fromarray(a)
    if MIX_MODE:                                                       # soft drop shadow lifts the products off the faded photos
        from PIL import ImageFilter
        al=cv.split()[3].filter(ImageFilter.GaussianBlur(2.4*S)).point(lambda v:int(v*0.55))
        sh=Image.new('RGBA',cv.size,(0,0,0,0)); sh.putalpha(al); sh=sh.transform(sh.size,Image.AFFINE,(1,0,-1.5*S,0,1,-2.5*S))
        out=Image.new('RGBA',cv.size,(0,0,0,0)); out.alpha_composite(sh); out.alpha_composite(cv); cv=out
    b=io.BytesIO(); cv.save(b,"PNG")
    body.append(f'<image x="0" y="0" width="{CW}" height="{CH:.3f}" xlink:href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/>')
PHOTOS=CUTS
# ---- name and offer, left of the logo
TR=SX-14; topw=TR-LEFT
body.append(right(RK7,"متجر الشرق",fit(RK7,"متجر الشرق",34,topw),STONE,TR,45))
body.append(right(R4,"Al Sharq Store",fit(R4,"Al Sharq Store",11.5,topw),STONE,TR,60))
off=["ألبسة رجالية ونسائية وولادية","هدايا وتذكارات وأقمشة"]; osz=min(fit(R5,t,9.2,topw) for t in off)
for i,t in enumerate(off): body.append(right(R5,t,osz,STONE,TR,73+10.8*i))
TAG="حيث تنتهي الحميدية… يبدأ الشرق"
body.append(right(RK6,TAG,fit(RK6,TAG,13,R-LEFT),STONE,R,103.5))
# ---- contacts: icon | name | number
ICON=13.0; GAP=7.0
rows=[(WA_PATH,"#25D366",NAME_WA,PHONE),(CALL_PATH,QAMAR,NAME_MOB,CALL),(CALL_PATH,QAMAR,LAND_LABEL,LAND)]
SZ_N=11.5; SZ_T=10.5
name_w=max(width(R5,r[2],SZ_T) for r in rows)
name_right=R-ICON-GAP; num_right=name_right-name_w-12
for i,(path,col,name,num) in enumerate(rows):
    b=121+16.5*i
    body.append(f'<rect x="{R-ICON:.2f}" y="{b-ICON+3:.2f}" width="{ICON}" height="{ICON}" rx="3.2" fill="{col}"/>')
    s=(ICON*0.62)/24; ox=R-ICON+ICON*0.19; oy=b-ICON+3+ICON*0.19
    body.append(f'<path transform="translate({ox:.3f} {oy:.3f}) scale({s:.4f})" fill="#fff" d="{path}"/>')
    body.append(right(R5,name,SZ_T,STONE,name_right,b))
    body.append(right(R6,num,SZ_N,STONE,num_right,b))
cleft=num_right-max(width(R6,r[3],SZ_N) for r in rows)
# ---- QR on a stone panel (dark modules on light = scans reliably), under the logo side
QP=52.0; QM=4.0; QX=LEFT; QY=22.0
body.append(f'<rect x="{QX}" y="{QY}" width="{QP}" height="{QP}" rx="5" fill="{STONE}"/>')
body.append(qr_rects(QX+QM,QY+QM,QP-2*QM,BAS))
qc=QX+QP/2
body.append(center(R5,"امسح للتواصل",8.6,STONE,qc,QY+QP+10))
# ---- address and handle, right block
aw=R-139.0
addr="سوق المرادية، آخر سوق الحميدية، دمشق القديمة"
body.append(right(R4,addr,fit(R4,addr,9.6,aw),STONE,R,178.5))
body.append(right(R4,HANDLE,9.6,STONE,R,189))
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="96mm" height="56mm" viewBox="0 0 {W} {H}">'+"".join(body)+'</svg>')
k=1452/W; m=round(11.34*k)
os.makedirs(f"{OUT}/print/v2",exist_ok=True)
writer=PdfWriter(); writer.add_page(PdfReader(io.BytesIO(cairosvg.svg2pdf(bytestring=svg.encode()))).pages[0])
png=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=1452))).convert("RGB")
png.crop((m,m,1452-m,round(H*k)-m)).save(f"{OUT}/print/v2/alsharq-business-card-v2{SFX}-preview.png")
with open(f"{OUT}/print/v2/alsharq-business-card-v2{SFX}-print.pdf","wb") as f: writer.write(f)
open(f"{OUT}/print/v2/alsharq-business-card-v2{SFX}.svg","w").write(svg)
print("variant:", "background" if BG_MODE else ("mix" if MIX_MODE else "side lineup")); print("card v2 built:", NAME_WA,PHONE,"|",NAME_MOB,CALL,"|",LAND_LABEL,LAND,"| QR ->",URL,"| product cutouts:",len(PHOTOS))
print("contacts leftmost x=%.1f, QR panel right edge x=%.1f, title block width avail %.1f"%(cleft,QX+QP,topw))
