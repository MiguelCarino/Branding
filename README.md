# Carino Branding

The living reference for the **Carino** visual language — the shared navbar, the
gold-on-black palette, and every component pattern used across the workshop.
Hosted at **branding.carino.systems**.

All component styles live in **`carino-branding.css`** — the hosted source of
truth. `index.html` links it, and so does every copied snippet.

Every section has a **Copy** button. It lifts the component's markup preceded by
a link to the hosted stylesheet:

```html
<!-- Carino Branding · Buttons · https://branding.carino.systems -->
<link rel="stylesheet" href="https://branding.carino.systems/carino-branding.css">
<div class="demo">…</div>
```

Paste that anywhere and the component renders correctly — it pulls its styling
straight from `branding.carino.systems`, no local CSS needed. The Colors
section's Copy button yields the raw design-token CSS (`:root { … }`) for when
you want the values inline. When the style changes, edit `carino-branding.css`
first and treat it as the source of truth.

## What's inside
Color tokens · typography · buttons & toggles · tabs · form controls · alerts ·
badges/chips/status · cards & panels · dropdown/diagnostics · tables · code
blocks · loading (spinner / progress / EKG) · slice menu.

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

## License

Licensed under the **MIT License** — see [LICENSE](LICENSE). Copyright © 2026 Miguel Carino.

Deliberately permissive: this repo is the fleet design system, meant to be copied
from freely. Snippets and components carry no copyleft obligation.
