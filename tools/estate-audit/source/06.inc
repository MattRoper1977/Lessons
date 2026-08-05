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
