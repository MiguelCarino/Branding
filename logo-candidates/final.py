"""The finished marks: bold C, one solid element, optically centred.

Geometry lives here so the mark is reproducible rather than a bitmap somebody
has to trace. Emits SVG (source of truth) plus the raster sizes the fleet
actually consumes: a 50x50 webp favicon and the desktop icon PNGs.
"""
import math, os, subprocess

GOLD = "#eab308"
OUT = os.path.dirname(os.path.abspath(__file__))
CX = CY = 50.0
R, SW, GAP = 34.0, 16.0, 44.0
RO, RI = R + SW / 2, R - SW / 2          # 42 / 26


def pt(deg, rad=R):
    return (CX + rad * math.cos(math.radians(deg)), CY - rad * math.sin(math.radians(deg)))


def shell(gap=GAP):
    x1, y1 = pt(gap, R)
    x2, y2 = pt(-gap, R)
    return (f'<path d="M {x1:.2f} {y1:.2f} A {R} {R} 0 1 0 {x2:.2f} {y2:.2f}" '
            f'fill="none" stroke="{GOLD}" stroke-width="{SW}" stroke-linecap="butt"/>')


SQ = 17.0
SQ_MOUTH_X = 60.0


def body_mouth():
    return shell() + (f'<rect x="{SQ_MOUTH_X}" y="{50 - SQ/2}" width="{SQ}" height="{SQ}" '
                      f'rx="2.5" fill="{GOLD}"/>')


def body_centre():
    return shell() + (f'<rect x="{50 - SQ/2}" y="{50 - SQ/2}" width="{SQ}" height="{SQ}" '
                      f'rx="2.5" fill="{GOLD}"/>')


def body_plain():
    return shell()


# Optical centring: the C's rightmost ink is the outer corner of a terminal,
# not the ring's full width, so the raw drawing sits left of centre. Each mark
# gets fitted to its own bounding box with equal padding.
def bbox(name):
    term_x = CX + RO * math.cos(math.radians(GAP))          # 80.2
    right = {"mouth": max(term_x, SQ_MOUTH_X + SQ),
             "centre": term_x, "plain": term_x}[name]
    return (CX - RO, CY - RO, right, CY + RO)               # l, t, r, b


def fitted(name, body, pad=7.0):
    l, t, r, b = bbox(name)
    w, h = r - l, b - t
    s = (100 - 2 * pad) / max(w, h)
    tx = pad + (100 - 2 * pad - w * s) / 2 - l * s
    ty = pad + (100 - 2 * pad - h * s) / 2 - t * s
    return f'<g transform="translate({tx:.3f} {ty:.3f}) scale({s:.4f})">{body}</g>'


MARKS = {"mouth": body_mouth, "centre": body_centre, "plain": body_plain}


def svg(name):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
            'width="512" height="512" role="img" aria-label="Carino">'
            + fitted(name, MARKS[name]()) + "</svg>")


if __name__ == "__main__":
    for name in MARKS:
        p = os.path.join(OUT, f"f_{name}.svg")
        with open(p, "w") as fh:
            fh.write(svg(name))
        for s in (16, 24, 32, 48, 50, 64, 128, 256, 512):
            subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), p,
                            "-o", os.path.join(OUT, f"f_{name}_{s}.png")], check=True)
        subprocess.run(["magick", os.path.join(OUT, f"f_{name}_50.png"),
                        "-define", "webp:lossless=true",
                        os.path.join(OUT, f"f_{name}.webp")], check=True)
    print("ok")
