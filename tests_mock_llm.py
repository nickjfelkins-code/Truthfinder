"""Fake OpenAI-compatible server, ONLY to test the AI display path offline. Its answer is canned, NOT real analysis."""
import json
from flask import Flask, jsonify
m = Flask(__name__)
@m.post("/v1/chat/completions")
def c():
    out = {"summary": "[MOCK TEST OUTPUT - not a real analysis]", "evidence_sufficient": True, "confidence": "Medium",
           "confidence_reasons": ["mock"], "strongest_counterargument": "mock counter-argument",
           "verify_yourself": ["mock step"],
           "claims": [{"claim": "Mock claim cited with a fake id and one source", "category": "Proven",
                       "supporting_sources": [1, 999], "contradicting_sources": [], "explanation": "test", "who_benefits": "test"},
                      {"claim": "Mock disputed claim", "category": "Disputed", "supporting_sources": [2],
                       "contradicting_sources": [3], "explanation": "test", "who_benefits": "test"}]}
    return jsonify({"choices": [{"message": {"content": json.dumps(out)}}]})
m.run(port=5055)
