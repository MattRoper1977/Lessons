## D15 — One re-run is a discriminating test; a second identical failure is an outage

An install-time failure — one that happens before any test body runs — is
re-run **once**, not as a retry but as the test that tells you which it was: the
runner, or the change. If it passes, the first result was the runner. If it fails
identically, that is an outage, and an outage is **waited out**, never bypassed,
never merged past, never disabled.

Observed 2026-09-09 on #469 (two YAML lines and a digest pin). All four
Chromium-dependent checks failed at browser install, twice, verbatim:

```
E: Failed to fetch https://dl.google.com/linux/chrome-stable/deb/dists/stable/main/binary-amd64/Packages.gz  Hash Sum mismatch
   Last modification reported: Wed, 09 Sep 2026 09:41:12 +0000
   Release file created at:    Wed, 09 Sep 2026 17:16:59 +0000
E: Some index files failed to download. They have been ignored, or old ones used instead.
Failed to install browsers
Error: Installation process exited with code: 100
```

Google's own apt index disagreeing with its own `Release` file — a stale CDN
edge, external to this estate and to GitHub. `browser-matrix` fails one step
later with `browserType.launch: Executable doesn't exist at
…/chromium_headless_shell-1181/…`, which is the same failure seen downstream: the
install never happened, so the binary is not there.

A failure **inside** a test body is never attributed to infrastructure without
evidence. The eleven non-browser checks on that PR all passed, and the diff
touches nothing any of the four exercises — but that is the argument for waiting,
not for merging.

---
