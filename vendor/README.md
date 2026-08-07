# Third-party code bundled here

Everything this project needs is vendored: it loads no script, style, font, map
or module from anywhere but its own origin — no CDN, no network, no account.
That is the point of the tool, and it makes the licences below *this project's*
responsibility rather than a package manager's.

**Every library here has its licence text in this directory.** Naming a licence
is not the same as shipping it: MIT and BSD both require the permission text
itself to travel with a copy, and most minified bundles drop it. Where a bundle
does carry the full text inline, the row says so and no separate file is needed.

These two power the "export this page as PDF" action in the design-system
reference. Nothing else here is third-party.

## What is here, and under what licence

| File | Package | Licence | Licence text |
| --- | --- | --- | --- |
| `html2canvas.min.js` | [html2canvas](https://html2canvas.hertzen.com) 1.4.1 | MIT | [`LICENSE-html2canvas.txt`](LICENSE-html2canvas.txt) — the header names MIT and © 2022 Niklas von Hertzen but omits the permission text |
| `jspdf.umd.min.js` | [jsPDF](https://github.com/parallax/jsPDF) 2.5.1 | MIT | **Inline** — `@license` block carries the full MIT text |

## The rule

Adding a file to this directory means adding a row here **in the same commit**.
A record kept from the first vendored file is trivial; one reconstructed two
years later is not.
