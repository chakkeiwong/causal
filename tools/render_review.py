#!/usr/bin/env python3
"""Render PDFs and contact sheets for an actual human/agent visual review."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


def main():
    state = json.loads((ROOT / "docs/program/state.json").read_text())
    reconstruction = state.get("revision") in ("3.0-reconstruction", "4.0-scientific-completion", "5.0-scope-completion", "6.0-dynamic-construction", "6.1-linkage-inference", "7.0-gap-closure", "8.0-reliability-extension", "9.0-calibration-completion", "10.0-precision-streaming")
    output_root = ROOT / ("docs/reviews/rendered-foundations" if reconstruction else "docs/reviews/rendered-v2")
    output_root.mkdir(parents=True, exist_ok=True)
    records = []
    stems = ("causal_foundations", "sponsor_reconstruction") if reconstruction else ("causal_banking_product", "sponsor_proposal")
    for stem in stems:
        pdf = ROOT / "docs" / (stem + ".pdf")
        digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
        out = output_root / (stem + "-" + digest[:16])
        out.mkdir(parents=True, exist_ok=True)
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
        n = int(re.search(r"(?m)^Pages:\s+(\d+)", info).group(1))
        subprocess.run(["pdftoppm","-scale-to","1000","-png",str(pdf),str(out/stem)],check=True,capture_output=True)
        # Hash-specific directories prevent old two-digit and new three-digit
        # page names from colliding when a later document exceeds 99 pages.
        candidates = {int(p.stem.rsplit("-", 1)[1]):p for p in out.glob(stem+"-*.png")}
        pages = [candidates[i] for i in range(1,n+1)]
        sheets = []
        for batch in range(0,n,12):
            sheet = Image.new("RGB",(1000,1480),"#d9e1e7")
            draw = ImageDraw.Draw(sheet)
            for offset,p in enumerate(pages[batch:batch+12]):
                im = Image.open(p).convert("RGB")
                im.thumbnail((316,342))
                x = (offset%3)*333+(333-im.width)//2
                y = (offset//3)*370+24
                sheet.paste(im,(x,y))
                draw.text(((offset%3)*333+12,(offset//3)*370+6),f"{stem} PDF page {batch+offset+1}",fill="black")
            target = out/f"{stem}-contact-{batch//12+1}.jpg"
            sheet.save(target,quality=90)
            sheets.append(str(target.relative_to(ROOT)))
        records.append({"pdf":str(pdf.relative_to(ROOT)),
                        "sha256":digest,
                        "pages":n,"contact_sheets":sheets,
                        "scope":"Rendered artifacts only; visual inspection is separately recorded."})
        subprocess.run(["pdftotext","-layout",str(pdf),str(ROOT/"docs/build"/(stem+".txt"))],check=True)
    receipt = "docs/reviews/foundations-render-receipt.json" if reconstruction else "docs/reviews/render-receipt.json"
    (ROOT/receipt).write_text(json.dumps(records,indent=2)+"\n")
    print(json.dumps(records))


if __name__ == "__main__":
    main()
