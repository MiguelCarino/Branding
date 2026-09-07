"""The Carino marks: a gold C with one character set beside it.

Geometry is inherited, not invented. The bare C and the lettered C both already
exist in the fleet -- Carino-Systems/logo.svg and DICOM-editor/logo.svg -- and
the numbers below are read back off those files:

    bare C      centre (56.03, 50)  r 34.81  stroke 16.38
    lettered C  centre (38.35, 50)  r 25.38  stroke 11.94   (everything x 0.729)
    glyph box   x 69.71..93.00, y 30.59..69.41

That box is 23.29 x 38.82, and decoding dcm's E and Topo's T shows both are
drawn on a 7.76 module -- 3 columns by 5 rows. Three columns is too coarse to
keep letters apart: on it, A, K and M each sit ONE cell from H. So the grid
here is the HALF module, 3.88 -- 6 columns by 10 rows. Stems stay two modules
(7.76), so E and T come out byte-identical to the files already shipping, while
A gets a real apex, K real arms and V a real taper.

Not type: Red Hat Display 900, the fleet's own display face, has a stem/cap
ratio of 77/700 = 0.11, where this glyph is 7.76/38.82 = 0.20 and the C's arc
is 11.94/62.7 = 0.19. A typeset letter reads weedy beside the ring. The blocky
letter is a weight, not a pixel affectation.

Diagonals are stepped rather than drawn: at 32px a stepped module stays crisp
where a hairline diagonal turns to porridge.

Every filled cell is emitted as a rect subpath inside ONE <path>. Cells sharing
an edge are then unioned by the scanline filler instead of each antialiasing
against its neighbour, so the glyph has no internal seams.
"""
import os

GOLD = "#eab308"
OUT = os.path.dirname(os.path.abspath(__file__))

BARE_C = ('<path d="M 81.07 25.82 A 34.81 34.81 0 1 0 81.07 74.18" fill="none" '
          f'stroke="{GOLD}" stroke-width="16.38" stroke-linecap="butt"/>')
SMALL_C = ('<path d="M 56.61 32.37 A 25.38 25.38 0 1 0 56.61 67.63" fill="none" '
           f'stroke="{GOLD}" stroke-width="11.94" stroke-linecap="butt"/>')

# Half module, 6 columns by 10 rows. The edges are interpolated across the box
# rather than stepped by a rounded cell: 3.88 x 6 is 23.28, which would leave
# the grid 0.01 short of the right edge. Interpolated, the boundaries round to
# 77.47 / 85.24 / 38.35 / 46.12 / 53.88 / 61.65 -- the exact numbers in the E
# and T already shipping.
X0, X1, Y0, Y1, COLS, ROWS = 69.71, 93.00, 30.59, 69.41, 6, 10

# The two marks already in the fleet keep their original path verbatim, so this
# script cannot quietly redraw a logo that is already shipping.
BUILT = {
    "E": ('<path d="M 69.71 30.59 H 93.00 V 38.35 H 77.47 V 46.12 H 93.00 V 53.88 '
          'H 77.47 V 61.65 H 93.00 V 69.41 H 69.71 Z" fill="%s"/>' % GOLD),
    "T": ('<path d="M 69.71 30.59 H 93.00 V 38.35 H 85.24 V 69.41 H 77.47 V 38.35 '
          'H 69.71 Z" fill="%s"/>' % GOLD),
}

def cells(bitmap):
    """10 strings of 6 chars, '#' filled -> one path of rect subpaths."""
    rows = [r for r in bitmap.strip().splitlines()]
    assert len(rows) == ROWS and all(len(r) == COLS for r in rows), bitmap
    d = []
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != "#":
                continue
            x0 = X0 + (X1 - X0) * c / COLS
            x1 = X0 + (X1 - X0) * (c + 1) / COLS
            y0 = Y0 + (Y1 - Y0) * r / ROWS
            y1 = Y0 + (Y1 - Y0) * (r + 1) / ROWS
            d.append(f"M {x0:.2f} {y0:.2f} H {x1:.2f} V {y1:.2f} H {x0:.2f} Z")
    return f'<path d="{" ".join(d)}" fill="{GOLD}"/>'

def svg(label, glyph_svg):
    body = (BARE_C if glyph_svg is None else SMALL_C + glyph_svg)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
            f'width="512" height="512" role="img" aria-label="{label}">{body}</svg>')


# ---- the characters ---------------------------------------------------------
# Read each as five rows of three cells. Letters first, then the symbols the
# repeating initials gave way to.
GLYPHS = {
 # ---- letters: 6 columns x 10 rows, stems two modules wide ----------------
 "A": "..##../..##../.#..#./.#..#./##..##/######/######/##..##/##..##/##..##",
 "B": "#####./##..##/##..##/##..##/#####./#####./##..##/##..##/##..##/#####.",
 "D": "#####./##..##/##..##/##..##/##..##/##..##/##..##/##..##/##..##/#####.",
 "F": "######/######/##..../##..../#####./#####./##..../##..../##..../##....",
 "H": "##..##/##..##/##..##/##..##/######/######/##..##/##..##/##..##/##..##",
 "I": "######/######/..##../..##../..##../..##../..##../..##../######/######",
 "K": "##..##/##..##/##.##./##.##./####../####../##.##./##.##./##..##/##..##",
 "L": "##..../##..../##..../##..../##..../##..../##..../##..../######/######",
 "play":    "##..../###.../####../#####./######/######/#####./####../###.../##....",
 "N": "##..##/##..##/###.##/###.##/###.##/##.###/##.###/##.###/##..##/##..##",
 "O": "######/######/##..##/##..##/##..##/##..##/##..##/##..##/######/######",
 "P": "######/######/##..##/##..##/######/######/##..../##..../##..../##....",
 "Q": "######/######/##..##/##..##/##..##/##..##/######/######/....##/....##",
 "R": "######/######/##..##/##..##/######/######/##.##./##.##./##..##/##..##",
 "S": "######/######/##..../##..../######/######/....##/....##/######/######",
 "V": "##..##/##..##/##..##/##..##/##..##/##..##/.#..#./.#..#./..##../..##..",
 # ---- the symbols the repeating initials gave way to ----------------------
 "dotdash":  "....../....../##..../##..../....../....../######/######/....../......",
 "star":     "##..##/.#..#./..##../..##../######/######/..##../..##../.#..#./##..##",
 "percent":  "##..##/##..##/##.##./...##./..##../..##../.##.../.##.##/##..##/##..##",
 "bang":     "..##../..##../..##../..##../..##../..##../..##../....../..##../..##..",
 "Y": "##..##/##..##/##..##/.####./.####./..##../..##../..##../..##../..##..",
 "quote":    "##.##./##.##./##.##./##.##./.#..#./....../....../....../....../......",
 "query":    ".####./######/##..##/....##/...##./..##../..##../....../..##../..##..",
 "tick":     "....../....##/....##/...##./...##./##.##./##.##./.####./..##../......",
 "hash":     "##.##./##.##./######/######/##.##./##.##./######/######/##.##./##.##.",
 "court":    "..##../.####./######/######/##..##/##..##/##..##/##..##/##..##/##..##",
 "bars":     "######/######/....../....../######/######/....../....../######/######",
 "tiles":    "##..##/##..##/##..##/##..##/....../....../##..##/##..##/##..##/##..##",
 "note":     "....##/....##/....##/....##/....##/....##/######/######/####../####..",
 "prompt":   "....../##..../.##.../..##../..##../.##.../##..../....../..####/..####",
 "rise":     "....##/....##/..####/..####/..####/######/######/######/######/######",
 "into":     "....##/....##/..####/..####/######/######/..####/..####/....##/....##",
 "up":       "..##../.####./######/..##../..##../..##../..##../..##../..##../..##..",
 "colon":    "....../..##../..##../....../....../....../....../..##../..##../......",
 "screen":   "######/######/##..##/##..##/##..##/######/######/..##../######/######",
}

# The two shipped marks re-expressed on the half module, for the collision check.
BUILT_BITS = {
 "E": "######/######/##..../##..../######/######/##..../##..../######/######",
 "T": "######/######/..##../..##../..##../..##../..##../..##../..##../..##..",
}

# ---- the fleet --------------------------------------------------------------
# (file stem, aria label, character key or None for the hub's bare C)
MARKS = [
 ("carino",       "Carino",                None),
 ("aldis",        "Carino Aldis Lamp",     "dotdash"),
 ("asobi",        "Carino Asobi",          "A"),
 ("branding",     "Carino Branding",       "B"),
 ("compass",      "Carino Compass",        "star"),
 ("currency",     "Carino Currency",       "percent"),
 ("cve",          "Carino CVE",            "bang"),
 ("cybercity",    "Carino CyberCity",      "Y"),
 ("dcm",          "Carino Editor",         "E"),
 ("desk",         "Carino Desk",           "quote"),
 ("dicom",        "Carino DICOM",          "D"),
 ("distro",       "Carino Distro",         "query"),
 ("fiscal",       "Carino Fiscal",         "tick"),
 ("font",         "Carino Fonts",          "F"),
 ("hardware",     "Carino Hardware",       "H"),
 ("hash",         "Carino Hash",           "hash"),
 ("images",       "Carino Images",         "I"),
 ("kanban",       "Carino Kanban",         "K"),
 ("law",          "Carino Law",            "court"),
 ("learn",        "Carino Learn",          "L"),
 ("media",        "Carino Media",          "play"),
 ("metadata",     "Carino Metadata",       "bars"),
 ("multiweb",     "Carino MultiWeb",       "tiles"),
 ("music",        "Carino Music",          "note"),
 ("netplan",      "Carino Netplan",        "N"),
 ("offline",      "Carino Offline",        "O"),
 ("password",     "Carino Password",       "P"),
 ("quote",        "Carino Quote",          "Q"),
 ("retina",       "Carino Retina",         "R"),
 ("setup",        "Carino Setup",          "prompt"),
 ("software",     "Carino Software",       "S"),
 ("stocks",       "Carino Stocks",         "rise"),
 ("subs",         "Carino Sync Studio",    "into"),
 ("teleprompter", "Carino TelePrompter",   "up"),
 ("time",         "Carino Time",           "colon"),
 ("topo",         "Carino Topo",           "T"),
 ("tv",           "Carino TV",             "screen"),
 ("vitae",        "Carino Vitae",          "V"),
]


def glyph_svg(key):
    if key is None:
        return None
    if key in BUILT:
        return BUILT[key]
    return cells(GLYPHS[key].replace("/", "\n"))


if __name__ == "__main__":
    import subprocess, shutil
    raster = shutil.which("rsvg-convert") and shutil.which("magick")
    for stem, label, key in MARKS:
        path = os.path.join(OUT, f"{stem}.svg")
        with open(path, "w") as fh:
            fh.write(svg(label, glyph_svg(key)))
        if not raster:
            continue
        # 50x50 lossless webp: the size and format the fleet's favicons already use.
        png = os.path.join(OUT, f"{stem}-50.png")
        subprocess.run(["rsvg-convert", "-w", "50", "-h", "50", path, "-o", png], check=True)
        subprocess.run(["magick", png, "-define", "webp:lossless=true",
                        os.path.join(OUT, f"{stem}.webp")], check=True)
        os.remove(png)
    print(f"{len(MARKS)} marks written to {OUT}" + ("" if raster else "  (svg only: no rsvg-convert/magick)"))
