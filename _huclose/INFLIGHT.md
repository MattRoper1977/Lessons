# IN-FLIGHT — Pass HU-CLOSE (v2)

**Declared 2026-08-05, before any other write.** Base derived at run start: `origin/main` = `067c76a`
("Merge Pass SEMH-2 (sections 3+6 only) — RES-AS1-01 applied, records; proposal sets stay held on PR #45").

No SHA quoted in the commissioning document is this pass's base. `efc6cb3`, `b080a7c` and `84f4f31`
are all observation points belonging to other sessions; each is behind `067c76a`.

## Phases and their scopes

| phase | branch | scope — writes confined to |
|---|---|---|
| P1 — complete the Humanities Lundy landing | `claude/hu-close-lundy` | `Humanities_Teesside/Lundy_Humanities/**`, `quality/LUNDY_HUMANITIES_*`, `_huclose/`, records files |
| P2 — Humanities visuals slice | `claude/hu-close-visuals` | `{Build,Grow,Launch}/Slideshows/*_HUM_*` (22 of 24 — the assessed pair excluded), `resources.json` year-tag metadata only |
| P3 — Science visual-learning | `claude/hu-close-science-visuals` | `Science_Teesside/visual-learning/**`, then `Science_Teesside/{Build,Grow,Launch}/*.html` loader mount only, `resources.json` entries only |
| P4 — day-close inputs | — | verify-only, no writes |
| P5 — outstanding surface | `claude/hu-close-lundy` | `_huclose/` only |

## Frozen in every phase

- `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html` and
  `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html` — 0 bytes, tree hashes emitted at close.
- `biology/`, `chemistry/`, `2 Physics 10/` — read permitted, write banned; tree hashes are the baseline.
- No in-place injector. No supplied patch applied. No rollback recipe. No force-push, no rebase
  onto a moved base without re-enumerating.

## Known open work this pass may read but must not write

PR #45 (three proposal sets, held) · PR #43 `tk1-access-2` (held on the large-print check) ·
PR #35 `semh1-art-runtime` (held on the art print check) · the shared deferral at open-items 24 ·
the D&T set behind local safety sign-off · Art_Teesside quarantine · D&T v5 print-pack no-touch.

Estate Visuals is the next queued session and will later edit humanities and science lessons.
Where this pass lands a visual layer, that half becomes verify-only for it — recorded in the
handover queue, not left to be discovered.
