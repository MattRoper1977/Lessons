#!/usr/bin/env python3
"""
triage_movers.py  —  Pass Q (KO Triage) CHECK SCRIPT (NOT an instrument; Tier-1 ledger artefact)

Reads ko_staleness.py's OWN functions (import, no modification — R-E09 respected) and, for each
candidate it identifies, prints the FULL content-mover subject list plus two evidence hashes:
  - ko_same : the KO block text is byte-identical HEAD vs the KO's last-change commit (must be True
              for a candidate; a False here would mean the instrument's own model disagrees)
  - excl_same : visible body with the R-E07 self-declaring not-KO regions removed
              (class="lm-strip" / class="lm-own" / id="print-feedback" block) is identical
              HEAD vs the KO's last-change commit. excl_same True => everything that moved lies
              inside regions a KO does not summarise => CLEAN-ARTEFACT candidate (proof, per file).
              This does NOT modify ko_staleness; it is a separate evidence lens for the ledger.
Output is JSON on stdout (machine surface); assumptions/labels to stderr per R-E12 contract.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "LundyLoop" / "tools"))
import ko_staleness as K  # noqa: E402  (import, not modify)

REPO = K.REPO
# R-E07 self-declaring not-KO regions + the Loop Mark print-feedback block.
LM_STRIP = re.compile(r'<td[^>]*class="[^"]*\blm-strip\b[^"]*"[^>]*>.*?</td>', re.S | re.I)
LM_OWN = re.compile(r'<span[^>]*class="[^"]*\blm-own\b[^"]*"[^>]*>.*?</span>', re.S | re.I)
# print-feedback region the Loop Mark writes into (id="print-feedback" ... up to next id="print-")
def strip_feedback(src):
    i = src.find('id="print-feedback"')
    while i >= 0:
        j = src.find('id="print-', i + 12)
        src = src[:i] + " " + (src[j:] if j > 0 else "")
        i = src.find('id="print-feedback"')
    return src

def excl_visible(src):
    src = strip_feedback(src)
    src = LM_STRIP.sub(" ", src)
    src = LM_OWN.sub(" ", src)
    return K.visible(src)

def main():
    files = [p for p in K.sh("git", "ls-files", "-z", "*.html").split("\0") if p]
    ko_files = [f for f in files if K.KO_SLOT in K.sh("git", "show", f"HEAD:{f}")]
    out = []
    for f in ko_files:
        log = [c for c in K.sh("git", "log", "--format=%H", "--", f).split("\n") if c]
        seen = [(c, K.h(K.visible(K.sh("git", "show", f"{c}:{f}"))),
                 K.h(K.ko_text(K.sh("git", "show", f"{c}:{f}")))) for c in log]
        def last_change(idx):
            for k in range(len(seen) - 1):
                if seen[k][idx] != seen[k + 1][idx]:
                    return k
            return len(seen) - 1
        i_ko, i_body = last_change(2), last_change(1)
        if i_ko <= i_body:
            continue
        movers = [seen[k][0] for k in range(i_body, i_ko)]
        subjects = [K.sh("git", "log", "-1", "--format=%s", c).strip() for c in movers]
        content = [s for s in subjects if not K.ARCHITECTURE.match(s)]
        if not content:
            continue
        ko_commit = seen[i_ko][0]
        head_src = K.sh("git", "show", f"HEAD:{f}")
        ko_src = K.sh("git", "show", f"{ko_commit}:{f}")
        ko_same = K.h(K.ko_text(head_src)) == K.h(K.ko_text(ko_src))
        excl_same = K.h(excl_visible(head_src)) == K.h(excl_visible(ko_src))
        out.append({"file": f, "n_content": len(content),
                    "ko_last_change": ko_commit[:10], "ko_same": ko_same,
                    "excl_same": excl_same, "content_movers": content})
    print(json.dumps(out, indent=0))
    print(f"emitted {len(out)} candidate records", file=sys.stderr)

if __name__ == "__main__":
    main()
