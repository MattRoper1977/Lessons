#!/usr/bin/env python3
"""Create labelled RSH viewport/A4 contact sheets and extract measured ink/text data."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]


def font(size: int, bold: bool = False):
    names = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


TITLE = font(28, True)
LABEL = font(18, True)


def ink(image: Image.Image) -> float:
    gray = image.convert("L")
    histogram = gray.histogram()
    total = image.width * image.height
    return round(sum(histogram[:245]) / total, 6)


def thumb(image: Image.Image, width: int = 250, height: int = 350) -> Image.Image:
    out = image.convert("RGB").copy()
    out.thumbnail((width, height), Image.Resampling.LANCZOS)
    return out


def viewport_sheet(directory: Path, slug: str, viewport: str, slide_count: int) -> tuple[Path, list[dict]]:
    entries = []
    metrics = []
    for index in range(1, slide_count + 1):
        for position in ("top", "bottom"):
            source = directory / f"{viewport}-slide-{index:02d}-{position}.png"
            with Image.open(source) as image:
                entries.append((f"S{index} {position}", thumb(image)))
                metrics.append({"slide": index, "position": position, "inkCoverage": ink(image)})
    cell_w, cell_h = 274, 392
    cols = 3
    rows = (len(entries) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * cell_w, 62 + rows * cell_h), "#e9edf1")
    draw = ImageDraw.Draw(canvas)
    draw.text((14, 12), f"{slug} · {viewport}", font=TITLE, fill="#17223b")
    for number, (label, image) in enumerate(entries):
        row, col = divmod(number, cols)
        x, y = col * cell_w + 12, 62 + row * cell_h + 8
        draw.text((x, y), label, font=LABEL, fill="#17223b")
        canvas.paste(image, (x, y + 28))
    target = directory / f"contact-{viewport}.png"
    canvas.save(target, optimize=True)
    return target, metrics


def normalise_ligatures(text: str) -> str:
    return text.translate(str.maketrans({"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}))


def pdf_sheet(directory: Path, slug: str, pdf: Path) -> tuple[Path, dict]:
    reader = PdfReader(pdf)
    pypdf_pages = [normalise_ligatures(page.extract_text() or "") for page in reader.pages]
    poppler = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], check=True, text=True, capture_output=True).stdout
    poppler_pages = [normalise_ligatures(part) for part in poppler.split("\f") if part.strip()]
    rendered = []
    with tempfile.TemporaryDirectory(prefix="rsh-a4-") as temp:
        prefix = Path(temp) / "page"
        subprocess.run(["pdftoppm", "-r", "96", "-png", str(pdf), str(prefix)], check=True, capture_output=True)
        for item in sorted(Path(temp).glob("page-*.png")):
            with Image.open(item) as image:
                rendered.append((thumb(image, 390, 560), ink(image)))
    gap, top = 18, 62
    canvas = Image.new("RGB", (max(420, len(rendered) * 408 + gap), 640), "#dfe4e8")
    draw = ImageDraw.Draw(canvas)
    draw.text((14, 12), f"{slug} · A4", font=TITLE, fill="#17223b")
    x = gap
    for index, (image, _) in enumerate(rendered, 1):
        draw.text((x, top), f"Page {index}", font=LABEL, fill="#17223b")
        canvas.paste(image, (x, top + 28))
        x += 408
    target = directory / "contact-a4.png"
    canvas.save(target, optimize=True)
    return target, {
        "pdf": str(pdf.relative_to(ROOT)),
        "pageCount": len(reader.pages),
        "pypdfPageChars": [len(page.strip()) for page in pypdf_pages],
        "pdftotextPageChars": [len(page.strip()) for page in poppler_pages],
        "pypdfTextSha256": hashlib.sha256(re.sub(r"\s+", " ", "\f".join(pypdf_pages)).strip().encode()).hexdigest(),
        "pdftotextTextSha256": hashlib.sha256(re.sub(r"\s+", " ", "\f".join(poppler_pages)).strip().encode()).hexdigest(),
        "inkCoverage": [coverage for _, coverage in rendered],
    }


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "references"
    root = ROOT / "_sownb/rsh/output" / mode
    report = json.loads((root / "render_metrics.json").read_text(encoding="utf-8"))
    output = {"mode": mode, "targets": []}
    for row in report["targets"]:
        directory = root / row["slug"]
        item = {"slug": row["slug"], "viewports": {}, "print": None, "contactSheets": []}
        for viewport in row["viewports"]:
            target, measured = viewport_sheet(directory, row["slug"], viewport["viewport"]["name"], len(viewport["slides"]))
            item["viewports"][viewport["viewport"]["name"]] = measured
            item["contactSheets"].append(str(target.relative_to(ROOT)))
        pdf = ROOT / row["print"]["pdf"]
        target, measured = pdf_sheet(directory, row["slug"], pdf)
        item["print"] = measured
        item["contactSheets"].append(str(target.relative_to(ROOT)))
        output["targets"].append(item)
    (root / "contact_metrics.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"mode": mode, "targets": len(output["targets"]), "sheets": sum(len(x["contactSheets"]) for x in output["targets"])}, indent=2))


if __name__ == "__main__":
    main()
