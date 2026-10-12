# Truth-Finder plan: from prototype to public

## Honest starting point
**No tool can be infallible, including this one.** Sources can be wrong, search engines decide what we see,
and AI models can misread or make things up. Truth-Finder's job is not to be an oracle. It shows its work so that
*you* can check it, and it says "I don't know" instead of guessing.

### How it guards against errors and manipulation (today)
| Risk | Guard |
|---|---|
| AI invents sources | Code deletes any citation not in the real source list |
| AI overclaims | "Proven" auto-downgraded unless 2+ supporting sources of 2+ types and none contradicting |
| Too little evidence | "Evidence is thin" shown; no verdict produced |
| A source is down | Shown on the page; never silently ignored |
| Junk results padding the list | Keyword relevance filter (reported as "filtered out") |
| One-sided sources | Pulls 7 source types; labels type + approximate news leaning |
| Web pages containing hidden instructions to the AI ("prompt injection") | Prompt tells the model source text is data only; and the code-level checks above still apply |
| Confirmation bias | Strongest counter-argument always shown |
| Blind trust | Every link shown + "verify it yourself" steps |

Added in v0.2: multi-model cross-check (disagreements shown in red; weakest verdict wins), exact-quote citations with an
automatic check that each quote really appears in the source, full-article reading, fact-checker search, optional Google
Fact Check Tools API, opposing-framing searches, dates and reliability notes per source type, 24h caching.

### Known gaps to fix next
- Full text is read for up to 8 web pages; research papers still use abstracts/titles only.
- Cross-checking only helps if the models are truly different (use different companies). They can still share the same blind spots.
- Quote checking proves a quote exists, not that it was understood correctly or in context.
- Fact-checker search through DuckDuckGo often returns generic pages (filtered out); the free Google Fact Check API key works much better.
- Search results come from DuckDuckGo/Bing ranking, which has its own biases. Next: add more search backends (e.g. Brave, Mojeek, SearXNG).
- The leaning table is small and hand-made. Next: use a published, cited dataset and show the citation.
- The relevance filter is keyword-based and can drop good sources or keep bad ones.
- Add dedicated news-from-multiple-leanings search (e.g. GDELT free API), plus fact-checker search (Google Fact Check Tools API is free with a key).
- Save every answer with a public link and a "report a mistake" button, and publish the error log.
- Test set: 100 questions with known answers, re-run on every code change, publish the accuracy score.

## Steps to make it public (nothing has been done yet; needs Nicholas's OK)
1. Create a free GitHub account/organization (e.g. `truthfinder-org`) and push this folder. MIT license is already included.
2. Add `CONTRIBUTING.md`, a code of conduct, and issue templates for "wrong answer" reports.
3. Host it (free options, as of 2026 - check current terms, they change):
   - **Render** / **Koyeb** free web-service tiers (sleep when idle; slow first load).
   - **Hugging Face Spaces** (free CPU tier, good for open AI projects).
   - **Fly.io** small machines (low cost, close to free at low traffic).
4. AI: start with a free tier (Groq, OpenRouter free models, Google Gemini free tier) or donated credits.

## Costs (prices checked 2026-10-12 on the providers' own pricing pages; they change often)

### Token estimate per question (current design: 2 models, full text) - ESTIMATE
Measured on the box: the source pack for real questions was 19,760-23,609 characters (≈5,000-6,000 tokens).
- Claim-splitting call (model 1): ≈6,500 in / 200 out
- Judge call, per model: ≈7,000 in / ≈2,000 out (assumes JSON with quotes; "thinking" models may use more)
- **Total for 2 models ≈ 21,000 input + 4,200 output tokens per question** (assumption, not measured on a real model yet)

### Model prices (USD per 1M tokens, input / output)
| Model | Price | Free tier? | Source |
|---|---|---|---|
| Google Gemini 2.5 Flash-Lite | $0.10 / $0.40 | **Yes** (free tier; free-tier data may be used to improve Google products; limits shown in AI Studio) | https://ai.google.dev/gemini-api/docs/pricing |
| Google Gemini 3.1 Flash-Lite | $0.25 / $1.50 | Yes | same |
| OpenAI gpt-5-nano | $0.05 / $0.40 | No | https://developers.openai.com/api/docs/pricing |
| OpenAI gpt-4o-mini | $0.15 / $0.60 | No | same |
| OpenAI gpt-5-mini | $0.25 / $2.00 | No | same |
| Anthropic Claude Haiku 5.5 (prompts ≤100k) | $0.10 / $0.50 | Small trial credits only | https://docs.claude.com/en/docs/about-claude/pricing |
| DeepSeek deepseek-flash | $0.30 / $1.20 peak, half off-peak | No | https://api-docs.deepseek.com/quick_start/pricing |
| Groq openai/gpt-oss-120b | free tier: 30 req/min, 1,000 req/day, **8K tokens/min** | **Yes** | https://console.groq.com/docs/rate-limits |
| Ollama (local) | $0 per question | n/a | runs on your own computer |

Notes: Groq's 8K tokens/minute free limit is smaller than one full judge prompt, so use the `max_chars` option (e.g. 700) for Groq; that means it sees less text. Anthropic and Google Gemini aren't natively "OpenAI-compatible" in every case; Gemini offers an OpenAI-compatible endpoint (used in the README example). Anthropic would need a small adapter (not built yet). Ollama: an 8B model needs roughly 8 GB of free RAM (GPU optional but much faster); it's slower and less accurate than hosted models (general guidance, not tested here).

### Per-question and monthly cost - ESTIMATES (AI only, before caching)
Pair A = cheapest cross-check (Gemini 2.5 Flash-Lite splits claims + judges; gpt-5-nano judges). Pair B = stronger (gpt-5-mini + Claude Haiku 5.5).
| | Per question | ~100/mo (just Nicholas) | 1,000/mo | 30,000/mo | 300,000/mo |
|---|---|---|---|---|---|
| **Free tiers** (Gemini free + Groq free) | $0 | **$0** | $0 if under the daily limits (Groq 1,000/day) | not realistic on free tiers | no |
| **Pair A** | ≈ $0.0034 | ≈ $0.34 | ≈ $3.40 | ≈ $100 | ≈ $1,000 |
| **Pair B** | ≈ $0.0095 | ≈ $0.95 | ≈ $9.50 | ≈ $285 | ≈ $2,850 |
| **Local Ollama** | $0 (electricity) | $0 | $0, slow | needs real servers | needs real servers |
Caching: if ~30% of public questions repeat (assumption), cut AI costs ~30%.

### Hosting and search - ESTIMATES
| Scale | Hosting | Search | Notes |
|---|---|---|---|
| Just Nicholas | $0: run on his own computer, or Render free web service (512 MB, sleeps when idle) - https://render.com/pricing | $0 | |
| 1,000/mo | $0-7 (Render free or $7/mo "less than 1 CPU") | $0 | |
| 30,000/mo | ≈ $25-85/mo | DuckDuckGo scraping will likely get blocked; a paid search API would be needed (price NOT verified here) | Wikipedia/OpenAlex/Crossref/PubMed are free but rate-limited; cache |
| 300,000/mo | ≈ $175-450/mo (several CPUs) | paid search API, likely the biggest cost after AI (not verified) | |

**Rough all-in totals (estimates): just Nicholas $0; 1,000/mo ≈ $0-15; 30,000/mo ≈ $150-400; 300,000/mo ≈ $1,500-4,000+.**

### Cheapest way for Nicholas to start testing real AI mode ($0)
1. Get a free Gemini API key at Google AI Studio (aistudio.google.com) with a Google account.
2. Get a free Groq key at console.groq.com (different model family = a more independent cross-check).
3. Run with the `TF_MODELS` example in the README. Cost: $0 within free limits.
Caveat: free-tier inputs may be used by the provider to improve their products, so don't type anything private.

## Keeping it free
- **Caching:** the same popular questions get asked a lot; reuse answers (with a "refresh" button).
- **Donations:** GitHub Sponsors, Open Collective (shows every dollar in and out publicly - fits the transparency goal).
- **Grants:** Mozilla Foundation, Wikimedia-related grants, Knight Foundation (journalism/info), NLnet (open source), Google News Initiative. (Eligibility varies; check each.)
- **Donated credits:** AI and cloud companies often give credits to open-source/nonprofit projects.
- Rule: **no ads, no selling data, no paid "better answers."** Anyone funding it gets no say over answers; publish all funders.

## Bias and transparency
- Open code, open prompt (it's in `app.py`), open source list, open funding.
- Show source types and leanings; aim for balance across leanings and types for every answer.
- Publish the test set and accuracy results, including failures.
- Public "wrong answer" reports, reviewed in the open.
- Let users choose the AI model, so no single AI company controls the answers.
