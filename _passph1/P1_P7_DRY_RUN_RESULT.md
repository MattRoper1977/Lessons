# PH-1 P1–P7 dry-run result

- Input branch commit: `a5a7a8c9fc2895895dcc6973179469b7578cee19`
- Runtime executor SHA-256: `bdc57244b5abcd2a638fbb1b9c1c9b0465300dc7e227940a0e26883aa054afd2`
- Exit code: **1**
- Result: **FAIL**

## Failure log

```text
Traceback (most recent call last):
  File "/tmp/ph1_apply_runtime.py", line 402, in <module>
    acted += replace_exact_outside_id(path, "print-witness", old, new, expected, 2)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/ph1_apply_runtime.py", line 111, in replace_exact_outside_id
    raise RuntimeError(f"{path}: protected witness block changed")
RuntimeError: LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html: protected witness block changed
```
