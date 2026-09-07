"""Follow each site's own <link rel=icon> and check what it actually lands on.

Asserts rather than reports: the href is resolved relative to the page that
declares it, the bytes at the end of it must equal that site's mark, and no
two sites may end up on the same file.
"""
import os, re, hashlib, sys, collections
GH = os.path.expanduser("~/Github")
SRC = os.path.join(GH, "Branding/marks")

SITES = {
 "Aldis-Lamp/index.html": "aldis",        "Asobi/index.html": "asobi",
 "Branding/index.html": "branding",       "Carino-PACS/docs/index.html": "dicom",
 "Carino-Systems/index.html": "carino",   "Compass/index.html": "compass",
 "Currency/index.html": "currency",       "Custom-Images/docs/index.html": "images",
 "CVE/index.html": "cve",                 "CyberCity/index.html": "cybercity",
 "Desk/index.html": "desk",               "DICOM-editor/index.html": "dcm",
 "findmeadistro/index.html": "distro",    "Fiscal/index.html": "fiscal",
 "Fonts/index.html": "font",              "Hardware/index.html": "hardware",
 "Hash/index.html": "hash",               "Kanban/index.html": "kanban",
 "Law/index.html": "law",                 "Learn/index.html": "learn",
 "Media/index.html": "media",             "Metadata/index.html": "metadata",
 "MultiWeb/index.html": "multiweb",       "MusicGrid/index.html": "music",
 "NetplanConfig/index.html": "netplan",   "Offline/index.html": "offline",
 "Password/index.html": "password",       "Quote/index.html": "quote",
 "Retina/index.html": "retina",           "SimpleSetup/index.html": "setup",
 "SoftwareCatalog/index.html": "software","SyncSubsStudio/index.html": "subs",
 "Teleprompter/index.html": "teleprompter","Time/index.html": "time",
 "Topo/index.html": "topo",               "TV/index.html": "tv",
 "Vitae/index.html": "vitae",
}
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
BLACK = "70b0e044dbdcbeff0da2edb2bcbd9be6"   # the old face, for the record

fails, seen = [], collections.defaultdict(list)
for page, stem in sorted(SITES.items()):
    html = open(os.path.join(GH, page), encoding="utf-8", errors="replace").read()
    links = re.findall(r'<link[^>]*rel="[^"]*\bicon\b[^"]*"[^>]*>', html)
    hrefs = [re.search(r'href="([^"]+)"', l).group(1) for l in links
             if re.search(r'href="([^"]+)"', l) and 'playwright' not in l]
    if not hrefs:
        fails.append(f"{page}: declares no favicon"); continue
    for href in hrefs:
        target = os.path.normpath(os.path.join(GH, os.path.dirname(page), href))
        if not os.path.exists(target):
            fails.append(f"{page}: href {href} -> missing file"); continue
        ext = os.path.splitext(target)[1]
        if ext == ".png":
            # No .png source: re-run the same rasterisation at the file's own
            # size and compare, so the check still bites.
            import subprocess, tempfile
            from PIL import Image
            n = Image.open(target).size[0]
            tmp = tempfile.mkstemp(suffix=".png")[1]
            subprocess.run(["rsvg-convert", "-w", str(n), "-h", str(n),
                            os.path.join(SRC, stem + ".svg"), "-o", tmp], check=True)
            a = list(Image.open(target).convert("RGBA").getdata())
            b = list(Image.open(tmp).convert("RGBA").getdata())
            os.remove(tmp)
            if a != b:
                fails.append(f"{page}: {href} does not match the {stem} mark")
            else:
                seen["png:" + stem].append(page)
            continue
        want = os.path.join(SRC, stem + ext)
        if not os.path.exists(want):
            fails.append(f"{page}: no source mark {os.path.basename(want)}"); continue
        got, exp = md5(target), md5(want)
        if got != exp:
            fails.append(f"{page}: {href} is {'the OLD BLACK MARK' if got==BLACK else got[:8]}, "
                         f"expected {stem} ({exp[:8]})")
        else:
            seen[got].append(page)

for h, pages in seen.items():
    if len(pages) > 1:
        fails.append(f"same mark on {len(pages)} sites: {', '.join(pages)}")

print(f"{len(SITES)} sites checked, {sum(len(v) for v in seen.values())} icon links resolved")
if fails:
    print(f"\n{len(fails)} FAILURES:"); [print("  x", f) for f in fails]; sys.exit(1)
print("PASS -- every site's favicon link lands on that site's own mark, all distinct")
