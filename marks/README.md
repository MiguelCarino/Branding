# The Carino marks

One gold `C` with one character set beside it, for every site in the fleet.
38 of them: 36 tools in `tools.json`, plus CyberCity (live, still unregistered)
and the hub itself, which keeps the bare `C` and no character.

`marks.py` draws all of them. Run it and it rewrites every `.svg` and `.webp`
in this folder:

    python3 marks.py        # needs rsvg-convert and magick for the webp

`deploy.py` copies each mark to every path its site actually looks for one at,
and `verify.py` follows each site's own `<link rel=icon>` and asserts the bytes
at the end of it are that site's mark, all 37 distinct. Both are checked in
beside the marks so this is repeatable rather than a one-off.

    python3 deploy.py       # run from ~/Github
    python3 verify.py

**Deployed.** The old black `logo.webp` is gone from the fleet — zero files
matching it remain.

## The geometry is inherited, not invented

Read back off the two marks already shipping — `DICOM-editor/logo.svg` and
`Topo/logo.svg`:

| | |
|---|---|
| bare C | centre (56.03, 50), r 34.81, stroke 16.38 |
| lettered C | centre (38.35, 50), r 25.38, stroke 11.94 — everything x 0.729 |
| character box | x 69.71..93.00, y 30.59..69.41 |

`dcm.svg` and `topo.svg` come out **byte-identical** to the files in those
repos. The generator carries their original path strings verbatim so it cannot
quietly redraw a logo that is already in circulation.

## Six columns, ten rows

The box is 23.29 x 38.82. `E` and `T` are drawn on a 7.76 module — 3 columns by
5 rows — and three columns is too coarse to keep an alphabet apart: on that
grid **A, K and M each sit one cell from H**. So the grid here is the half
module, 3.88, giving 6 x 10. Stems stay two modules (7.76), which is why E and
T survive unchanged, while A gets a real apex, K real arms and V a real taper.

Closest pair in the finished set is 6 modules of 60 — B/D, D/O, F/P and H/N,
which are just ordinary alphabet relationships.

Every filled module is a rect subpath inside **one** `<path>`. Modules sharing
an edge are unioned by the scanline filler rather than each antialiasing
against its neighbour, so a glyph has no internal seams.

## Why not type

Red Hat Display 900, the fleet's own display face, has a stem-to-cap ratio of
77/700 = **0.11**. This glyph is 7.76/38.82 = **0.20**, and the C's own arc is
11.94/62.7 = **0.19**. A typeset letter reads weedy beside the ring. The blocky
letter is a weight, not a pixel affectation.

Diagonals are stepped rather than drawn: at 32px a stepped module stays crisp
where a hairline diagonal turns to porridge.

## Which character, and why

The character is the site's own initial wherever that initial is unclaimed.
Eighteen sites get one that way. The rest share an initial — four sites want C,
four want T, four want M, four want S — so all but one holder of each takes a
symbol instead. Where a symbol says more than the letter would, it wins
outright: `hash` gets `#`, `music` a note, `media` a play triangle.

Three characters are **not** the site's initial, each for a reason worth
keeping:

* **dcm — E**, for Editor. Already shipping. It is what keeps dcm off the
  D pile.
* **media — a play triangle, not M.** M cannot be drawn six columns wide: any
  ink in the two middle columns fills them completely, so the vee cannot narrow
  and it reads as a solid-topped Pi.
* **cybercity — Y**, not a symbol. Y is unused, drawable, and sits in
  CyberCity's own name.

## Known weak point

`law` is the weakest glyph in the set. The box is three stems wide, so any
pictogram needing two separated uprights reads as one mass with a slot cut in
it — the scales came out looking like a bolt and a house came out looking like
a battery. What survives is a pedimented portico with its feet open, which
reads as *an institution* rather than specifically as *law*. The section sign
`§` is the right symbol and was tried first: at this size it collapses into an
S, which is `software`'s letter.

## What deploying touched

82 files across 37 sites. Most took `<stem>.svg` as `logo.svg` and
`<stem>.webp` as `logo.webp`, but the map in `deploy.py` is built from a survey
of what each page actually references, not from that pattern, because several
sites do not follow it:

* **Carino-PACS** serves `dicom.carino.systems` out of `docs/`, and
  `docs/favicon.webp`, `docs/logo.webp` and `pacs/web/{logo,favicon}.webp` were
  all one file. The DICOM editor embedded at `pacs/web/editor/` keeps the
  editor's own E, not the PACS D.
* **Custom-Images** serves out of `docs/`; **MusicGrid** and **SoftwareCatalog**
  out of `assets/images/`.
* **CyberCity** declared no favicon at all — it got a `<link>` as well as files.
* **findmeadistro** pointed its favicon at `img/distromoe-inverted.png`, which
  is also a button graphic on the page, so the link was repointed rather than
  that file overwritten.
* **SimpleSetup** draws its hero mark inline on purpose (its own comment says
  why), so the bare C in the markup became the lettered one.
* **Fiscal** also ships a 180x180 `apple-touch-icon.png`, regenerated from
  `fiscal.svg`.

Three desktop apps generate their icons rather than copying them, from a
`make_icon.py` that draws with the standard library alone. Carino-PACS's drew
the bare C and now draws the D; Retina's drew a pupil inside the ring and now
draws the R; DICOM-editor's already drew its E and is untouched. All three
`write_svg()` outputs are **byte-identical to the copies here**, which is two
independent derivations landing on the same numbers.

`stocks` is the one mark with nowhere to go: a registry entry with no repo and
no CNAME.
