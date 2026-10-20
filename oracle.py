#!/usr/bin/env python3
# Clamp Math oracle - mirrors engine.js with Fractions: the line is solved from its two points, the width for a target size is found by bisection on exact fractions, and rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

def num(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,5}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def rnd(fr, places):  # exact Fraction to a scaled integer, ties away from zero
    d = Decimal(fr.numerator) / Decimal(fr.denominator) * (10 ** places)
    return int(d.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
def txt(v, places):
    neg = v < 0; a = abs(v); ip, fp = divmod(a, 10 ** places)
    fs = str(fp).zfill(places).rstrip("0") if places else ""
    return ("-" if neg else "") + (f"{ip}.{fs}" if fs else str(ip))
MIN = "the smallest size must be a whole number of px from 1 to 200"
MAX = "the largest size must be a whole number of px from 1 to 200"
W1 = "the smallest width must be a whole number of px from 200 to 4000"
W2 = "the largest width must be a whole number of px from 200 to 4000"
def pair(a, b, c, d):
    m = num(a, MIN, 1, 200); M = num(b, MAX, 1, 200); w = num(c, W1, 200, 4000); W = num(d, W2, 200, 4000)
    if M <= m: raise ValueError("the largest size must be bigger than the smallest size")
    if W <= w: raise ValueError("the largest width must be wider than the smallest width")
    return m, M, w, W
def line(m, M, w, W):
    slope = F(M - m, W - w)            # px of text per px of width
    icpt = F(m) - slope * w            # px at width 0
    assert icpt + slope * w == m and icpt + slope * W == M
    return slope, icpt

def formula(a, b, c, d, root):
    m, M, w, W = pair(a, b, c, d); r = num(root, "the root size must be a whole number of px from 8 to 32", 8, 32)
    slope, icpt = line(m, M, w, W)
    return f"clamp({txt(rnd(F(m, r), 4), 4)}rem, {txt(rnd(icpt / r, 4), 4)}rem + {txt(rnd(slope * 100, 4), 4)}vw, {txt(rnd(F(M, r), 4), 4)}rem) takes the text from {m}px at {w}px wide to {M}px at {W}px wide, counting 1rem as {r}px. The numbers are rounded to 4 places, so the ends can be off by a tiny fraction of a pixel."
def size(a, b, c, d, at):
    m, M, w, W = pair(a, b, c, d); v = num(at, "the viewport width must be a whole number of px from 1 to 20000", 1, 20000)
    if v <= w: return f"At {v}px wide the text sits at its smallest size, {m}px."
    if v >= W: return f"At {v}px wide the text sits at its largest size, {M}px."
    slope, icpt = line(m, M, w, W)
    return f"At {v}px wide the text is {txt(rnd(icpt + slope * v, 2), 2)}px, between {m}px and {M}px."
def reach(a, b, c, d, t):
    m, M, w, W = pair(a, b, c, d); t = num(t, "the target size must be a whole number of px from 1 to 200", 1, 200)
    if t < m or t > M: return f"A size of {t}px is outside the range from {m}px to {M}px, so the text never has it."
    slope, icpt = line(m, M, w, W)
    lo, hi = F(w), F(W)
    for _ in range(200):  # bisection on exact fractions
        mid = (lo + hi) / 2
        if icpt + slope * mid < t: lo = mid
        else: hi = mid
    x = (lo + hi) / 2
    # snap to the exact answer when bisection has converged to it
    exact = (t - icpt) / slope
    assert abs(x - exact) < F(1, 10 ** 30)
    return f"The text is {t}px at {txt(rnd(exact, 1), 1)}px wide."

FNS = {"formulaTruth": formula, "sizeTruth": size, "reachTruth": reach}

def cases():
    c = []
    bases = [("16","24","400","1200"),("14","40","320","1920"),("1","200","200","4000"),("199","200","200","201"),("16","17","200","4000"),("10","11","333","999"),("12","18","375","1440"),("18","60","360","1280"),("7","9","1000","3001")]
    for b in bases:
        for root in ["16","10","8","32","15","24"][:3 if b[0] not in ("16","14") else 6]: c.append(("formulaTruth", list(b) + [root]))
    for b in bases:
        for v in ["1","200","400","401","800","1200","1201","20000"]: c.append(("sizeTruth", list(b) + [v]))
    for b in bases:
        for t in ["1","14","16","20","24","60","200"]: c.append(("reachTruth", list(b) + [t]))
    bad = ["", "x", "0", "1.5", "-1", "300000"]
    for i in range(4):
        for v in bad[:5] + ["201", "5"]:
            a = list(bases[0]); a[i] = v
            c += [("formulaTruth", a + ["16"]), ("sizeTruth", a + ["800"]), ("reachTruth", a + ["20"])]
    c += [("formulaTruth", ["24","16","400","1200","16"]), ("formulaTruth", ["16","16","400","1200","16"]), ("formulaTruth", ["16","24","1200","400","16"]), ("formulaTruth", ["16","24","800","800","16"]),
          ("formulaTruth", ["16","24","400","1200","7"]), ("formulaTruth", ["16","24","400","1200","33"]), ("formulaTruth", ["16","24","400","1200",""]),
          ("sizeTruth", ["16","24","400","1200","0"]), ("sizeTruth", ["16","24","400","1200","20001"]), ("sizeTruth", ["16","24","400","1200",""]),
          ("reachTruth", ["16","24","400","1200","0"]), ("reachTruth", ["16","24","400","1200","201"]), ("reachTruth", ["16","24","400","1200",""]),
          ("formulaTruth", [" 16 "," 24 "," 400 "," 1200 "," 16 "])]
    r = random.Random(706)
    for _ in range(10):
        m = r.randint(1, 100); M = r.randint(m + 1, 200); w = r.randint(200, 3000); W = r.randint(w + 1, 4000)
        c.append(("formulaTruth", [str(m), str(M), str(w), str(W), str(r.randint(8, 32))]))
        c.append(("sizeTruth", [str(m), str(M), str(w), str(W), str(r.randint(1, 5000))]))
        c.append(("reachTruth", [str(m), str(M), str(w), str(W), str(r.randint(m, M))]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":")) for o in out) + "\n]\n")
print(len(out), "cases written")
