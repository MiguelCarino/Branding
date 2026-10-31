# The Carino marks

Every site in the fleet wears the hub's gold `C`. The hub keeps its bowl empty —
that is what makes it the parent — and every tool's bowl holds one pictogram of
the job it does: a key for Password, an eye for Retina, a clock for Time. 39 in
all: 38 tools plus the hub.

`marks.py` draws all of them. Run it and it rewrites, for every site:

| file | what it is |
|---|---|
| `<stem>.svg` | the **mark**: ring + pictogram, 100 x 100, gold on transparency |
| `<stem>.webp` | the mark at 50x50, lossless — the favicon every page links |
| `<stem>-glyph.svg` | the **glyph**: the pictogram alone, 24 grid, stroke 2, `currentColor` |

plus `sheet.html` (every mark at 128/64/32/16 and every glyph at 24/16, on dark
and light) and `dicom-options/`.

    python3 marks.py        # needs rsvg-convert and magick for the webp
    python3 deploy.py       # run from anywhere; paths are under ~/Github
    python3 verify.py

`deploy.py` copies each mark to every path its site actually looks for one at,
plus the hub's vendored `Carino-Systems/assets/marks/` and the profile site's
`MiguelCarino/assets/`, and re-renders Fiscal's 180px `apple-touch-icon.png`.
`verify.py` follows each site's own `<link rel=icon>` and asserts the bytes at
the end of it are that site's mark, all distinct.

## The geometry

| | |
|---|---|
| ring | centre (56.03, 50), r 34.81, stroke 16.38 — the hub's, unchanged |
| bowl | clear disc of radius 26.62 |
| pictogram | drawn on a 24 grid, scaled to 40 units, centred on the ring |
| stroke | 3 grid units in the mark, 2 in the glyph |

`carino.svg` comes out byte-identical to the first file that shipped. A
pictogram stays within 2..22 of its grid, so its farthest point is 23.6 from
the centre; with half a stroke (2.5) it clears the ring by ~0.5. The mark's
stroke is heavier than the glyph's because beside a 16.38 ring a 3.3 line
reads as a hairline.

## Drawing rules

* **As few parts as the idea allows** — most are two or three.
* **At least one solid shape in each.** Lines alone dissolve at 16px; a solid
  shape keeps a silhouette. Hash, Ping and Offline are the line-only exceptions,
  because a fingerprint, a pulse and a crossed-out cloud have no solid form.
* **Drawn here from primitives**, not copied from an icon set.
* **The mark is for a dock, a hero or a share card; the glyph for anything
  text-sized.** Under about 32px the pictogram inside the ring gets small and
  the ring carries the brand alone — the glyph is what reads in a list.

## Why it replaced the first set

The first marks set one blocky character beside a smaller C (on a 6 x 10 grid
of 3.88 modules). At 16px the character was 1.24 device px per module, so a
wall of forty marks read as forty copies of one logo, and a letter said nothing
about what the tool does. Those letters are in this folder's git history.

## Pictograms worth not re-deriving

* **dicom / dcm are a pair.** The Editor is one chest film (two solid lungs);
  Carino DICOM is a stack of the same film. Every candidate tried for DICOM —
  stack with a cross, CT scanner, bone, head slices, workstation, slice series,
  skull — is in `dicom-options/` with its own sheet. The CT scanner read as a
  goblet face-on and a `£` from the side; head slices read as a `0`; a skull
  says poison.
* **currency is a `$`.** A banknote and a coin stack were tried; the coin stack
  reads as a database cylinder.
* **cybercity has a spire.** Plain towers read as Stocks' bar chart.
* **teleprompter is lines with an `A`**, not an up arrow.

## Desktop apps

Carino-DICOM, DICOM-editor and Retina each have a `desktop/assets/make_icon.py`.
They no longer draw the mark: `deploy.py` puts the mark there as `logo.svg`,
and the script rasterises it (with `rsvg-convert`) into the window, tray and
`.icns`/`.ico`/Linux packaging icons. Rerun it in each repo after a deploy.
