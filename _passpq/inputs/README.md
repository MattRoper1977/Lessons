# _passpq/inputs/ — the official instruments

**Status: EMPTY. Phase 0 blocked.** `asdan.org.uk` is refused by this environment's
network policy (proxy gateway returns `403 connect_rejected` — a policy denial, not a
transient error; confirmed via `$HTTPS_PROXY/__agentproxy/status`). Neither `curl` nor
`WebFetch` can reach it, and there is no per-tool fix. The audit therefore ran against
the brief's **§2 baseline as PROVISIONAL authority**, with every spec-dependent line
flagged `UNVERIFIED-AGAINST-SPEC`. The moment the three PDFs below are committed here,
that flag comes off and the coverage matrices reconcile against the real instrument.

## Publicly hosted — download and drop into this folder (no login needed)

1. **PEQ Qualification Specification** — the primary instrument. Expect Version 1.2,
   October 2025. If a newer version is served, use it and report the version delta.
   `https://www.asdan.org.uk/media/looduarj/asdan-peq-specification.pdf`
2. **PEQ flyer**
   `https://www.asdan.org.uk/media/yoebz1qg/personal-effectiveness-qualifications-flyer.pdf`
3. **ASDAN qualifications key dates & performance information 2026**
   `https://www.asdan.org.uk/media/qvxkrtjy/asdan-qualifications-key-dates-and-performance-information-2026.pdf`

**Verify each downloaded file is what it claims before relying on it** (open it, confirm
the title/version) — the estate rule is that any third-party or AI-generated ASDAN
description has repeatedly fabricated requirements and is never authoritative.

## Member-gated — a shopping list for Matt / Cheryl (ASDAN member login required)

These were **not** guessed at. Any audit finding that depends on one is marked
`UNDETERMINED — needs <document>` in FINDINGS.md, never inferred.

- PEQ **delivery guide**
- The **unit assessment booklets** (ComSkE3 etc.)
- **Assessment Planning Guidance**
- **Internal Quality Assurance Guidance**
- The **PEQ qualification tracker**
- The **PEQ challenge bank**

## RESUME SEQUENCE (once the three PDFs are dropped here) — from Matt's close-out ruling

1. **Verify each downloaded file is what it claims** — state title page, version, and page
   count for each before relying on it.
2. **Commit them** to `_passpq/inputs/`.
3. **Reconcile every §2 claim against the spec and clear or amend each
   `UNVERIFIED-AGAINST-SPEC` flag individually — never as a batch stamp.**
4. **Re-derive CLAIMS and both COVERAGE deltas** wherever a flag moved.
5. **State any spec-vs-§2 mismatch as a finding** (the spec wins; report the delta).
6. Then the conditional builds unlock: **T2-2 / T2-3 unit-code corrections** execute only
   where the **spec and the Evidence Binder agree** on every target code (two-source);
   any disagreement converts that code to a tabled finding.

## Note on the strongest internal corroborator

`ASDAN/ASDAN PEQs/Evidence_Binder_PEQ_v7.html` embeds a unit/criterion/credit data model
that **carries Ofqual unit reference numbers** (e.g. ComSkE3 = `R/651/6411`, 3 credits /
30 GLH) and matches §2 line-for-line. It is not the spec, but a fabricated table does not
carry live Ofqual URNs, so it is treated in this audit as a **strong internal
corroborator** of §2 — still to be checked against the committed PDF, but load-bearing
until then.
