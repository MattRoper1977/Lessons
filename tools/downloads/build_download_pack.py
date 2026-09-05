#!/usr/bin/env python3
"""Build a deterministic, explicitly scoped lesson ZIP without changing sources.

Only explicit files and statically discoverable runtime dependencies are copied.
HTML anchors are navigation, never a licence to crawl the whole catalogue.
Dynamic JavaScript cannot be proved complete by this scanner; the report records
that limit and a browser/offline acceptance pass remains required before release.
"""
from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile


STAMP = (1980, 1, 1, 0, 0, 0)
GENERATED = {"index.html", "START_HERE.html", "PACK.json", "README_OFFLINE.txt"}
ALLOWED = {".html", ".htm", ".css", ".js", ".mjs", ".json", ".svg", ".png",
           ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".ico", ".woff", ".woff2",
           ".ttf", ".otf", ".mp4", ".webm", ".mp3", ".ogg", ".wav", ".vtt",
           ".md", ".txt", ".pdf"}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I | re.S)
CSS_IMPORT = re.compile(r"@import\s+(['\"])(.*?)\1", re.I | re.S)
# Deliberately narrow: literal runtime calls only, never every quoted filename.
JS_LITERAL = re.compile(r"(?:\bfetch\s*\(|\bimport\s*\(|\bnew\s+(?:URL|Worker|SharedWorker)\s*\()\s*(['\"])([^'\"\n]+)\1")
JS_IMPORT = re.compile(r"\b(?:import|export)\s+(?:[^;\n]*?\s+from\s+)?(['\"])([^'\"\n]+)\1")
SLOT_MOUNT = re.compile(r"MBMArtsSlots\.mount\(\s*(\{[^;\n]+\})\s*\)")
GROW_HUD_LOADER = re.compile(r'function\s+add\(src,onfail\).*?document\.body\.appendChild\(s\);', re.S)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_member(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value:
        raise ValueError("Source paths must be non-empty POSIX relative paths")
    parsed = urlsplit(value)
    parts = PurePosixPath(value).parts
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment or value.startswith("/"):
        raise ValueError(f"Source path is not repository-relative: {value}")
    if any(p in {".", ".."} or p.startswith((".", "_")) for p in parts):
        raise ValueError(f"Private path or traversal is prohibited: {value}")
    if str(PurePosixPath(value)) != value or Path(value).suffix.lower() not in ALLOWED:
        raise ValueError(f"Non-canonical or unsupported source path: {value}")
    if any(re.search(r"(?:^|[ _-])sow(?:[ _.-]|$)", p, re.I) for p in parts):
        raise ValueError(f"Scheme-of-work source is prohibited: {value}")
    return value


def strip_js_comments(text: str) -> str:
    """Preserve string literals; do not turn https:// into a line comment."""
    token = re.compile(r"('(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`(?:\\.|[^`\\])*`)|(/\*[\s\S]*?\*/|//[^\n]*)")
    return token.sub(lambda m: m.group(1) or " " * len(m.group(0)), text)


def css_refs(text: str):
    cleaned = re.sub(r"/\*[\s\S]*?\*/", "", text)
    for match in CSS_URL.finditer(cleaned):
        yield match.group(2).strip(), "css-url"
    for match in CSS_IMPORT.finditer(cleaned):
        yield match.group(2).strip(), "css-import"


def js_refs(text: str):
    cleaned = strip_js_comments(text)
    for pattern in (JS_LITERAL, JS_IMPORT):
        for match in pattern.finditer(cleaned):
            yield match.group(2), "javascript-literal"
    for match in SLOT_MOUNT.finditer(cleaned):
        try:
            config = json.loads(match.group(1))
        except ValueError:
            continue
        if isinstance(config.get("url"), str):
            yield config["url"], "award-slot-reader"
    # The older GROW lessons load the HUD through this reviewed tiny helper.
    # A generic every-string scan would create dependencies from teaching prose.
    if GROW_HUD_LOADER.search(cleaned):
        for match in re.finditer(r'\badd\(\s*([\"\'])(/?hud\.js)\1', cleaned):
            yield match.group(2), "grow-hud-loader"


class Dependencies(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.anchors = []
        self.inline = None
        self.base = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "base" and a.get("href"):
            self.base = a["href"]
        if tag in {"script", "img", "audio", "video", "source", "track", "iframe", "embed"} and a.get("src"):
            self.refs.append((a["src"], tag + "-src"))
        if tag == "object" and a.get("data"):
            self.refs.append((a["data"], "object-data"))
        if tag == "video" and a.get("poster"):
            self.refs.append((a["poster"], "video-poster"))
        if tag == "link" and a.get("href") and set((a.get("rel") or "").lower().split()) & {"stylesheet", "icon", "preload", "modulepreload"}:
            self.refs.append((a["href"], "link-" + a.get("rel", "")))
        if tag in {"img", "source"} and a.get("srcset"):
            # A data URL is already embedded. Ordinary srcsets use comma-separated URLs.
            if not a["srcset"].lstrip().startswith("data:"):
                for candidate in a["srcset"].split(","):
                    if candidate.strip():
                        self.refs.append((candidate.strip().split()[0], "srcset"))
        if a.get("style"):
            self.refs.extend(css_refs(a["style"]))
        if tag == "a" and a.get("href"):
            self.anchors.append(a["href"])
        if tag == "style":
            self.inline = "css"
        elif tag == "script" and a.get("type", "").lower() in {"", "text/javascript", "application/javascript", "module"}:
            self.inline = "js"

    def handle_endtag(self, tag):
        if tag in {"style", "script"}:
            self.inline = None

    def handle_data(self, data):
        if self.inline == "css":
            self.refs.extend(css_refs(data))
        elif self.inline == "js":
            self.refs.extend(js_refs(data))


def resolve(owner: str, raw: str):
    """Root-relative URLs belong to the Site origin, not the Lessons subtree."""
    url = urlsplit(html.unescape(raw).strip())
    if url.scheme in {"data", "blob"} or (not url.path and not url.netloc):
        return "embedded", None
    if url.scheme or url.netloc:
        return "external", raw
    path = unquote(url.path)
    if path.startswith("/"):
        return "site-root", path
    if "\\" in path or "\0" in path:
        return "unsafe", path
    local = posixpath.normpath(posixpath.join(posixpath.dirname(owner), path))
    try:
        return "local", safe_member(local)
    except ValueError:
        return "unsafe", local


class LessonLabel(HTMLParser):
    """Read authored lesson metadata or its opening heading, never its filename."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.config = []
        self.heading = []
        self.in_config = False
        self.in_heading = False
        self.heading_finished = False

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("id") == "lesson-config":
            self.in_config = True
        if tag == "h1" and not self.heading_finished:
            self.in_heading = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_config = False
        if tag == "h1" and self.in_heading:
            self.in_heading = False
            self.heading_finished = True

    def handle_data(self, value):
        if self.in_config:
            self.config.append(value)
        elif self.in_heading:
            self.heading.append(value)


def lesson_label(data: bytes) -> str | None:
    parser = LessonLabel()
    parser.feed(data.decode("utf-8"))
    if parser.config:
        config = json.loads("".join(parser.config))
        label = config.get("title")
        if isinstance(label, str) and label.strip():
            return " ".join(label.split())
    heading = " ".join(" ".join(parser.heading).split())
    return heading or None


def portal(title: str, entries: list[str], owner: str = "index.html",
           labels: dict | None = None, slots_file: str | None = None) -> bytes:
    labels = labels or {}
    links = "".join(f'<li><a href="{html.escape(posixpath.relpath(p, posixpath.dirname(owner) or "."), quote=True)}">{html.escape(labels.get(p) or f"Open lesson {i + 1}")}</a></li>' for i, p in enumerate(entries))
    slots = ("<p>For Arts Award session details, use Teacher tools to choose the included "
             f"{html.escape(slots_file)}. This snapshot does not confirm an event or booking.</p>") if slots_file else ""
    return ("<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{html.escape(title)} · Downloaded pack</title><style>body{{font:18px/1.5 system-ui;background:#f4f2ed;color:#172d38;max-width:900px;margin:auto;padding:24px}}a{{color:#163d54;display:inline-block;min-height:44px;box-sizing:border-box;padding:8px}}li{{margin:8px 0}}a:focus-visible{{outline:3px solid #b64e13}}h1{{line-height:1.2}}</style>"
        f"<main><p>Made by Matt · Downloaded lesson pack</p><h1>{html.escape(title)}</h1><p>Open these lessons after extracting the whole ZIP. Keep its folders together.</p><ul>{links}</ul>"
        f"<p>Video websites and other external links need an internet connection.</p>{slots}</main></html>\n").encode()


def continuation_page(pack_title: str, member: str, record: dict) -> bytes:
    """An explicit online continuation; never pretend another lesson is bundled."""
    url = urlsplit(record.get('onlineUrl', ''))
    if url.scheme != 'https' or url.hostname != 'madebymatt.uk' or not url.path.startswith('/Lessons/') or url.username or url.password:
        raise ValueError('Continuation must name an explicit canonical online lesson')
    if not isinstance(record.get('title'), str) or not record['title'].strip():
        raise ValueError('Continuation needs its actual lesson title')
    back = posixpath.relpath('START_HERE.html', posixpath.dirname(member) or '.')
    return (f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(record["title"])} · Another lesson pack</title>'
            '<style>body{font:18px/1.5 system-ui;color:#172d38;background:#f4f2ed;max-width:800px;margin:auto;padding:24px}a{display:inline-block;margin:12px 0;padding:8px;color:#163d54}a:focus-visible{outline:3px solid #b64e13}</style>'
            f'<main><p>{html.escape(pack_title)} · Downloaded pack</p><h1>This lesson is in another term’s pack</h1>'
            f'<p>{html.escape(record["title"])} is outside this download. Return to the lessons in this pack, or open that lesson online when you have an internet connection.</p>'
            f'<p><a href="{html.escape(back,quote=True)}">Back to this pack</a></p>'
            f'<p><a href="{html.escape(record["onlineUrl"],quote=True)}">Open {html.escape(record["title"])} online · needs internet</a></p></main></html>\n').encode()


def build(repo: Path, definition: dict, destination: Path | None = None) -> dict:
    repo = repo.resolve()
    if not repo.is_dir():
        raise ValueError("Repository source does not exist")
    if not isinstance(definition, dict) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", str(definition.get("id", ""))):
        raise ValueError("Pack needs a safe id")
    if not isinstance(definition.get("title"), str) or not definition["title"].strip():
        raise ValueError("Pack needs a title")
    files = definition.get("files")
    if not isinstance(files, list) or not files:
        raise ValueError("Pack needs an explicit non-empty files list")
    explicit = [safe_member(p) for p in files]
    if len(explicit) != len(set(explicit)):
        raise ValueError("Duplicate explicitly requested members")
    if len({p.casefold() for p in explicit}) != len(explicit):
        raise ValueError("Case-folding collision is not portable")
    entry = safe_member(definition.get("entry", ""))
    if entry not in explicit or Path(entry).suffix.lower() not in {".html", ".htm"}:
        raise ValueError("Entry must be an explicitly listed HTML file")
    if GENERATED.intersection(explicit):
        raise ValueError("Source path collides with generated pack entry files")
    queue = list(explicit)
    members = {}
    sources = []
    errors = []
    dependencies = []
    external = []
    anchors = []
    warnings = []
    while queue:
        member = queue.pop(0)
        if member in members:
            continue
        source = repo / member
        # Reject a symlink even if it currently resolves inside the repository.
        if any(p.is_symlink() for p in [source, *source.parents] if p != repo.parent) or not source.resolve().is_relative_to(repo):
            errors.append({"file": member, "reason": "symlink or source escape"})
            continue
        if not source.is_file():
            errors.append({"file": member, "reason": "missing local dependency"})
            continue
        data = source.read_bytes()
        if member == "tools/artsaward/SLOTS.json":
            try:
                slots = json.loads(data)
                if slots.get("schema") != "arts-award-slots-v1" or not slots.get("slots") or any(s.get("entries") != [] for s in slots["slots"].values()):
                    raise ValueError("Only the canonical empty, unconfirmed slot register may be packaged")
            except (ValueError, AttributeError, TypeError) as exc:
                errors.append({"file": member, "reason": str(exc)})
                continue
        members[member] = data
        sources.append({"path": member, "bytes": len(data), "sha256": digest(data)})
        suffix = Path(member).suffix.lower()
        refs = []
        if suffix in {".html", ".htm", ".svg", ".css", ".js", ".mjs"}:
            try:
                text = data.decode("utf-8")
            except UnicodeError:
                errors.append({"file": member, "reason": "Text source is not UTF-8"})
                continue
            if suffix in {".html", ".htm", ".svg"}:
                parser = Dependencies()
                parser.feed(text)
                if parser.base:
                    errors.append({"file": member, "reason": "HTML base URL needs an explicit offline adaptation", "url": parser.base})
                refs = parser.refs
                anchors.extend((member, href) for href in parser.anchors)
            elif suffix == ".css":
                refs = list(css_refs(text))
            else:
                refs = list(js_refs(text))
        for raw, kind in refs:
            scope, target = resolve(member, raw)
            edge = {"from": member, "url": raw, "kind": kind, "scope": scope, "target": target}
            dependencies.append(edge)
            if scope == "local":
                if target in GENERATED:
                    errors.append({**edge, "reason": "Runtime dependency collides with generated portal"})
                elif target not in members and target not in queue:
                    queue.append(target)
            elif scope == "external":
                external.append(edge)
                errors.append({**edge, "reason": "External runtime dependency cannot be bundled without an approved local source"})
            elif scope in {"site-root", "unsafe"}:
                errors.append({**edge, "reason": "Origin-root dependency is not a Lessons file" if scope == "site-root" else "Dependency escapes public pack scope"})

    continuations = definition.get('continuations', {})
    if not isinstance(continuations, dict):
        raise ValueError('Continuations must be an explicit member-to-lesson map')
    for name, record in continuations.items():
        safe_member(name)
        if name in members or name in GENERATED or Path(name).suffix.lower() != '.html':
            raise ValueError('Continuation collides with a copied or generated member')
        members[name] = continuation_page(definition['title'], name, record)
    nav = []
    aliases = set()
    for owner, raw in anchors:
        scope, target = resolve(owner, raw)
        row = {"from": owner, "url": raw, "scope": scope, "target": target}
        if scope == "local" and target not in members and PurePosixPath(target).name.lower() in {"index.html", "start_here.html"}:
            aliases.add(target)
            row["resolution"] = "generated-pack-home"
        elif scope == "local" and target not in members:
            row["resolution"] = "outside-explicit-pack-not-crawled"
        elif scope == "local":
            row["resolution"] = "included"
        nav.append(row)
    menu = definition.get("lessons", explicit)
    if not isinstance(menu, list) or any(p not in explicit for p in menu):
        raise ValueError("Menu lessons must be explicit pack members")
    entries = [entry] + [p for p in menu if p != entry and Path(p).suffix.lower() in {".html", ".htm"}]
    labels = {p: lesson_label(members[p]) for p in entries if p in members}
    slots_file = "tools/artsaward/SLOTS.json" if "tools/artsaward/SLOTS.json" in members else None
    for name in sorted(aliases | {"index.html", "START_HERE.html"}):
        if name not in members:
            members[name] = portal(definition["title"], entries, name, labels, slots_file)
    members["README_OFFLINE.txt"] = ("Extract the whole ZIP, then open START_HERE.html. Keep the folder structure.\n"
        "Source lessons are unchanged. Home links lead to this pack, not the whole online catalogue.\n"
        "External navigation links (including videos) need the internet. Browser file:// restrictions can affect fetched data; Arts Award Teacher tools accepts the included SLOTS.json file manually. No event is confirmed by this pack.\n"
        "This package resolves statically discoverable runtime dependencies. Dynamic script behavior still needs an offline browser acceptance check.\n").encode()
    if len({p.casefold() for p in members}) != len(members):
        errors.append({"reason": "Case-folding collision among collected members"})
    report = {"schema": "lesson-download-pack-v1", "id": definition["id"], "title": definition["title"], "entry": entry,
        "status": "REFUSED" if errors else "BUILT", "sourceMutation": False,
        "definitionSha256": digest(json.dumps(definition, sort_keys=True, separators=(",", ":")).encode()),
        "sources": sorted(sources, key=lambda r: r["path"]), "dependencies": sorted(dependencies, key=lambda r: (r["from"], r["url"], r["kind"])),
        "navigation": sorted(nav, key=lambda r: (r["from"], r["url"])), "generatedHomeAliases": sorted(aliases), "errors": errors,
        "onlineContinuations": continuations,
        "warnings": warnings, "acceptanceLimit": "Static dependency packaging only; dynamic JavaScript and real offline interactions require browser acceptance."}
    if errors:
        return report
    members["PACK.json"] = (json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode()
    report["memberCount"] = len(members)
    report["members"] = [{"path": p, "bytes": len(data), "sha256": digest(data)} for p, data in sorted(members.items())]
    if destination:
        destination = destination.resolve()
        if destination.is_relative_to(repo):
            raise ValueError("Build output must be outside the read-only source repository")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".zip", delete=False) as tmp:
            temp = Path(tmp.name)
        try:
            with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                for member, data in sorted(members.items()):
                    info = zipfile.ZipInfo(member, STAMP)
                    info.create_system = 3
                    info.external_attr = 0o100644 << 16
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, data, compresslevel=9)
            os.replace(temp, destination)
        finally:
            temp.unlink(missing_ok=True)
        report["zipBytes"] = destination.stat().st_size
        report["zipSha256"] = digest(destination.read_bytes())
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--definition", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    try:
        result = build(args.repo, json.loads(args.definition.read_text()), args.output)
    except (ValueError, OSError) as exc:
        result = {"status": "REFUSED", "errors": [{"reason": str(exc)}]}
    if args.report.resolve().is_relative_to(args.repo.resolve()):
        raise SystemExit("Report must remain outside the read-only source repository")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in ("id", "status", "memberCount", "zipBytes", "zipSha256", "errors") if k in result}))
    return 0 if result["status"] == "BUILT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
