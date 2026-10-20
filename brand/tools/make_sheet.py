"""Usage: python tools/make_sheet.py print/v2/alsharq-business-card-v2-mix-print.pdf
Puts a one-page card PDF (96x56 mm incl. 3 mm bleed) on an A4 sheet, 2 x 4 copies, with crop marks at the
90x50 mm trim corners. Writes <name>-A4-sheet.pdf next to the card. Print at 100% / "actual size", never "fit to page"."""
import sys, io, os
import cairosvg
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
src=sys.argv[1]; MM=72/25.4; CW,CH,GX,GY=96,56,8,8; COLS,ROWS=2,4
PW,PH=210,297; X0=(PW-(COLS*CW+(COLS-1)*GX))/2; Y0=(PH-(ROWS*CH+(ROWS-1)*GY))/2
card=PdfReader(src).pages[0]; sheet=PageObject.create_blank_page(width=PW*MM,height=PH*MM)
marks=[]
for r in range(ROWS):
    for c in range(COLS):
        x=X0+c*(CW+GX); y=Y0+r*(CH+GY)                                   # y from the top, mm
        sheet.merge_transformed_page(card,Transformation().translate(x*MM,(PH-y-CH)*MM))
        for tx,sx in ((x+3,-1),(x+CW-3,1)):
            for ty,sy in ((y+3,-1),(y+CH-3,1)):
                bx=x if sx<0 else x+CW; by=y if sy<0 else y+CH           # bleed edges
                marks.append(f'<line x1="{bx+sx*1}" y1="{ty}" x2="{bx+sx*4}" y2="{ty}"/><line x1="{tx}" y1="{by+sy*1}" x2="{tx}" y2="{by+sy*4}"/>')
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}mm" height="{PH}mm" viewBox="0 0 {PW} {PH}"><g stroke="#000" stroke-width=".15">{"".join(marks)}</g></svg>'
sheet.merge_page(PdfReader(io.BytesIO(cairosvg.svg2pdf(bytestring=svg.encode()))).pages[0])
w=PdfWriter(); w.add_page(sheet); w.compress_identical_objects(); out=src.replace("-print.pdf","-A4-sheet.pdf")
with open(out,"wb") as f: w.write(f)
print(out, round(os.path.getsize(out)/1e6,1),"MB")
