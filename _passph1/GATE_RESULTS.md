# PH-1 Phase 3 — gate results

- Repository: `MattRoper1977/Lessons`
- Immutable BASE: `ae1d3c7af2526781aad6fb82e7cbbf6b87ded380`
- Gate input tip: `55c35cd68cdd423c7c9c16c68a34348a1150e9f9`
- Touched production HTML files: **25**
- Overall: **RED**
- Red gates: **G2, G6, G8**

| Gate | BASE measurement | Tip measurement | Result |
|---|---|---|---|
| G1 | 37 inline blocks, 0 syntax errors | 37 inline blocks, 0 syntax errors | **PASS** |
| G2 | 25 loaded; 10 failed; harness-failed=False | 25 loaded; 10 failed; harness-failed=False; jsdom 26.1.0 | **RED** |
| G3 | print-section total 151 | print-section total 151; changed files 0 | **PASS** |
| G4 | witness set 145 | witness set 145; changed 0; added 0; missing 0 | **PASS** |
| G5 | loop-mark sentinel 50 | loop-mark sentinel 50; +0/-0 | **PASS** |
| G6 | {"ASDAN Studio \u00b7 ASDAN Studio": 0, "Communication 10-hour/600-minute": 0, "Delivering a Project": 0, "adjacent-level not both": 0, "affirmative L2 registration": 2} | {"ASDAN Studio \u00b7 ASDAN Studio": 0, "Communication 10-hour/600-minute": 0, "Delivering a Project": 0, "adjacent-level not both": 0, "affirmative L2 registration": 2} | **RED** |
| G7 | reduced-motion blocks 29 | reduced-motion blocks 29; changed files 0 | **PASS** |
| G8 | 6 balance/end errors | 6 balance/end errors | **RED** |
| G9 | diff files 39 | unexpected files 0 | **PASS** |
| G10 | localStorage keys 58; ASDAN PDFs 0 | added keys 0; ASDAN PDFs 0; fixture-name gate=True | **PASS** |

## G1 — PASS

```json
{
  "pass": true,
  "base": {
    "blocks": 37,
    "files": 25,
    "per_file": {
      "BUILD_ASDAN/BUILD_ASDAN_Hub.html": 0,
      "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html": 4,
      "BUILD_ASDAN/Careers/START_HERE.html": 0,
      "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html": 4,
      "BUILD_ASDAN/Community_Project/START_HERE.html": 0,
      "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html": 4,
      "BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html": 0,
      "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html": 4,
      "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html": 4,
      "BUILD_ASDAN/FoodWise/START_HERE.html": 0,
      "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html": 4,
      "BUILD_ASDAN/Living_Independently/START_HERE.html": 0,
      "Build/Slideshows/BUILD_DT_W6_Handover.html": 4,
      "GROW_ASDAN/GROW_ASDAN_Hub.html": 0,
      "GROW_ASDAN/Scheme_and_Resources.html": 0,
      "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html": 0,
      "LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html": 3,
      "LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html": 3,
      "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html": 3,
      "LAUNCH_ASDAN/PEQ/START_HERE.html": 0,
      "LAUNCH_ASDAN/Resources_and_Tools.html": 0,
      "LAUNCH_ASDAN/Scheme_of_Work.html": 0,
      "LAUNCH_ASDAN/Vocational/START_HERE.html": 0,
      "build_asdan.html": 0,
      "build_dt_upcycling.html": 0
    },
    "errors": [],
    "pass": true
  },
  "tip": {
    "blocks": 37,
    "files": 25,
    "per_file": {
      "BUILD_ASDAN/BUILD_ASDAN_Hub.html": 0,
      "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html": 4,
      "BUILD_ASDAN/Careers/START_HERE.html": 0,
      "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html": 4,
      "BUILD_ASDAN/Community_Project/START_HERE.html": 0,
      "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html": 4,
      "BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html": 0,
      "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html": 4,
      "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html": 4,
      "BUILD_ASDAN/FoodWise/START_HERE.html": 0,
      "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html": 4,
      "BUILD_ASDAN/Living_Independently/START_HERE.html": 0,
      "Build/Slideshows/BUILD_DT_W6_Handover.html": 4,
      "GROW_ASDAN/GROW_ASDAN_Hub.html": 0,
      "GROW_ASDAN/Scheme_and_Resources.html": 0,
      "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html": 0,
      "LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html": 3,
      "LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html": 3,
      "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html": 3,
      "LAUNCH_ASDAN/PEQ/START_HERE.html": 0,
      "LAUNCH_ASDAN/Resources_and_Tools.html": 0,
      "LAUNCH_ASDAN/Scheme_of_Work.html": 0,
      "LAUNCH_ASDAN/Vocational/START_HERE.html": 0,
      "build_asdan.html": 0,
      "build_dt_upcycling.html": 0
    },
    "errors": [],
    "pass": true
  }
}
```

## G2 — RED

```json
{
  "pass": false,
  "base": {
    "pass": false,
    "harness_failed": false,
    "returncode": 1,
    "files": 25,
    "failures": [
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/Build/Slideshows/BUILD_DT_W6_Handover.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      }
    ],
    "results": [
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/BUILD_ASDAN_Hub.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Careers/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Community_Project/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/FoodWise/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/BUILD_ASDAN/Living_Independently/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/Build/Slideshows/BUILD_DT_W6_Handover.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/GROW_ASDAN/GROW_ASDAN_Hub.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/GROW_ASDAN/Scheme_and_Resources.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/LAUNCH_ASDAN/PEQ/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/LAUNCH_ASDAN/Resources_and_Tools.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/LAUNCH_ASDAN/Scheme_of_Work.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/LAUNCH_ASDAN/Vocational/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/build_asdan.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.FUAkwiyTmJ/build_dt_upcycling.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      }
    ]
  },
  "tip": {
    "pass": false,
    "harness_failed": false,
    "returncode": 1,
    "files": 25,
    "failures": [
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/Build/Slideshows/BUILD_DT_W6_Handover.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      }
    ],
    "results": [
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/BUILD_ASDAN_Hub.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Careers/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Community_Project/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/FoodWise/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/BUILD_ASDAN/Living_Independently/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/Build/Slideshows/BUILD_DT_W6_Handover.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/GROW_ASDAN/GROW_ASDAN_Hub.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/GROW_ASDAN/Scheme_and_Resources.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": [
          "RESOURCE_ERROR file:///hud.js: Error: ENOENT: no such file or directory, open '/hud.js'",
          "JSDOM_ERROR: Error: Could not load script: \"file:///hud.js\"",
          "CONSOLE_ERROR: ASDAN Visual Learning did not mount: {}"
        ]
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/LAUNCH_ASDAN/PEQ/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/LAUNCH_ASDAN/Resources_and_Tools.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/LAUNCH_ASDAN/Scheme_of_Work.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/LAUNCH_ASDAN/Vocational/START_HERE.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/build_asdan.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      },
      {
        "file": "/tmp/tmp.wJmiR2bRNv/build_dt_upcycling.html",
        "rendered": true,
        "readyState": "complete",
        "marker": null,
        "errors": []
      }
    ]
  },
  "jsdom_version": "26.1.0"
}
```

## G3 — PASS

```json
{
  "pass": true,
  "base_total": 151,
  "tip_total": 151,
  "base": {
    "BUILD_ASDAN/BUILD_ASDAN_Hub.html": 0,
    "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html": 16,
    "BUILD_ASDAN/Careers/START_HERE.html": 0,
    "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html": 15,
    "BUILD_ASDAN/Community_Project/START_HERE.html": 0,
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html": 15,
    "BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html": 0,
    "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html": 15,
    "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html": 15,
    "BUILD_ASDAN/FoodWise/START_HERE.html": 0,
    "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html": 15,
    "BUILD_ASDAN/Living_Independently/START_HERE.html": 0,
    "Build/Slideshows/BUILD_DT_W6_Handover.html": 15,
    "GROW_ASDAN/GROW_ASDAN_Hub.html": 0,
    "GROW_ASDAN/Scheme_and_Resources.html": 0,
    "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html": 0,
    "LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html": 15,
    "LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html": 15,
    "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html": 15,
    "LAUNCH_ASDAN/PEQ/START_HERE.html": 0,
    "LAUNCH_ASDAN/Resources_and_Tools.html": 0,
    "LAUNCH_ASDAN/Scheme_of_Work.html": 0,
    "LAUNCH_ASDAN/Vocational/START_HERE.html": 0,
    "build_asdan.html": 0,
    "build_dt_upcycling.html": 0
  },
  "tip": {
    "BUILD_ASDAN/BUILD_ASDAN_Hub.html": 0,
    "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html": 16,
    "BUILD_ASDAN/Careers/START_HERE.html": 0,
    "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html": 15,
    "BUILD_ASDAN/Community_Project/START_HERE.html": 0,
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html": 15,
    "BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html": 0,
    "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html": 15,
    "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html": 15,
    "BUILD_ASDAN/FoodWise/START_HERE.html": 0,
    "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html": 15,
    "BUILD_ASDAN/Living_Independently/START_HERE.html": 0,
    "Build/Slideshows/BUILD_DT_W6_Handover.html": 15,
    "GROW_ASDAN/GROW_ASDAN_Hub.html": 0,
    "GROW_ASDAN/Scheme_and_Resources.html": 0,
    "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html": 0,
    "LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html": 15,
    "LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html": 15,
    "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html": 15,
    "LAUNCH_ASDAN/PEQ/START_HERE.html": 0,
    "LAUNCH_ASDAN/Resources_and_Tools.html": 0,
    "LAUNCH_ASDAN/Scheme_of_Work.html": 0,
    "LAUNCH_ASDAN/Vocational/START_HERE.html": 0,
    "build_asdan.html": 0,
    "build_dt_upcycling.html": 0
  },
  "diffs": {}
}
```

## G4 — PASS

```json
{
  "pass": true,
  "base_count": 145,
  "tip_count": 145,
  "missing_at_tip": [],
  "added_at_tip": [],
  "changed": [],
  "mutation_proof": "delete red; content red; whitespace green; hub false-positive excluded"
}
```

## G5 — PASS

```json
{
  "pass": true,
  "base_count": 50,
  "tip_count": 50,
  "added": [],
  "removed": [],
  "base_set": [
    "Art_Teesside/Build/BUILD_ART_W1_The_Local_Canvas.html",
    "Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html",
    "Art_Teesside/Build/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html",
    "Art_Teesside/Build/BUILD_ART_W4_Build_the_Brief.html",
    "Art_Teesside/Build/BUILD_ART_W5_Critique_Test_and_Redirect.html",
    "Art_Teesside/Build/BUILD_ART_W6_Resolve_the_Artwork.html",
    "Art_Teesside/Build/BUILD_ART_W7_Curate_the_Showcase.html",
    "Art_Teesside/Build/BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html",
    "BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html",
    "BUILD_ASDAN/Careers/CAREERS_W2_Jobs_in_My_Community.html",
    "BUILD_ASDAN/Careers/CAREERS_W3_Skills_Employers_Want.html",
    "BUILD_ASDAN/Careers/CAREERS_W4_Routines_and_Reliability.html",
    "BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html",
    "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html",
    "BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html",
    "BUILD_ASDAN/Community_Project/COMM_W1_Choose_Our_Asset.html",
    "BUILD_ASDAN/Community_Project/COMM_W2_The_Site's_Need.html",
    "BUILD_ASDAN/Community_Project/COMM_W3_Our_Team_Roles.html",
    "BUILD_ASDAN/Community_Project/COMM_W4_Partner_Update.html",
    "BUILD_ASDAN/Community_Project/COMM_W5_Plan_the_Handover.html",
    "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W2_A_Kindness_Challenge.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W3_An_Eco_Challenge.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W4_An_Independence_Challenge.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W5_Our_Social_Enterprise.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html",
    "BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html",
    "BUILD_ASDAN/FoodWise/FW_W2_A_Balanced_Plate.html",
    "BUILD_ASDAN/FoodWise/FW_W3_Reading_Labels.html",
    "BUILD_ASDAN/FoodWise/FW_W4_Kitchen_Hygiene_and_Safety.html",
    "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html",
    "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html",
    "BUILD_ASDAN/Living_Independently/LI_W1_Where_Money_Comes_From.html",
    "BUILD_ASDAN/Living_Independently/LI_W2_Notes_and_Coins.html",
    "BUILD_ASDAN/Living_Independently/LI_W3_Needs_vs_Wants.html",
    "BUILD_ASDAN/Living_Independently/LI_W4_Everyday_Prices.html",
    "BUILD_ASDAN/Living_Independently/LI_W5_A_Simple_Budget.html",
    "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html",
    "Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html",
    "Build/Slideshows/BUILD_DT_W2_Blueprint.html",
    "Build/Slideshows/BUILD_DT_W3_Core_Cut.html",
    "Build/Slideshows/BUILD_DT_W4_Assembly.html",
    "Build/Slideshows/BUILD_DT_W5_Finish.html",
    "Build/Slideshows/BUILD_DT_W6_Handover.html",
    "Science_Teesside/Build/SCI_B_W3_Backbones.html",
    "Science_Teesside/Build/SCI_B_W4_Muscle_Pairs.html",
    "Science_Teesside/Build/SCI_B_W5_Right_Nutrition.html",
    "Science_Teesside/Build/SCI_B_W6_Balanced_Plate.html",
    "Science_Teesside/Build/SCI_B_W7_Where_Food_Comes_From.html"
  ],
  "tip_set": [
    "Art_Teesside/Build/BUILD_ART_W1_The_Local_Canvas.html",
    "Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html",
    "Art_Teesside/Build/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html",
    "Art_Teesside/Build/BUILD_ART_W4_Build_the_Brief.html",
    "Art_Teesside/Build/BUILD_ART_W5_Critique_Test_and_Redirect.html",
    "Art_Teesside/Build/BUILD_ART_W6_Resolve_the_Artwork.html",
    "Art_Teesside/Build/BUILD_ART_W7_Curate_the_Showcase.html",
    "Art_Teesside/Build/BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html",
    "BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html",
    "BUILD_ASDAN/Careers/CAREERS_W2_Jobs_in_My_Community.html",
    "BUILD_ASDAN/Careers/CAREERS_W3_Skills_Employers_Want.html",
    "BUILD_ASDAN/Careers/CAREERS_W4_Routines_and_Reliability.html",
    "BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html",
    "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html",
    "BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html",
    "BUILD_ASDAN/Community_Project/COMM_W1_Choose_Our_Asset.html",
    "BUILD_ASDAN/Community_Project/COMM_W2_The_Site's_Need.html",
    "BUILD_ASDAN/Community_Project/COMM_W3_Our_Team_Roles.html",
    "BUILD_ASDAN/Community_Project/COMM_W4_Partner_Update.html",
    "BUILD_ASDAN/Community_Project/COMM_W5_Plan_the_Handover.html",
    "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W2_A_Kindness_Challenge.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W3_An_Eco_Challenge.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W4_An_Independence_Challenge.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W5_Our_Social_Enterprise.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html",
    "BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html",
    "BUILD_ASDAN/FoodWise/FW_W2_A_Balanced_Plate.html",
    "BUILD_ASDAN/FoodWise/FW_W3_Reading_Labels.html",
    "BUILD_ASDAN/FoodWise/FW_W4_Kitchen_Hygiene_and_Safety.html",
    "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html",
    "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html",
    "BUILD_ASDAN/Living_Independently/LI_W1_Where_Money_Comes_From.html",
    "BUILD_ASDAN/Living_Independently/LI_W2_Notes_and_Coins.html",
    "BUILD_ASDAN/Living_Independently/LI_W3_Needs_vs_Wants.html",
    "BUILD_ASDAN/Living_Independently/LI_W4_Everyday_Prices.html",
    "BUILD_ASDAN/Living_Independently/LI_W5_A_Simple_Budget.html",
    "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html",
    "Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html",
    "Build/Slideshows/BUILD_DT_W2_Blueprint.html",
    "Build/Slideshows/BUILD_DT_W3_Core_Cut.html",
    "Build/Slideshows/BUILD_DT_W4_Assembly.html",
    "Build/Slideshows/BUILD_DT_W5_Finish.html",
    "Build/Slideshows/BUILD_DT_W6_Handover.html",
    "Science_Teesside/Build/SCI_B_W3_Backbones.html",
    "Science_Teesside/Build/SCI_B_W4_Muscle_Pairs.html",
    "Science_Teesside/Build/SCI_B_W5_Right_Nutrition.html",
    "Science_Teesside/Build/SCI_B_W6_Balanced_Plate.html",
    "Science_Teesside/Build/SCI_B_W7_Where_Food_Comes_From.html"
  ]
}
```

## G6 — RED

```json
{
  "pass": false,
  "base": {
    "counts": {
      "Delivering a Project": 0,
      "ASDAN Studio \u00b7 ASDAN Studio": 0,
      "affirmative L2 registration": 2,
      "Communication 10-hour/600-minute": 0,
      "adjacent-level not both": 0
    },
    "occurrences": {
      "Delivering a Project": [],
      "ASDAN Studio \u00b7 ASDAN Studio": [],
      "affirmative L2 registration": [
        {
          "file": "GROW_ASDAN/Scheme_and_Resources.html",
          "line": 21,
          "match": "can be registered for Level 2",
          "context": "olor:#64748b\">\u00b7 Thursday P4</span></h2> <p class=\"bank\">ASDAN PEQ Level 1 Award (Entry 3 floor). Stretch tier written to L2 evidence standard throughout \u2014 pupils who fly can be registered for Level 2 units (UAS coordinator decision).</p> <table><tr><th>Wk</th><th>Lesson</th><th>Core outcome</th><th>Banks</th></tr><tr><td><b>W1</b></td><td><b>Knowing Myself</b> \u2014 Strengths, interests, starting points</td><td>I can audit my strengths and"
        },
        {
          "file": "LAUNCH_ASDAN/Scheme_of_Work.html",
          "line": 15,
          "match": "L2 registration",
          "context": "Certificate; E3\u2013L1 only in 2026/27). Autumn 1 completes Communication skills (ComSk1). Stretch tier written to an L2 evidence standard \u2014 stretch language only, never an L2 registration. Registered with ASDAN before assessment counts.</p><table><tr><th>Wk</th><th>Lesson</th><th>Core outcome</th><th>Banks</th></tr><tr><td><b>W1</b></td><td><b>Intro and Choosing My Level</b></td><td>I can name the six PEQ skills</td><td>ASD"
        }
      ],
      "Communication 10-hour/600-minute": [],
      "adjacent-level not both": []
    },
    "pass": false
  },
  "tip": {
    "counts": {
      "Delivering a Project": 0,
      "ASDAN Studio \u00b7 ASDAN Studio": 0,
      "affirmative L2 registration": 2,
      "Communication 10-hour/600-minute": 0,
      "adjacent-level not both": 0
    },
    "occurrences": {
      "Delivering a Project": [],
      "ASDAN Studio \u00b7 ASDAN Studio": [],
      "affirmative L2 registration": [
        {
          "file": "GROW_ASDAN/Scheme_and_Resources.html",
          "line": 21,
          "match": "can be registered for Level 2",
          "context": "olor:#64748b\">\u00b7 Thursday P4</span></h2> <p class=\"bank\">ASDAN PEQ Level 1 Award (Entry 3 floor). Stretch tier written to L2 evidence standard throughout \u2014 pupils who fly can be registered for Level 2 units (UAS coordinator decision).</p> <table><tr><th>Wk</th><th>Lesson</th><th>Core outcome</th><th>Banks</th></tr><tr><td><b>W1</b></td><td><b>Knowing Myself</b> \u2014 Strengths, interests, starting points</td><td>I can audit my strengths and"
        },
        {
          "file": "LAUNCH_ASDAN/Scheme_of_Work.html",
          "line": 15,
          "match": "L2 registration",
          "context": "Certificate; E3\u2013L1 only in 2026/27). Autumn 1 completes Communication skills (ComSk1). Stretch tier written to an L2 evidence standard \u2014 stretch language only, never an L2 registration. Registered with ASDAN before assessment counts.</p><table><tr><th>Wk</th><th>Lesson</th><th>Core outcome</th><th>Banks</th></tr><tr><td><b>W1</b></td><td><b>Intro and Choosing My Level</b></td><td>I can name the six PEQ skills</td><td>ASD"
        }
      ],
      "Communication 10-hour/600-minute": [],
      "adjacent-level not both": []
    },
    "pass": false
  }
}
```

## G7 — PASS

```json
{
  "pass": true,
  "base_blocks": 29,
  "tip_blocks": 29,
  "diffs": {}
}
```

## G8 — RED

```json
{
  "pass": false,
  "base": {
    "pass": false,
    "files": 25,
    "errors": [
      {
        "file": "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html",
        "errors": [
          {
            "tag": "div",
            "open": 233,
            "close": 231
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      },
      {
        "file": "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html",
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      },
      {
        "file": "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html",
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      },
      {
        "file": "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html",
        "errors": [
          {
            "tag": "div",
            "open": 213,
            "close": 211
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      },
      {
        "file": "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html",
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      },
      {
        "file": "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html",
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      }
    ],
    "detail": {
      "BUILD_ASDAN/BUILD_ASDAN_Hub.html": {
        "errors": [],
        "ends_html": true
      },
      "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html": {
        "errors": [
          {
            "tag": "div",
            "open": 233,
            "close": 231
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/Careers/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html": {
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/Community_Project/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html": {
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html": {
        "errors": [
          {
            "tag": "div",
            "open": 213,
            "close": 211
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html": {
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/FoodWise/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html": {
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/Living_Independently/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "Build/Slideshows/BUILD_DT_W6_Handover.html": {
        "errors": [],
        "ends_html": true
      },
      "GROW_ASDAN/GROW_ASDAN_Hub.html": {
        "errors": [],
        "ends_html": true
      },
      "GROW_ASDAN/Scheme_and_Resources.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/PEQ/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/Resources_and_Tools.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/Scheme_of_Work.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/Vocational/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "build_asdan.html": {
        "errors": [],
        "ends_html": true
      },
      "build_dt_upcycling.html": {
        "errors": [],
        "ends_html": true
      }
    }
  },
  "tip": {
    "pass": false,
    "files": 25,
    "errors": [
      {
        "file": "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html",
        "errors": [
          {
            "tag": "div",
            "open": 233,
            "close": 231
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      },
      {
        "file": "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html",
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      },
      {
        "file": "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html",
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      },
      {
        "file": "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html",
        "errors": [
          {
            "tag": "div",
            "open": 213,
            "close": 211
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      },
      {
        "file": "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html",
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      },
      {
        "file": "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html",
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ]
      }
    ],
    "detail": {
      "BUILD_ASDAN/BUILD_ASDAN_Hub.html": {
        "errors": [],
        "ends_html": true
      },
      "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html": {
        "errors": [
          {
            "tag": "div",
            "open": 233,
            "close": 231
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/Careers/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html": {
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/Community_Project/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html": {
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html": {
        "errors": [
          {
            "tag": "div",
            "open": 213,
            "close": 211
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html": {
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/FoodWise/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html": {
        "errors": [
          {
            "tag": "div",
            "open": 207,
            "close": 205
          },
          {
            "tag": "style",
            "open": 4,
            "close": 3
          }
        ],
        "ends_html": true
      },
      "BUILD_ASDAN/Living_Independently/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "Build/Slideshows/BUILD_DT_W6_Handover.html": {
        "errors": [],
        "ends_html": true
      },
      "GROW_ASDAN/GROW_ASDAN_Hub.html": {
        "errors": [],
        "ends_html": true
      },
      "GROW_ASDAN/Scheme_and_Resources.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/PEQ/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/Resources_and_Tools.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/Scheme_of_Work.html": {
        "errors": [],
        "ends_html": true
      },
      "LAUNCH_ASDAN/Vocational/START_HERE.html": {
        "errors": [],
        "ends_html": true
      },
      "build_asdan.html": {
        "errors": [],
        "ends_html": true
      },
      "build_dt_upcycling.html": {
        "errors": [],
        "ends_html": true
      }
    }
  },
  "balance_tags": [
    "div",
    "script",
    "style",
    "table",
    "svg",
    "ul",
    "ol"
  ]
}
```

## G9 — PASS

```json
{
  "pass": true,
  "base_changed_file_count": 39,
  "tip_changed_file_count": 39,
  "changed_paths": [
    "BUILD_ASDAN/BUILD_ASDAN_Hub.html",
    "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html",
    "BUILD_ASDAN/Careers/START_HERE.html",
    "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html",
    "BUILD_ASDAN/Community_Project/START_HERE.html",
    "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html",
    "BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html",
    "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html",
    "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html",
    "BUILD_ASDAN/FoodWise/START_HERE.html",
    "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html",
    "BUILD_ASDAN/Living_Independently/START_HERE.html",
    "Build/Slideshows/BUILD_DT_W6_Handover.html",
    "GROW_ASDAN/GROW_ASDAN_Hub.html",
    "GROW_ASDAN/Scheme_and_Resources.html",
    "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html",
    "LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html",
    "LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html",
    "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html",
    "LAUNCH_ASDAN/PEQ/START_HERE.html",
    "LAUNCH_ASDAN/Resources_and_Tools.html",
    "LAUNCH_ASDAN/Scheme_of_Work.html",
    "LAUNCH_ASDAN/Vocational/START_HERE.html",
    "_passph1/C7_FINDING.md",
    "_passph1/CENSUS.md",
    "_passph1/EXECUTOR_FAILURE.md",
    "_passph1/G2_HARNESS.cjs",
    "_passph1/G2_HARNESS_PROOF.md",
    "_passph1/G4_DETECTOR_FINDING.md",
    "_passph1/G4_MUTATION_PROOF.md",
    "_passph1/G4_WITNESS_COMPARATOR.py",
    "_passph1/L1_DEMAND_REPORT.md",
    "_passph1/P1_P7_DRY_RUN_RESULT.md",
    "_passph1/P7_NOT_DEPLOYED.md",
    "_passph1/SCOPE_GUARD_PROOF.md",
    "_passph1/SIGNOFF_CLASSIFICATION.md",
    "_passph1/TEST_COPY_DIVERGENCE.md",
    "build_asdan.html",
    "build_dt_upcycling.html"
  ],
  "unexpected": []
}
```

## G10 — PASS

```json
{
  "pass": true,
  "base": {
    "localStorage_key_count": 58,
    "tracked_ASDAN_PDFs": 0
  },
  "tip": {
    "fixture_name_gate_pass": true,
    "fixture_name_output": "SCOPE: /tmp/tmp.wJmiR2bRNv\n  1955 file(s), no path filter and no type filter; skipped: .git, node_modules, vendor, audit-output\n  predicate: a fixture-marker token with >=2 Titlecase words, or containing a listed surname\n\nALLOWED, each with its reason:\n  RELEASE_LEDGER_2026-08-16.md: CANARY_PUPIL_Jamie_Roper (\u00d73)\n     the dated record of what was planted, and the provenance the fixture-naming rule rests on\n  tools/verify_fixture_names.mjs: CANARY_PUPIL_Jamie_Roper (\u00d76)\n     this check's own red vector \u2014 the string that actually shipped\n  tools/verify_fixture_names.mjs: FIXTURE_John_Smith (\u00d73)\n     this check's own red vector \u2014 a plain first name + surname\n  tools/verify_fixture_names.mjs: SAMPLE_roper (\u00d73)\n     this check's own red vector \u2014 a listed surname in lower case\n  tools/verify_fixture_names.mjs: CANARY_PUPIL_Alice_Roper (\u00d73)\n     the seeded string the self-test writes and deletes, quoted here to assert on it\n\nNo person-shaped fixture strings. Clean, with the scope printed above.\nNOTE: this catches person-shaped NAMES, not plausible pupil PROSE \u2014 see the header.",
    "tracked_ASDAN_PDFs": [],
    "localStorage_key_count": 58,
    "localStorage_keys_added": []
  }
}
```
