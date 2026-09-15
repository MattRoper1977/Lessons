"""Check actual browser PDF output, including the first-use organiser regression."""
import json
from pathlib import Path
import sys

import fitz


def inspect(directory):
    results = []
    expected = {
        **{f"pupil-{route}.pdf": 6 for route in ("supported", "standard", "stretch")},
        "organiser.pdf": 1, "staff.pdf": 1, "answers.pdf": 2,
        **{f"arrival-answers-{route}.pdf": 1 for route in ("supported", "standard", "stretch")},
    }
    organiser_phrases = ["KNOWLEDGE ORGANISER", "LEARNING OBJECTIVE",
                         "Read the whole sugar line", "A claim the evidence can support"]
    for name, count in expected.items():
        with fitz.open(directory / name) as pdf:
            texts = [page.get_text() for page in pdf]
            failures = []
            if len(pdf) != count:
                failures.append(f"Expected {count} pages, got {len(pdf)}")
            for index, text in enumerate(texts, 1):
                if not text.strip():
                    failures.append(f"Page {index} has no readable text")
            if name == "organiser.pdf" or name.startswith("pupil-"):
                first = " ".join(texts[0].split()) if texts else ""
                for phrase in organiser_phrases:
                    if phrase not in first:
                        failures.append(f"First page missing organiser text: {phrase}")
            if name.startswith("pupil-") and texts:
                route = name.removeprefix("pupil-").removesuffix(".pdf").title()
                if texts[-1].count(f"Sugar evidence · {route}") != 2:
                    failures.append("Final page must contain two complete exit tickets")
                if texts[-1].count("Next lesson: Body Science Checkpoint") != 2:
                    failures.append("Both exit tickets must retain their final line")
                # Keep actual exit text clear of the paper edges (10 mm).
                page = pdf[-1]
                margin = 10 * 72 / 25.4
                for word in page.get_text("words"):
                    x0, y0, x1, y1 = word[:4]
                    if min(x0, y0, page.rect.width-x1, page.rect.height-y1) < margin:
                        failures.append("Exit text enters the 10 mm paper-edge margin")
                        break
            results.append({"file": name, "pages": len(pdf),
                            "textCharacters": [len(t.strip()) for t in texts],
                            "failures": failures})
    return {"status": "FAIL" if any(r["failures"] for r in results) else "PASS",
            "files": results,
            "limits": ["Text and pagination checks do not replace visual or screen-reader review."]}


if __name__ == "__main__":
    directory = Path(sys.argv[1])
    result = inspect(directory)
    (directory / "pdf-report.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
    raise SystemExit(result["status"] != "PASS")
