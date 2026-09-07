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
               "Carino-PACS/pacs/web/editor/logo.svg"],
              ["DICOM-editor/logo.webp", "Carino-PACS/pacs/web/editor/logo.webp"]),
 "desk":     (["Desk/logo.svg"], ["Desk/logo.webp"]),
 # dicom: the public site is docs/, the PACS server ships its own web UI, and
 # docs/favicon.webp + pacs/web/{logo,favicon}.webp are all one file today.
 "dicom":    (["Carino-PACS/docs/logo.svg", "Carino-PACS/desktop/assets/logo.svg"],
              ["Carino-PACS/docs/favicon.webp", "Carino-PACS/docs/logo.webp",
               "Carino-PACS/pacs/web/logo.webp", "Carino-PACS/pacs/web/favicon.webp"]),
 "distro":   (["findmeadistro/logo.svg"], ["findmeadistro/logo.webp"]),
 "fiscal":   (["Fiscal/logo.svg"], ["Fiscal/logo.webp"]),
 "font":     (["Fonts/logo.svg"], ["Fonts/logo.webp"]),
 "hardware": (["Hardware/logo.svg"], ["Hardware/logo.webp"]),
 "hash":     (["Hash/logo.svg"], ["Hash/logo.webp"]),
 "images":   (["Custom-Images/docs/logo.svg"], ["Custom-Images/docs/logo.webp"]),
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
 "quote":    (["Quote/logo.svg"], ["Quote/logo.webp"]),
 "retina":   (["Retina/logo.svg", "Retina/desktop/assets/logo.svg"], ["Retina/logo.webp"]),
 "setup":    (["SimpleSetup/logo.svg"], ["SimpleSetup/logo.webp"]),
 "software": (["SoftwareCatalog/assets/images/logo.svg"],
              ["SoftwareCatalog/assets/images/logo.webp"]),
 "subs":     (["SyncSubsStudio/logo.svg"], ["SyncSubsStudio/logo.webp"]),
 "teleprompter": (["Teleprompter/logo.svg"], ["Teleprompter/logo.webp"]),
 "time":     (["Time/logo.svg"], ["Time/logo.webp"]),
 "topo":     (["Topo/logo.svg"], ["Topo/logo.webp"]),
 "tv":       (["TV/logo.svg"], ["TV/logo.webp"]),
 "vitae":    (["Vitae/logo.svg"], ["Vitae/logo.webp"]),
}
# stocks has a registry entry but no repository and no CNAME -- nowhere to put it.
SKIP = {"stocks"}


def main():
    import subprocess
    made = new = 0
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
    print(f"\n{made} files written ({new} new), {len(T)} sites; skipped: {', '.join(SKIP)}")

main()
