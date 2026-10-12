"""Repeatability test: same question 3x with fresh sources, then 3x with pinned sources. Compares URL/domain overlap + headline."""
import json, sys, time, itertools, requests
from urllib.parse import urlparse
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5003"
QS = sys.argv[3].split("||") if len(sys.argv) > 3 else ["are uaps none human intelagents", "Did Nikola Tesla invent free energy?", "Is solar the cheapest source of electricity?"]
def ask(q, mode):
    body = {"question": q, "refresh": True}
    if mode == "fresh": body["refresh_sources"] = True
    t = time.time(); d = requests.post(BASE + "/api/ask", json=body, timeout=900).json(); d["_secs"] = round(time.time() - t)
    return d
def jac(a, b): return len(a & b) / max(1, len(a | b))
def dom(u): return ".".join(urlparse(u).netloc.replace("www.", "").split(".")[-2:])
out = {}
for mode in (sys.argv[2].split(",") if len(sys.argv) > 2 else ("fresh", "pinned")):
    for q in QS:
        runs = []
        for r in range(3):
            d = ask(q, mode); a = d.get("analysis", {})
            runs.append({"urls": sorted({s["url"] for s in d.get("sources", [])}), "banner": a.get("banner", {}).get("word"),
                         "claims": [c["category"] for c in a.get("claims", [])], "secs": d["_secs"], "n": len(d.get("sources", [])),
                         "voices": a.get("independent_voices"), "err": d.get("error") or a.get("note")})
            print(mode, q[:30], r + 1, runs[-1]["banner"], runs[-1]["n"], "src", runs[-1]["voices"], "voices", runs[-1]["secs"], "s", runs[-1]["err"] or "", flush=True)
            time.sleep(25)
        pairs = list(itertools.combinations(runs, 2))
        out[f"{mode}|{q}"] = {"runs": runs,
            "url_overlap": round(sum(jac(set(a["urls"]), set(b["urls"])) for a, b in pairs) / 3, 2),
            "domain_overlap": round(sum(jac({dom(u) for u in a["urls"]}, {dom(u) for u in b["urls"]}) for a, b in pairs) / 3, 2),
            "headline_same": len({r["banner"] for r in runs}) == 1,
            "claim_verdicts_same": sum(len(set(x)) == 1 for x in zip(*[r["claims"] for r in runs])) , "claims": min(len(r["claims"]) for r in runs)}
        json.dump(out, open("eval/repeat_results.json", "w"), indent=1)
for k, v in out.items():
    print(f"{k[:60]:60} URL overlap {v['url_overlap']:.0%}  domain overlap {v['domain_overlap']:.0%}  headline same: {v['headline_same']} {[r['banner'] for r in v['runs']]}  claims same {v['claim_verdicts_same']}/{v['claims']}")
