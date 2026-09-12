# SB1 release closeout — next small pass

## Current checkpoint — SB1 release closeout and PIN1 gate-A refresh

Measured 2026-09-12T14:12:04.207Z. Lessons main `12828ac35af20b1058b9f5f1c0774f30d34df0b1` is deployed.
Publication `34697885918`: build `103564413750` and deploy `103565487223` SUCCESS.
Served proof job `103564412966` binds the exact successful publications and records
**59/59 byte-identical, 0 red, 0 inconclusive**. Both publication artifacts are present
and unexpired. All **20 main checks are terminal: 16 SUCCESS, 4 FAIL**. The failures
are one unchanged stale-evidence sweep and three Watch summaries reporting it.
Latest Watch `103565796156`: 5 PASS / 1 FAIL / 0 NO VERDICT / 0 pending among its
21 derived workflows (12 dormant, 3 dispatch-only). No blanket-green claim.

SB1 is CLOSED and its old board row is corrected. PIN1's actual digest gate was
freshly censused at verified main Git blobs: 444 declared distinct pins, **440
asserted Lessons paths, 6 triggered, 434 asserted but not triggered**, zero missing
asserted files. Four reverse-asymmetry trigger paths are intentional checker,
workflow and documentation coverage. See `PIN1_GATE_A_NEXT_PASS.md` and the full
path-level `rf3-evidence/PIN1_GATE_A_REFRESH.json`.

Next eligible implementation is PIN1 §2.1's actual digest-gate derivation, followed
by its §3 scratch-branch proofs. The separate §2.2 UX2 fallback is already delivered.
This pass changes no production code or pins; it closes release verification,
refreshes the source census, and reconciles the programme board. TH1C recovery
returned no usable original order; its lane remains held. LP1 and the remaining
recorded holds remain unchanged. The first scheduled invocation of the new PIN1
census is still not claimed from a PR or push run.


## Exact publication and live evidence

- Source/main: `12828ac35af20b1058b9f5f1c0774f30d34df0b1` (SB1 #516).
- Publication run `34697885918`, build `103564413750`, deploy `103565487223`: SUCCESS.
- Review artifact `10299726121`: 732,463,339 bytes, unexpired.
- Pages artifact `10299183924`: 730,882,422 bytes, unexpired.
- Served proof: FieldOps run `34697885618`, job `103564412966`, SUCCESS.
  At 14:07:22 UTC: 59 served byte-identical / 0 red / 0 inconclusive of 59 derived.
  This is the verifier's defined route population, not every file on the site.
- Exact publication legs: Site bf796475 / run 34691568030;
  Lessons 12828ac3 / run 34697885918; Apps c9a7a4e3 / run 34693856307;
  Games 809b6c9a / run 34319079851. The proof binds checked and deployed source
  commits and publication artifacts before comparing live bytes.
- Main sweep `103564412878`: 1,418 stale / 6,307 live / 6,899 row labels /
  47 unmatched files, exit 2. Exactly the recorded baseline; not repaired here.
- Latest Watch `103565796156` identifies FieldOps run 34697885618 as the failing
  workflow. Its 5 PASS / 1 FAIL tally uses its workflow/window rules, distinct
  from the 16 SUCCESS / 4 FAIL count of all current-main check runs.

SB1's implementation/main schema proof remains as recorded in SB1_RELEASE_READOUT.md.
This supplement resolves its previously pending publication and main checks. The
runtime changes are already merged; this pass does not create a second code PR.

## Recovery and board

A targeted Personal Context lookup for the original TH1C order returned no usable
matching instruction. The tool also reported exhausted retrieval budget; no further
queries were spent. That is a retrieval limitation, not proof that the order never
existed. No scope was reconstructed from its title or from TH1 A4/A5.

The saved programme table now reflects SB1_CLOSED and PIN1's actual remaining work.
Other completed or held lanes retain their historical evidence and limits. The
fresh gate-A census and next implementation boundary are recorded separately.

SB1_CLOSED · PIN1_PARTIAL
