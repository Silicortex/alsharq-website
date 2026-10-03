"""Usage: python tools/make_card.py "<WhatsApp>" "<mobile>" "<landline>"
       e.g. python tools/make_card.py "+963 938 695 132" "0933 917 095" "011 226 3552"
Al Sharq business card -> print-ready 2-page PDF (96x56 mm incl. 3 mm bleed), outlined text."""
import sys, os, base64, io
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from tp import shape, static_font
import qrcode, cairosvg
from PIL import Image
from pypdf import PdfReader, PdfWriter
PHONE=sys.argv[1] if len(sys.argv)>1 else "+963 938 695 132"   # WhatsApp
CALL=sys.argv[2] if len(sys.argv)>2 else "0933 917 095"        # mobile, calls inside Syria
LAND=sys.argv[3] if len(sys.argv)>3 else "011 226 3552"        # Damascus landline
HANDLE="@alsharq.damascus"; URL="https://alsharq-damascus.vercel.app"; OUT=os.path.join(HERE,"..")
BAS,MUT,STONE,TEAL="#2A2826","#605952","#E8DDC7","#1F6A70"
q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=0); q.add_data(URL); q.make(fit=True); M=q.get_matrix(); n=len(M)
def qr_rects(x,y,size,fill):
    s=size/n; return "".join(f'<rect x="{x+c*s:.3f}" y="{y+r*s:.3f}" width="{s+0.02:.3f}" height="{s+0.02:.3f}" fill="{fill}"/>' for r,row in enumerate(M) for c,v in enumerate(row) if v)
RK_FILE="ReemKufi-Variable.ttf"; RX_FILE="ReadexPro-Variable.ttf"
RK7=static_font("ReemKufi-Variable.ttf",700); R4=static_font("ReadexPro-Variable.ttf",400); R5=static_font("ReadexPro-Variable.ttf",500)
def run(font,t,size,fill,x0,base):
    r=shape(font,t,size); return f'<path transform="translate({x0:.3f} {base:.3f})" fill="{fill}" d="{r["d"]}"/>', r["width"]
def width(font,t,size): return shape(font,t,size)["width"]
def words_rtl(font,words,size,fill,right,base,gap):
    out=[]; x=right
    for w in words:
        wd=width(font,w,size); p,_=run(font,w,size,fill,x-wd,base); out.append(p); x-=wd+gap
    return out, x+gap
def words_ltr_right(font,words,size,fill,right,base,gap):
    ws=[width(font,w,size) for w in words]; total=sum(ws)+gap*(len(ws)-1); x=right-total; out=[]
    for w,wd in zip(words,ws): p,_=run(font,w,size,fill,x,base); out.append(p); x+=wd+gap
    return out
W,H=362.835,211.654; R=W-26; parts=[]; DY=9.0
def page(body,bg): return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="96mm" height="56mm" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')
gap=0.30*17
p,left=words_rtl(RK7,["متجر","الشرق"],17,BAS,R,43.0+DY,gap); parts+=p
dw=width(RK7,"·",17); p,_=run(RK7,"·",17,MUT,left-gap-dw,43.0+DY); parts.append(p)
parts+=words_ltr_right(RK7,["Al","Sharq","Store"],17,BAS,left-gap-dw-gap,43.0+DY,gap)
t="سوق المرادية، آخر الحميدية، دمشق"; p,_=run(R4,t,12,BAS,R-width(R4,t,12),66.0+DY); parts.append(p)
for i,l in enumerate(["Souq Al-Muradiyya, Old Damascus"]):
    p,_=run(R4,l,12,MUT,R-width(R4,l,12),84.1+DY+16.8*i); parts.append(p)
labels=["واتساب","موبايل","أرضي","إنستغرام · فيسبوك"]; values=[PHONE,CALL,LAND,HANDLE]
lab_w=max(width(R4,l,12) for l in labels); min_x=1e9
for i,(l,v) in enumerate(zip(labels,values)):
    b=110.2+DY+16.8*i
    p,_=run(R4,l,12,MUT,R-width(R4,l,12),b); parts.append(p)
    vx=R-lab_w-10-width(R5,v,12); min_x=min(min_x,vx)
    p,_=run(R5,v,12,BAS,vx,b); parts.append(p)
parts.append(qr_rects(32,26+DY,64,BAS))
for t,f,c,b in (("امسح للتواصل",R4,BAS,109.5),("Scan to",R4,MUT,125.4),("reach us",R4,MUT,141.0)):
    p,_=run(f,t,12,c,64-width(f,t,12)/2,b+DY); parts.append(p)
back=page("".join(parts),"#FFFFFF")
logo=open(os.path.join(OUT,"logo","alsharq-logo.png"),"rb").read(); lw,lh=Image.open(io.BytesIO(logo)).size; h=156; w=h*lw/lh
# ---- front: logo on the start (right) side, tagline + what we sell beside it
TAG_AR="حيث تنتهي الحميدية… يبدأ الشرق"; TAG_EN="Where Hamidiyya ends, Al Sharq begins."
OFF_AR=["ألبسة رجالية ونسائية وولادية","هدايا وتذكارات وأقمشة"]
OFF_EN=["Men’s, women’s & children’s clothing","Gifts, souvenirs & fabrics"]
RK6=static_font(RK_FILE,600); RX3=static_font(RX_FILE,300)
lh_=148; lw_=lh_*lw/lh; lx=W-26-lw_; colR=lx-20; colW=colR-26
def fit(font,t,size):
    wd=width(font,t,size); return size if wd<=colW else size*colW/wd
rows=[(RK6,TAG_AR,fit(RK6,TAG_AR,16),STONE,1.55),
      (RX3,TAG_EN,fit(RX3,TAG_EN,10.5),STONE,1.5),
      None,
      (R5,OFF_AR[0],min(fit(R5,OFF_AR[0],11.5),fit(R5,OFF_AR[1],11.5)),STONE,1.55),
      (R5,OFF_AR[1],min(fit(R5,OFF_AR[0],11.5),fit(R5,OFF_AR[1],11.5)),STONE,1.55),
      (RX3,OFF_EN[0],min(fit(RX3,OFF_EN[0],10),fit(RX3,OFF_EN[1],10)),STONE,1.5),
      (RX3,OFF_EN[1],min(fit(RX3,OFF_EN[0],10),fit(RX3,OFF_EN[1],10)),STONE,1.5)]
RULE=14   # space taken by the divider between tagline and offer
total=sum(r[2]*r[4] for r in rows if r)+RULE
y=(H-total)/2; fparts=[]
for r in rows:
    if r is None:
        fparts.append(f'<rect x="{colR-26:.3f}" y="{y+RULE/2-0.7:.3f}" width="26" height="1.4" fill="#7A9E97"/>'); y+=RULE; continue
    font,t,size,col,lead=r; base=y+size*lead*0.78
    p,_=run(font,t,size,col,colR-width(font,t,size),base); fparts.append(p); y+=size*lead
front=page(f'<image x="{lx:.3f}" y="{(H-lh_)/2:.3f}" width="{lw_:.3f}" height="{lh_}" xlink:href="data:image/png;base64,{base64.b64encode(logo).decode()}"/>'+"".join(fparts),TEAL)
writer=PdfWriter(); k=1452/W; m=round(11.34*k)
for svg,name in ((front,"front"),(back,"back")):
    writer.add_page(PdfReader(io.BytesIO(cairosvg.svg2pdf(bytestring=svg.encode()))).pages[0])
    png=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=1452))).convert("RGB")
    png.crop((m,m,1452-m,round(H*k)-m)).save(f"{OUT}/print/alsharq-business-card-{name}-preview.png")
with open(f"{OUT}/print/alsharq-business-card-print.pdf","wb") as f: writer.write(f)
open(f"{OUT}/print/alsharq-business-card-back.svg","w").write(back)
print("card built:", PHONE, "|", CALL, "|", LAND, "|", HANDLE)
print("leftmost contact value x=%.1f (QR column ends ~100)" % min_x)
