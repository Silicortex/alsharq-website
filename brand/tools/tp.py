"""Text -> SVG path helper with real Arabic shaping (HarfBuzz) and fontTools outlines."""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.varLib import instancer
import os, functools

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")

@functools.lru_cache(None)
def static_font(name, wght=None):
    """Return path to a static TTF (instancing variable fonts at wght)."""
    src = os.path.join(FONT_DIR, name)
    if wght is None:
        return src
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, f"_inst_{os.path.splitext(name)[0]}_{wght}.ttf".replace("[", "").replace("]", "").replace(",", "-"))
    if not os.path.exists(out):
        f = TTFont(src)
        axes = {a.axisTag: a.defaultValue for a in f["fvar"].axes}
        axes["wght"] = wght
        inst = instancer.instantiateVariableFont(f, axes)
        inst.save(out)
    return out

@functools.lru_cache(None)
def _load(path):
    tt = TTFont(path)
    blob = hb.Blob.from_file_path(path)
    face = hb.Face(blob)
    font = hb.Font(face)
    return tt, tt.getGlyphSet(), tt.getGlyphOrder(), font, face.upem

def shape(path, text, size, tracking=0.0, features=None):
    """Shape `text`; returns dict(d, width, bbox=(xmin,ymin,xmax,ymax)) in SVG coords
    with the pen starting at x=0 and baseline at y=0 (y grows downward).
    tracking is in em units (e.g. 0.12)."""
    tt, gs, order, font, upem = _load(path)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {"kern": True, "liga": True})
    s = size / upem
    track_units = tracking * upem
    parts, x = [], 0.0
    bp_all = [None, None, None, None]
    infos, poss = buf.glyph_infos, buf.glyph_positions
    for i, (info, pos) in enumerate(zip(infos, poss)):
        g = order[info.codepoint]
        tx = (x + pos.x_offset) * s
        ty = -pos.y_offset * s
        sp = SVGPathPen(gs)
        gs[g].draw(TransformPen(sp, (s, 0, 0, -s, tx, ty)))
        cmd = sp.getCommands()
        if cmd:
            parts.append(cmd)
            bp = BoundsPen(gs)
            gs[g].draw(TransformPen(bp, (s, 0, 0, -s, tx, ty)))
            if bp.bounds:
                b = bp.bounds
                for k, fn in ((0, min), (1, min), (2, max), (3, max)):
                    bp_all[k] = b[k] if bp_all[k] is None else fn(bp_all[k], b[k])
        x += pos.x_advance + (track_units if i < len(infos) - 1 else 0)
    return {"d": " ".join(parts), "width": x * s, "bbox": tuple(bp_all)}

def path_el(res, dx, dy, fill, extra=""):
    return f'<path transform="translate({dx:.2f} {dy:.2f})" fill="{fill}" d="{res["d"]}" {extra}/>'
