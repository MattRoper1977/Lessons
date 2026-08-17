# PH-1 replacement G4 — witness comparator mutation proof

- Immutable BASE: `ae1d3c7af2526781aad6fb82e7cbbf6b87ded380`.
- Witness surfaces derived at BASE: **147**.
- Comparator: extract each surface’s own witness block, canonicalise whitespace, SHA-256 the canonical block, then compare BASE and tip sets and fingerprints.

## Mandatory mutations

1. **Delete a witness section entirely** — `BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html`
   - Baseline fingerprint: `6ea2c7ea0d475b858ef02ec35a58e42bf63c03d7ee45dbd31ae7c3d248b3f010`
   - Mutated fingerprint: `None`
   - Comparator went red: **True**.

2. **Alter witness content** — `LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html`
   - Baseline fingerprint: `21d420b44286345b3633b7fdd22eae0ff7d8a1f305ae53225e6892e1a776d7ba`
   - Mutated fingerprint: `a0b1fd795aec5bf8c44c371fb7334e62b53ed2f3984aabdce3e3d4e24415b342`
   - Comparator went red: **True**.

3. **Whitespace-only reformat** — `Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html`
   - Baseline fingerprint: `39efe4531efd94391b327dbdddb12b76501551d45af2a1b68e9d9f772720393c`
   - Mutated fingerprint: `39efe4531efd94391b327dbdddb12b76501551d45af2a1b68e9d9f772720393c`
   - Comparator stayed green: **True**.

**MUTATION VERDICT: PROVEN.** All three required detector behaviours were observed.

Real G4 remains pending until BASE is compared with the final branch tip after P1–P7.
