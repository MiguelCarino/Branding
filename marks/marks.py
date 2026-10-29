"""The Carino marks: the hub's gold C with a pictogram of the job inside it.

Every site in the fleet wears the hub's bare C. The hub's own bowl is empty --
that is what makes it the parent -- and every tool's holds one pictogram of the
job it does: a key for Password, an eye for Retina, a clock for Time. Each tool
is drawn in two variants from ONE pictogram, so they cannot drift apart:

    <stem>.svg        the mark: ring + pictogram, 100 x 100, gold on transparency.
    <stem>.webp       the mark at 50x50, lossless -- the favicon size the fleet links.
    <stem>-glyph.svg  the pictogram alone on a 24 grid, stroke 2, currentColor,
                      for list rows, a navbar tag, anywhere text-sized.
    <stem>-color.svg  the mark with a colourful pictogram: the ring stays gold,
                      each part of the pictogram takes the next PALETTE colour.
                      For the playful pages (Software first); never the favicon.

Run it and it rewrites all three for every site, plus sheet.html (the review
page) and dicom-options/:

    python3 marks.py        # needs rsvg-convert and magick for the webp

then deploy.py and verify.py from this folder, as before.

Why this replaced the first set (a small C with one blocky letter beside it):
the letter was 1.24 device px per module at 16px, so a wall of forty marks
read as forty copies of one logo, and the letter said nothing about the job.
A pictogram says what the tool is for, and the glyph variant is legible at the
sizes where the mark is not.

Geometry. The bare C is the hub's, unchanged: centre (56.03, 50), r 34.81,
stroke 16.38, read back off Carino-Systems/logo.svg -- carino.svg still comes
out byte-identical. Its bowl is a clear disc of radius 26.62. The 24 grid is
scaled to 40 units and centred on the C's centre; pictograms stay within 2..22
of the grid, so their farthest point sits 23.6 from the centre, plus half a
stroke (2.5), inside the ring with ~0.5 to spare. Inside the mark the stroke is
3 grid units (5 of 100) rather than the glyph's 2: beside a 16.38 ring a 3.3
line reads as a hairline, the same reason the old letters were drawn at a 0.20
stem ratio rather than typeset.

Drawing rules: as few parts as the idea allows (most are two or three), and at
least one solid shape in each, so the pictogram keeps a silhouette at 16px
instead of dissolving into lines. Every pictogram is drawn here from
primitives, not copied from an icon set.
"""
import os

GOLD = "#eab308"
OUT = os.path.dirname(os.path.abspath(__file__))

CX, CY = 56.03, 50.0
SCALE = 40.0 / 24
MARK_STROKE = 3.0
GLYPH_STROKE = 2.0

# The colour variant's palette, in the order parts take it. Yellow is last
# because it sits closest to the gold ring.
PALETTE = ["#4285f4", "#ea4335", "#34a853", "#fbbc04"]
# Stems of deleted sites. They still hold their place in the colour order, so
# removing one does not shift the colours of every mark after it.
RETIRED = {"multiweb"}   # MultiWeb, deleted 2026-10-29

BARE_C = ('<path d="M 81.07 25.82 A 34.81 34.81 0 1 0 81.07 74.18" fill="none" '
          f'stroke="{GOLD}" stroke-width="16.38" stroke-linecap="butt"/>')

# ---- the pictograms ---------------------------------------------------------
# On the 24 grid. {F} is the fill colour, for the solid parts.
# Everything else is stroked by the enclosing group.
P = {
 "aldis":     '<circle cx="8.5" cy="12" r="5.5" fill="{F}" stroke="none"/><path d="M17 6.5l4-2M17.5 12h4.5M17 17.5l4 2"/>',
 "asobi":     '<path d="M12 2.5l6.5 3.5 2 15.5h-17L5.5 6z" fill="{F}"/>',
 "branding":  '<path d="M12 3a9 9 0 1 0 0 18c1.4 0 2-.8 2-1.8 0-1.2-1-1.6-1-2.7 0-1 .9-1.5 2-1.5h2a4 4 0 0 0 4-4c0-4.4-4-8-9-8z"/>'
              '<circle cx="8" cy="11" r="1.7" fill="{F}" stroke="none"/><circle cx="12.5" cy="7.5" r="1.7" fill="{F}" stroke="none"/>',
 "compass":   '<circle cx="12" cy="12" r="9"/><path d="M16 8l-2.2 5.8L8 16l2.2-5.8z" fill="{F}"/>',
 "currency":  '<path d="M12 2.5v19M17 6.8C16 5 14.2 4.5 12 4.5c-2.8 0-5 1.3-5 3.7 0 2.6 2.5 3.2 5 3.8s5 1.3 5 3.9c0 2.4-2.2 3.6-5 3.6-2.3 0-4.2-.7-5.2-2.6" stroke-width="2.8"/>',
 "cve":       '<path d="M12 7a4.5 4.5 0 0 1 4.5 4.5v3a4.5 4.5 0 0 1-9 0v-3A4.5 4.5 0 0 1 12 7z" fill="{F}"/>'
              '<path d="M3.5 10.5l4 1.5M3.5 18l4-1.5M20.5 10.5l-4 1.5M20.5 18l-4-1.5M9 3.5L10.5 7M15 3.5L13.5 7"/>',
 "cybercity": '<g fill="{F}" stroke="none"><path d="M2.5 21v-7l2.25-2 2.25 2v7z"/><path d="M8.5 21V7.5L11 5l2.5 2.5V21z"/>'
              '<rect x="15" y="10" width="6.5" height="11"/></g><path d="M11 1.5V5"/>',
 "dcm":       '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 5.5v6"/>'
              '<path d="M10.8 7.5C7.5 7.5 5.5 12 5.5 17c0 1.3 1 2 2.3 1.4l3-1.4zM13.2 7.5c3.3 0 5.3 4.5 5.3 9.5 0 1.3-1 2-2.3 1.4l-3-1.4z" fill="{F}" stroke-width="1"/>',
 "desk":      '<path d="M4 4h16v13H9l-5 4z"/><path d="M13.5 6.5l-4.5 5h3.2l-1.2 4 4.5-5.2h-3.2z" fill="{F}" stroke-width="1"/>',
 "dicom":     '<path d="M8 6.5V3h13v13h-3.5"/><rect x="3" y="7.5" width="14" height="14" rx="1.5"/><path d="M10 10v3.5"/>'
              '<path d="M9 11.2c-2.2 0-3.4 3-3.4 6.3 0 .9.7 1.3 1.6.9L9 17.6zM11 11.2c2.2 0 3.4 3 3.4 6.3 0 .9-.7 1.3-1.6.9L11 17.6z" fill="{F}" stroke-width=".8"/>',
 "distro":    '<path d="M12 3v18M8.5 21h7"/><path d="M12 5h6.5l2.5 2.5-2.5 2.5H12zM12 12.5H5.5L3 15l2.5 2.5H12z" fill="{F}"/>',
 "fiscal":    '<circle cx="12" cy="5.5" r="2.5"/><path d="M12 8v3.5M5 20.5h14"/><rect x="4.5" y="11.5" width="15" height="5" rx="1" fill="{F}"/>',
 "font":      '<path d="M12 22L5.5 12.5 8 4h8l2.5 8.5z"/><path d="M12 22v-8"/><circle cx="12" cy="12" r="1.8" fill="{F}" stroke="none"/>',
 "hardware":  '<rect x="6" y="6" width="12" height="12" rx="1.5" fill="{F}"/><path d="M9.5 2v4M14.5 2v4M9.5 18v4M14.5 18v4M2 9.5h4M2 14.5h4M18 9.5h4M18 14.5h4"/>',
 "hash":      '<path d="M5 16V10a7 7 0 0 1 14 0v6M8.5 21V11a3.5 3.5 0 0 1 7 0v10M12 11v10"/>',
 "images":    '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3" fill="{F}" stroke="none"/>',
 "jellyfish": '<path d="M3.5 12a8.5 8.5 0 0 1 17 0z" fill="{F}"/><path d="M7.5 12c0 3-1.5 5-1.5 9M12 12v9M16.5 12c0 3 1.5 5 1.5 9"/>',
 "kanban":    '<rect x="2.5" y="3" width="4.8" height="12" rx="1" fill="{F}" stroke="none"/><rect x="9.6" y="3" width="4.8" height="18" rx="1" fill="{F}" stroke="none"/>'
              '<rect x="16.7" y="3" width="4.8" height="8" rx="1" fill="{F}" stroke="none"/>',
 "law":       '<path d="M3 8.5L12 3l9 5.5z" fill="{F}"/><path d="M6 11.5V18M12 11.5V18M18 11.5V18M3 21h18"/>',
 "learn":     '<path d="M2 9.5l10-5.5 10 5.5-10 5.5z" fill="{F}"/><path d="M6 12.5v4.5c3 2.5 9 2.5 12 0v-4.5"/>',
 "media":     '<path d="M14 3H5v18h14V8z"/><path d="M7.5 18l3.5-5 2.5 3 1-1.2 2 3.2z" fill="{F}"/>',
 "metadata":  '<path d="M15 7.5V3H4v18h5"/><circle cx="15" cy="15" r="4.5" fill="{F}"/><path d="M18.5 18.5L22 22"/>',
 "music":     '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3" fill="{F}"/><circle cx="17" cy="16" r="3" fill="{F}"/>',
 "netplan":   '<path d="M4 5h16v11h-3.5v3.5h-9V16H4z"/><path d="M8.5 8.5v3.5M12 8.5v3.5M15.5 8.5v3.5"/>',
 "offline":   '<path d="M8 19h9.5a3.5 3.5 0 0 0 1.4-6.7M15.6 7.6A6 6 0 0 0 6.2 10.2 4.5 4.5 0 0 0 5 19"/><path d="M3 3l18 18"/>',
 "password":  '<circle cx="8" cy="16" r="5" fill="{F}"/><path d="M11.5 12.5L20.5 3.5M17 7l3 3"/>',
 "ping":      '<path d="M2 12h4.5l2.5-6.5 4.5 13 2.5-6.5H22"/>',
 "quote":     '<path d="M5 3h14v18l-2.33-1.5L14.33 21 12 19.5 9.67 21 7.33 19.5 5 21z"/><path d="M9 9h6M9 13.5h6"/>',
 "retina":    '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3.8" fill="{F}" stroke="none"/>',
 "setup":     '<g transform="translate(2.2 1.6)"><path d="M14.5 3.2a5 5 0 0 0-5.3 6.6L3.6 15.4a2 2 0 0 0 2.8 2.8l5.6-5.6a5 5 0 0 0 6.6-5.3l-2.9 2.9-2.8-.8-.8-2.8z" fill="{F}"/></g>',
 "software":  '<rect x="3" y="3" width="7" height="7" rx="1.5" fill="{F}"/><rect x="14" y="3" width="7" height="7" rx="1.5"/>'
              '<rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5" fill="{F}"/>',
 "stocks":    '<path d="M2.5 18.5l6.5-6.5 4 4 8-8.5"/><path d="M15.5 6.5h6v6z" fill="{F}"/>',
 "subs":      '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M6 12.5h12M8 16h8"/>',
 "teleprompter": '<path d="M2.5 6h8M2.5 12h8M2.5 18h5"/><path d="M12.5 20.5L17 3.5h1.2l4.6 17M14.2 14.5h7.1" stroke-width="2.6"/>',
 "test":      '<path d="M3 18a9 9 0 1 1 18 0"/><path d="M12 17l4.5-6.5"/><circle cx="12" cy="17" r="2.2" fill="{F}" stroke="none"/>',
 "time":      '<circle cx="12" cy="12" r="9"/><path d="M12 6.5V12l4 2.5"/>',
 "topo":      '<path d="M12 5L5 18h14z"/><circle cx="12" cy="5" r="3" fill="{F}"/><circle cx="5" cy="18" r="3" fill="{F}"/><circle cx="19" cy="18" r="3" fill="{F}"/>',
 "tv":        '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M12 3v14M2 10h20M8 21h8"/>',
 "vitae":     '<rect x="4" y="2" width="16" height="20" rx="2"/><circle cx="12" cy="9" r="3" fill="{F}" stroke="none"/><path d="M7.5 17.5a4.5 4.5 0 0 1 9 0z" fill="{F}"/>',
}

# Colour-variant overrides, for a pictogram whose outlined parts read better
# solid once each part has its own colour. {C0}..{C3} are PALETTE entries.
PC = {
 "software":  '<rect x="3" y="3" width="7" height="7" rx="1.5" fill="{C0}" stroke="none"/><rect x="14" y="3" width="7" height="7" rx="1.5" fill="{C1}" stroke="none"/>'
              '<rect x="3" y="14" width="7" height="7" rx="1.5" fill="{C2}" stroke="none"/><rect x="14" y="14" width="7" height="7" rx="1.5" fill="{C3}" stroke="none"/>',
}

# ---- the fleet --------------------------------------------------------------
# (file stem, aria label). The hub is the only stem with no pictogram.
MARKS = [
 ("carino",       "Carino"),
 ("aldis",        "Carino Aldis Lamp"),
 ("asobi",        "Carino Asobi"),
 ("branding",     "Carino Branding"),
 ("compass",      "Carino Compass"),
 ("currency",     "Carino Currency"),
 ("cve",          "Carino CVE"),
 ("cybercity",    "Carino CyberCity"),
 ("dcm",          "Carino Editor"),
 ("desk",         "Carino Desk"),
 ("dicom",        "Carino DICOM"),
 ("distro",       "Carino Distro"),
 ("fiscal",       "Carino Fiscal"),
 ("font",         "Carino Fonts"),
 ("hardware",     "Carino Hardware"),
 ("hash",         "Carino Hash"),
 ("images",       "Carino Images"),
 ("jellyfish",    "Carino Jellyfish"),
 ("kanban",       "Carino Kanban"),
 ("law",          "Carino Law"),
 ("learn",        "Carino Learn"),
 ("media",        "Carino Media"),
 ("metadata",     "Carino Metadata"),
 ("music",        "Carino Music"),
 ("netplan",      "Carino Netplan"),
 ("offline",      "Carino Offline"),
 ("password",     "Carino Password"),
 ("ping",         "Carino Ping"),
 ("quote",        "Carino Quote"),
 ("retina",       "Carino Retina"),
 ("setup",        "Carino Setup"),
 ("software",     "Carino Software"),
 ("stocks",       "Carino Stocks"),
 ("subs",         "Carino Sync Studio"),
 ("teleprompter", "Carino Teleprompter"),
 ("test",         "Carino Test"),
 ("time",         "Carino Time"),
 ("topo",         "Carino Topo"),
 ("tv",           "Carino TV"),
 ("vitae",        "Carino Vitae"),
]


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def mark_svg(label, body):
    """The ring, with the pictogram (if any) scaled into its bowl."""
    inner = ""
    if body is not None:
        tx, ty = CX - 12 * SCALE, CY - 12 * SCALE
        inner = (f'<g transform="translate({tx:.3f} {ty:.3f}) scale({SCALE:.5f})" fill="none" '
                 f'stroke="{GOLD}" stroke-width="{MARK_STROKE}" stroke-linecap="round" '
                 f'stroke-linejoin="round">{body.replace("{F}", GOLD)}</g>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
            f'width="512" height="512" role="img" aria-label="{esc(label)}">{BARE_C}{inner}</svg>')


def top_level_parts(body):
    """Split a pictogram into its top-level elements (a <g> counts as one)."""
    import re
    parts, depth, start = [], 0, 0
    for m in re.finditer(r"<(/?)(\w+)[^>]*?(/?)>", body):
        closing, selfclose = m.group(1), m.group(3)
        if depth == 0:
            start = m.start() if not closing else start
        if closing:
            depth -= 1
        elif not selfclose:
            depth += 1
        if depth == 0:
            parts.append(body[start:m.end()])
    return parts


def color_body(stem, body):
    """Each top-level part stroked and filled in the next PALETTE colour."""
    if stem in PC:
        out = PC[stem]
        for i, c in enumerate(PALETTE):
            out = out.replace("{C%d}" % i, c)
        return out
    # Each mark starts its cycle on a different one of the first three
    # colours, so the one-part pictograms are not all blue side by side.
    first = sorted(set(P) | RETIRED).index(stem) % 3 if stem in P else 0
    out = []
    for i, part in enumerate(top_level_parts(body)):
        c = PALETTE[(first + i) % len(PALETTE)]
        head_end = part.index(">") + (0 if part[part.index(">") - 1] != "/" else -1)
        head = part[:head_end]
        if 'stroke="' not in head:   # keep an explicit stroke="none"
            part = part[:head_end] + f' stroke="{c}"' + part[head_end:]
        out.append(part.replace("{F}", c))
    return "".join(out)


def color_svg(label, stem, body):
    """The mark, with the pictogram in PALETTE colours instead of gold."""
    return mark_svg(label, color_body(stem, body)) if body is not None else None


def glyph_svg(label, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
            f'role="img" aria-label="{esc(label)}" fill="none" stroke="currentColor" '
            f'stroke-width="{GLYPH_STROKE}" stroke-linecap="round" stroke-linejoin="round">'
            f'{body.replace("{F}", "currentColor")}</svg>')


def sheet_row(name, src, glyph, color_src=None):
    g = glyph or ""
    small = g.replace('width="24" height="24"', 'width="16" height="16"')
    return (f'<div class="row"><span class="name">{name}</span>'
            + "".join(f'<img src="{src}" width="{s}" height="{s}" alt="">' for s in (128, 64, 32, 16))
            + (f'<span class="g light"><img src="{color_src}" width="64" height="64" alt="">'
               f'<img src="{color_src}" width="32" height="32" alt=""></span>' if color_src else "")
            + (f'<span class="g dark">{g}{small}</span><span class="g light">{g}</span>' if g else "")
            + '</div>')


SHEET_CSS = ("body{margin:0;background:#0c0a09;color:#e7e5e4;font:13px system-ui;padding:16px}"
             ".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(760px,1fr));gap:6px 24px}"
             ".row{display:flex;align-items:center;gap:14px;border-bottom:1px solid #292524;padding:4px 0}"
             ".name{width:200px;flex:none}"
             ".g{display:inline-flex;gap:10px;align-items:center;padding:6px 8px;border-radius:6px}"
             ".dark{color:#e7e5e4}.light{background:#fafaf9;color:#1c1917}")


def sheet(title, rows):
    return (f'<!doctype html><meta charset="utf-8"><title>{title}</title><style>{SHEET_CSS}</style>'
            '<p>mark 128/64/32/16 &middot; colour mark 64/32 on light &middot; glyph 24/16 on dark &middot; glyph on light</p>'
            f'<div class="grid">{"".join(rows)}</div>')


def write(path, text):
    with open(path, "w") as fh:
        fh.write(text)


# Every candidate tried for Carino DICOM, kept side by side in
# dicom-options/ for the record. Chosen: stacked-films -- the Editor's
# chest film with a second behind it, so the pair reads as one film to edit
# and a stack of studies to keep moving.
DICOM_OPTIONS = {
 "stack-cross":   ('Stack of studies, cross cut through the front one',
                   '<path d="M8 8V3h13v13h-5"/>'
                   '<path d="M2.5 8.5h13v13h-13z M7.7 11.3v2.6H5.3v2.6h2.4v2.6h2.6v-2.6h2.4v-2.6h-2.4v-2.6z" fill="{F}" fill-rule="evenodd" stroke="none"/>'),
 "ct-side":       ('CT scanner from the side, table into the ring',
                   '<circle cx="14.5" cy="10" r="6.5" stroke-width="3.6"/><rect x="2" y="11.2" width="15" height="2.8" rx=".6" fill="{F}" stroke="none"/>'
                   '<path d="M6 14v7M2.5 21h19"/>'),
 "bone":          ('A bone',
                   '<g fill="{F}" stroke="none"><circle cx="5.2" cy="15.8" r="3"/><circle cx="8.2" cy="18.8" r="3"/>'
                   '<circle cx="15.8" cy="5.2" r="3"/><circle cx="18.8" cy="8.2" r="3"/></g><path d="M7.5 16.5l9-9" stroke-width="4.6"/>'),
 "stack-headslice": ('Stack of studies, head slice on the front one',
                   '<path d="M8.5 7.5V3h12.5v12.5h-4.5"/><path d="M2.5 8h14v14h-14z M9.5 10.3a4.3 5 0 1 0 .01 0z M9.5 12.3a2.5 3 0 1 1-.01 0z" fill="{F}" fill-rule="evenodd" stroke="none"/>'),
 "axial-slice":   ('Axial head slice',
                   '<path d="M12 2.5a8 9.5 0 1 0 .01 0z M12 6a4.8 6 0 1 1-.01 0z" fill="{F}" fill-rule="evenodd" stroke="none"/><path d="M12 7v10"/>'),
 "monitor-scan":  ('Workstation monitor showing a head scan',
                   '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>'
                   '<path d="M12 5.5a3.6 4.5 0 1 0 .01 0z M12 7.5a1.8 2.5 0 1 1-.01 0z" fill="{F}" fill-rule="evenodd" stroke="none"/>'),
 "slice-series":  ('A series of slices, in perspective',
                   '<path d="M3 16l9 4.5 9-4.5M3 12l9 4.5 9-4.5"/><path d="M3 8l9-4.5L21 8l-9 4.5z" fill="{F}"/>'),
 "stacked-films": ('Stacked X-ray films (the Editor\'s film, with one behind)',
                   '<path d="M8 6.5V3h13v13h-3.5"/><rect x="3" y="7.5" width="14" height="14" rx="1.5"/><path d="M10 10v3.5"/>'
                   '<path d="M9 11.2c-2.2 0-3.4 3-3.4 6.3 0 .9.7 1.3 1.6.9L9 17.6zM11 11.2c2.2 0 3.4 3 3.4 6.3 0 .9-.7 1.3-1.6.9L11 17.6z" fill="{F}" stroke-width=".8"/>'),
 "skull":         ('A skull',
                   '<path d="M12 2.5c-5 0-8.5 3.5-8.5 8 0 2.8 1.3 4.5 3 5.5v3.5a1.5 1.5 0 0 0 1.5 1.5h8a1.5 1.5 0 0 0 1.5-1.5V16c1.7-1 3-2.7 3-5.5 0-4.5-3.5-8-8.5-8z'
                   'M8.6 9.3a2.2 2.2 0 1 0 .01 0z M15.4 9.3a2.2 2.2 0 1 0 .01 0z" fill="{F}" fill-rule="evenodd" stroke="none"/>'),
}


def dicom_options():
    out = os.path.join(OUT, "dicom-options")
    os.makedirs(out, exist_ok=True)
    rows = []
    for key, (desc, body) in DICOM_OPTIONS.items():
        write(os.path.join(out, f"{key}.svg"), mark_svg("Carino DICOM", body))
        g = glyph_svg("Carino DICOM", body)
        write(os.path.join(out, f"{key}-glyph.svg"), g)
        rows.append(sheet_row(f"<b>{key}</b><br>{esc(desc)}", f"{key}.svg", g))
    rows.append(sheet_row("<b>dcm</b><br>the Editor, for reference", "../dcm.svg", None))
    write(os.path.join(out, "sheet.html"), sheet("DICOM options", rows))
    return len(DICOM_OPTIONS)


if __name__ == "__main__":
    import subprocess, shutil
    raster = shutil.which("rsvg-convert") and shutil.which("magick")
    rows = []
    for stem, label in MARKS:
        body = P.get(stem)
        path = os.path.join(OUT, f"{stem}.svg")
        write(path, mark_svg(label, body))
        g = color = None
        if body is not None:
            g = glyph_svg(label, body)
            write(os.path.join(OUT, f"{stem}-glyph.svg"), g)
            color = f"{stem}-color.svg"
            write(os.path.join(OUT, color), color_svg(label, stem, body))
        rows.append(sheet_row(stem, f"{stem}.svg", g, color))
        if not raster:
            continue
        # 50x50 lossless webp: the size and format the fleet's favicons already use.
        png = os.path.join(OUT, f"{stem}-50.png")
        subprocess.run(["rsvg-convert", "-w", "50", "-h", "50", path, "-o", png], check=True)
        subprocess.run(["magick", png, "-define", "webp:lossless=true",
                        os.path.join(OUT, f"{stem}.webp")], check=True)
        os.remove(png)
    write(os.path.join(OUT, "sheet.html"), sheet("Carino marks", rows))
    n = dicom_options()
    print(f"{len(MARKS)} marks written to {OUT}, {n} DICOM options"
          + ("" if raster else "  (svg only: no rsvg-convert/magick)"))
