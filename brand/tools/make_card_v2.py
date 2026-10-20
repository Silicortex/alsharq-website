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
IG_PATH="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"
FB_PATH="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"
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
SH=66.0; SW=SH*sw/sh; SX=R-SW; SY=24.0
# ---- optional product cutouts: a large lineup on the left edge, bottom-aligned, fading into the teal toward the text
CUTS=sorted(glob.glob(os.path.join(os.environ.get("CARD_PRODUCTS_DIR",os.path.join(OUT,"products","cutouts")),"*.png")))[:3]
if BG_MODE or MIX_MODE:
    import numpy as np
    BGP=sorted(f for ext in ("png","jpg") for f in glob.glob(os.path.join(OUT,"products","background","*."+ext)))[:1]   # one background image
    BW=(W if MIX_MODE else 190.0); S=3.2; th=H/max(1,len(BGP)); OVL=12.0; cv=Image.new("RGBA",(round(BW*S),round(H*S)),(0,0,0,0))
    for bi,bf in enumerate(BGP):                                       # tiles overlap and cross-fade, so there are no hard seams
        y0=max(0.0,bi*th-OVL); y1=min(H,(bi+1)*th+OVL); tw,tt=round(BW*S),round((y1-y0)*S)
        im=Image.open(bf).convert("RGB"); r=min(im.width/tw,im.height/tt); cw,ch=tw*r,tt*r
        oy=(im.height-ch)*0.62                                          # crop band sits a little below centre (keeps fabrics and mosque)
        im=im.crop((round((im.width-cw)/2),round(oy),round((im.width+cw)/2),round(oy+ch))).resize((tw,tt),Image.LANCZOS).convert("RGBA")
        ys=(np.arange(tt)/S)[:,None]; fade=np.ones((tt,1))
        if bi>0: fade=np.minimum(fade,np.clip(ys/(2*OVL),0,1))
        if bi<len(BGP)-1: fade=np.minimum(fade,np.clip(((y1-y0)-ys)/(2*OVL),0,1))
        t=np.array(im); t[...,3]=(255*fade[:,0:1].repeat(tw,1)).astype(np.uint8)
        cv.alpha_composite(Image.fromarray(t),(0,round(y0*S)))
    a=np.array(cv); xs=(np.arange(a.shape[1])/S)[None,:]
    if MIX_MODE: a[...,3]=(a[...,3]*(0.58-0.28*xs/W)).astype(np.uint8)         # whole card: 58% at the left edge down to 30% at the right
    else: a[...,3]=(a[...,3]*0.55*np.clip((BW-xs)/(BW-70),0,1)).astype(np.uint8)   # 55% at the left edge, solid teal again by x=190
    b=io.BytesIO(); Image.fromarray(a).save(b,"PNG")
    body.append(f'<image x="0" y="0" width="{BW}" height="{H:.3f}" xlink:href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/>')
    if BG_MODE: CUTS=[]
BAND_Y=164.5
body.append(f'<rect x="0" y="{BAND_Y}" width="{W}" height="{H-BAND_Y:.2f}" fill="#174F54"/><rect x="0" y="{BAND_Y}" width="{W}" height=".8" fill="{STONE}" fill-opacity=".35"/>')
if CUTS:
    import numpy as np
    S=3.2; CW,CH=150.0,H; FEET=193.0; PH=(106.0 if MIX_MODE else 104.0)                       # canvas width, items height, feet line (inside the trim)
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
# logo symbol drawn above the background photos so they never veil it
body.append(f'<image x="{SX:.3f}" y="{SY}" width="{SW:.3f}" height="{SH}" xlink:href="data:image/png;base64,{base64.b64encode(sym).decode()}"/>')
# ---- name and offer, left of the logo
TR=SX-14; topw=TR-LEFT
body.append(right(RK7,"متجر الشرق",fit(RK7,"متجر الشرق",32,topw),STONE,TR,46))
body.append(right(R4,"Al Sharq Store",fit(R4,"Al Sharq Store",11.5,topw),STONE,TR,61))
# what we sell: small text, items joined by an apricot "+"
OFF_LINES=[["ألبسة رجالية","نسائية","ولادية"],["هدايا","تذكارات","أقمشة","صابون"]]
OSZ=9.0; PG=3.2; pw=width(R6,"+",OSZ)
for li,items in enumerate(OFF_LINES):
    x=TR; base=75+10.5*li
    for k,t in enumerate(items):
        w=width(R5,t,OSZ); body.append(run(R5,t,OSZ,STONE,x-w,base)); x-=w
        if k<len(items)-1: body.append(run(R6,"+",OSZ,QAMAR,x-PG-pw,base)); x-=2*PG+pw
TAG="حيث تنتهي الحميدية… يبدأ الشرق"
body.append(right(RK6,TAG,fit(RK6,TAG,13,R-LEFT),STONE,R,104))
# ---- contacts: icon | name | number
ICON=13.0; GAP=7.0
rows=[(WA_PATH,"#25D366",NAME_WA,PHONE),(CALL_PATH,QAMAR,NAME_MOB,CALL),(CALL_PATH,QAMAR,LAND_LABEL,LAND)]
SZ_N=11.5; SZ_T=10.5
name_w=max(width(R5,r[2],SZ_T) for r in rows)
name_right=R-ICON-GAP; num_right=name_right-name_w-12
for i,(path,col,name,num) in enumerate(rows):
    b=124+15.5*i
    body.append(f'<rect x="{R-ICON:.2f}" y="{b-ICON+3:.2f}" width="{ICON}" height="{ICON}" rx="3.2" fill="{col}"/>')
    s=(ICON*0.62)/24; ox=R-ICON+ICON*0.19; oy=b-ICON+3+ICON*0.19
    body.append(f'<path transform="translate({ox:.3f} {oy:.3f}) scale({s:.4f})" fill="#fff" d="{path}"/>')
    body.append(right(R5,name,SZ_T,STONE,name_right,b))
    body.append(right(R6,num,SZ_N,STONE,num_right,b))
cleft=num_right-max(width(R6,r[3],SZ_N) for r in rows)
# ---- QR on a stone panel (dark modules on light = scans reliably), under the logo side
QP=56.0; QM=4.5; QX=LEFT; QY=24.0
body.append(f'<rect x="{QX}" y="{QY}" width="{QP}" height="{QP}" rx="5" fill="{STONE}"/>')
body.append(qr_rects(QX+QM,QY+QM,QP-2*QM,BAS))
qc=QX+QP/2
# ---- address and handle, right block
aw=R-139.0
addr="سوق المرادية، آخر سوق الحميدية، دمشق القديمة"
body.append(right(R4,addr,fit(R4,addr,9.6,aw),STONE,R,174.5))
# separate line for the username, with the logos of the two services it belongs to (Instagram, Facebook)
body.append(f'<rect x="{R-aw:.2f}" y="178.2" width="{aw:.2f}" height=".6" fill="{STONE}" fill-opacity=".35"/>')
T=9.2; TY=179.6; TG=3.0
body.append('<defs><radialGradient id="ig" cx="30%" cy="107%" r="140%"><stop offset="0" stop-color="#FDF497"/><stop offset=".05" stop-color="#FDF497"/><stop offset=".45" stop-color="#FD5949"/><stop offset=".6" stop-color="#D6249F"/><stop offset=".9" stop-color="#285AEB"/></radialGradient></defs>')
for k,(path,fill) in enumerate(((IG_PATH,"url(#ig)"),(FB_PATH,"#1877F2"))):
    tx=R-T-k*(T+TG)
    body.append(f'<rect x="{tx:.2f}" y="{TY}" width="{T}" height="{T}" rx="2.4" fill="{fill}"/>')
    body.append(f'<path transform="translate({tx+T*0.17:.3f} {TY+T*0.17:.3f}) scale({(T*0.66)/24:.4f})" fill="#fff" d="{path}"/>')
body.append(right(R4,HANDLE,9.6,STONE,R-2*T-TG-6,TY+T-1.3))
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
