## D26 — STANDING RULE: path, never basename

Every comparison between an original and a re-cut, and every payload-to-original
lookup anywhere in this estate, is keyed on **full path**. A lookup with no path
match is a **listed conflict reported by name**; it never falls back to basename
and never resolves silently.

The rule exists because it already bit. `B02_Ready_Respectful_Safe.html` exists in
the originals pack *and* in batch 02. A §6b check keyed on basename compared each
batch collection's payload against the **original** deck and reported **17 of 42
mismatching** — a confident, specific, entirely false finding. Scoped to the
package the collection came from, the answer is 42 of 42.

A basename collision does not announce itself. It produces a plausible number.
