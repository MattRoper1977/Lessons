# PH-1 P1–P7 dry-run result

- Input branch commit: `ce36afb6ed765ab2a0c77d2696ce77d8ec69cbe9`
- Executor SHA-256: `bd4568673c827ac81620e741c4b7aa6c792f3c88c934783f512e163e041ebc2e`
- Exit code: **1**
- Result: **FAIL**

## Failure log

```text
Traceback (most recent call last):
  File "/tmp/tmp.lrYeBqxnfb/.github/ph1_apply.py", line 353, in <module>
    acted += replace_exact(path, old, new, expected)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/tmp.lrYeBqxnfb/.github/ph1_apply.py", line 63, in replace_exact
    raise RuntimeError(f"{path}: expected {expected} occurrences of {old!r}; measured {count}")
RuntimeError: BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html: expected 1 occurrences of 'Witness staff sign off the profile as portfolio evidence.'; measured 0
```
