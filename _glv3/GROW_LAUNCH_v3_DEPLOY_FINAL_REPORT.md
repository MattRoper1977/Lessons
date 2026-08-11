DEPLOYED_VERIFIED

# GROW + LAUNCH Estates v3 final production dossier

Alternative GROW + LAUNCH Autumn 1 v3 route added for 2026-27; existing lessons remain the default; implementation verified against supplied constraints with residual documentation items listed in AMBERS.md.

## Immutable identity and publication chain

- Candidate SHA: `62a92d7d0216c00ae3ab9929528ab705c3ad2a30`
- Feature merge SHA: `a9dc6fc8214ff16a5f9effe183ca7329f4f7f615`
- Current main / production-verification base SHA: `7144254402dd967c5e3392b232d6f1bb282a9d03`
- Published SHA verified during the production suite: `7144254402dd967c5e3392b232d6f1bb282a9d03`
- Prompt A candidate run: `31479359464`
- Original feature publication run: `31481229802`
- Current production deployment run: `31486678631`
- Deployment completed: `2026-08-11T11:28:19Z`
- Canonical production URL: `https://madebymatt.uk/Lessons/`
- Production verification timestamp: `2026-08-11T11:57:11.271Z`
- Evidence closeout commit and its subsequent Pages merge/publication SHA are bound externally in the evidence PR, commit status and PR #108 closeout comment because a commit cannot contain its own SHA or a future merge SHA without changing that identity.

## Authoritative source provenance retained

- GROW repaired ZIP SHA-256: `95bf78a4124f20196508748c4b44c3935b0eb09181bac69fcc00c4c0a5e6f58a`
- LAUNCH repaired ZIP SHA-256: `aacbeda81d4bb5d665a0d70aafd5732431b64457a313e2f8843a120d0515768c`
- Validated deterministic transport SHA-256: `782ff5865e1406c159c78081bcc218bdaa46678e5c42448a6f298f696ca73f5e`
- Candidate-stage evidence ZIP SHA-256: `36b3761d91758d7c8ea38c679150f14706e286bdd649094235c01f6a1e21454c`
- Prompt C did not request, reconstruct or regenerate the source archives.

## Final measured counts

- GROW lessons: 34
- LAUNCH lessons: 46
- Total lessons: 80
- Installed generated HTML: 94
- Print-bearing lessons: 24
- Screen-only lessons: 56
- Catalogue additions: 88
- Contact-sheet PNGs: 83

## Full production acceptance

- Published SHA identity: PASS
- Public generated route census: 94/94 PASS
- Lesson interaction smoke: 80/80 PASS
- Estate console errors: 0
- Estate page errors: 0
- Failed estate assets: 0
- Print contract: 24/24 PASS
- Screen-only classification: 56/56 PASS
- Responsive checks: 480/480 PASS
- Keyboard/focus production smoke: 80/80 PASS (not formal WCAG certification)
- Unexpected external requests: 0
- Catalogue entries reachable: 88/88 PASS
- Catalogue advertised, rendered and JSON-derived chip counts reconcile; see `PRODUCTION_GATES.json`.
- Science reuse: PASS
- Existing default/protected estate: PASS
- Public legacy filename residue: 0
- Rewritten support links: 64 references across 4 pages; broken = 0
- Claim safety: PASS
- Contact-sheet inventory: 83 PNGs; integrity failures = 0

## AMBERs retained transparently

- 56/80 lessons are intentionally screen-only because no print pack was authored.
- Six LAUNCH PEQ lessons retain source-authored `ComSk1` boundary wording; no criterion mapping was inferred.
- GROW W2/W4 and LAUNCH W8 Arts Award tag reductions remain adviser judgements.
- No root `sitemap.xml` existed at the integration base, so none was invented.
- Candidate-stage documentary and reading-load observations remain in `AMBERS.md`.
- Production Lesson Hub recorded 0 local catalogue-shell 404 diagnostic occurrence(s). They were non-external, did not target a new GLV3 route and did not prevent 88/88 GLV3 entries from resolving.

## Final evidence

- `_glv3/GROW_LAUNCH_v3_DEPLOY_FINAL_REPORT.md`
- `_glv3/GROW_LAUNCH_v3_DEPLOY_PROOF.json`
- `_glv3/GROW_LAUNCH_v3_REPORT_AND_PROOF.zip`
- `_glv3/AUTONOMOUS_SENTINEL.json`
- `_glv3/PRODUCTION_GATES.json`
- `_glv3/PRODUCTION_IDENTITY.json`
- `_glv3/FINAL_EVIDENCE_ZIP_INTEGRITY.json`

The final production ZIP hash is stored outside the ZIP in `FINAL_EVIDENCE_ZIP_INTEGRITY.json` to avoid a self-referential archive hash.

## Rollback

Use a targeted revert of feature merge `a9dc6fc8214ff16a5f9effe183ca7329f4f7f615` according to its merge-parent structure if the GLV3 feature itself must be withdrawn. Revert the later verifier-maintenance or evidence-only closeout commit separately only when that narrow record/tooling change must be undone. Never reset the repository wholesale to historic anchor `1e8a428b523d1b970a8a3a2ab2a99f48a8271d09`.
