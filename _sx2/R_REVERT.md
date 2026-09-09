# SX2R R1 - Autumn 1 refresh: revert proof

Order SX2R R1. Byte-identical revert for all 35 refreshed files, proved against
live main **c0e7f491f36bf73596017de05ea16bc895140834** before any landing PR is
opened, as 0.4 requires of a taught-now patch.

## Method, and why a file copy would not have been a proof

The revert is not simulated by copying bytes back. The patch was committed on a
scratch branch cut from origin/main, then reverted with `git revert`, and the
resulting **tree object hash** compared with the one main carries. A tree hash is
a single value covering every path and every byte, so it proves the revert
restored the whole repository and not merely the 35 files someone remembered to
check.

```
origin/main tree     0781ca1c3eb6a877f9d29bb504edb41471bbaf2b
patch commit tree    27e7a603733156a6f46a0c7f56d4155db3086d92   differs, so the patch is real
after revert tree    0781ca1c3eb6a877f9d29bb504edb41471bbaf2b   identical to origin/main

git diff --name-only origin/main <after revert>   ->  0 files, across the whole tree
```

**Not vacuous.** All 35 files are changed by the patch (0 no-ops), so no revert
here is trivially the identity. The patch commit is 35 files, +5433 / -905.

| family | files | revert byte-identical |
|---|---|---|
| BUILD | 5 | 5/5 |
| GROW | 15 | 15/15 |
| LAUNCH | 15 | 15/15 |
| **total** | **35** | **35/35** |

## Hashes, both directions

live is the sha256 at main c0e7f491. patched is what the landing PR will carry.
reverted is the sha256 after git revert; it must equal live on every row, and does.

| file | live (pre) | patched | reverted (post) | = live |
|---|---|---|---|---|
| `Build/SCI_B_W3_Backbones.html` | `b3c0a0b3c66b` | `d2144cf1fdd0` | `b3c0a0b3c66b` | yes |
| `Build/SCI_B_W4_Muscle_Pairs.html` | `4178be1248b5` | `4383acf0c158` | `4178be1248b5` | yes |
| `Build/SCI_B_W5_Right_Nutrition.html` | `1d06ba869b18` | `75ad8c54b72e` | `1d06ba869b18` | yes |
| `Build/SCI_B_W6_Balanced_Plate.html` | `238e4f1c87b3` | `7e3c45479248` | `238e4f1c87b3` | yes |
| `Build/SCI_B_W7_Where_Food_Comes_From.html` | `a5d84a74f963` | `d845841f4dab` | `a5d84a74f963` | yes |
| `Grow/SCI_G_W3_Friction.html` | `56c1655062d8` | `be35a43b7e59` | `56c1655062d8` | yes |
| `Grow/SCI_G_W4_Mechanisms.html` | `a2d4bd4b2ec8` | `1204070df60d` | `a2d4bd4b2ec8` | yes |
| `Grow/SCI_G_W5_Fair_Test.html` | `bb73bf1bb84d` | `ab61a5727b39` | `bb73bf1bb84d` | yes |
| `Grow/SCI_G_W6_Earth_And_Planets.html` | `83eaeaca1b23` | `5a871c6d5cfa` | `83eaeaca1b23` | yes |
| `Grow/SCI_G_W7_The_Moon.html` | `abaf614900cf` | `21e057d0723b` | `abaf614900cf` | yes |
| `Grow/resources/GS_W3A.html` | `eb1beee0d5e2` | `0a954ab07e09` | `eb1beee0d5e2` | yes |
| `Grow/resources/GS_W3B.html` | `b71aeff7b086` | `341c38d6993b` | `b71aeff7b086` | yes |
| `Grow/resources/GS_W4A.html` | `1dd08453ad84` | `85c6d4e250a3` | `1dd08453ad84` | yes |
| `Grow/resources/GS_W4B.html` | `3176b8f4e037` | `7abd856ad164` | `3176b8f4e037` | yes |
| `Grow/resources/GS_W5A.html` | `b51a5c099d3d` | `cb1d8d8f9520` | `b51a5c099d3d` | yes |
| `Grow/resources/GS_W5B.html` | `faaa268b4c7b` | `acbf53b0d345` | `faaa268b4c7b` | yes |
| `Grow/resources/GS_W6A.html` | `5d1a23aaf009` | `bf698d52abde` | `5d1a23aaf009` | yes |
| `Grow/resources/GS_W6B.html` | `409ecebac8dc` | `ce86ee9383c2` | `409ecebac8dc` | yes |
| `Grow/resources/GS_W7A.html` | `71757b20a899` | `dde1253d6726` | `71757b20a899` | yes |
| `Grow/resources/GS_W7B.html` | `fc1a5418ee8d` | `8ce304773ab0` | `fc1a5418ee8d` | yes |
| `Launch/SCI_L_W3_L1_Microscopy.html` | `bf0780f4b675` | `812a8bfe43b9` | `bf0780f4b675` | yes |
| `Launch/SCI_L_W3_L2_Magnification.html` | `fa14921a2719` | `904806ec6ad5` | `fa14921a2719` | yes |
| `Launch/SCI_L_W3_L3_ExamSkills.html` | `1079ebc632ad` | `3f8e49154cf8` | `1079ebc632ad` | yes |
| `Launch/SCI_L_W4_L1_Diffusion.html` | `20b0e2ffffc8` | `228d99f8f01d` | `20b0e2ffffc8` | yes |
| `Launch/SCI_L_W4_L2_GasExchange.html` | `28b9caeb861a` | `35ce30b24a9f` | `28b9caeb861a` | yes |
| `Launch/SCI_L_W4_L3_ExamSkills.html` | `03ef1369b379` | `7166343287d4` | `03ef1369b379` | yes |
| `Launch/SCI_L_W5_L1_Osmosis.html` | `9cb8d5f96b0a` | `ad70bf934cda` | `9cb8d5f96b0a` | yes |
| `Launch/SCI_L_W5_L2_OsmosisCP.html` | `47fffdce040c` | `a241a97bf653` | `47fffdce040c` | yes |
| `Launch/SCI_L_W5_L3_Evaluate.html` | `77050311f5f2` | `fe6ab45f94bd` | `77050311f5f2` | yes |
| `Launch/SCI_L_W6_L1_ActiveTransport.html` | `13f0723b04fd` | `c12b31cb1b1b` | `13f0723b04fd` | yes |
| `Launch/SCI_L_W6_L2_RootAndGut.html` | `492cba68126e` | `c4cb7deaf67f` | `492cba68126e` | yes |
| `Launch/SCI_L_W6_L3_Compare.html` | `2f04f8832f62` | `b2fca1f46d58` | `2f04f8832f62` | yes |
| `Launch/SCI_L_W7_L1_RoundUp.html` | `ce34177b8657` | `b78df8e052af` | `ce34177b8657` | yes |
| `Launch/SCI_L_W7_L2_CommandWords.html` | `83c201990e8f` | `bf5f02faad96` | `83c201990e8f` | yes |
| `Launch/SCI_L_W7_L3_ExamPractice.html` | `627198f1c946` | `692040c2dc8f` | `627198f1c946` | yes |

The twelve-character prefixes are unambiguous across 35 rows; the tree hash above
is the binding proof.

## What the revert PR is

One revert commit per landing PR, prepared and linked in that PR body **before**
it merges, per SX2 0.4. Each landing PR is one family, so its revert restores that
family only; the three together restore the tree hash above.
