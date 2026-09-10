## D39 — the seeded faults are content and are never repaired

`W08_Bug_Hunt`'s three faults and `W07_Bug_Hunt`'s wrong-sprite rule **are the
lesson**. Any future pass that "fixes" them reds.

### DO-NOT-AUTOFIX

Relative to `ICT/Teaching_Packs/GROW_Computing/`:

```
Week_07/Scratch_Projects/W07_Bug_Hunt.sb3
Week_07/Scratch_Projects/W07_Recovery_Win.sb3
Week_07/Teacher_Only/W07_Teacher_Model.sb3
Week_08/Scratch_Projects/W08_Bug_Hunt.sb3
Week_08/Scratch_Projects/W08_Recovery_Challenge.sb3
Week_08/Teacher_Only/W08_Teacher_Model.sb3
```

### What is deliberate in them, measured in the revision

| file | seeded state | measured |
|---|---|---|
| `W08_Bug_Hunt` | down arrow uses `change y by 10`, so down moves up | `motion_changeyby` `10`, positive |
| `W08_Bug_Hunt` | wall check has no `forever`, so it runs once at the flag | Player holds exactly **1** `forever` |
| `W08_Bug_Hunt` | win script has no empty `say`, so the message survives restart | only `'Made it!'`, no clearing say |
| `W07_Bug_Hunt` | contact rule on the wrong sprite | `Player` touches `[Finish, Maze]`; `Hazard` touches `[Player]` |

The recovery and teacher-model files are on the list for the same reason in
reverse: they encode the *correct* states a pupil is meant to reach, and a pass
that "harmonised" them with the bug-hunt file would destroy the comparison the
lesson turns on.

### Why an autofixer would reach for these

Every one of the four reads as a defect to a linter and to a person skimming. A
positive `change y by` under a down arrow, a wall check with no loop, a missing
clearing `say`, a touch test on the wrong sprite — each is exactly what a repair
pass looks for. The revision's own authoring record draws the line explicitly:

> "5. Repaired six unintended Scratch block-parent links. **The intentional
> classroom bug-hunt faults remain**, with the correct explanation and separate
> working model."

Six unintended links repaired; four intended faults untouched. Same pack, same
pass, opposite treatment, because one set is an error and the other is the
teaching.
