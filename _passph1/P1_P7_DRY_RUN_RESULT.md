# PH-1 P1–P7 dry-run result

- Input branch commit: `9d3cac167d4efd307d7565b27c68bd98246f40a0`
- Runtime executor SHA-256: `5739baab453dc8397bdff24a3e48fe9bf945dee6839f6b1b33a684dfdbb8575f`
- Exit code: **1**
- Result: **FAIL**

## Failure log

```text
Traceback (most recent call last):
  File "/tmp/ph1_apply_runtime.py", line 493, in <module>
    raise RuntimeError(f"G4 comparator red after P1-P7: {json.dumps(witness_result, indent=2)}")
RuntimeError: G4 comparator red after P1-P7: {
  "pass": false,
  "base_count": 147,
  "tip_count": 147,
  "missing_at_tip": [],
  "added_at_tip": [],
  "changed": [
    "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html",
    "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html"
  ]
}
```
