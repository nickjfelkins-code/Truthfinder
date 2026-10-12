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

Added in v0.4: identical compact "evidence pack" for every model (most relevant sentences per source, picked by plain
keyword ranking, so it is the same every run); a third model (Qwen) with a transparent majority vote ("MAJORITY 2 of 3",
dissent named, never called "strong"); fixed seed + temperature 0; a "reported belief" guard (quotes like "proponents
claim..." no longer count as support); per-site fact-checker searches (Snopes, PolitiFact, FactCheck.org...).

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

## FINAL cost answer for going public (checked 2026-10-12; estimates are labeled)

**Putting the code on GitHub costs $0.** Public repos are free. Publishing code does NOT mean running a public website;
anyone could run their own copy with their own free keys. The costs below are only for running a public *website*.

### What one question actually uses (MEASURED on real runs, v0.4, 3 models)
- 4 AI calls (claim split + 3 judges): about 8,300-10,600 input + 4,300-5,500 output tokens in total.
- About 10 web searches (DuckDuckGo) + 6 free research/encyclopedia API calls + up to 8 page downloads.
- 22-58 seconds per fresh question (cached repeats are instant).

### Prices used
- Gemini 3.5 Flash-Lite: free tier, or $0.30 in / $2.50 out per 1M tokens - https://ai.google.dev/gemini-api/docs/pricing
- Groq free tier: 1,000 requests/day and 8K tokens/minute per model - https://console.groq.com/docs/rate-limits . Groq paid prices were NOT checked; assumed about $0.15 / $0.60 per 1M (ESTIMATE).
- Search at scale: Brave Search API, $5 per 1,000 requests; even its free plan needs a credit card on file - https://brave.com/search/api/
- Hosting: Render free (512 MB, sleeps when idle), $7/mo small, $25/mo 1 CPU, $175+/mo 4 CPU - https://render.com/pricing

### Tiers (monthly, ESTIMATES)
| Tier | Questions/mo | AI | Search | Hosting | **Total** | Notes |
|---|---|---|---|---|---|---|
| 0. Just Nicholas | ~100 | $0 (free tiers) | $0 (DuckDuckGo) | $0 (his PC or the box) | **$0** | Works today |
| 1. Small public beta | ~1,000 (~35/day) | $0 (free tiers; about 1 question/minute max) | $0 (DuckDuckGo; may get blocked at times) | $0-7 | **$0-7** | Slow first load on free hosting; free-tier providers may use inputs to improve their models |
| 2. Real public site | ~30,000 (~1,000/day) | ~$240 (~$0.008/question, paid tiers needed) | ~$750 (5 Brave searches/question) | ~$25-85 | **~$1,000** (~$700 with 30% cache hits) | Free tiers can't handle this |
| 3. Popular | ~300,000 | ~$2,400 | ~$7,500 | ~$175-450 | **~$10,000** (~$7,000 with caching) | Needs grants/donations |

Correction to earlier versions of this plan: at scale, **search, not AI, is the biggest cost.** Ways to cut it: fewer
searches per question (~5 instead of ~10), heavy caching, or a self-hosted SearXNG metasearch server (free software, but
it relies on other engines and can get blocked; untested).

### Recommendation
Publishing the code on GitHub is free and safe. Run a public website only at Tier 1 ($0-7/mo) until there is funding
(grants/donations) for Tier 2.

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
