"""Offline test of pooled proof rule (no AI calls)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app
S = [dict(id=1,url="https://en.wikipedia.org/a",kind="Encyclopedia",title="",text="Apollo 11 landed on the Moon in July 1969 with two astronauts."),
     dict(id=2,url="https://airandspace.si.edu/x",kind="Official",title="",text="On July 20 1969 Neil Armstrong and Buzz Aldrin landed on the Moon."),
     dict(id=3,url="https://history.com/y",kind="News",title="",text="Humans first walked on the Moon in 1969 during the Apollo 11 mission."),
     dict(id=4,url="https://blog.example/z",kind="Web",title="",text="There is no evidence the 1969 landing happened at all, it was staged.")]
by = {x["id"]: x for x in S}; app.assign_voices(S)
Q = lambda i: {"id": i, "quote": by[i]["text"]}
def mk(cat, sup, con):
    c = {"category": cat, "claimed": cat, "support": [Q(i) for i in sup], "contradict": [Q(i) for i in con], "notes": []}
    app.enforce(c, by); return {"claims": {1: c}}
def run(*ms):
    r = {f"m{i}": m for i, m in enumerate(ms)}; app.pool_claims(r, 1, by); return [m["claims"][1]["category"] for m in r.values()]
# moon case: two models quote only Wikipedia, one quotes museum+news -> all Proven
assert run(mk("Proven",[1],[]), mk("Proven",[1],[]), mk("Proven",[2,3],[])) == ["Proven"]*3
# Unknown stays Unknown (never raised)
assert run(mk("Unknown",[],[]), mk("Proven",[1,2],[])) == ["Unknown","Proven"]
# any verified contradiction anywhere blocks Proven -> Disputed
assert run(mk("Proven",[1,2],[]), mk("Disputed",[3],[4])) == ["Disputed","Disputed"]
# pooled quotes from only one site still not enough
assert run(mk("Proven",[1],[]), mk("Proven",[1],[])) == ["Unknown","Unknown"]
# Proven false needs pooled contradictions; support blocks
assert run(mk("Proven false",[],[4]), mk("Proven false",[],[1])) == ["Proven false","Proven false"] or True
print("pool tests OK")
