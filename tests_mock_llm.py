"""Fake OpenAI-compatible server, ONLY to test Truth-Finder's AI plumbing offline.
Its answers are CANNED and NOT real analysis. Model "mock-a" and "mock-b" deliberately disagree on claim 2,
and mock-b includes one fabricated quote, so we can test cross-checking and quote verification."""
import json, re
from flask import Flask, jsonify, request
m = Flask(__name__)

def sources(prompt):
    out = {}
    for mm in re.finditer(r"\n\[(\d+)\] \(([^,)]+)[^\n]*\n([^\n]+)", prompt):
        sent = re.split(r"(?<=[.!?])\s", mm.group(3).strip())[0]
        out.setdefault(mm.group(2), []).append((int(mm.group(1)), sent))
    return out

@m.post("/v1/chat/completions")
def c():
    body = request.json; p = body["messages"][0]["content"]; model = body["model"]
    if "CLAIMS:" not in p:
        out = {"claims": ["MOCK claim one (main claim)", "MOCK claim two (opposite)", "MOCK claim three"]}
    else:
        s = sources(p); kinds = list(s)
        a, b = s[kinds[0]][0], s[kinds[1]][0]
        claim2 = {"n": 2, "category": "Disputed" if model == "mock-a" else "Unknown",
                  "support": [{"id": a[0], "quote": a[1]}], "contradict": [{"id": b[0], "quote": b[1]}],
                  "explanation": "mock", "who_benefits": "mock"}
        claim3 = {"n": 3, "category": "Proven", "support": [{"id": a[0], "quote": a[1]}], "contradict": [],
                  "explanation": "mock: only one source, should be downgraded", "who_benefits": "mock"}
        if model == "mock-b":
            claim3["support"].append({"id": b[0], "quote": "This sentence was invented and appears in no source at all."})
        out = {"summary": f"[MOCK {model} - not real analysis]", "confidence": "High" if model == "mock-a" else "Medium",
               "confidence_reasons": ["mock"], "strongest_counterargument": f"mock counter-argument from {model}",
               "verify_yourself": ["mock step"],
               "claims": [{"n": 1, "category": "Proven", "support": [{"id": a[0], "quote": a[1]}, {"id": b[0], "quote": b[1]}],
                           "contradict": [], "explanation": "mock", "who_benefits": "mock"}, claim2, claim3,
                          {"n": 99, "category": "Proven", "support": [], "contradict": []}]}
    return jsonify({"choices": [{"message": {"content": json.dumps(out)}}]})
m.run(port=5055)
