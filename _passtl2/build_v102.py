#!/usr/bin/env python3
"""TL-2 Part A: assemble the v1.0.2 package from the canonical v1.0.1 FINAL tree."""
import hashlib, json, re, shutil, subprocess
from datetime import datetime, timezone
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Lessons/91716126-0bef-5b42-b826-d86d99576965/scratchpad")
SRC = SCR / "townlife" / "MBM_Town_Life_v1_0_1_FINAL"
DST = SCR / "townlife" / "MBM_Town_Life_v1_0_2"
RUNTIME_NAME = "MBM_Town_Life_GOLD_v1_0.html"

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)

# ---- 1. swap in the renamed, version-bumped runtime ----
new_rt = (SCR / "build" / "v102.html").read_bytes()
(DST / RUNTIME_NAME).write_bytes(new_rt)

# ---- 2. live-claim docs: rename. History files deliberately untouched. ----
DOC_EDITS = {
    "README.md": [
        ("faster Washworks conversion", "faster Exchange conversion", 1),
        ("- Northstar Washworks.", "- Northstar Exchange.", 1),
        ("**Garage + Washworks:**", "**Garage + Exchange:**", 1),
        ("garage recovery and Washworks conversion;", "garage recovery and Exchange conversion;", 1),
    ],
    "TECHNICAL_ARCHITECTURE.md": [
        ("- Washworks conversion duration.", "- Exchange conversion duration.", 1),
    ],
    "ORIGINALITY_AND_SAFETY_NOTES.md": [
        ("and Washworks conversion are abstract game systems",
         "and Exchange conversion are abstract game systems", 1),
        ("- Washworks conversion is a delayed economy mechanic",
         "- Exchange conversion is a delayed economy mechanic", 1),
    ],
}
doc_log = []
for name, pairs in DOC_EDITS.items():
    p = DST / name
    t = p.read_text(encoding="utf-8")
    for old, new, exp in pairs:
        c = t.count(old)
        assert c == exp, (name, old, c, exp)
        t = t.replace(old, new)
        doc_log.append((name, old, new))
    p.write_text(t, encoding="utf-8")

# History files that must still say Washworks (records of what 1.0.1 did not change)
HISTORY = ["CHANGELOG.md", "GOLD_MASTER_RELEASE_NOTES.md", "VERIFICATION_REPORT.md"]
history_counts = {h: (DST / h).read_text(encoding="utf-8").count("Washworks") for h in HISTORY}

# ---- 3. CHANGELOG: prepend the 1.0.2 entry (history below is untouched) ----
cl = DST / "CHANGELOG.md"
entry = """# Town Life v1.0.2 — Washworks rename

## TL-2 Part A — 18 August 2026

- Renamed the player-facing business **Northstar Washworks** to **Northstar Exchange**, per Matt's
  2026-08-18 ruling to rename Washworks only. 17 player-visible occurrences changed across location
  and business names, notify text, action labels, HUD lines, the civic-decree description and the
  synergy descriptions. Grammatical agreement was re-read per string, not pattern-substituted: one
  article moved from `A` to `An`, and three strings gained or kept `the` to stay idiomatic.
- Left the internal identifier `businessSynergySnapshot().garageWashworks` unchanged (5 occurrences).
  It was proved **not persisted**: with Garage + Exchange both owned, the payload under
  `mbm_town_life_v10` contains neither the key nor the string `Washworks`.
- Left `state.laundering`, `LaunderingManager`, `state.dirtyBonds` and the `laundry` business id
  unchanged. The `laundry` id is a save-schema key; renaming it would invalidate existing saves.
- Corrected the executable version marker from `1.0.1` to `1.0.2`; save schema remains `10` and the
  save key remains `mbm_town_life_v10`.
- Changed no role, content, economy value, vehicle tuning, utility behaviour, business rule,
  Civic Bank flow, conversion flow, Sylvia flow or Mischief behaviour.

"""
cl.write_text(entry + cl.read_text(encoding="utf-8"), encoding="utf-8")

# ---- 4. runtime measurements ----
rt = DST / RUNTIME_NAME
raw = rt.read_bytes(); txt = raw.decode("utf-8")
inline = re.search(r"<script\b(?![^>]*src=)[^>]*>(.*?)</script>", txt, re.S).group(1)
ib = inline.encode("utf-8")
ids = re.findall(r'(?<![-\w])id\s*=\s*"([^"]*)"', txt)
M = {
    "utf8Bytes": len(raw), "unicodeCharacters": len(txt), "sha256": hashlib.sha256(raw).hexdigest(),
    "inlineScriptUtf8Bytes": len(ib), "inlineScriptUnicodeCharacters": len(inline),
    "inlineScriptSha256": hashlib.sha256(ib).hexdigest(),
    "idAttributes": len(ids), "httpUrlTokens": txt.count("http://"), "httpsUrlTokens": txt.count("https://"),
    "washworksResidual": txt.count("Washworks"), "v101": txt.count("1.0.1"), "v102": txt.count("1.0.2"),
}

# ---- 5. RELEASE_MANIFEST.json: regenerate identity + inventory ----
mp = DST / "RELEASE_MANIFEST.json"
man = json.loads(mp.read_text(encoding="utf-8"))
man["release"] = "Gold v1.0.2 TL-2 Part A rename candidate"
man["generatedAt"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
man["runtime"].update({
    "version": "1.0.2", "utf8Bytes": M["utf8Bytes"], "unicodeCharacters": M["unicodeCharacters"],
    "sha256": M["sha256"], "inlineScriptUtf8Bytes": M["inlineScriptUtf8Bytes"],
    "inlineScriptUnicodeCharacters": M["inlineScriptUnicodeCharacters"],
    "inlineScriptSha256": M["inlineScriptSha256"], "idAttributes": M["idAttributes"],
})
man["evidenceTreeProvenance"] = (
    "The packaged evidence tree was produced against runtime sha256 "
    "7d31850989bd36849be29b2e53e72e1906ff4597ab62e81e9225fa95cae9afd2 (v1.0.1) and no longer "
    "matches the shipped runtime. Claims about the executable are inherited, not re-proven, except "
    "those re-run in TL-2 A4/A6 and recorded in V1_0_2_IDENTITY.md."
)
mp.write_text(json.dumps(man, indent=2) + "\n", encoding="utf-8")

# ---- 6. V1_0_2_IDENTITY.md ----
rows = "\n".join(f"| `{n}` | `{o}` | `{x}` |" for n, o, x in doc_log)
(DST / "V1_0_2_IDENTITY.md").write_text(f"""# Town Life v1.0.2 — executable identity

Produced by TL-2 Part A on 18 August 2026 from the canonical `MBM_Town_Life_v1_0_1_FINAL` package.

## Runtime identity

| Measure | v1.0.1 (previous) | v1.0.2 (shipped) |
|---|---|---|
| Path | `{RUNTIME_NAME}` | `{RUNTIME_NAME}` |
| UTF-8 bytes (`wc -c`) | 304,742 | {M['utf8Bytes']:,} |
| Characters (`LC_ALL=C.UTF-8 wc -m`) | 304,462 | {M['unicodeCharacters']:,} |
| SHA-256 | `7d31850989bd36849be29b2e53e72e1906ff4597ab62e81e9225fa95cae9afd2` | `{M['sha256']}` |
| Inline script bytes | 265,585 | {M['inlineScriptUtf8Bytes']:,} |
| Inline script SHA-256 | `0a6b44170737dc71c8d04a9877eee62502617257489f5b924fe2d3dbbdca3bd1` | `{M['inlineScriptSha256']}` |
| `id` attributes | 164 | {M['idAttributes']} |
| `http://` / `https://` literals | 0 / 0 | {M['httpUrlTokens']} / {M['httpsUrlTokens']} |
| Save schema / key | 10 / `mbm_town_life_v10` | 10 / `mbm_town_life_v10` (unchanged) |

Byte counts are from `wc -c`/`stat`; character counts from `LC_ALL=C.UTF-8 wc -m`. The two differ by
280 because the runtime carries 171 non-ASCII characters (17 distinct: 62 two-byte, 109 three-byte).
The TL-2 prompt's house rule states 151; the measured figure is **171 occurrences**, and the 280-byte
delta it quotes is confirmed exactly.

## THE EVIDENCE TREE IS INHERITED, NOT RE-PROVEN

**The 196-file evidence tree in this package was produced against runtime
`7d31850989bd36849be29b2e53e72e1906ff4597ab62e81e9225fa95cae9afd2` (v1.0.1) and no longer matches the
shipped runtime `{M['sha256']}`.** Every claim in that tree that is *about the executable* is inherited
rather than re-proven, except the checks re-run in TL-2 A4/A6 and recorded below. The packaged
`qa/QA_SYSTEM_RESULTS.json` 99/99 result describes the v1.0.1 binary; it has **not** been re-run in
full against v1.0.2 and must not be quoted as if it had.

## What WAS re-proven against v1.0.2 (30/30 passed)

Harness: real Chromium 1194 over a loopback **HTTP origin** (`http://127.0.0.1:PORT/townlife/?qa`),
not `page.set_content`. Full results: `_tl2/PARTA_GATES.json`.

- **A3 persistence gate** — with Garage + Exchange owned, `garageWashworks` is absent from the saved
  payload, and the string `Washworks` appears nowhere in it. Computed, not persisted; Class 2 unchanged.
- **A4-1** — a v1.0.1 save written mid-conversion loads, resumes and completes in v1.0.2. Payout
  **£740** identical across v1.0.1 live, v1.0.1 seeded and v1.0.2 seeded (amount 320, rate 0.75).
- **A4-2** — a v1.0.1 save with `dirtyBonds` 250 and no conversion starts one under the new name.
- **A4-3** — the legacy normaliser executes: a synthetic `mbm_town_life_v01` fixture (profile Legacy,
  cash 777) funnels through, persists under v10, and the legacy record is not deleted.
  **This proves the code path runs, nothing more** — there are still no genuine v0.9–v0.1 artefacts.
- **A4-4** — default role on a fresh save is still `Resident`.
- **A6** — version declarations read 1.0.2, schema still 10, synergy still fires, conversion starts
  and completes, no `Washworks` in rendered text, ledger renders "Northstar Exchange", 390px
  horizontal overflow **0**, all 12 rendered visible controls ≥44px, zero console/page errors.
- **D3 (real-origin storage)** — storage mode resolves to **`local`** on a real origin, not
  `volatile memory save`. TL-1 recorded this UNPROVEN because managed Chromium's
  `URLBlocklist: ["*"]` blocked `file://` and loopback; that constraint does not apply here.
  Confirmation on the published `https://madebymatt.uk/townlife/` still awaits Part B.

## Still unexecuted — unchanged by this pass

Firefox, WebKit, Chromebook, Android, iOS, physical thermal/low-power, human screen-reader and
motor/cognitive evaluation, and genuine v0.9–v0.1 save artefacts.

## Documentation edits (live claims only)

{rows}

History files were deliberately **not** rewritten — they record what v1.0.1 did or did not change,
and rewriting them would falsify the record, exactly as A5 protects 1.0.1 references. Residual
`Washworks` counts, all historical: {json.dumps(history_counts)}.
""", encoding="utf-8")

# ---- 7. regenerate CHECKSUMS.sha256 ----
ck = DST / "CHECKSUMS.sha256"
files = sorted(p for p in DST.rglob("*") if p.is_file() and p != ck)
ck.write_text("".join(f"{sha(p)}  {p.relative_to(DST).as_posix()}\n" for p in files), encoding="utf-8")
verify = subprocess.run(["sha256sum", "-c", ck.name], cwd=DST, capture_output=True, text=True)
ok = verify.stdout.count(": OK"); bad = verify.stdout.count(": FAILED")

print(json.dumps({
    "runtime": M,
    "packageFiles": len(files) + 1,
    "checksumEntries": len(files),
    "checksumOK": ok, "checksumFAILED": bad,
    "docEdits": len(doc_log),
    "historyWashworksRetained": history_counts,
}, indent=1))
