#!/usr/bin/env python3
# food_gate.py — pass PEQ-YEAR-1 §6: the cooking-content red gate.
#
# The pass builds the colleague a FRAME and explicitly builds no cooking content:
# "a generated recipe or menu is a red gate" (§4). Two different assertions, because
# the estate already ships some food vocabulary and must keep it:
#
#   ZERO   on the surfaces this pass CREATED. Not one dish, recipe, menu or ingredient.
#   FROZEN on the surfaces that already existed. The Staff Guide's progression ladder
#          legitimately names typical dishes; this pass may neither add to nor remove
#          from that. The census must match the pinned baseline exactly.
#
# Planted control (the gate proving itself):
#   PEQ_YEAR1_PLANT_DISH=1 python3 _passpq/tools/food_gate.py   -> must exit 1
#
# Exit 0 = green. Exit 1 = red.

import os, re, sys, json, collections

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
KIT = os.path.join(ROOT, "GROW_ASDAN", "PEQ_L2_Kitchen")
BASELINE = os.path.join(ROOT, "_passpq", "inputs", "food_census_baseline.json")

# Surfaces this pass created — must carry ZERO cooking content.
NEW_SURFACES = ["Cooking_Handover.html", "Kitchen_Week_Shell.html",
                "Criteria_By_Week.html", "Kitchen_Completion_Checklist.html",
                "COOKING_HANDOVER.md"]
# Surfaces that already existed — their food census must not move.
EXISTING_SURFACES = ["Scheme_of_Work.html", "Criteria_Coverage_Matrix.html",
                     "Evidence_Sheets.html", "Plan_Templates.html", "Plan_Hours_Grid.html",
                     "Assessor_Checklists.html", "Staff_Kitchen_Guide.html"]

# Named dishes and ingredients. NOT the abstract category words ("recipe", "menu",
# "dish", "ingredient") — the frame has to be able to TALK ABOUT recipes while
# containing none, and a gate that cannot tell those apart is useless.
# Named dishes and ingredients, as EXPLICIT LISTS. Not a pipe-delimited blob: the first
# version of this gate built its alternation by splitting one, which (a) produced empty
# alternatives that matched at every position, and (b) tore "fish and chips" into three
# entries, so the bare word "and" became a dish. Lists cannot do either.
# These are NOT the abstract category words ("recipe", "menu", "dish", "ingredient") —
# the frame has to be able to TALK ABOUT recipes while containing none, and a gate that
# cannot tell those apart is useless.
DISHES = [
    "lasagne", "lasagna", "bolognese", "carbonara", "risotto", "paella", "curry",
    "tagine", "chilli con carne", "casserole", "stew", "soup", "broth", "omelette",
    "frittata", "quiche", "shepherd'?s pie", "cottage pie", "fish and chips", "fishcake",
    "pizza", "burger", "sandwich", "toastie", "panini", "tortilla wrap", "salad",
    "coleslaw", "stir[- ]?fry", "nuggets", "scone", "muffin", "cupcake", "brownie",
    "flapjack", "shortbread", "cookie", "biscuit", "pancake", "waffle", "crumble",
    "trifle", "cheesecake", "victoria sponge", "focaccia", "baguette", "smoothie",
    "milkshake", "hummus", "guacamole", "salsa", "pesto", "gravy", "custard",
    "meringue", "porridge", "granola", "gnocchi", "noodles",
]
INGREDIENTS = [
    "onions?", "garlic", "tomato(?:es)?", "potato(?:es)?", "carrots?", "broccoli",
    "cauliflower", "courgettes?", "aubergines?", "mushrooms?", "spinach", "lettuce",
    "cucumbers?", "celery", "leeks?", "sweetcorn", "chicken", "beef", "pork", "lamb",
    "bacon", "sausages?", "mince", "turkey", "salmon", "tuna", "prawns?",
    "flour", "sugar", "butter", "margarine", "milk", "cheese", "yoghurt", "yogurt",
    "double cream", "rice", "pasta", "spaghetti", "oats", "lentils?", "chickpeas?",
    "baking powder", "yeast", "cinnamon", "paprika", "oregano", "basil", "coriander",
]
# Recipe/menu STRUCTURE — the shape of a recipe, whatever it is made of. Raw regexes,
# so these are used verbatim and never word-boundary-wrapped.
STRUCTURE = [
    r"ingredients\s*:", r"method\s*:", r"you will need\s*:", r"serves\s+\d",
    r"makes\s+\d\s", r"preheat", r"\b\d+\s?(?:g|kg|ml|oz|lb)\b", r"\btbsp\b",
    r"\btsp\b", r"\b\d{2,3}\s?°\s?[CF]\b", r"gas mark", r"main course",
    r"set menu", r"today'?s special",
]

def _alts(entries):
    """Word-bounded alternation from an explicit list. Asserts it cannot match nothing."""
    assert entries and all(e.strip() for e in entries), "empty alternative matches everywhere"
    pat = re.compile(r"\b(?:" + "|".join(entries) + r")\b", re.I)
    assert not pat.match(""), "pattern matches the empty string"
    return pat

PATTERNS = {
    "dish": _alts(DISHES),
    "ingredient": _alts(INGREDIENTS),
    "structure": re.compile("|".join(STRUCTURE), re.I),
}

# The neutral kit list the Staff Guide already carries is explicitly allowed.
KIT_ALLOW = re.compile(r"colour-coded boards|bench mats|knife set|peelers|graters|"
                       r"measuring sets|baking trays|mixing bowls|oven gloves|aprons|"
                       r"blue plasters|cleaning caddies|plate stock", re.I)


def scan(path, text):
    hits = collections.Counter()
    detail = []
    for kind, pat in PATTERNS.items():
        for m in pat.finditer(text):
            lo = max(0, m.start() - 60)
            ctx = text[lo:m.end() + 60].replace("\n", " ")
            if KIT_ALLOW.search(ctx):
                continue
            hits[kind] += 1
            line = text.count("\n", 0, m.start()) + 1
            detail.append({"kind": kind, "match": m.group(0), "line": line,
                           "context": ctx[:150]})
    return hits, detail


def read(name):
    p = os.path.join(KIT, name)
    if not os.path.isfile(p):
        return None
    return open(p, encoding="utf-8").read()


def main():
    plant = os.environ.get("PEQ_YEAR1_PLANT_DISH") == "1"
    red = []

    # --- 1. NEW surfaces: zero -------------------------------------------------
    print("ZERO check — surfaces created by this pass")
    for name in NEW_SURFACES:
        t = read(name)
        if t is None:
            red.append(f"{name}: MISSING — the pass is supposed to create it")
            print(f"  {name:<34} MISSING")
            continue
        if plant and name == "Cooking_Handover.html":
            t += "\n<p>Week 3: we are cooking spaghetti bolognese. Ingredients: 500g mince, "\
                 "2 onions, tinned tomatoes. Method: preheat to 180C.</p>"
        hits, detail = scan(name, t)
        n = sum(hits.values())
        print(f"  {name:<34} {n:>3} hits {dict(hits) if n else ''}")
        if n:
            red.append(f"{name}: {n} cooking-content hits {dict(hits)}")
            for d in detail[:6]:
                print(f"      L{d['line']} [{d['kind']}] {d['match']!r} … {d['context'][:90]}")

    # --- 2. EXISTING surfaces: frozen -----------------------------------------
    print("\nFROZEN check — surfaces that already existed")
    census = {}
    for name in EXISTING_SURFACES:
        t = read(name)
        if t is None:
            red.append(f"{name}: MISSING")
            continue
        hits, _ = scan(name, t)
        census[name] = dict(sorted(hits.items()))

    if not os.path.isfile(BASELINE):
        with open(BASELINE, "w") as f:
            json.dump({"note": "PEQ-YEAR-1 food census baseline — the pre-existing Kitchen "
                               "surfaces' food vocabulary, frozen. A move in either direction "
                               "is a red gate.", "census": census}, f, indent=1)
        print(f"  baseline WRITTEN (first run) -> {BASELINE}")
        for k, v in census.items():
            print(f"  {k:<34} {v}")
    else:
        base = json.load(open(BASELINE))["census"]
        for name in EXISTING_SURFACES:
            b, c = base.get(name), census.get(name)
            same = b == c
            print(f"  {name:<34} {'UNCHANGED' if same else 'MOVED'}  {c}")
            if not same:
                red.append(f"{name}: food census moved {b} -> {c}")

    print()
    if red:
        print("RED — food gate failed:")
        for r in red:
            print("   - " + r)
        if plant:
            print("\n(planted control was active — a red result here is the gate working)")
        return 1
    if plant:
        print("RED EXPECTED but gate stayed green — THE CONTROL FAILED, the gate is not "
              "detecting planted cooking content.")
        return 1
    print("GREEN — zero cooking content on the new surfaces; existing food census unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
