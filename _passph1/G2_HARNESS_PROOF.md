# PH-1 replacement G2 — jsdom harness proof

- jsdom requested: `26.1.0`.
- jsdom resolved: `26.1.0`.
- Node: `v22.23.2`.
- Environment: GitHub Actions runner with network available for the pinned package install.

## Broken control

- Fixture: inline `throw new Error("PH1_CONTROL_THROW")`.
- Harness exit: **1**.
- Genuine runtime throw detected: **True**.

```json
[
  {
    "file": "/tmp/ph1-g2-controls-cege_pt_/broken.html",
    "rendered": true,
    "readyState": "complete",
    "marker": null,
    "errors": [
      "JSDOM_ERROR: Error: Uncaught [Error: PH1_CONTROL_THROW]"
    ]
  }
]
```

## Clean control

- Fixture: clean body plus an inline script setting `data-ph1-control="clean-ran"`.
- Harness exit: **0**.
- Rendered, marker observed and zero errors: **True**.

```json
[
  {
    "file": "/tmp/ph1-g2-controls-cege_pt_/clean.html",
    "rendered": true,
    "readyState": "complete",
    "marker": "clean-ran",
    "errors": []
  }
]
```

**CONTROL VERDICT: PROVEN.** The harness rejects a genuine runtime throw and accepts the known-clean page.

This proves the detector only. Real G2 remains pending until it is run across the touched production files after P1–P7.
