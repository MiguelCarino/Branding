// node --test tests/ — Branding's Export (PDF | HTML) and its strings.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const read = (f) => readFileSync(join(ROOT, f), 'utf8');

// branding-export.js: its pure half, loaded without a DOM.
const BX = (() => {
    const win = {};
    new Function('window', read('branding-export.js'))(win);
    return win.BrandingExport;
})();

// i18n.js: the dictionaries only (the rest wires the page).
const I18N = new Function(read('i18n.js').replace(/let LOCALE[\s\S]*/, '') + ';return I18N;')();
const LOCALES = ['es', 'pt-BR', 'ja', 'ru'];
const INDEX = read('index.html');

test('unicode-range parsing', () => {
    assert.equal(BX.parseRanges(''), null);
    assert.equal(BX.parseRanges(undefined), null);
    assert.deepEqual(BX.parseRanges('U+0000-00FF, U+0131, U+4??'), [[0, 0xff], [0x131, 0x131], [0x400, 0x4ff]]);
    assert.deepEqual(BX.parseRanges('U+2000-206F,bogus'), [[0x2000, 0x206f]]);
});

test('a font range is kept only when the text uses it', () => {
    const latin = "@font-face { font-family: 'IBM Plex Sans'; src: url(./a.woff2); unicode-range: U+0000-00FF, U+2000-206F; }";
    const cyr = "@font-face { font-family: 'IBM Plex Sans'; src: url(./c.woff2); unicode-range: U+0301, U+0400-045F; }";
    const any = "@font-face { font-family: 'X'; src: url(./x.woff2); }";
    const en = BX.codePoints('Carino Branding — tokens');
    const ru = BX.codePoints('Карино');
    assert.equal(BX.keepFontFace(latin, en), true);
    assert.equal(BX.keepFontFace(cyr, en), false);
    assert.equal(BX.keepFontFace(cyr, ru), true);
    assert.equal(BX.keepFontFace(any, en), true);
    assert.equal(BX.rangesHit([[10, 20]], [5, 21]), false);
    assert.equal(BX.rangesHit([[10, 20]], new Set([20])), true);
});

test('relative url()s become absolute against their stylesheet', () => {
    const css = "src: url(./IBMPlexMono-400-latin.woff2) format('woff2'); background: url('img/a.png'); mask: url(\"data:image/svg+xml,%3Csvg%3E\"); fill: url(#g);";
    const out = BX.absUrls(css, 'https://branding.carino.systems/fonts/carino-fonts.css');
    assert.match(out, /url\("https:\/\/branding\.carino\.systems\/fonts\/IBMPlexMono-400-latin\.woff2"\)/);
    assert.match(out, /url\("https:\/\/branding\.carino\.systems\/fonts\/img\/a\.png"\)/);
    assert.match(out, /url\("data:image\/svg\+xml,%3Csvg%3E"\)/);
    assert.match(out, /url\(#g\)/);
});

test('the HTML file: standalone, same paper and foot as the PDF', () => {
    const html = BX.shell({
        attrs: { lang: 'ja', 'data-carino-theme': 'color', 'data-theme': '', dir: null },
        title: 'Carino <Branding>',
        css: '.x{color:red}',
        hero: '<div class="guide-hero"><h1>Carino Branding</h1></div>',
        specs: ['<section class="spec" id="a"></section>', '<section class="spec" id="b"></section>'],
    });
    assert.match(html, /^<!DOCTYPE html>\n<html lang="ja" data-carino-theme="color">/);
    assert.doesNotMatch(html, /<script|<link\b/i);
    assert.match(html, /<meta charset="utf-8">/);
    assert.match(html, /<title>Carino &lt;Branding&gt;<\/title>/);
    assert.match(html, /<body class="pdf-mode">/);
    assert.match(html, /<style id="bxPaper">/);
    // A4, the PDF's 36px margins, its foot line and page number, each section from a new page
    assert.match(html, /@page\{size:A4;margin:36px 36px 50px;/);
    assert.ok(html.includes('content:"' + BX.FOOT + '"'));
    assert.match(html, /@bottom-right\{content:counter\(page\)/);
    assert.match(html, /\.bx-doc main \.spec\{break-before:page/);
    // the 1032px capture width, scaled to A4's content width as the PDF scales it
    assert.equal(BX.WIDTH, 1032);
    assert.ok(Math.abs(BX.ZOOM - (210 * 96 / 25.4 - 72) / 1032) < 1e-9);
    assert.ok(html.indexOf('id="a"') < html.indexOf('id="b"'));
    assert.ok(html.indexOf('guide-hero') < html.indexOf('<main>'));
});

test('the preview: the switch above the file name, one Download last', () => {
    const ov = INDEX.slice(INDEX.indexOf('id="rpOverlay"'), INDEX.indexOf('</div>\n  </div>\n', INDEX.indexOf('id="rpOverlay"')));
    assert.match(ov, /<p class="rpv-name" id="rpName">/);
    assert.doesNotMatch(ov, /id="rpDownload"[^>]*data-i18n(?!-)/, 'the Download label follows the switch, not data-i18n');
    const actions = ov.slice(ov.indexOf('class="rpv-actions"'));
    const btns = actions.match(/<button[^>]*>/g);
    assert.equal(btns.length, 2);
    assert.match(btns[0], /id="rpPrint"/);
    assert.match(btns[1], /class="btn btn-primary" id="rpDownload"/);
    // the switch is put in front of the file name, never into .rpv-opts
    assert.match(INDEX, /nameEl\.parentNode\.insertBefore\(fmt\.el, nameEl\)/);
    assert.match(INDEX, /<script src="carino-pdf\.js" defer><\/script>/);
    assert.match(INDEX, /<script src="branding-export\.js" defer><\/script>/);
});

test('the anatomy demo shows the switch between the options and the name', () => {
    const rack = INDEX.slice(INDEX.indexOf('<div class="rpv-rack">'), INDEX.indexOf('<div class="rpv-stage"><div class="rpv-demo-sheet"'));
    const opts = rack.indexOf('class="rpv-opts"');
    const fmt = rack.indexOf('class="rpv-format"');
    const name = rack.indexOf('class="rpv-name"');
    const acts = rack.indexOf('class="rpv-actions"');
    assert.ok(opts > 0 && opts < fmt && fmt < name && name < acts);
    // .rpv-opts closes before the switch starts
    const optsBody = rack.slice(opts, fmt);
    assert.equal((optsBody.match(/<div\b/g) || []).length, (optsBody.match(/<\/div>/g) || []).length);
    assert.match(rack, /role="radiogroup"/);
    assert.match(rack, /data-format="pdf">PDF<\/button>/);
    assert.match(rack, /data-format="html">HTML<\/button>/);
});

test('the copied snippet cannot close the page script early', () => {
    const at = INDEX.indexOf('const RPV_PDF_SNIPPET');
    const body = INDEX.slice(at, INDEX.indexOf('].join("\\n");', at));
    assert.ok(body.length > 100);
    assert.doesNotMatch(body, /<\/script>/i);
    assert.match(body, /CarinoPdf\.formatSwitch/);
    assert.match(body, /CarinoPdf\.download/);
});

test('every Export string is translated (PDF and HTML stay Latin)', () => {
    const keys = ['File', 'Download PDF', 'Download HTML', 'Creating the PDF…', 'Could not create the PDF.',
        'Creating the HTML…', 'Could not create the HTML.', '{n} sections', '1 page', '{n} pages',
        'Rendering {i} / {n}…', 'PDF engine still loading…', 'Report preview', '🖨 Print', '⤓ Export',
        'Preview the full reference, then download it as PDF or HTML', 'Open the Export preview',
        'Report preview reference: Branding (Export), DICOM Editor (report).', 'Wiring the PDF | HTML switch',
        'Copy the snippet', 'Close'];
    for (const l of LOCALES) {
        for (const k of keys) {
            assert.ok(typeof I18N[l][k] === 'string' && I18N[l][k], l + ' lacks ' + JSON.stringify(k));
        }
        assert.match(I18N[l]['Download PDF'], /PDF/);
        assert.match(I18N[l]['Download HTML'], /HTML/);
        if (I18N[l]['{n} sections']) assert.match(I18N[l]['{n} sections'], /\{n\}/);
    }
});

test('every status the Export script says has a translation', () => {
    const at = INDEX.indexOf('/* ---- Export: the whole reference as PDF or HTML');
    const code = INDEX.slice(at, INDEX.indexOf('window.brandingPdfPreview =', at));
    const said = [...code.matchAll(/status\("([^"]+)"/g)].map((m) => m[1]);
    assert.ok(said.length >= 6);
    for (const l of LOCALES) for (const k of said) assert.ok(I18N[l][k], l + ' lacks ' + JSON.stringify(k));
});

test('the data-i18n-html notes of section 19 are all translated', () => {
    const sec = INDEX.slice(INDEX.indexOf('<section class="spec" id="modal">'), INDEX.indexOf('</section>', INDEX.indexOf('<section class="spec" id="modal">')));
    const notes = [...sec.matchAll(/<div class="note" data-i18n-html>([\s\S]*?)<\/div>/g)].map((m) => m[1].trim().replace(/\s+/g, ' '));
    assert.ok(notes.some((n) => n.startsWith('<strong>PDF or HTML.</strong>')));
    for (const l of LOCALES) for (const n of notes) assert.ok(I18N[l][n], l + ' lacks the note ' + n.slice(0, 40));
});

test('a stylesheet is written in from its own text: imports followed, var() shorthands kept', async () => {
    const files = {
        'http://x.test/b.css': "@import url('./ui.css');\n/* note */ .h1 { background: var(--gold-text); background-clip: text; }\n@font-face { font-family: F; src: url(f/c.woff2); unicode-range: U+0400-045F; }",
        'http://x.test/ui.css': "@import 'print.css' print;\n.btn { background: url(img/a.svg); }",
        'http://x.test/print.css': '.btn { color: #000; }',
    };
    const css = await BX.sheetCss(files['http://x.test/b.css'], 'http://x.test/b.css', null, BX.codePoints('Carino'),
        (u) => Promise.resolve(files[u] ?? null));
    assert.match(css, /background: var\(--gold-text\); background-clip: text;/);
    assert.match(css, /@media print\{\n\.btn \{ color: #000; \}\n\}/);
    assert.match(css, /url\("http:\/\/x\.test\/img\/a\.svg"\)/);
    assert.doesNotMatch(css, /@import|note|@font-face/);
    assert.ok(css.indexOf('@media print') < css.indexOf('.btn { background') && css.indexOf('.btn { background') < css.indexOf('.h1'));
});
