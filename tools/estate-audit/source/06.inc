      return;
    }
    push('error', event.error || event.message || 'unknown window error');
  }, true);
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
  return {clicked:false, label, element:target};
})();
"""


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="Lessons checkout root")
    parser.add_argument("--site-root", required=True, help="Read-only mattroper1977.github.io checkout")
    parser.add_argument("--output", default="audit-output", help="Evidence directory")
    parser.add_argument("--browser", action="store_true", help="Open all HTML in headless Chrome")
    parser.add_argument("--live", action="store_true", help="Check madebymatt.uk publication")
    parser.add_argument("--browser-modes", default="desktop,mobile-reduced", help="Comma-separated modes")
    parser.add_argument("--page-timeout", type=float, default=20.0)
    parser.add_argument("--settle", type=float, default=0.35)
    parser.add_argument("--published-ref", default="origin/main", help="Git ref used for live/main byte comparisons")
    parser.add_argument("--strict", action="store_true", help="Reserved for future escalation policy")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    modes = [mode.strip() for mode in args.browser_modes.split(",") if mode.strip()]
    audit = Audit(
        pathlib.Path(args.repo_root), pathlib.Path(args.site_root), pathlib.Path(args.output),
        args.strict, args.published_ref,
    )
    try:
        return audit.run(args.browser, args.live, modes, args.page_timeout, args.settle)
    except KeyboardInterrupt:
        raise
    except Exception as exc:
        audit.add("error", "audit", "<estate>", "Unhandled audit failure", details=f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}")
        with contextlib.suppress(Exception):
            audit._write_outputs()
        print(traceback.format_exc(), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
