# Carino Branding

The living reference for the **Carino** visual language — the shared navbar, the
gold-on-black palette, and every component pattern used across the workshop.
Hosted at **branding.carino.systems**.

Two files hold everything sites share:

- **`carino-ui.css`**: the design tokens, the base, and every production
  component. This is the source of truth for how a Carino page looks.
- **`carino-ui.js`**: the behaviour some components need (the workspace drawer
  and the `#module` slice router). Opt-in by markup; it does nothing on a page
  that uses neither.

`Carino-Systems/propagate.sh` copies both into every site that carries them, the
way it copies `carino-navbar.js`. A site adopts them by linking `carino-ui.css`
before its own stylesheet and deleting its local `:root` and look-alike classes
in the same change. Sites may add new tokens but never redefine one declared in
`carino-ui.css`.

`carino-branding.css` imports `carino-ui.css` and adds only what this reference
page needs: its chrome, the frames components are shown in, and the page-type
sketches.

Every section has a **Copy** button. It lifts the component's markup preceded by
a link to the hosted stylesheet:

```html
<!-- Carino Branding · Buttons · https://branding.carino.systems -->
<link rel="stylesheet" href="https://branding.carino.systems/carino-branding.css">
<div class="demo">…</div>
```

Paste that anywhere and the component renders correctly: the hosted stylesheet
imports `carino-ui.css`. The Colors section's Copy button yields the raw token
CSS (`:root { … }`). When the style changes, edit `carino-ui.css` first.

## What's inside
Color tokens · themes (Gold & Black, Colourful) · typography · buttons & toggles · tabs · form controls · alerts ·
badges/chips/status · cards & panels · dropdown/diagnostics · tables · code
blocks · loading (spinner / progress / EKG) · slice menu and router · toast ·
navbar action portal · dropzone · modal · command block · workspace shell and
drawer · key caps · map · data viz and freshness states · currency · animations ·
landing hero · short hero · privacy line · filter chips · entry card and source
line · store (featured banner, shelf, store card, category tile) · lab and progress · footer · play controls · page types.

## Page types
Every site is one page of one of eight types — `hub`, `tool`, `suite`, `live`,
`reference`, `learn`, `play`, `product` — and the type fixes its layout: the
blocks it must have, may add and never has. Section 36 (`#pagetypes`) defines
them. Each site declares its type in `Carino-Systems/baseline/sites.json` as
`"type"`, with an optional `"also"` for a second type whose blocks it borrows.
A new type is added in Branding first, then in `sites.json`. Each block in a
type's sketch links to the component it is built from.

## Breakpoints
Two, and nothing else: at 900px and below a workspace rail becomes a drawer; at
640px and below is the phone layout.

## Design tokens
| Token | Value |
|-------|-------|
| accent (Sharp Gold) | `#eab308` |
| background | `#050505` |
| border | `#262626` |
| text / secondary / muted | `#ffffff` / `#a3a3a3` / `#666666` |
| display font | Red Hat Display (900, uppercase) |
| body font | IBM Plex Sans |
| mono font | IBM Plex Mono |

## Navbar
The canonical navbar ships as two self-injecting, CDN-free local files —
`carino-navbar.js` (include with `<script src="carino-navbar.js" data-app="Branding" defer>`)
and its companion `carino-clock.js`. Both are byte-identical copies of the shared
originals (edit `Carino-Systems/carino-clock.js` + `CVE/carino-navbar.js`, then
run `Carino-Systems/propagate.sh`). Favicon/brand glyph is `logo.webp`.

The brand is **two separate links**: the gradient **Carino** wordmark →
`https://carino.systems/` (the hub), and the app-tag chip → `./` (a fresh
reload of the current app). Both anchors carry `text-decoration: none`; the
chip gets a subtle gold hover (accent border + faint gold background).

## Cross-browser conventions
The sites target Chromium, Gecko (Firefox) and WebKit (Safari) equally. The
recurring gaps and the house rules for them:

- **Prefix pairs, `-webkit-` first.** Safari still only honours the prefixed form
  of some properties. Always ship both: `backdrop-filter` **needs**
  `-webkit-backdrop-filter`; gradient text needs `-webkit-background-clip: text`
  **and** `background-clip: text` plus `-webkit-text-fill-color: transparent`.
- **Scrollbars, both mechanisms.** `::-webkit-scrollbar` (Chromium + WebKit) has
  no Firefox equivalent; Firefox reads only `scrollbar-width` / `scrollbar-color`,
  which are *inherited*, so set them once on `:root`. `carino-branding.css` does
  both — copy that block, don't reinvent it.
- **Canvas image export.** Older WebKit silently returns a PNG data URL for
  `toDataURL('image/webp')`. Name the download from the returned MIME, not the
  requested one, or you ship a PNG under a `.webp` name.
- **`localStorage` can throw.** Safari private browsing (and a full quota) throw
  on `setItem`. Wrap every write in `try/catch` and degrade, never assume it took.
- **Clipboard needs a fallback.** `navigator.clipboard` is absent outside secure
  contexts; guard it and fall back to a `prompt()`/selection copy (see `index.html`).

## Licensing

**Mine — MIT licence.** Everything in this repository *except* the paths
listed below. Copyright © 2026 Miguel Carino. Full terms in [LICENSE](LICENSE).

**Not mine.** The files below are third-party works redistributed here. This
project's licence does not cover them and could not: they are not mine to
relicense. Each keeps its own terms, and each carries its own notice.

| Path | What it is | Licence | Notice |
| --- | --- | --- | --- |
| [`fonts/`](fonts/) | IBM Plex Mono, IBM Plex Sans, Red Hat Display | SIL OFL 1.1 | [`fonts/OFL.txt`](fonts/OFL.txt) |
| [`vendor/`](vendor/) | third-party JavaScript | per package — see the notice | [`vendor/README.md`](vendor/README.md) |

Those files travel with any fork, mirror or repackaging of this repository, and
their notices must travel with them.

**Why MIT and not AGPL.** This repository is the fleet design system, meant to be
copied from freely — snippets and components carry no copyleft obligation. That
is a deliberate exception to the fleet default, not an oversight. Note the
consequence: unlike the AGPL repositories, this one grants no leverage for a
commercial exception, because a permissive licence already gives away everything
such an exception would sell.
