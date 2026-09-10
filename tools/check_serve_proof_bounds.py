#!/usr/bin/env python3
"""GW1-C §1.1 · the three serve-proof bounds have to agree, and this proves it.

WHY THIS EXISTS. #498 raised the caller's --wait-seconds to 1800 and left the
ceiling inside the tool it calls at 300. Main went red instantly, rejecting the
caller's own argument. Two of three numbers were right, which is worse than one:
it looked like a fix and shipped like one.

    tool ceiling    the most this tool will ever be asked to wait. A promise
                    that the job cannot hold a runner indefinitely on another
                    workflow that may never finish. NOT a claim about how long a
                    publication takes.
    tool default    how long it actually waits. This one tracks the measured
                    publication runtime.
    caller          --wait-seconds in the workflow. Must be <= the ceiling.
    job timeout     timeout-minutes on the job. Must EXCEED the wait, or the job
                    is killed mid-wait and the wait buys nothing.

The relations, in order of how they broke:

    caller <= ceiling          #498 broke this one
    job timeout > caller       #498 fixed this one at the same time
    ceiling < job timeout      a wait the job would kill anyway is not a wait
    default <= caller          the caller may shorten, never lengthen past the cap

--self-test plants a violation of each and requires the check to FAIL, then runs
against the real files and requires it to PASS. A guard that has never failed is
not known to work.
"""
import re, sys, argparse
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / 'tools/prepare_served_publications.py'
FLOW = REPO / '.github/workflows/fieldops-p2-and-sweep.yml'
JOB = 'Merged is not served'


def read(tool_text, flow_text):
    """Every number is READ, none is passed in. A checker fed its own
    expectations checks nothing."""
    def one(pattern, text, what):
        m = re.search(pattern, text)
        if not m:
            raise SystemExit('cannot find %s -- the check cannot run, which is a '
                             'failure and not a pass' % what)
        return int(m.group(1))

    lines = flow_text.split('\n')
    idx = [n for n, l in enumerate(lines) if JOB in l]
    if not idx:
        raise SystemExit('cannot find the %r job' % JOB)
    timeout = [l for l in lines[idx[0]:idx[0] + 8] if 'timeout-minutes' in l]
    if not timeout:
        raise SystemExit('the %r job declares no timeout-minutes' % JOB)
    return {
        'ceiling': one(r'args\.wait_seconds <= (\d+)', tool_text, 'the tool ceiling'),
        'default': one(r"'--wait-seconds', type=int, default=(\d+)", tool_text, 'the tool default'),
        'caller': one(r'--wait-seconds (\d+)', flow_text, "the caller's --wait-seconds"),
        'timeout': int(timeout[0].split(':')[1]) * 60,
    }


def check(v):
    return [
        ('caller <= ceiling', v['caller'] <= v['ceiling'],
         'the caller asks for %ds and the tool refuses anything over %ds -- it will '
         'reject its own argument and fail instantly' % (v['caller'], v['ceiling'])),
        ('job timeout > caller', v['timeout'] > v['caller'],
         'the job is killed at %ds and the wait is %ds -- the job dies mid-wait and '
         'the wait buys nothing' % (v['timeout'], v['caller'])),
        ('ceiling < job timeout', v['ceiling'] < v['timeout'],
         'the ceiling %ds is at or above the job timeout %ds -- a wait the job would '
         'kill anyway is not a wait' % (v['ceiling'], v['timeout'])),
        ('default <= caller', v['default'] <= v['caller'],
         'the default %ds exceeds what the caller asks for, %ds' % (v['default'], v['caller'])),
    ]


def run(tool_text, flow_text, quiet=False):
    v = read(tool_text, flow_text)
    rows = check(v)
    if not quiet:
        print('  ceiling %ds · default %ds · caller %ds · job timeout %ds (%d min)'
              % (v['ceiling'], v['default'], v['caller'], v['timeout'], v['timeout'] // 60))
        for name, ok, why in rows:
            print('  %-22s %s%s' % (name, 'OK' if ok else '*** FAILS ***',
                                    '' if ok else '\n      ' + why))
    return all(ok for _, ok, _ in rows)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    tool, flow = TOOL.read_text(encoding='utf-8'), FLOW.read_text(encoding='utf-8')

    if a.self_test:
        print('RED PROOFS -- each plants one violation and requires a FAIL:')
        ok = True
        # EVERY PLANT IS DERIVED FROM THE REAL VALUES, never a hard-coded literal.
        # The first version pasted the numbers in, and the moment the ceiling moved
        # from 2700 to 2400 its plant matched nothing and quietly stopped testing
        # anything. The script noticed -- see the "PLANT DID NOT FIRE" branch below,
        # which is the only reason that was visible -- but a plant that has to be
        # kept in step by hand will fall out of step again.
        now = read(tool, flow)
        sub = lambda t, pat, val: re.sub(pat, lambda m: m.group(1) + str(val), t, count=1)
        CEIL = r'(args\.wait_seconds <= )\d+'
        DEFT = r"('--wait-seconds', type=int, default=)\d+"
        CALL = r'(--wait-seconds )\d+'
        TMO = r'(%s.*?timeout-minutes: )\d+' % JOB
        plants = [
            ('caller above ceiling  (#498 exactly)',
             tool, sub(flow, CALL, now['ceiling'] + 1)),
            ('job timeout below the wait',
             tool, re.sub(TMO, lambda m: m.group(1) + str(max(1, now['caller'] // 60 - 1)),
                          flow, flags=re.S, count=1)),
            ('ceiling at or above the job timeout',
             sub(tool, CEIL, now['timeout']), flow),
            ('default above the caller',
             sub(tool, DEFT, now['caller'] + 1), flow),
        ]
        for name, t, f in plants:
            if (t, f) == (tool, flow):
                print('  %-38s *** PLANT DID NOT FIRE -- it changed nothing ***' % name)
                ok = False
                continue
            fired = not run(t, f, quiet=True)
            print('  %-38s %s' % (name, 'FAILS as it must' if fired else '*** DID NOT FAIL ***'))
            ok &= fired
        print('\nAND THE REAL FILES, which must PASS:')
        passes = run(tool, flow)
        ok &= passes
        print('\nself-test %s' % ('PASS -- the check fails on each violation and passes on the truth'
                                  if ok else '*** FAIL ***'))
        sys.exit(0 if ok else 1)

    sys.exit(0 if run(tool, flow) else 1)
