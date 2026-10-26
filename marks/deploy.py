"""Put each mark where its site actually looks for one.

Targets come from the icon survey, not from a guess: every path below is
either referenced by a <link rel=icon>/og:image, or is an existing logo file
that would otherwise be left showing the old mark.
"""
import os, shutil, sys

SRC = os.path.expanduser("~/Github/Branding/marks")
GH  = os.path.expanduser("~/Github")

# stem -> (svg destinations, raster destinations)
T = {
 "aldis":    (["Aldis-Lamp/logo.svg"], ["Aldis-Lamp/logo.webp"]),
 "asobi":    (["Asobi/logo.svg"], ["Asobi/logo.webp"]),
 "branding": (["Branding/logo.svg"], ["Branding/logo.webp"]),
 "carino":   (["Carino-Systems/logo.svg"], ["Carino-Systems/logo.webp"]),
 "compass":  (["Compass/logo.svg"], ["Compass/logo.webp"]),
 "currency": (["Currency/logo.svg"], ["Currency/logo.webp"]),
 "cve":      (["CVE/logo.svg"], ["CVE/logo.webp"]),
 "cybercity":(["CyberCity/logo.svg"], ["CyberCity/logo.webp"]),
 # dcm: site root, plus the desktop app's asset
 "dcm":      (["DICOM-editor/logo.svg", "DICOM-editor/desktop/assets/logo.svg",
               "Carino-DICOM/pacs/web/editor/logo.svg"],
              ["DICOM-editor/logo.webp", "Carino-DICOM/pacs/web/editor/logo.webp"]),
 "desk":     (["Desk/logo.svg"], ["Desk/logo.webp"]),
 # dicom: the public site is docs/, the PACS server ships its own web UI, and
 # docs/favicon.webp + pacs/web/{logo,favicon}.webp are all one file today.
 "dicom":    (["Carino-DICOM/docs/logo.svg", "Carino-DICOM/desktop/assets/logo.svg"],
              ["Carino-DICOM/docs/favicon.webp", "Carino-DICOM/docs/logo.webp",
               "Carino-DICOM/pacs/web/logo.webp", "Carino-DICOM/pacs/web/favicon.webp"]),
 "distro":   (["findmeadistro/logo.svg"], ["findmeadistro/logo.webp"]),
 "fiscal":   (["Fiscal/logo.svg"], ["Fiscal/logo.webp"]),
 "font":     (["Fonts/logo.svg"], ["Fonts/logo.webp"]),
 "hardware": (["Hardware/logo.svg"], ["Hardware/logo.webp"]),
 "hash":     (["Hash/logo.svg"], ["Hash/logo.webp"]),
 "images":   (["Custom-Images/docs/logo.svg"], ["Custom-Images/docs/logo.webp"]),
 "jellyfish":(["Jellyfish/logo.svg"], ["Jellyfish/logo.webp"]),
 "kanban":   (["Kanban/logo.svg"], ["Kanban/logo.webp"]),
 "law":      (["Law/logo.svg"], ["Law/logo.webp"]),
 "learn":    (["Learn/logo.svg"], ["Learn/logo.webp"]),
 "media":    (["Media/logo.svg"], ["Media/logo.webp"]),
 "metadata": (["Metadata/logo.svg"], ["Metadata/logo.webp"]),
 "multiweb": (["MultiWeb/logo.svg"], ["MultiWeb/logo.webp"]),
 "music":    (["MusicGrid/assets/images/logo.svg"], ["MusicGrid/assets/images/logo.webp"]),
 "netplan":  (["NetplanConfig/logo.svg"], ["NetplanConfig/logo.webp"]),
 "offline":  (["Offline/logo.svg"], ["Offline/logo.webp"]),
 "password": (["Password/logo.svg"], ["Password/logo.webp"]),
 "ping":     (["Ping/logo.svg"], ["Ping/logo.webp"]),
 "quote":    (["Quote/logo.svg"], ["Quote/logo.webp"]),
 "retina":   (["Retina/logo.svg", "Retina/desktop/assets/logo.svg"], ["Retina/logo.webp"]),
 "setup":    (["SimpleSetup/logo.svg"], ["SimpleSetup/logo.webp"]),
 "software": (["SoftwareCatalog/assets/images/logo.svg"],
              ["SoftwareCatalog/assets/images/logo.webp"]),
 "stocks":   (["Stocks/logo.svg"], ["Stocks/logo.webp"]),
 "subs":     (["SyncSubsStudio/logo.svg"], ["SyncSubsStudio/logo.webp"]),
 "teleprompter": (["Teleprompter/logo.svg"], ["Teleprompter/logo.webp"]),
 "test":     (["Test/logo.svg"], ["Test/logo.webp"]),
 "time":     (["Time/logo.svg"], ["Time/logo.webp"]),
 "topo":     (["Topo/logo.svg"], ["Topo/logo.webp"]),
 "tv":       (["TV/logo.svg"], ["TV/logo.webp"]),
 "vitae":    (["Vitae/logo.svg"], ["Vitae/logo.webp"]),
}


# Vendored copies outside the sites themselves. The hub draws every tool's mark
# from its own assets/marks/ (the spotlight and the plate wall), and the
# profile site, MiguelCarino, shows a subset beside its project list. Both were
# byte copies of the files here, so they move with them.
HUB = "Carino-Systems/assets/marks"
PROFILE = "MiguelCarino/assets"
for stem, (svgs, _) in T.items():
    if os.path.exists(os.path.join(GH, HUB, f"{stem}.svg")):
        svgs.append(f"{HUB}/{stem}.svg")
    if os.path.exists(os.path.join(GH, PROFILE, f"{stem}.svg")):
        svgs.append(f"{PROFILE}/{stem}.svg")


# PNG icons are re-rendered from the stem's svg at the file's own size rather
# than copied: there is no .png source here. Fiscal ships a 180x180
# apple-touch-icon.png, which verify.py checks the same way.
PNG = {"fiscal": ["Fiscal/apple-touch-icon.png"]}


def main():
    import subprocess, struct
    made = new = 0
    for stem, dests in sorted(PNG.items()):
        for dst in dests:
            p = os.path.join(GH, dst)
            with open(p, "rb") as fh:
                w = struct.unpack(">I", fh.read(24)[16:20])[0]
            subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(w),
                            os.path.join(SRC, f"{stem}.svg"), "-o", p], check=True)
            made += 1
            print(f"    {dst} ({w}px)")
    for stem, (svgs, rasters) in sorted(T.items()):
        for dst, src in [(d, f"{stem}.svg") for d in svgs] + [(d, f"{stem}.webp") for d in rasters]:
            s, p = os.path.join(SRC, src), os.path.join(GH, dst)
            assert os.path.exists(s), s
            if not os.path.isdir(os.path.dirname(p)):
                print(f"  MISSING DIR for {dst}"); sys.exit(1)
            fresh = not os.path.exists(p)
            shutil.copyfile(s, p)
            made += 1; new += fresh
            print(f"  {'+' if fresh else ' '} {dst}")
    print(f"\n{made} files written ({new} new), {len(T)} sites")

main()
