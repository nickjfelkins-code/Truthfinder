"""Measure agreement and stability across saved Truth-Finder results. Usage: metrics.py label q1run1.json q1run2.json -- q2run1.json ..."""
import json, sys
def load(p): return json.load(open(p))["analysis"]
groups, cur = [], []
for a in sys.argv[2:]:
    if a == "--": groups.append(cur); cur = []
    else: cur.append(a)
groups.append(cur)
tot = agree = unk_dis = 0; same_main = 0; pairs = 0; rows = []
for g in groups:
    runs = [load(p) for p in g]
    mains = []
    for a in runs:
        cs = a["claims"]; tot += len(cs)
        agree += sum(c["agree"] for c in cs)
        unk_dis += sum((not c["agree"]) and c["category"] == "Unknown" for c in cs)
        mains.append(cs[0]["category"] if cs else "none")
    q = json.load(open(g[0]))["question"]
    rows.append((q, mains, [sorted(c["category"] for c in a["claims"]) for a in runs]))
    pairs += 1; same_main += len(set(mains)) == 1
print(f"== {sys.argv[1]}: claims={tot}  all-models-agree={agree/tot:.0%}  unknown-because-disagree={unk_dis/tot:.0%}  main-claim-stable={same_main}/{pairs}")
for q, m, cats in rows: print(f"  {q[:45]:45} main-claim verdicts per run: {m}  | all: {cats}")

# Extra: decisive rate (unanimous or clear majority) and a 2-model-only view (Gemini + gpt-oss) for apples-to-apples comparison
dec = two_tot = two_agree = 0
for g in groups:
    for p in g:
        for c in load(p)["claims"]:
            dec += c["agree"] or c.get("majority", False)
            pm = c.get("per_model", {})
            pair = [v for k, v in pm.items() if "gemini" in k or "oss" in k]
            if len(pair) == 2: two_tot += 1; two_agree += pair[0] == pair[1]
print(f"  decisive (unanimous or majority) = {dec/tot:.0%}" + (f";  Gemini-vs-gpt-oss agreement = {two_agree/two_tot:.0%}" if two_tot else ""))
