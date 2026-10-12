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

### Known gaps to fix next
- Snippets are short; the AI sees summaries, not full articles. Next: fetch and read full pages/abstracts.
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

## Rough monthly cost (ESTIMATES - assumptions labeled)
| Usage (assumption) | Hosting | AI (assume ~6k input + 1k output tokens per question, small model at ~$0.15/$0.60 per million tokens - typical 2025-26 small-model prices) | Total |
|---|---|---|---|
| 1,000 questions/mo | $0 (free tier) | ≈ $1.50 | **≈ $0-5** |
| 30,000 questions/mo | $7-25 (basic paid tier) | ≈ $45 | **≈ $50-75** |
| 300,000 questions/mo | $50-150 | ≈ $450 + caching savings | **≈ $400-600** |
Free source APIs (Wikipedia, OpenAlex, Crossref, PubMed) have rate limits; at large scale, ask them for access and cache results. DuckDuckGo HTML scraping is not an official API and may block heavy use; a paid search API (e.g. Brave, ~$5 per 1,000 queries - estimate) may be needed at scale.

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
