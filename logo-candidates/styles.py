"""Carino C, four ways: oekaki, Japanese, cyberpunk, corpo — and the crosses.

Everything is generated from the same C skeleton (44 deg to 316 deg, mouth on
the right) so the marks are comparable rather than twenty unrelated drawings.
Randomness is seeded: the same seed always draws the same wobble, or the mark
is not a mark.
"""
import math, os, subprocess

OUT = os.path.dirname(os.path.abspath(__file__))
GOLD = "#eab308"
GOLD_LT = "#fde047"
GOLD_DK = "#b45309"
INK = "#0a0a0a"
VERMILION = "#c1272d"
CYAN = "#22d3ee"
MAGENTA = "#e935c1"

CX = CY = 50.0
R, W = 34.0, 16.0
A0, A1 = 44.0, 316.0          # start / end of the arc, degrees, CCW


def polar(deg, rad):
    return (CX + rad * math.cos(math.radians(deg)), CY - rad * math.sin(math.radians(deg)))


def wob(t, seed, n=3):
    """Smooth deterministic wobble in roughly [-1, 1]."""
    v = 0.0
    for k in range(1, n + 1):
        ph = (seed * 7.31 + k * 2.17) % (2 * math.pi)
        v += math.sin(2 * math.pi * k * t * 1.3 + ph) / k
    return v / sum(1.0 / k for k in range(1, n + 1))


def brush(seed=1.0, width=W, radius=R, a0=A0, a1=A1, samples=120,
          wob_r=0.0, wob_w=0.0, taper=0.0, taper_end=None, tilt=0.0):
    """A stroked C as a filled outline, so the width can vary along it."""
    taper_end = taper if taper_end is None else taper_end
    outer, inner = [], []
    for i in range(samples):
        t = i / (samples - 1)
        a = a0 + (a1 - a0) * t
        rc = radius + wob_r * wob(t, seed)
        # pressure: thin at the entry, full through the belly, thin at the exit
        head = min(1.0, t / 0.22) if taper else 1.0
        tail = min(1.0, (1 - t) / 0.22) if taper_end else 1.0
        p = 1.0 - taper * (1 - head) - taper_end * (1 - tail)
        w = width * p * (1 + wob_w * wob(t, seed + 3.3))
        w *= 1 + tilt * math.cos(math.radians(a) - math.pi / 4)
        outer.append(polar(a, rc + w / 2))
        inner.append(polar(a, rc - w / 2))
    pts = outer + inner[::-1]
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"
    return d


def arc_stroke(width=W, radius=R, a0=A0, a1=A1, colour=GOLD, cap="butt", extra=""):
    x1, y1 = polar(a0, radius)
    x2, y2 = polar(a1, radius)
    large = 1 if abs(a1 - a0) > 180 else 0
    return (f'<path d="M {x1:.2f} {y1:.2f} A {radius} {radius} 0 {large} 0 {x2:.2f} {y2:.2f}" '
            f'fill="none" stroke="{colour}" stroke-width="{width}" stroke-linecap="{cap}" {extra}/>')


# =====================================================================
# A. OEKAKI  — the browser-doodle lineage the current mark already sits in
# =====================================================================
def m_oekaki_brush(ns):
    """Drawn with a mouse, which is the whole charm of the form."""
    d = brush(seed=2.4, wob_r=3.4, wob_w=0.4, taper=0.6, taper_end=0.8, samples=64)
    return f'<path d="{d}" fill="{GOLD}"/>'


def m_oekaki_sticker(ns):
    """Die-cut sticker: the doodle with a keyline holding it off the ground."""
    d = brush(seed=8.3, wob_r=2.8, wob_w=0.3, taper=0.5, taper_end=0.7, samples=64)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="11" '
            f'stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#f5f1e6" stroke-width="6.5" '
            f'stroke-linejoin="round"/><path d="{d}" fill="{GOLD}"/>')


def m_oekaki_fill(ns):
    """Flat colour laid down slightly off the ink line, the way a paint-bucket
    fill misses in a 200x200 oekaki canvas."""
    d = brush(seed=5.1, wob_r=1.4, wob_w=0.12, taper=0.4, taper_end=0.6)
    return (f'<g transform="translate(3.2 2.4)"><path d="{d}" fill="{GOLD_DK}" opacity=".85"/></g>'
            f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-width="2.4"/>')


def m_oekaki_glasses(ns):
    """The current logo's one memorable feature, kept: the C wears the glasses."""
    d = brush(seed=1.7, wob_r=1.3, wob_w=0.14, taper=0.45, taper_end=0.6)
    g = (f'<g fill="none" stroke="{GOLD}" stroke-width="3">'
         f'<circle cx="44" cy="50" r="9.5"/><circle cx="69" cy="50" r="9.5"/>'
         f'<path d="M53.5 50 h6"/></g>')
    return f'<path d="{d}" fill="{GOLD}" opacity=".95"/>{g}'


# =====================================================================
# B. JAPANESE
# =====================================================================
def _seal_mask(ns, shape, dcut):
    return (f'<mask id="{ns}m"><rect width="100" height="100" fill="#000"/>'
            f'{shape}<path d="{dcut}" fill="#000"/></mask>')


def m_hanko(ns):
    """Tenkoku seal: the character is carved out of a filled field, and the
    strokes run to the frame the way a carved seal's do."""
    d = brush(seed=9.2, wob_r=0.9, wob_w=0.08, radius=32, width=14)
    tile = '<rect x="6" y="6" width="88" height="88" rx="10" fill="#fff"/>'
    return (_seal_mask(ns, tile, d) +
            f'<rect x="6" y="6" width="88" height="88" rx="10" fill="{VERMILION}" '
            f'mask="url(#{ns}m)"/>')


def m_hanko_gold(ns):
    d = brush(seed=9.2, wob_r=0.9, wob_w=0.08, radius=32, width=14)
    tile = '<rect x="5" y="5" width="90" height="90" rx="12" fill="#fff"/>'
    return (_seal_mask(ns, tile, d) +
            f'<rect x="5" y="5" width="90" height="90" rx="12" fill="{GOLD}" '
            f'mask="url(#{ns}m)"/>')


def _kasure(ns, seeds=((0, 120, 200, 4.5), (7, 60, 175, 3.2), (3, 210, 300, 3.8),
                       (11, 150, 250, 2.6), (5, 250, 320, 3.4))):
    """Dry-brush streaks: gaps torn along the stroke where the bristles ran out.
    Cut with a mask so they take the ground with them rather than painting over."""
    st = "".join(
        f'<path d="{brush(seed=20 + s, wob_r=1.1, wob_w=0.5, a0=a, a1=b, width=w, radius=R + o)}" '
        f'fill="#000"/>'
        for (s, a, b, w), o in zip(seeds, (3.5, -4.0, 1.0, -1.5, 5.0)))
    return f'<mask id="{ns}k"><rect width="100" height="100" fill="#fff"/>{st}</mask>'


def m_enso(ns):
    """Enso: the open circle drawn in one breath. It is already a C."""
    d = brush(seed=4.8, wob_r=2.6, wob_w=0.34, taper=0.8, taper_end=0.92,
              a0=34, a1=332, width=19)
    return _kasure(ns) + f'<path d="{d}" fill="{GOLD}" mask="url(#{ns}k)"/>'


def m_kamon(ns):
    """Maru-ni: a crest is a geometric figure inside a thin ring."""
    return (f'<circle cx="50" cy="50" r="45" fill="none" stroke="{GOLD}" stroke-width="4"/>'
            + arc_stroke(width=12, radius=26) +
            f'<rect x="43" y="43" width="14" height="14" rx="1" fill="{GOLD}"/>')


def m_sumi(ns):
    """One stroke, full pressure to dry exit."""
    d = brush(seed=6.6, wob_r=1.8, wob_w=0.22, taper=0.15, taper_end=0.95, width=19)
    return f'<path d="{d}" fill="{GOLD}"/>'


# =====================================================================
# C. CYBERPUNK
# =====================================================================
def m_neon(ns):
    glow = (f'<filter id="{ns}g" x="-60%" y="-60%" width="220%" height="220%">'
            f'<feGaussianBlur stdDeviation="4.5" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="b"/>'
            f'<feMergeNode in="SourceGraphic"/></feMerge></filter>')
    return (glow + f'<g filter="url(#{ns}g)">' + arc_stroke(width=13, colour=GOLD) + "</g>"
            + arc_stroke(width=4.5, colour="#fffbe6"))


def m_glitch(ns):
    """Chroma split and a sliced offset — the C mid-frame-tear."""
    body = arc_stroke(width=W)
    return (f'<g opacity=".55" transform="translate(-3 1.5)">'
            + arc_stroke(width=W, colour=CYAN) + "</g>"
            f'<g opacity=".55" transform="translate(3 -1.5)">'
            + arc_stroke(width=W, colour=MAGENTA) + "</g>"
            f'<mask id="{ns}s"><rect width="100" height="100" fill="#fff"/>'
            f'<rect y="38" width="100" height="7" fill="#000"/>'
            f'<rect y="62" width="100" height="4" fill="#000"/></mask>'
            f'<g mask="url(#{ns}s)">{body}</g>'
            f'<g transform="translate(7 0)"><mask id="{ns}s2">'
            f'<rect y="38" width="100" height="7" fill="#fff"/></mask>'
            f'<g mask="url(#{ns}s2)">{body}</g></g>')


def m_crt(ns):
    """Amber phosphor: the C as it would come up on the console it runs on."""
    lines = "".join(f'<rect y="{y}" width="100" height="2.4" fill="#000"/>'
                    for y in range(4, 100, 7))
    glow = (f'<filter id="{ns}g" x="-50%" y="-50%" width="200%" height="200%">'
            f'<feGaussianBlur stdDeviation="3"/></filter>')
    return (glow + f'<mask id="{ns}sl"><rect width="100" height="100" fill="#fff"/>{lines}</mask>'
            f'<g filter="url(#{ns}g)" opacity=".5">' + arc_stroke(width=W) + "</g>"
            f'<g mask="url(#{ns}sl)">' + arc_stroke(width=W) +
            f'<rect x="41.5" y="41.5" width="17" height="17" rx="1" fill="{GOLD}"/></g>')


def m_hud(ns):
    """Chamfered terminals, registration ticks, one data block."""
    ticks = "".join(
        f'<rect x="48.6" y="1.5" width="2.8" height="7" fill="{GOLD}" opacity=".75" '
        f'transform="rotate({a} 50 50)"/>' for a in (0, 90, 180, 270))
    return (ticks + arc_stroke(width=W) +
            f'<path d="M62 41.5 h13 l4 4 v9 l-4 4 h-13 z" fill="{GOLD}"/>')


# =====================================================================
# D. CORPO
# =====================================================================
def m_squircle(ns):
    d = brush(radius=26, width=13)
    tile = '<rect x="2" y="2" width="96" height="96" rx="22" fill="#fff"/>'
    return (_seal_mask(ns, tile, d) +
            f'<rect x="2" y="2" width="96" height="96" rx="22" fill="{GOLD}" '
            f'mask="url(#{ns}m)"/>')


def m_gradient(ns):
    grad = (f'<linearGradient id="{ns}g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{GOLD_LT}"/><stop offset=".5" stop-color="{GOLD}"/>'
            f'<stop offset="1" stop-color="{GOLD_DK}"/></linearGradient>')
    return (grad + arc_stroke(width=W, colour=f"url(#{ns}g)") +
            f'<rect x="41.5" y="41.5" width="17" height="17" rx="2.5" fill="url(#{ns}g)"/>')


def m_bevel(ns):
    """Chrome: a lit edge and a shadowed one, the enterprise-logo trick."""
    grad = (f'<linearGradient id="{ns}g" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#fff3b0"/><stop offset=".45" stop-color="{GOLD}"/>'
            f'<stop offset="1" stop-color="#7c3d06"/></linearGradient>')
    return (grad + arc_stroke(width=W + 2.5, colour="#5c2d04") +
            arc_stroke(width=W, colour=f"url(#{ns}g)") +
            arc_stroke(width=3, radius=R + 5.2, colour="#fff8d0", extra='opacity=".55"') +
            f'<rect x="41.5" y="41.5" width="17" height="17" rx="2.5" fill="url(#{ns}g)" '
            f'stroke="#5c2d04" stroke-width="1.5"/>')


def m_corpo_mono(ns):
    """Built on the grid it will be rebuilt on: eight units, no curves left free."""
    n = 11
    cells = "".join(
        f'<rect x="{polar(A0 + (A1 - A0) * i / (n - 1), 32)[0] - 7.5:.2f}" '
        f'y="{polar(A0 + (A1 - A0) * i / (n - 1), 32)[1] - 7.5:.2f}" '
        f'width="15" height="15" rx="3" fill="{GOLD}"/>' for i in range(n))
    return cells + f'<rect x="42.5" y="42.5" width="15" height="15" rx="3" fill="{GOLD}"/>'


def m_thin(ns):
    """Restraint: hairline geometry, wide counter, the square doing the work."""
    return (arc_stroke(width=7, radius=38) +
            f'<rect x="42" y="42" width="16" height="16" rx="2" fill="{GOLD}"/>')


# =====================================================================
# E. CROSSES
# =====================================================================
def m_hanko_corpo(ns):
    """Seal discipline, drawn on the grid instead of by hand."""
    d = (f"M {polar(44, 40)[0]:.2f} {polar(44, 40)[1]:.2f} "
         f"A 40 40 0 1 0 {polar(316, 40)[0]:.2f} {polar(316, 40)[1]:.2f} "
         f"L {polar(316, 22)[0]:.2f} {polar(316, 22)[1]:.2f} "
         f"A 22 22 0 1 1 {polar(44, 22)[0]:.2f} {polar(44, 22)[1]:.2f} Z")
    tile = '<rect x="4" y="4" width="92" height="92" rx="16" fill="#fff"/>'
    return (f'<mask id="{ns}m"><rect width="100" height="100" fill="#000"/>{tile}'
            f'<path d="{d}" fill="#000"/>'
            f'<rect x="43" y="43" width="14" height="14" rx="2" fill="#000"/></mask>'
            f'<rect x="4" y="4" width="92" height="92" rx="16" fill="{GOLD}" '
            f'mask="url(#{ns}m)"/>')


def m_neon_hanko(ns):
    d = brush(seed=9.2, wob_r=0.9, radius=32, width=14)
    glow = (f'<filter id="{ns}g" x="-60%" y="-60%" width="220%" height="220%">'
            f'<feGaussianBlur stdDeviation="3.5" result="b"/><feMerge>'
            f'<feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    return (glow + f'<g filter="url(#{ns}g)">'
            f'<rect x="6" y="6" width="88" height="88" rx="10" fill="none" '
            f'stroke="{MAGENTA}" stroke-width="3"/>'
            f'<path d="{d}" fill="{CYAN}" opacity=".9"/></g>'
            f'<path d="{d}" fill="#e8fbff"/>')


def m_oekaki_neon(ns):
    d = brush(seed=2.4, wob_r=1.6, wob_w=0.18, taper=0.5, taper_end=0.7)
    glow = (f'<filter id="{ns}g" x="-60%" y="-60%" width="220%" height="220%">'
            f'<feGaussianBlur stdDeviation="4" result="b"/><feMerge>'
            f'<feMergeNode in="b"/><feMergeNode in="b"/>'
            f'<feMergeNode in="SourceGraphic"/></feMerge></filter>')
    return (glow + f'<g filter="url(#{ns}g)"><path d="{d}" fill="{GOLD}"/></g>'
            f'<path d="{d}" fill="none" stroke="#fffbe6" stroke-width="1.8"/>')


def m_enso_corpo(ns):
    """The enso's asymmetry, redrawn with no wobble at all — the gesture kept,
    the hand removed."""
    d = brush(seed=0, wob_r=0, wob_w=0, taper=0.45, taper_end=0.8, a0=40, a1=326, width=18)
    return f'<path d="{d}" fill="{GOLD}"/>'


def m_kamon_corpo(ns):
    return (f'<mask id="{ns}m"><circle cx="50" cy="50" r="46" fill="#fff"/>'
            + arc_stroke(width=15, radius=27, colour="#000") +
            f'<rect x="43.5" y="43.5" width="13" height="13" rx="1.5" fill="#000"/></mask>'
            f'<circle cx="50" cy="50" r="46" fill="{GOLD}" mask="url(#{ns}m)"/>')


def m_maru_ni(ns):
    """Maru-ni proper: the crest sits inside a double ring, and the inner figure
    never touches it."""
    return (f'<circle cx="50" cy="50" r="47" fill="none" stroke="{GOLD}" stroke-width="3.5"/>'
            f'<circle cx="50" cy="50" r="41" fill="none" stroke="{GOLD}" stroke-width="2"/>'
            + arc_stroke(width=11, radius=24) +
            f'<circle cx="50" cy="50" r="5.5" fill="{GOLD}"/>')


def m_hanko_kana(ns):
    """A seal carries the name, not an initial. Katakana runs beside the C the
    way a two-column tenkoku seal reads: top to bottom, right to left."""
    d = brush(seed=9.2, wob_r=1.0, wob_w=0.1, radius=26, width=13)
    tile = '<rect x="5" y="5" width="90" height="90" rx="9" fill="#fff"/>'
    kana = (f'<text x="76" y="50" font-family="Noto Sans CJK JP" font-size="20" '
            f'font-weight="700" fill="#000" text-anchor="middle" '
            f'writing-mode="tb">カリノ</text>')
    return (f'<mask id="{ns}m"><rect width="100" height="100" fill="#000"/>{tile}'
            f'<g transform="translate(36 50) scale(0.78) translate(-50 -50)">'
            f'<path d="{d}" fill="#000"/></g>{kana}</mask>'
            f'<rect x="5" y="5" width="90" height="90" rx="9" fill="{VERMILION}" '
            f'mask="url(#{ns}m)"/>')


def m_cyber_kana(ns):
    """Neon signage: the mark, and the name in the local alphabet under it."""
    glow = (f'<filter id="{ns}g" x="-60%" y="-60%" width="220%" height="220%">'
            f'<feGaussianBlur stdDeviation="3.2" result="b"/><feMerge>'
            f'<feMergeNode in="b"/><feMergeNode in="b"/>'
            f'<feMergeNode in="SourceGraphic"/></feMerge></filter>')
    return (glow + f'<g filter="url(#{ns}g)">'
            + arc_stroke(width=12, radius=29, colour=GOLD) +
            f'<text x="50" y="94" font-family="Noto Sans CJK JP" font-size="15" '
            f'font-weight="700" fill="{CYAN}" text-anchor="middle">'
            f'カリノ</text></g>'
            + arc_stroke(width=4, radius=29, colour="#fffbe6"))


def m_sumi_square(ns):
    """Brush C, brush square — the detail drawn by the same hand."""
    d = brush(seed=6.6, wob_r=1.9, wob_w=0.25, taper=0.2, taper_end=0.9, width=18)
    sq = ('M 42.5 41.8 L 58.6 42.6 L 57.9 58.4 L 41.9 57.6 Z')
    return f'<path d="{d}" fill="{GOLD}"/><path d="{sq}" fill="{GOLD}"/>'


def m_crt_tile(ns):
    """Console glass in an app tile: scanlines, but disciplined."""
    lines = "".join(f'<rect y="{y}" width="100" height="2" fill="#000" opacity=".55"/>'
                    for y in range(6, 100, 6))
    d = brush(radius=26, width=13)
    tile = '<rect x="2" y="2" width="96" height="96" rx="22" fill="#fff"/>'
    return (f'<mask id="{ns}m"><rect width="100" height="100" fill="#000"/>{tile}'
            f'<path d="{d}" fill="#000"/></mask>'
            f'<g mask="url(#{ns}m)"><rect x="2" y="2" width="96" height="96" rx="22" '
            f'fill="{GOLD}"/>{lines}</g>')


def m_enso_neon(ns):
    d = brush(seed=4.8, wob_r=2.6, wob_w=0.34, taper=0.8, taper_end=0.92,
              a0=34, a1=332, width=16)
    glow = (f'<filter id="{ns}g" x="-60%" y="-60%" width="220%" height="220%">'
            f'<feGaussianBlur stdDeviation="4" result="b"/><feMerge>'
            f'<feMergeNode in="b"/><feMergeNode in="b"/>'
            f'<feMergeNode in="SourceGraphic"/></feMerge></filter>')
    return (glow + _kasure(ns) + f'<g filter="url(#{ns}g)" mask="url(#{ns}k)">'
            f'<path d="{d}" fill="{GOLD}"/></g>')


FAMILIES = [
    ("Oekaki", [
        ("oekaki-brush", "Inked", m_oekaki_brush),
        ("oekaki-fill", "Off-register fill", m_oekaki_fill),
        ("oekaki-glasses", "The C wears the glasses", m_oekaki_glasses),
        ("oekaki-sticker", "Die-cut sticker", m_oekaki_sticker),
    ]),
    ("Japanese", [
        ("hanko", "Hanko, vermilion", m_hanko),
        ("hanko-gold", "Hanko, gold", m_hanko_gold),
        ("hanko-kana", "Seal with the name", m_hanko_kana),
        ("enso", "Enso", m_enso),
        ("sumi", "One stroke", m_sumi),
        ("sumi-square", "Brush C, brush square", m_sumi_square),
        ("kamon", "Kamon", m_kamon),
        ("maru-ni", "Maru-ni, double ring", m_maru_ni),
    ]),
    ("Cyberpunk", [
        ("neon", "Neon", m_neon),
        ("glitch", "Frame tear", m_glitch),
        ("crt", "Amber phosphor", m_crt),
        ("hud", "HUD", m_hud),
        ("cyber-kana", "Neon signage", m_cyber_kana),
    ]),
    ("Corpo", [
        ("squircle", "App tile", m_squircle),
        ("gradient", "Gradient", m_gradient),
        ("bevel", "Chrome", m_bevel),
        ("thin", "Hairline", m_thin),
        ("corpo-mono", "Built on the grid", m_corpo_mono),
    ]),
    ("Crosses", [
        ("hanko-corpo", "Hanko x corpo", m_hanko_corpo),
        ("neon-hanko", "Hanko x cyberpunk", m_neon_hanko),
        ("oekaki-neon", "Oekaki x cyberpunk", m_oekaki_neon),
        ("enso-corpo", "Enso x corpo", m_enso_corpo),
        ("enso-neon", "Enso x cyberpunk", m_enso_neon),
        ("kamon-corpo", "Kamon x corpo", m_kamon_corpo),
        ("crt-tile", "Cyberpunk x corpo", m_crt_tile),
    ]),
]

ALL = [(slug, label, fn) for _, items in FAMILIES for slug, label, fn in items]


def svg(slug, fn, size=512):
    ns = slug.replace("-", "")
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
            f'width="{size}" height="{size}">' + fn(ns) + "</svg>")


if __name__ == "__main__":
    for slug, _, fn in ALL:
        p = os.path.join(OUT, f"s_{slug}.svg")
        with open(p, "w") as fh:
            fh.write(svg(slug, fn))
        for s in (16, 32, 512):
            subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), p,
                            "-o", os.path.join(OUT, f"s_{slug}_{s}.png")], check=True)
    print("rendered", len(ALL))
