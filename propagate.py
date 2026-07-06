#!/usr/bin/env python3
"""Validate bracket.json and propagate knockout winners into the next round.

Usage: python3 propagate.py
Exits 0 on success (prints what it changed, if anything), 1 on invalid data.
Safe to run repeatedly — idempotent.
"""
import json, sys, os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bracket.json")

# match -> (feeder for t1, feeder for t2); mirrors META in index.html
FEEDERS = {
    "89": ("74", "77"), "90": ("73", "75"), "91": ("76", "78"), "92": ("79", "80"),
    "93": ("83", "84"), "94": ("81", "82"), "95": ("86", "88"), "96": ("85", "87"),
    "97": ("89", "90"), "98": ("93", "94"), "99": ("91", "92"), "100": ("95", "96"),
    "101": ("97", "98"), "102": ("99", "100"),
    "104": ("101", "102"),
}
THIRD_PLACE = ("101", "102")  # match 103 takes the LOSERS of the semis

def team(m, k):
    return m.get("t1") if k == 1 else m.get("t2")

def main():
    try:
        with open(PATH) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"INVALID: bracket.json failed to parse: {e}")
        return 1

    ms = data.get("m", {})
    problems, changes = [], []

    for num, m in ms.items():
        w = m.get("w")
        if w not in (None, 1, 2):
            problems.append(f"M{num}: w must be 1, 2 or null (got {w!r})")
        if w and not team(m, w):
            problems.append(f"M{num}: w={w} but t{w} is empty")

    def fill(target, slot, name, why):
        cur = ms[target].get(slot)
        if cur == name:
            return
        if cur and cur != name:
            problems.append(f"M{target}.{slot} is '{cur}' but {why} is '{name}'")
            return
        ms[target][slot] = name
        changes.append(f"M{target}.{slot} <- {name} ({why})")

    # winners advance
    for target, (f1, f2) in FEEDERS.items():
        for slot, feeder in (("t1", f1), ("t2", f2)):
            fm = ms.get(feeder, {})
            if fm.get("w"):
                name = team(fm, fm["w"])
                if name:
                    fill(target, slot, name, f"winner of M{feeder}")

    # semifinal losers meet in the third-place match
    if "103" in ms:
        for slot, feeder in (("t1", THIRD_PLACE[0]), ("t2", THIRD_PLACE[1])):
            fm = ms.get(feeder, {})
            if fm.get("w"):
                name = team(fm, 2 if fm["w"] == 1 else 1)
                if name:
                    fill("103", slot, name, f"loser of M{feeder}")

    # champion from the final
    fm = ms.get("104", {})
    if fm.get("w"):
        name = team(fm, fm["w"])
        if name and data.get("champion") != name:
            data["champion"] = name
            changes.append(f"champion <- {name}")

    if problems:
        print("INVALID:")
        for p in problems:
            print("  " + p)
        return 1

    if changes:
        with open(PATH, "w") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print("Propagated:")
        for c in changes:
            print("  " + c)
    else:
        print("OK: valid, nothing to propagate")
    return 0

if __name__ == "__main__":
    sys.exit(main())
