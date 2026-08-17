# PH-1 Amendment 2 — unexpected executor failure before transport retirement

- The temporary workflow still existed, so the executor failed before its Phase 0d transport-retirement commit.
- No force-push, reset, merge or PR was performed.
- The tail of the executor output follows.

```text
Traceback (most recent call last):
  File "/tmp/ph1_amendment2_execute.py", line 2054, in <module>
    main()
  File "/tmp/ph1_amendment2_execute.py", line 1970, in main
    c7_actual = banned_state(summary, BASE)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/ph1_amendment2_execute.py", line 1729, in banned_state
    "affirmative_l2_registration": affirmative_l2(texts),
                                   ^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/ph1_amendment2_execute.py", line 1696, in affirmative_l2
    if re.search(
       ^^^^^^^^^^
  File "/usr/lib/python3.12/re/__init__.py", line 177, in search
    return _compile(pattern, flags).search(string)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/__init__.py", line 307, in _compile
    p = _compiler.compile(pattern, flags)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/_compiler.py", line 745, in compile
    p = _parser.parse(p, flags)
        ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/_parser.py", line 979, in parse
    p = _parse_sub(source, state, flags & SRE_FLAG_VERBOSE, 0)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/_parser.py", line 460, in _parse_sub
    itemsappend(_parse(source, state, verbose, nested + 1,
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/_parser.py", line 840, in _parse
    raise source.error('global flags not at the start '
re.error: global flags not at the start of the expression at position 89
```
