#!/usr/bin/env python3
"""Whole-repository audit for the Lessons GitHub Pages estate.

The tool is intentionally read-only. It inventories every tracked file, validates
web/code/document formats, resolves local references against the combined
madebymatt.uk + /Lessons/ layout, opens HTML entry points in a real browser, and
checks publication evidence against the live site.

It writes machine-readable evidence and a human report to --output. No repository
file is changed by the audit itself.
"""

from __future__ import annotations

import argparse
import ast
import concurrent.futures
import contextlib
import csv
import dataclasses
import datetime as dt
import hashlib
import html as html_module
import http.server
import io
import json
import mimetypes
import os
import pathlib
import posixpath
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import tomllib
import traceback
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter, defaultdict
from typing import Any, Iterable, Iterator, Sequence

try:
    import html5lib  # type: ignore
except Exception:  # pragma: no cover - dependency gate reports this
    html5lib = None

try:
    import tinycss2  # type: ignore
except Exception:  # pragma: no cover
    tinycss2 = None

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

try:
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover
    jsonschema = None

try:
    from PIL import Image  # type: ignore
except Exception:  # pragma: no cover
    Image = None

try:
    from pypdf import PdfReader  # type: ignore
except Exception:  # pragma: no cover
    PdfReader = None


TEXT_EXTENSIONS = {
    ".html", ".htm", ".css", ".js", ".mjs", ".cjs", ".json", ".jsonl",
    ".py", ".sh", ".bash", ".zsh", ".fish", ".md", ".txt", ".csv", ".tsv",
    ".xml", ".svg", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".conf",
    ".scss", ".sass", ".less", ".sql", ".webmanifest", ".map", ".gitignore",
    ".gitattributes", ".editorconfig", ".properties", ".bat", ".ps1",
}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".ico", ".avif"}
OFFICE_ZIP_EXTENSIONS = {".docx", ".xlsx", ".pptx", ".odt", ".ods", ".odp", ".epub"}
ARCHIVE_EXTENSIONS = {".zip"}
MEDIA_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".mp4", ".webm", ".mov", ".mkv", ".avi"}
FONT_EXTENSIONS = {".woff", ".woff2", ".ttf", ".otf", ".eot"}
SCRIPT_TYPES = {
    "", "text/javascript", "application/javascript", "application/ecmascript",
    "text/ecmascript", "module",
}
NON_JS_SCRIPT_TYPES = {
    "application/json", "application/ld+json", "application/importmap+json",
    "importmap", "speculationrules", "text/template", "text/x-template",
}
EXCLUDED_PUBLIC_SEGMENTS = {
    ".git", ".github", "node_modules", "vendor", "vendors", "test", "tests",
    "tools", "reports", "quality", "fixtures", "fixture", "coverage",
}
KNOWN_EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "sms", "data", "blob", "javascript"}
WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))
}
SEVERE_HTML5_CODES = {
    "duplicate-attribute", "expected-closing-tag-but-got-eof", "eof-in-element-that-can-contain-only-text",
    "unexpected-null-character", "invalid-codepoint", "invalid-character-in-attribute-name",
    "unexpected-character-in-unquoted-attribute-value", "unexpected-end-tag", "end-tag-too-early",
}
SAFE_BUTTON_WORDS = re.compile(r"\b(next|continue|start|play|begin|enter|open|launch|ready|go)\b", re.I)
DESTRUCTIVE_BUTTON_WORDS = re.compile(r"\b(delete|remove|reset|clear|erase|wipe|submit|send|buy|purchase|logout|sign out)\b", re.I)
URL_ATTRS = {"href", "src", "poster", "action", "data-src", "data-href", "data-url", "formaction"}
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("github-token", re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{30,}\b")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("stripe-secret", re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9]{20,}\b")),
]


@dataclasses.dataclass(slots=True)
class Issue:
    severity: str
    category: str
    path: str
    message: str
    line: int | None = None
    details: str | None = None
    blocking: bool = False

    def as_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass(slots=True)
class RefRecord:
    source: str
    attribute: str
    value: str
    line: int | None = None
    public_source: bool = False


@dataclasses.dataclass(slots=True)
class HtmlRecord:
    path: str
    ids: set[str]
    duplicate_ids: list[str]
    refs: list[RefRecord]
    public: bool
    title: str
    lang: str
    has_viewport: bool
    has_doctype: bool
    reduced_motion_declared: bool
    visible_control_count: int = 0
    unnamed_control_count: int = 0


class Audit:
    def __init__(self, root: pathlib.Path, site_root: pathlib.Path, output: pathlib.Path, strict: bool, published_ref: str) -> None:
        self.root = root.resolve()
        self.site_root = site_root.resolve()
        self.output = output.resolve()
        self.strict = strict
        self.published_ref = published_ref
        self.issues: list[Issue] = []
        self.metrics: dict[str, Any] = {}
        self.html: dict[str, HtmlRecord] = {}
        self.references: list[RefRecord] = []
        self.resolved_public_targets: set[str] = set()
        self.browser_results: list[dict[str, Any]] = []
        self.live_results: list[dict[str, Any]] = []
        self.site_checks: dict[str, Any] = {}
        self.inventory: list[dict[str, Any]] = []
        self._text_cache: dict[str, str] = {}
        self._file_set: set[str] = set()
        self._site_file_set: set[str] = set()
        self._casefold_files: dict[str, list[str]] = defaultdict(list)
        self._casefold_site_files: dict[str, list[str]] = defaultdict(list)
        self._lock = threading.Lock()

    def add(
        self,
        severity: str,
        category: str,
        path: str,
        message: str,
        *,
        line: int | None = None,
        details: str | None = None,
        blocking: bool | None = None,
    ) -> None:
        if blocking is None:
            blocking = severity == "error"
        self.issues.append(Issue(severity, category, path, message, line, details, blocking))

    @property
    def blocking_count(self) -> int:
        return sum(1 for issue in self.issues if issue.blocking)

    def run(self, browser: bool, live: bool, browser_modes: Sequence[str], page_timeout: float, settle: float) -> int:
        self.output.mkdir(parents=True, exist_ok=True)
        self.metrics["published_ref"] = self.published_ref
        self._check_dependencies(browser)
        files = self._tracked_files()
        self._index_site_files()
        self._inventory_files(files)
        self._validate_files(files)
        self._validate_resources_schema()
        self._resolve_all_references()
        self._check_site_repository()
        if browser:
            self._browser_probe(browser_modes, page_timeout, settle)
        if live:
            self._live_probe()
        self._write_outputs()
        return 1 if self.blocking_count else 0

    def _check_dependencies(self, browser: bool) -> None:
        dependencies = {
            "html5lib": html5lib,
            "tinycss2": tinycss2,
            "yaml": yaml,
            "jsonschema": jsonschema,
            "Pillow": Image,
            "pypdf": PdfReader,
        }
        missing = [name for name, module in dependencies.items() if module is None]
        if missing:
            self.add("error", "environment", "<runner>", f"Missing audit dependencies: {', '.join(missing)}")
        if not shutil.which("node"):
            self.add("error", "environment", "<runner>", "Node.js is unavailable; JavaScript syntax cannot be checked")
        if not shutil.which("bash"):
            self.add("error", "environment", "<runner>", "bash is unavailable; shell syntax cannot be checked")
        if browser:
            try:
                import selenium  # noqa: F401  # type: ignore
            except Exception as exc:
                self.add("error", "environment", "<runner>", "Selenium is unavailable; browser pass cannot run", details=str(exc))
            if not any(shutil.which(name) for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")):
                self.add("error", "environment", "<runner>", "No Chrome/Chromium executable was found")

    def _tracked_files(self) -> list[pathlib.Path]:
        proc = subprocess.run(
            ["git", "ls-files", "-z"], cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
        )
        if proc.returncode != 0:
            self.add("error", "git", "<repository>", "git ls-files failed", details=proc.stderr.decode("utf-8", "replace"))
            return []
        names = [name for name in proc.stdout.decode("utf-8", "surrogateescape").split("\0") if name]
        files: list[pathlib.Path] = []
        for name in names:
            path = self.root / name
            if not path.exists() and not path.is_symlink():
                self.add("error", "git", name, "Tracked path is absent from the checkout")
                continue
            if path.is_file() or path.is_symlink():
                files.append(path)
                self._file_set.add(name)
                self._casefold_files[name.casefold()].append(name)
        try:
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        except Exception:
            commit = "unknown"
        self.metrics["lessons_commit"] = commit
        self.metrics["tracked_file_count"] = len(files)
        for folded, paths in sorted(self._casefold_files.items()):
            if len(paths) > 1:
                self.add("error", "path", paths[0], "Case-insensitive path collision", details=" | ".join(paths))
        return files

    def _index_site_files(self) -> None:
        if not self.site_root.exists():
            self.add("error", "site-config", str(self.site_root), "Website repository checkout is missing")
            return
        for path in self.site_root.rglob("*"):
            if ".git" in path.parts or not path.is_file():
