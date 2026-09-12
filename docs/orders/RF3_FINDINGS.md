# RF3 — release/control findings

Filed 12 September 2026 under RF3 §5.2. This path is internal documentation under
`docs/orders/`; it does not move or change the served `REGISTER.md`. The broader
Lane G migration remains its own publication transaction under the standing
no-REGISTER-write limit. F1–F11 and P5.1–P5.4 remain preserved in the RF1 readback;
this entry adds the explicitly requested P5.5 rather than pretending to relocate them.

## P5.5 — A carried figure acquires authority by repetition

**Rule, carried verbatim from RF3_HANDOVER.md §5:** Every order quoting a count
cites the measurement that produced it, or states it is unverified.

Owner: release/control. Status: FILED; apply to every future readback/count.

| Population | Historical measurement and provenance | Current interpretation |
|---|---|---|
| PRX1 closing-boundary source census | RF1 carried 133; RF2 measured 137; RF3 handover reports 129. Those scans did not share one recorded method. | Do not equate or average them. The reconstruction's `reports/prx1/SHAPE_CENSUS.md` records its own method, per-line ledger and exclusions at Site `30e86ad6`, 12 September 09:24 UTC. |
| PRX1 golden operations | Earlier RF1 31 comparisons omitted generated inputs. RF2's 33/33 omitted two upstream production generators. | Fresh proof at Site `6ba679a`, 12 September 09:27 UTC: 33/33 operations, 28 headers and 5 mains, every production generator enabled, zero differences/raises. These are operations across 28 distinct replacement pages; three body insertions are separate. |
| LP1 skipped proof census | `LP1_PIN1_S1_CENSUS.md`, measured 12 September 00:34–00:46 UTC: 18 independently gated proofs, or 16 with the three maker-splash steps collapsed. | Cite the population definition. Keep the 21 additional proofs in workflows without any PR trigger separate; they are not part of the 18. These are source-read classifications, not observed proof runs. |
| PIN1 pin set | Same census: 444 distinct paths, 443 excluding publisher caller, five registries; only one workflow asserts file-pin digests. | 89 is unlocated, not a baseline. Trigger coverage must be credited only to a gate that actually asserts the pin. |

For the fresh PRX1 source scan, 1,155 tracked files, 577 candidate code/HTML/YAML
files and 91 HTML/HTM files are separate denominators. Its 280 broad source-line
hits classify as 33 WRITING, 163 MEASURING, 74 NOT LOCATOR, 9 VENDOR/COMPILED and
1 BALANCED. That is a classified candidate census, not 280 defects.

The reproduction scripts and exact per-target hashes are committed in Site #350's
`reports/prx1/DECISIONS.md` and `SHAPE_CENSUS.md` at `70a22acb`. The last commit
changes documentation only from the code-tested `6ba679a`; no code or input was
changed between the golden test and its evidence commit.

No additional writer was repaired to align a count with a prior statement.
