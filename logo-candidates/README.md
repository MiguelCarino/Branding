# Logo candidates

Working drawings for a replacement Carino mark. Nothing here is in use yet — the
fleet still ships the face in `../logo.webp`.

## Why a rethink

The mark's only jobs are the browser favicon and the desktop app icon, because the
navbar draws **Carino** as type rather than as an image. That makes 16px the real
constraint, and the current mark fails it twice: it is an unreadable smudge below
about 32px, and it is pure black, so it disappears against a dark tab strip.
Meanwhile `Carino-PACS/desktop/assets/make_icon.py` draws a completely different
mark — a gold aperture — so there are already two Carino logos in circulation.

## The two sets

`final.py` — the shortlist. A bold C with a 90° mouth and **at most one** solid
element, large enough to read alone and separated from the arc by real space.
Three variants: `centre` (square at the isocentre, recommended), `mouth` (square
in the opening) and `plain` (no detail). Optical centring is computed per variant,
since the C's rightmost ink is a terminal corner rather than the ring's full width.

`styles.py` — 29 marks across oekaki, Japanese, cyberpunk and corpo, plus the
crosses between them. All are generated from one C skeleton so the treatments are
comparable. The hand-drawn wobble is **seeded**: a re-run redraws the same marks
rather than new ones.

## Regenerating

Both scripts write their PNG and webp output beside themselves, so expect
untracked files after a run. Only the sources and the contact sheets are committed.

    python3 final.py      # 3 marks: svg, webp, and PNG at 16…512
    python3 styles.py     # 29 marks: svg, and PNG at 16/32/512

Needs `rsvg-convert`, plus `magick` for the webp and a CJK font for the two
katakana marks. The seal and crest marks are **knockouts** — the C is a hole, so
it takes the colour of whatever sits behind it.

## Contact sheets

- `sheet_final.png` — the three finalists, both grounds, 16/24/32px
- `sheet_styles2.png` — all 29 at full size
- `sheet_small.png` — all 29 at 32 and 16px, which is where most of them die

## Not done

Picking one; deciding whether it replaces the fleet file (one `logo.webp` is
byte-identical across ~25 repositories, so this is a fleet change, not an app one)
or only Carino PACS; and regenerating `icon.icns` and `icon.ico`, which need the
app-builder run documented in `make_icon.py`.
