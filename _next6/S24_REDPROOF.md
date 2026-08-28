# s24-print-renders — red-proof

Both perturbations are applied to throwaway copies. The repository tree
is not modified by this script.

## Baseline

```
PASS     baseline · the unperturbed deck
         1 surfaces rendered · confirmation on paper 1/1 · 0 blank pages
```

## Perturbation A · confirmation block moved outside `.print-pack`

```
FAIL     A · confirmation block moved outside `.print-pack`
         1 surfaces rendered · confirmation on paper 0/1 · 0 blank pages
         · ../../../tmp/s24-red-1gtza786/BUILD_ASDAN_A2_CON_W1_Materials_Tools_and_Safety.html | CONFIRMATION BLOCK NOT ON PAPER | 2 pages rendered, sentinel absent from PDF text
```

- gate result: **RED (correct)**
- names the defect (`CONFIRMATION BLOCK NOT ON PAPER`): **yes**
- names the file: **yes**

## Perturbation B · print height overrides removed, `.slide` back at `height:91%`

```
FAIL     B · print height overrides removed, `.slide` back at `height:91%`
         1 surfaces rendered · confirmation on paper 1/1 · 1 blank pages
         · ../../../tmp/s24-red-ozo6h715/PEQ_W7_What_Makes_a_Team_Effective_Features_Advantages_Challenges_LAUNCH.html | BLANK PAGE | p10 ink=0.7117% chars=0
```

- gate result: **RED (correct)**
- names the defect (`BLANK PAGE`): **yes**
- names the file: **yes**

## Verdict

Gate passes clean and fails on both defects it was written for.
