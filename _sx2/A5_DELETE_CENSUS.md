# A5 — harnesses that delete a path they were handed

ORDER TH1 §A5. **Census only. Nothing here is fixed**, per the order. The harness
hardened earlier in the session stays hardened and is not re-litigated below.

Instrument: `tools/audit/census_unguarded_deletes.py` (`--self-test` plants five
fixtures). Re-run it; do not trust this table.

## Inclusion rule and universe

| | |
|---|---|
| **universe** | every file tracked at `origin/main` in the three repositories — Lessons `509c61de`, Site `85e3e02`, Apps `95e33a8` — **9,172 files** |
| **considered** | **4,424** by text suffix; **0** unreadable or binary excluded |
| **candidate** | a line matching one of eight delete verbs (`rm -rf`, `shutil.rmtree`, `os.remove`, `Path.unlink`, `fs.rm*`, `rimraf`/`del`, `find -delete`, `git clean -dfx`) |
| **finding** | a candidate whose target reaches an **external** source — directly, via a variable assigned from one earlier in the file, or as a relative target after `cd "$EXTERNAL"` — **and** with no containment proof above it |
| **not a finding** | a literal path; a `mktemp`/`TemporaryDirectory` the script owns; a variable whose values are a hardcoded list in the same file |
| **stated limit** | a regex census. It cannot follow a path across files or through a function boundary, and lines over 500 characters (minified bundles) are skipped. An LLM sweep ran beside it. |

## The two findings

### 1 · `_rx3/reland.sh:4` — Lessons

```bash
set -u; W=$1; IDS=$2; J=$3; P=/tmp/…/Classic_Lessons_33_Complete_Pack
cd "$W" && git checkout -q -- . && git clean -qfd -e tools/ . >/dev/null && …
```

`W` is `$1`. `git checkout -- .` discards every uncommitted change and
`git clean -qfd .` deletes every untracked file, in a directory the caller names.
The delete's own argument is `.`, so the danger is entirely in the `cd` — which is
why the first version of this census, looking only at the delete's argument,
reported nothing here.

### 2 · `_rx3/family_gates.sh:29` — Lessons

```bash
set -u; W=$1; SITE=$2; LAND=$3; OUT=$4; mkdir -p "$OUT"; cd "$W"; rc=0
…
echo "== s24 print render"; rm -rf "$OUT/s24"; …
```

`OUT` is `$4`, created with `mkdir -p` and never checked. Bounded by the `/s24`
suffix, so it can only remove a directory of that name — under whatever the
caller points at.

## How exposed they actually are

Neither is served: `public_file()` refuses both, because `_rx3/` begins with `_`.
This is a developer-machine and session-container finding, not a live-site one.

Both are invoked from exactly one place, `_rx3/family.sh`:

```bash
W=/home/user/$1                       # line 3
OUT=/tmp/gates_$1                     # line 8
```

So the containment does exist — **one level up, in the caller, and as a string
prefix rather than a check.** Three things follow, and the third is the point:

1. `$1` is a leaf name, but nothing stops it holding `..` or `/`.
2. Both scripts are directly executable with any `$1`/`$4`; the prefix is not
   theirs.
3. **`family.sh Lessons` is a plausible argument, not a malicious one**, and it
   resolves `W` to `/home/user/Lessons` — the live working tree. `reland.sh` would
   then `git checkout -- .` and `git clean -qfd .` across the whole repository.

That is the same failure as the `/dev/null` one: a path handed in, deleted
without asking where it points.

## The instrument was wrong twice before it was right

Worth more than the finding, because it is the shape of the mistake:

1. Testing the whole **line** for an external reference reported **ten**, of which
   eight were safe — `rm -f "$tmp"` after `tmp=$(mktemp)`, `rm -f _served/Lessons`
   with `$PWD` in the *other* command of the same line, `rm -rf "drop_$T"` over a
   hardcoded loop list, and two fixture copies of a workflow.
2. Narrowing to the **delete's own argument** then reported **zero** — a clean
   sheet over a universe already known by hand to hold two. The assignment pattern
   was anchored at `^`, and `set -u; W=$1; OUT=$4; …` puts four external
   assignments on one line after a command. The `cd`-then-relative-delete shape
   was invisible for the same reason.

A planted red proves a census can fail **on the planted shape**. It does not prove
it can fail on a shape nobody thought to plant. Both of the above are now fixtures,
so the self-test judges five: the archetype, its guarded twin, a hardcoded-loop
variable that must **not** be reported, `cd`-then-clean, and semicolon-separated
assignment.

## Rejected, with the reason

| path | why not a finding |
|---|---|
| `.github/workflows/glv3-production-byte-check.yml:47,58` | `tmp=$(mktemp)` on line 43 — script-owned |
| Site `.github/workflows/neonsync-verify.yml:65` | `TMP=$(mktemp)` on line 61 |
| Site `.github/workflows/mbm-audience-discovery-closeout.yml:692` | `S=$(mktemp -d)` on line 683 |
| `.github/workflows/ux2-gates.yml:123` | target `_served/Lessons` is literal; `$PWD` is the `ln -s` argument |
| `tools/fieldops/dropmatrix.sh:21,31` | `T` iterates a hardcoded `T1…T15`; script `cd`s to its own directory first |
| `tools/verify_axiomshift.sh:31`, `verify_charcoal.sh:38`, `verify_offbrand.sh:32`, Site `verify_olympics_live_selftest.sh:38`, `microtinkerer/run.sh:43`, `verify_pack_index_control.sh:23`, `verify_pipe_census_controls.sh:28`, `verify_inline_exit_control.sh:65`, `verify_audit_output_guard.sh:22` | `trap 'rm -rf "$X"' EXIT` where `X` is `mktemp -d` |
| `tools/fixtures/pr124/workflows/*` | fixture copies of workflows, not live harnesses |
| `_teachgreen/DECISIONS.md:409,412,417` | markdown quoting a diff |
| Site `uas/vendor/tesseract/worker.min.js:2` | minified vendor bundle; now below the 500-character line cap |
