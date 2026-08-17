# PH-1 replacement G4 — refined witness comparator mutation proof

- Immutable BASE: `ae1d3c7af2526781aad6fb82e7cbbf6b87ded380`.
- Actual witness surfaces derived at BASE: **145**.
- Surface rule: an explicit `id="print-witness"`, or an `Assessor Witness Statement` heading genuinely enclosed by a `print-section` element.
- False-positive control `LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html` excluded: **True**.

## Mandatory mutations

1. Delete witness section — `BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html` — red: **True**.
2. Alter witness content — `LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html` — red: **True**.
3. Whitespace-only reformat — `Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html` — stays green: **True**.

**MUTATION VERDICT: PROVEN.** The refined comparator rejects the known hub false positive and exhibits all three required mutation behaviours.

Real G4 remains pending until this comparator checks immutable BASE against the final branch tip.
