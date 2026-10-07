# Defender raid — script fixes

Two bugs in the quest Captain #34 gives you on the Hi-Tech floor: the Defender
raid on the cannibal settlement (Oazis) or the subway station. Both are in the
Fixed Edition itself, not in the translation. The fixed scripts ship in the patch
as `data/scripts/olxcchef.int` and `data/scripts/oln34.int`. Delete those two
files to go back to the original behaviour.

The exact source change is in [`defender-raid.diff`](defender-raid.diff): five
added lines in one script, and one small edit made twice in the other.

---

## 1. The squad leader stays in your party for good

**What players see.** You go on the raid, kill some of the cannibals, then leave
the main map — through the cave, the entrance, or onto the world map. You are
sent back to Olympus with *"You left the location. Your mission is over."* A
Defender in power armour with a minigun is still following you. Talk to him and
he asks, as if you were still on the raid, *"Do you think they had enough?"*

**Who he is.** The leader of the Punisher squad that goes with you
(`olxcchef.int`). The soldiers use a different script (`olxcartl.int`).

**What goes wrong.** Leaving the raid map is meant to end the mission. When it
happens, every squad member starts its own short timer, and whichever finishes
first sends everyone back to Olympus. The engine cancels every other pending
script timer when the map changes (`_queue_leaving_map()` in fallout2-ce's
`queue.cc`), so only one timer ever fires.

That is harmless for the soldiers, because they have a backup: on every update
they check "is the raid over (global 336) and am I still in the party?" and
leave if so. The leader has no such check. He can only leave inside his own
timer — which was just cancelled — and he never starts another. He stays a
permanent follower.

**The fix.** The leader gets the soldiers' exact check, copied from
`olxcartl.int`. Once the raid is over he leaves your party, however it ended.

**Saves where he is already following you:** he leaves the moment the save
loads.

**Unchanged on purpose:** leaving the main raid map still ends the mission —
that is the original design. The intended way to finish is to talk to the squad
leader and answer *"Yes, the rest will scatter anyway. It's time to get back."*

## 2. Captain #34 hands you a second Defender suit

**What players see.** "Here's your Defender suit. Put it on." — and you end up
with two.

**What goes wrong.** Captain #34's script (`oln34.int`, nodes `Node011` and
`Node012`, one per raid) always creates a new suit, even when you already carry
one.

**The fix.** If you carry a Defender suit he puts you in that one; he only
creates a new suit when you have none.

---

## How the fix was made and checked

1. Decompiled the shipped scripts with **int2ssl 8.4.9**.
2. Recompiled the *unmodified* decompiled source with **sslc** (sfall edition
   4.5.1, `-O0`). The output was **byte-identical** to the shipped `.int` files,
   so the toolchain reproduces the original exactly.
3. Made the edits in `defender-raid.diff`, compiled again, and decompiled the
   result. The only differences from the original are the intended lines.

Script-local variables used are ones these scripts already have, so existing
saves stay compatible.

**Not playtested.** If either bug still happens with the patch installed,
please report it.

## Known, not fixed

A separate problem in the same script, in the weapon test that comes before
the raid, can make *"all of my items are gone"*:

- During the test your gear is put in a hidden container. The script searches
  for that container on a different tile from the one it creates it on, and
  keeps the reference in a variable the game does not save. Saving and loading
  in the middle of the test can lose the reference, so your gear is never handed
  back. It is still in the game, in a container you cannot reach.
- The script marks the test finished before it gives your gear back. If that
  final conversation is cut short, the hand-back never runs again.

Either would explain that report. Neither is changed yet.
