#!/usr/bin/env python3
"""Adversarial packaging controls; no repository or source-file mutations."""
import json
from pathlib import Path
import tempfile
import zipfile

from build_download_pack import build, digest, lesson_label, portal


def controls():
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        repo = base / "repo"
        repo.mkdir()
        def put(name, value):
            dest = repo / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(value.encode() if isinstance(value, str) else value)
        def definition(files=None):
            return {"id": "test", "title": "A safe <pack>", "entry": "subject/lessons/start.html", "files": files or ["subject/lessons/start.html"]}
        def assert_control(name, ok):
            assert ok, name
            results.append({"id": name, "pass": True})
        def rejects(name, d):
            try:
                build(repo, d)
            except ValueError:
                assert_control(name, True)
            else:
                raise AssertionError(name)

        put("subject/lessons/start.html", '<link rel="stylesheet" href="../css/a.css"><a href="../../index.html">Home</a><a href="not-in-pack.html">Elsewhere</a><script>// fetch("missing.json")\nconst example = "https://example.com";</script>')
        put("subject/css/a.css", '@import "nested/b.css"; .a {background:url("../assets/pixel.png")}')
        put("subject/css/nested/b.css", '@font-face {src:url("../../assets/font.woff2")}')
        put("subject/assets/pixel.png", b"synthetic-png")
        put("subject/assets/font.woff2", b"synthetic-font")
        before = {str(p.relative_to(repo)): digest(p.read_bytes()) for p in repo.rglob("*") if p.is_file()}
        a = build(repo, definition(), base / "a.zip")
        b = build(repo, definition(), base / "b.zip")
        assert_control("nested-css-assets-resolved", a["status"] == "BUILT" and len(a["sources"]) == 5)
        assert_control("zip-byte-determinism", a["zipSha256"] == b["zipSha256"])
        assert_control("commented-script-not-dependency", all("missing.json" not in x["url"] for x in a["dependencies"]))
        assert_control("arbitrary-anchors-never-crawled", any(n.get("resolution") == "outside-explicit-pack-not-crawled" for n in a["navigation"]) and not any(s["path"].endswith("not-in-pack.html") for s in a["sources"]))
        with zipfile.ZipFile(base / "a.zip") as z:
            names = z.namelist()
            assert_control("unique-sorted-fixed-time-members", names == sorted(set(names)) and all(i.date_time == (1980,1,1,0,0,0) for i in z.infolist()))
            assert_control("generated-home-relative-entry", b'href="subject/lessons/start.html"' in z.read("index.html") and b"A safe &lt;pack&gt;" in z.read("index.html"))
            assert_control("source-bytes-preserved", all(z.read(p) == (repo / p).read_bytes() for p in before))
        assert_control("source-tree-unchanged", before == {str(p.relative_to(repo)): digest(p.read_bytes()) for p in repo.rglob("*") if p.is_file()})
        label = lesson_label(b'<title>Stale donor title</title><h1>Old heading</h1><script id="lesson-config">{"title":"Actual taught lesson"}</script>')
        assert_control("authored-title-over-stale-donor-title", label == "Actual taught lesson")
        assert_control("opening-heading-without-config-title", lesson_label(b'<title>Stale title</title><h1>Actual <span>lesson</span></h1><h1>Later stage</h1>') == "Actual lesson")
        assert_control("filename-never-becomes-menu-week", b'W99' not in portal('Pack', ['subject/W99.html']).split(b'>Open lesson')[1] and b'>Open lesson 1<' in portal('Pack', ['subject/W99.html']))
        assert_control("lesson-title-is-escaped", b'&lt;script&gt;' in portal('Pack', ['x.html'], labels={'x.html':'<script>'}))
        put("subject/lessons/start.html", '<h1>Current lesson</h1><a href="START_HERE.html">Pack</a><a href="next.html">Next</a>')
        scoped = definition()
        scoped['continuations'] = {'subject/lessons/next.html': {'title':'Next term lesson','onlineUrl':'https://madebymatt.uk/Lessons/subject/lessons/next.html'}}
        linked = build(repo, scoped, base/'linked.zip')
        with zipfile.ZipFile(base/'linked.zip') as z:
            assert_control('local-start-alias-opens-current-pack', b'>Current lesson<' in z.read('subject/lessons/START_HERE.html'))
            page = z.read('subject/lessons/next.html')
            assert_control('cross-term-link-has-honest-local-continuation', b'outside this download' in page and b'needs internet' in page and b'href="../../START_HERE.html"' in page)
            assert_control('continuation-does-not-rewrite-lesson', z.read('subject/lessons/start.html') == (repo/'subject/lessons/start.html').read_bytes())
        bad = {**scoped, 'continuations': {'subject/lessons/next.html': {'title':'Unsafe','onlineUrl':'javascript:alert(1)'}}}
        rejects('executable-continuation-refused', bad)
        rejects("explicit-duplicate-refused", definition(["subject/lessons/start.html", "subject/lessons/start.html"]))
        rejects("explicit-parent-traversal-refused", definition(["subject/lessons/start.html", "../outside.html"]))
        rejects("explicit-absolute-path-refused", definition(["subject/lessons/start.html", "/outside.html"]))
        rejects("explicit-private-source-refused", definition(["subject/lessons/start.html", "_sownb/private.json"]))
        rejects("workbook-refused", definition(["subject/lessons/start.html", "Build SOW.xlsx"]))
        rejects("case-collision-refused", definition(["subject/lessons/start.html", "subject/lessons/START.html"]))
        put("subject/lessons/start.html", '<script src="../../../outside.js"></script>')
        c = build(repo, definition(), base / "escape.zip")
        assert_control("dependency-parent-escape-refused", c["status"] == "REFUSED" and not (base / "escape.zip").exists())
        put("subject/lessons/start.html", '<script src="/%68ud.js"></script>')
        c = build(repo, definition())
        assert_control("encoded-site-root-not-repo-root", c["status"] == "REFUSED" and c["errors"][0]["target"] == "/hud.js")
        put("subject/lessons/start.html", '<img src="../../_sownb/private.png">')
        assert_control("dependency-private-path-refused", build(repo, definition())["status"] == "REFUSED")
        put("subject/lessons/start.html", '<script src="https://cdn.example.test/library.js"></script>')
        assert_control("external-runtime-source-refused", build(repo, definition())["status"] == "REFUSED")
        put("subject/lessons/start.html", '<script src="missing.js"></script>')
        assert_control("missing-local-runtime-refused", build(repo, definition())["status"] == "REFUSED")
        put("subject/lessons/start.html", '<script src="alias.js"></script>')
        (repo / "subject/lessons/alias.js").symlink_to(repo / "subject/css/a.css")
        assert_control("symlink-refused", build(repo, definition())["status"] == "REFUSED")
        put("subject/lessons/start.html", '<script>MBMArtsSlots.mount({"url":"../../tools/artsaward/SLOTS.json"});</script>')
        put("tools/artsaward/SLOTS.json", json.dumps({"schema":"arts-award-slots-v1", "slots":{"EVENT_SLOT":{"entries":[]}}}))
        c = build(repo, definition())
        assert_control("empty-canonical-slot-register-included", c["status"] == "BUILT" and any(s["path"] == "tools/artsaward/SLOTS.json" for s in c["sources"]))
        put("tools/artsaward/SLOTS.json", json.dumps({"schema":"arts-award-slots-v1", "slots":{"EVENT_SLOT":{"entries":[{"name":"Private Visit"}]}}}))
        assert_control("populated-slot-data-refused", build(repo, definition())["status"] == "REFUSED")
        put("subject/lessons/start.html", '<script id="grow-hud-loader">(function(){function add(src,onfail){var s=document.createElement("script");s.src=src;if(onfail)s.onerror=onfail;document.body.appendChild(s);}add("/hud.js",function(){add("hud.js");});})();</script>')
        c = build(repo, definition())
        assert_control("real-grow-helper-loader-detected", c['status'] == 'REFUSED' and len([e for e in c['dependencies'] if e['kind'] == 'grow-hud-loader']) == 2)
    return results


if __name__ == "__main__":
    rows = controls()
    target = Path(__file__).with_name("controls.json")
    target.write_text(json.dumps({"controls": rows, "passed": len(rows), "failed": 0}, indent=2) + "\n")
    print(f"{len(rows)}/{len(rows)} packaging controls passed")
