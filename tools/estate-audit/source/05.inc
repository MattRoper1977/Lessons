    def _write_issues_csv(self) -> None:
        with (self.output / "issues.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["severity", "blocking", "category", "path", "line", "message", "details"])
            writer.writeheader()
            for issue in sorted(self.issues, key=lambda item: (not item.blocking, item.severity, item.category, item.path, item.line or 0)):
                writer.writerow(issue.as_dict())

    def _render_report(self) -> str:
        counts = Counter(issue.severity for issue in self.issues)
        browser_counts = self.metrics.get("browser", {}).get("status_counts", {})
        live_counts = self.metrics.get("live", {}).get("status_counts", {})
        lines = [
            "# Lessons estate audit",
            "",
            f"- **Lessons commit:** `{self.metrics.get('lessons_commit', 'unknown')}`",
            f"- **Website commit (read-only evidence):** `{self.metrics.get('site_commit', 'unknown')}`",
            f"- **Generated:** {self.metrics.get('generated_at_utc', '')}",
            f"- **Tracked files examined:** {self.metrics.get('tracked_file_count', 0):,}",
            f"- **Tracked bytes:** {self.metrics.get('tracked_bytes', 0):,}",
            f"- **HTML files:** {self.metrics.get('html_file_count', 0):,} ({self.metrics.get('public_html_count', 0):,} public candidates; {self.metrics.get('support_html_count', 0):,} support/audit files)",
            f"- **Blocking findings:** {self.blocking_count:,}",
            f"- **All findings:** {counts.get('error', 0)} errors · {counts.get('warning', 0)} warnings · {counts.get('info', 0)} information notes",
            "",
            "## Pass status",
            "",
            "| Pass | Evidence | Result |",
            "|---|---|---|",
            f"| 1 · files, syntax, formats, references | inventory + parsers + local target resolution | {'PASS' if not any(i.blocking and i.category != 'browser' and i.category != 'live' for i in self.issues) else 'FINDINGS'} |",
            f"| 2 · browser execution | {self.metrics.get('browser', {}).get('result_count', 0):,} page/mode executions; {browser_counts} | {'PASS' if browser_counts and browser_counts.get('fail', 0) == 0 else 'FINDINGS/UNVERIFIED'} |",
            f"| 3 · publication and site.json | live public paths {live_counts}; exact hash checks + Pages API where authorised | {'PASS' if live_counts and live_counts.get('fail', 0) == 0 and not any(i.blocking and i.category == 'live' for i in self.issues) else 'FINDINGS/UNVERIFIED'} |",
            "| 4 · review package | this report, JSON/CSV evidence, checksums and patch plan | READY |",
            "",
            "## Scope and interpretation",
            "",
            "Every tracked file was inventoried. Web/code formats were parsed or syntax-checked; images, PDFs, archives and media were decoded/probed where the runner provides a decoder. All tracked HTML was opened through a combined local server that mirrors `madebymatt.uk/` plus `/Lessons/`. Public candidates are blocking; historical pass folders, reports, fixtures and tool pages are recorded but do not automatically block publication. The website repository was checked read-only.",
            "",
            "## Findings",
            "",
        ]
        if not self.issues:
            lines.append("No findings were recorded.")
        else:
            lines.extend(["| Severity | Blocking | Category | Path | Line | Finding |", "|---|---:|---|---|---:|---|"])
            for issue in sorted(self.issues, key=lambda item: (not item.blocking, {"error": 0, "warning": 1, "info": 2}.get(item.severity, 3), item.category, item.path, item.line or 0))[:500]:
                message = issue.message.replace("|", "\\|").replace("\n", " ")
                path = issue.path.replace("|", "\\|")
                lines.append(f"| {issue.severity.upper()} | {'yes' if issue.blocking else 'no'} | {issue.category} | `{path}` | {issue.line or ''} | {message} |")
            if len(self.issues) > 500:
                lines.append("")
                lines.append(f"The table is capped at 500 of {len(self.issues):,} findings. `issues.csv` and `issues.json` contain the complete set.")
        lines.extend([
            "",
            "## Website wiring evidence",
            "",
            f"- Lesson Hub doors found in `site.json`: **{self.site_checks.get('lesson_door_count', 0)}**",
            f"- `site.json` loaders: {', '.join(f'`{p}`' for p in self.site_checks.get('site_json_loaders', [])) or 'none'}",
            f"- Website files that explicitly reference `Lessons/`: **{len(self.site_checks.get('files_referencing_lessons', []))}**",
            f"- CNAME: `{self.site_checks.get('cname', '') or 'not present'}`",
            "",
            "## Evidence files",
            "",
            "- `inventory.csv` — every tracked path, size, classification and SHA-256",
            "- `issues.csv` / `issues.json` — complete findings",
            "- `browser-results.json` — each browser execution, console/runtime/network evidence and safe interaction result",
            "- `live-results.json` — exact-file comparisons, public URL census and Pages API responses",
            "- `site-checks.json` — `site.json` and related-file wiring",
            "- `PATCH_PLAN.md` — fix grouping for review; no automatic content rewrite",
            "- `checksums.sha256` and `download-manifest.json` — package integrity",
            "",
            "## Honest limits",
            "",
            "This is an automated engineering pass, not a human visual or curriculum-content approval. It does not claim that every animation is pedagogically ideal, that every print layout has been physically printed, or that every external third-party URL is permanently available. Those are deliberately separated from code/runtime/publication evidence.",
            "",
        ])
        return "\n".join(lines)

    def _render_patch_plan(self) -> str:
        groups: dict[str, list[Issue]] = defaultdict(list)
        for issue in self.issues:
            if issue.blocking:
                groups[issue.category].append(issue)
        lines = [
            "# Patch plan for review",
            "",
            f"Base: `{self.metrics.get('lessons_commit', 'unknown')}`",
            "",
            "No lesson content is rewritten by the audit. Blocking findings are grouped below so fixes can be authored as small, reviewable commits after Matt and Claude inspect the evidence.",
            "",
        ]
        if not groups:
            lines.append("No blocking patch group is required by this run.")
        else:
            for category, issues in sorted(groups.items()):
                lines.append(f"## {category} ({len(issues)})")
                lines.append("")
                for issue in sorted(issues, key=lambda item: (item.path, item.line or 0))[:100]:
                    suffix = f":{issue.line}" if issue.line else ""
                    lines.append(f"- `{issue.path}{suffix}` — {issue.message}")
                if len(issues) > 100:
                    lines.append(f"- … {len(issues) - 100} more in `issues.csv`.")
                lines.append("")
        lines.extend([
            "## Proposed commit discipline",
            "",
            "1. One defect family per commit; explicit path manifest only.",
            "2. Re-run the estate audit after each family; never weaken the gate to pass the content.",
            "3. Keep the website repository read-only unless publication wiring itself is proven defective and a separate minimal PR is authorised.",
            "4. Leave the pull request as draft until Matt and Claude have reviewed the rendered evidence and any pupil-facing text.",
            "",
        ])
        return "\n".join(lines)

    def _is_public_path(self, rel: str) -> bool:
        parts = pathlib.PurePosixPath(rel).parts
        if any(part.startswith("_") or part.startswith(".") for part in parts):
            return False
        if any(part.lower() in EXCLUDED_PUBLIC_SEGMENTS for part in parts[:-1]):
            return False
        return True

    @staticmethod
    def _looks_text(data: bytes) -> bool:
        if not data:
            return True
        sample = data[:8192]
        if b"\x00" in sample:
            return False
        control = sum(1 for byte in sample if byte < 9 or 13 < byte < 32)
        return control / max(1, len(sample)) < 0.02

    def _decode_text(self, rel: str, data: bytes) -> str:
        try:
            return data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            self.add("warning", "encoding", rel, "Text is not UTF-8; decoded as Windows-1252 for audit", line=data[:exc.start].count(b"\n") + 1, blocking=False)
            return data.decode("cp1252", "replace")

    @staticmethod
    def _sha256_path(path: pathlib.Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _json_safe(value: Any) -> Any:
        if isinstance(value, bytes):
            return f"<{len(value)} bytes>"
        if dataclasses.is_dataclass(value):
            return Audit._json_safe(dataclasses.asdict(value))
        if isinstance(value, dict):
            return {str(key): Audit._json_safe(child) for key, child in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [Audit._json_safe(child) for child in value]
        return value


class CombinedRequestHandler(http.server.SimpleHTTPRequestHandler):
    repo_root: pathlib.Path
    site_root: pathlib.Path

    def translate_path(self, path: str) -> str:
        parsed = urllib.parse.urlsplit(path)
        decoded = urllib.parse.unquote(parsed.path)
        if decoded == "/Lessons":
            decoded = "/Lessons/"
        if decoded.startswith("/Lessons/"):
            root = self.repo_root
            relative = decoded[len("/Lessons/"):]
        else:
            root = self.site_root
            relative = decoded.lstrip("/")
        normalized = posixpath.normpath(relative)
        if normalized in {"", "."}:
            normalized = ""
        parts = [part for part in normalized.split("/") if part not in {"", ".", ".."}]
        return str(root.joinpath(*parts))

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


class CombinedServer:
    def __init__(self, repo_root: pathlib.Path, site_root: pathlib.Path) -> None:
        handler = type("EstateHandler", (CombinedRequestHandler,), {"repo_root": repo_root, "site_root": site_root})
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, name="estate-http", daemon=True)
        self.origin = f"http://127.0.0.1:{self.httpd.server_port}"

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)


ERROR_HOOK_JS = r"""
(() => {
  window.__estateAuditErrors = [];
  const push = (kind, value) => {
    try {
      const text = typeof value === 'string' ? value : (value && (value.stack || value.message)) || String(value);
      window.__estateAuditErrors.push(`${kind}: ${text}`.slice(0, 2000));
    } catch (_) {}
  };
  window.addEventListener('error', event => push('error', event.error || event.message), true);
  window.addEventListener('unhandledrejection', event => push('unhandledrejection', event.reason), true);
})();
"""

BROWSER_SURFACE_JS = r"""
return (() => {
  const visible = el => {
    const s = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' && Number(s.opacity || 1) > 0 && r.width > 0 && r.height > 0;
  };
  const name = el => (el.getAttribute('aria-label') || el.getAttribute('title') || el.innerText || el.value || '').trim();
  const controls = [...document.querySelectorAll('button, a[href], input:not([type=hidden]), select, textarea, [role=button]')].filter(visible);
  const unnamed = controls.filter(el => !name(el) && !el.getAttribute('aria-labelledby')).length;
  const text = document.body ? (document.body.innerText || '').trim() : '';
  const renderable = !!document.querySelector('canvas, svg, img, video, iframe, model-viewer');
  return {
    has_surface: !!document.body && (text.length > 0 || renderable),
    body_text_length: text.length,
    visible_controls: controls.length,
    unnamed_controls: unnamed,
    document_width: document.documentElement ? document.documentElement.scrollWidth : 0,
    viewport_width: window.innerWidth,
    horizontal_overflow_px: document.documentElement ? Math.max(0, document.documentElement.scrollWidth - window.innerWidth) : 0,
  };
})();
"""

SAFE_INTERACTION_JS = r"""
return (() => {
  const visible = el => {
    const s = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return !el.disabled && s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
  };
  const safe = /\b(next|continue|start|play|begin|enter|open|launch|ready|go)\b/i;
  const bad = /\b(delete|remove|reset|clear|erase|wipe|submit|send|buy|purchase|logout|sign out)\b/i;
  const preferred = [
    '[data-action="next"]', '#nextBtn', '#next', '.next-btn', '.btn-next',
    '[data-action="start"]', '#startBtn', '#start', '.start-btn',
  ];
  let target = null;
  for (const selector of preferred) {
    const candidate = document.querySelector(selector);
    if (candidate && visible(candidate)) { target = candidate; break; }
  }
  if (!target) {
    target = [...document.querySelectorAll('button, [role=button]')].find(el => {
      if (!visible(el)) return false;
      const text = (el.innerText || el.getAttribute('aria-label') || el.title || '').trim();
      return safe.test(text) && !bad.test(text);
    }) || null;
  }
  if (!target) return {clicked:false, reason:'no safe generic control'};
  const label = (target.innerText || target.getAttribute('aria-label') || target.id || target.className || target.tagName).toString().trim().slice(0, 200);
  try {
    target.click();
    return {clicked:true, label};
  } catch (error) {
    return {clicked:false, label, reason:String(error)};
  }
})();
"""


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
