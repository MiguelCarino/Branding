/* branding-export.js — window.BrandingExport — the HTML version of Export.
 *
 * Branding's Export writes the whole reference as a PDF with its own vendored
 * html2canvas + jsPDF (index.html): the hero, then every section from a fresh
 * A4 page, captured at the 1032px content width on white paper (.pdf-mode),
 * with "Carino Branding · branding.carino.systems", the page number and a
 * gold rule at the foot of each page. This file makes the same report as one
 * standalone HTML file: the same hero and sections, as live text, on the same
 * white paper and in the same theme, with the page's stylesheets and the
 * fonts the text needs written into it, and no script. Printed, it gives the
 * PDF's pages: A4, the same margins, each section from a new page, the same
 * foot line (page margin boxes, where the browser has them).
 *
 * The pure half (parseRanges, rangesHit, keepFontFace, absUrls, sheetCss,
 * shell) runs under node in tests/; build() reads the live page.
 */
(function (root) {
    'use strict';

    var FOOT = 'Carino Branding · branding.carino.systems';
    var WIDTH = 1032;               // the content width the PDF captures sections at
    var A4_W = 210 * 96 / 25.4;     // A4 width in CSS px (793.7)
    var MARGIN = 36;                // the PDF's page margin, px
    var MARGIN_FOOT = 50;           // bottom margin: content stops 14px above the PDF's 36px
    var ZOOM = (A4_W - 2 * MARGIN) / WIDTH;

    // "U+0000-00FF, U+0131, U+4??" -> [[lo, hi], ...]; null when there is no range (every character).
    function parseRanges(s) {
        if (s == null || !String(s).trim()) return null;
        var out = [];
        String(s).split(',').forEach(function (part) {
            var m = /^\s*U\+([0-9a-f?]+)(?:-([0-9a-f]+))?\s*$/i.exec(part);
            if (!m) return;
            if (m[1].indexOf('?') >= 0) {
                out.push([parseInt(m[1].replace(/\?/g, '0'), 16), parseInt(m[1].replace(/\?/g, 'f'), 16)]);
            } else {
                var lo = parseInt(m[1], 16);
                out.push([lo, m[2] ? parseInt(m[2], 16) : lo]);
            }
        });
        return out;
    }

    // Does any code point fall in the ranges? (null ranges: yes)
    function rangesHit(ranges, cps) {
        if (!ranges) return true;
        var list = Array.isArray(cps) ? cps : Array.from(cps || []);
        for (var i = 0; i < list.length; i++) {
            for (var j = 0; j < ranges.length; j++) {
                if (list[i] >= ranges[j][0] && list[i] <= ranges[j][1]) return true;
            }
        }
        return false;
    }

    // The code points a text uses, as a Set.
    function codePoints(text) {
        var set = new Set();
        Array.from(String(text || '')).forEach(function (c) { set.add(c.codePointAt(0)); });
        return set;
    }

    // An @font-face rule is written into the file only when the text uses a
    // character in its unicode-range: Cyrillic only for Russian, and so on.
    function keepFontFace(ruleText, cps) {
        var m = /unicode-range\s*:\s*([^;}]+)/i.exec(String(ruleText || ''));
        return rangesHit(parseRanges(m ? m[1] : null), cps);
    }

    // Relative url()s made absolute against the stylesheet they came from.
    function absUrls(css, base) {
        return String(css || '').replace(/url\(\s*(["']?)([^"')]+)\1\s*\)/gi, function (all, q, u) {
            if (/^(data:|#|blob:)/i.test(u)) return all;
            try { return 'url("' + new URL(u, base).href + '")'; } catch (e) { return all; }
        });
    }

    function esc(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // What the file adds to the page's own styles: the PDF's paper and pages.
    function paperCss() {
        var foot = 'font:10.67px/1 Helvetica,Arial,"Liberation Sans",sans-serif;color:rgb(150,150,150);' +
            'vertical-align:top;padding-top:6px;border-top:0.75px solid rgb(234,179,8)';
        return [
            'html,body{background:#fff}',
            'body{margin:0}',
            '.bx-doc{max-width:' + WIDTH + 'px;margin:0 auto;padding:0 0 48px}',
            '.bx-doc main{max-width:none;margin:0;padding:0}',
            '.bx-doc .spec{display:block!important;animation:none!important}',
            '.bx-doc main .spec{border-top:2px solid rgb(234,179,8)}',
            '@page{size:A4;margin:' + MARGIN + 'px ' + MARGIN + 'px ' + MARGIN_FOOT + 'px;' +
                '@bottom-left{content:"' + FOOT + '";' + foot + '}' +
                '@bottom-right{content:counter(page);' + foot + '}}',
            '@media print{' +
                'body{-webkit-print-color-adjust:exact;print-color-adjust:exact}' +
                '.bx-doc{width:' + WIDTH + 'px;max-width:none;padding:0;zoom:' + ZOOM.toFixed(4) + '}' +
                '.bx-doc main .spec{break-before:page;border-top:0}' +
            '}',
        ].join('\n');
    }

    // The file around the page's parts. attrs: the <html> attributes that
    // set language and theme; css: the page's styles, already standalone.
    function shell(o) {
        var attrs = o.attrs || {};
        var a = Object.keys(attrs).filter(function (k) { return attrs[k] != null && attrs[k] !== ''; })
            .map(function (k) { return ' ' + k + '="' + esc(attrs[k]) + '"'; }).join('');
        return '<!DOCTYPE html>\n<html' + a + '>\n<head>\n<meta charset="utf-8">\n' +
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n' +
            '<title>' + esc(o.title || 'Carino Branding') + '</title>\n' +
            '<style>\n' + (o.css || '') + '\n</style>\n' +
            '<style id="bxPaper">\n' + paperCss() + '\n</style>\n' +
            '</head>\n<body class="pdf-mode">\n<div class="bx-doc">\n' + (o.hero || '') +
            '\n<main>\n' + (o.specs || []).join('\n') + '\n</main>\n</div>\n</body>\n</html>\n';
    }

    /* ---- the live page -------------------------------------------------- */

    function sameOrigin(url) {
        try { return new URL(url, document.baseURI).origin === location.origin; } catch (e) { return false; }
    }
    function dataUrl(url) {
        return fetch(url).then(function (r) { return r.ok ? r.blob() : null; }).then(function (b) {
            if (!b) return null;
            return new Promise(function (res) {
                var fr = new FileReader();
                fr.onload = function () { res(fr.result); };
                fr.onerror = function () { res(null); };
                fr.readAsDataURL(b);
            });
        }).catch(function () { return null; });
    }

    // One stylesheet's own text, made standalone: comments out, its @imports
    // read (fetchText) and written in place, @font-face rules for ranges the
    // text does not use left out, url()s absolute against the sheet. The
    // sheet's text is read rather than its CSSOM rules: Chromium serialises
    // a rule that mixes a var() shorthand with one of its longhands
    // (background: var(--gold-text); background-clip: text) with empty
    // values, and the hero's gold title would come out invisible.
    function sheetCss(text, base, media, cps, fetchText, depth) {
        depth = depth || 0;
        var css = String(text || '').replace(/\/\*[\s\S]*?\*\//g, '');
        var IMPORT = /@import\s+(?:url\(\s*(["']?)([^"')]+)\1\s*\)|(["'])([^"']+)\3)\s*([^;]*);/gi;
        var pieces = [];
        var last = 0, m;
        while ((m = IMPORT.exec(css))) {
            pieces.push(css.slice(last, m.index));
            var href = m[2] || m[4];
            var mt = (m[5] || '').trim();
            var abs = null;
            try { abs = new URL(href, base).href; } catch (e) { abs = null; }
            pieces.push(abs && depth < 8
                ? Promise.resolve(fetchText(abs)).then(function (abs, mt, t) {
                    return t == null ? '' : sheetCss(t, abs, mt && mt !== 'all' ? mt : null, cps, fetchText, depth + 1);
                }.bind(null, abs, mt))
                : '');
            last = IMPORT.lastIndex;
        }
        pieces.push(css.slice(last));
        return Promise.all(pieces).then(function (parts) {
            var body = parts.map(function (p, i) {
                if (i % 2) return p;             // an import, already standalone
                p = p.replace(/@font-face\s*\{[^}]*\}/gi, function (rule) { return keepFontFace(rule, cps) ? rule : ''; });
                return absUrls(p, base);
            }).join('').trim();
            return body && media ? '@media ' + media + '{\n' + body + '\n}' : body;
        });
    }

    function fetchText(url) {
        if (!sameOrigin(url)) return Promise.resolve(null);
        return fetch(url).then(function (r) { return r.ok ? r.text() : null; }).catch(function () { return null; });
    }

    // Every same-origin stylesheet, imports followed, unused font ranges left
    // out, each url() written in as data (an address that cannot be read is
    // dropped: the file makes no request when opened).
    function collectCss(cps) {
        var jobs = [];
        Array.prototype.forEach.call(document.styleSheets, function (s) {
            if (s.disabled) return;
            var node = s.ownerNode;
            if (node && node.closest && node.closest('#rpOverlay')) return;
            var mt = s.media && s.media.mediaText;
            var media = mt && mt !== 'all' ? mt : null;
            if (s.href) {
                jobs.push(fetchText(s.href).then(function (t) {
                    return t == null ? '' : sheetCss(t, s.href, media, cps, fetchText);
                }));
            } else if (node && node.textContent && node.textContent.trim()) {
                jobs.push(sheetCss(node.textContent, document.baseURI, media, cps, fetchText));
            } else {
                // a <style> filled through the CSSOM only
                var rules = '';
                try { rules = Array.prototype.map.call(s.cssRules, function (r) { return r.cssText; }).join('\n'); } catch (e) { rules = ''; }
                jobs.push(sheetCss(rules, document.baseURI, media, cps, fetchText));
            }
        });
        return Promise.all(jobs).then(function (parts) {
            var css = parts.filter(Boolean).join('\n');
            var urls = {};
            css.replace(/url\("([^"]+)"\)/g, function (all, u) { if (!/^data:/i.test(u)) urls[u] = 1; return all; });
            var fetches = Object.keys(urls).map(function (u) {
                return (sameOrigin(u) ? dataUrl(u) : Promise.resolve(null)).then(function (d) { urls[u] = d; });
            });
            return Promise.all(fetches).then(function () {
                return css.replace(/url\("([^"]+)"\)/g, function (all, u) {
                    if (/^data:/i.test(u)) return all;
                    return urls[u] ? 'url("' + urls[u] + '")' : 'url("")';
                });
            });
        });
    }

    // A part as the PDF shows it, minus the buttons that need the page's
    // script (Copy, Export): form state written into attributes, the
    // translation bookkeeping left out.
    function cleanClone(el) {
        var c = el.cloneNode(true);
        var src = el.querySelectorAll('input, textarea, select');
        var dst = c.querySelectorAll('input, textarea, select');
        Array.prototype.forEach.call(src, function (s, i) {
            var d = dst[i];
            if (!d) return;
            if (s.type === 'checkbox' || s.type === 'radio') {
                if (s.checked) d.setAttribute('checked', ''); else d.removeAttribute('checked');
            } else if (s.tagName === 'TEXTAREA') {
                d.textContent = s.value;
            } else if (s.tagName === 'SELECT') {
                Array.prototype.forEach.call(d.options, function (o, k) {
                    if (s.options[k] && s.options[k].selected) o.setAttribute('selected', ''); else o.removeAttribute('selected');
                });
            } else if (s.type !== 'file' && s.type !== 'password') {
                d.setAttribute('value', s.value);
            }
        });
        Array.prototype.forEach.call(c.querySelectorAll('.copy-btn, .hero-actions, script, template'), function (n) { n.remove(); });
        [c].concat(Array.prototype.slice.call(c.querySelectorAll('*'))).forEach(function (n) {
            Array.prototype.slice.call(n.attributes).forEach(function (a) {
                if (/^data-i18n/.test(a.name) || /^on/i.test(a.name)) n.removeAttribute(a.name);
            });
        });
        c.classList.remove('active', 'from-left', 'from-right');
        c.removeAttribute('style');
        return c;
    }

    // Pictures named in style attributes (the glyphs' --g:url(marks/…)) are
    // written in as data too: by address they would not resolve once the file
    // is opened on its own. One that cannot be read is dropped.
    function inlineStyleUrls(parts) {
        var els = [];
        parts.forEach(function (p) {
            [p].concat(Array.prototype.slice.call(p.querySelectorAll('[style]'))).forEach(function (n) {
                if (/url\(/i.test(n.getAttribute('style') || '')) els.push(n);
            });
        });
        var urls = {};
        var RE = /url\(\s*(["']?)([^"')]+)\1\s*\)/gi;
        els.forEach(function (n) {
            n.getAttribute('style').replace(RE, function (all, q, u) {
                if (!/^(data:|#)/i.test(u)) urls[u] = 1;
                return all;
            });
        });
        var jobs = Object.keys(urls).map(function (u) {
            var abs;
            try { abs = new URL(u, document.baseURI).href; } catch (e) { abs = null; }
            return (abs && sameOrigin(abs) ? dataUrl(abs) : Promise.resolve(null)).then(function (d) { urls[u] = d; });
        });
        return Promise.all(jobs).then(function () {
            els.forEach(function (n) {
                n.setAttribute('style', n.getAttribute('style').replace(RE, function (all, q, u) {
                    if (/^(data:|#)/i.test(u)) return all;
                    return urls[u] ? 'url("' + urls[u] + '")' : 'url("")';
                }));
            });
        });
    }

    // The HTML file: { html, sections }.
    function build(opts) {
        opts = opts || {};
        var hero = document.querySelector('.guide-hero');
        var specs = Array.prototype.slice.call(document.querySelectorAll('main .spec'));
        var text = (hero ? hero.textContent : '') + specs.map(function (s) { return s.textContent; }).join('') + FOOT;
        var de = document.documentElement;
        var attrs = {};
        ['lang', 'dir', 'data-carino-theme', 'data-theme'].forEach(function (k) {
            if (de.hasAttribute(k)) attrs[k] = de.getAttribute(k);
        });
        var heroC = hero ? cleanClone(hero) : null;
        var specC = specs.map(cleanClone);
        var parts = (heroC ? [heroC] : []).concat(specC);
        return Promise.all([collectCss(codePoints(text)), inlineStyleUrls(parts)]).then(function (got) {
            var html = shell({
                attrs: attrs,
                title: opts.title || 'Carino Branding',
                css: got[0],
                hero: heroC ? heroC.outerHTML : '',
                specs: specC.map(function (s) { return s.outerHTML; }),
            });
            // Pictures by address (the marks) are written in by the fleet's own
            // standalone-file step; it leaves an already standalone file as is.
            var P = root.CarinoPdf;
            return (P && P.htmlFile ? P.htmlFile(html) : Promise.resolve(html));
        }).then(function (html) { return { html: html, sections: specs.length }; });
    }

    root.BrandingExport = {
        FOOT: FOOT, WIDTH: WIDTH, ZOOM: ZOOM,
        parseRanges: parseRanges, rangesHit: rangesHit, codePoints: codePoints,
        keepFontFace: keepFontFace, absUrls: absUrls, sheetCss: sheetCss, paperCss: paperCss, shell: shell,
        build: build,
    };
}(typeof window !== 'undefined' ? window : this));
