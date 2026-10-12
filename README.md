# 🧭 Truth-Finder

A free, open-source tool, owned by everyone (MIT license). Type any question and it:

1. **Searches many independent kinds of sources at once** (no paid keys needed):
   Wikipedia (encyclopedia), OpenAlex + Crossref + PubMed (academic research), .gov/.edu/.int sites
   (official/primary), news, fact-checkers, and the general web (via DuckDuckGo).
2. **Labels every source** with its type, and for known news outlets an *approximate* political leaning.
3. **Filters off-topic results and removes duplicates.**
4. **With AI turned on:** breaks the answer into individual claims, sorts each into **Proven / Disputed / Unknown**,
   lists which sources **support** and which **contradict** each claim, says **who benefits** if the claim is believed,
   gives a **confidence level with reasons**, and always shows the **strongest counter-argument**.
5. **Always** shows every source link and a **"How to verify this yourself"** checklist.

### Safety rules built into the code (not just the AI prompt)
- **No AI key = no verdicts.** "Basic mode" just groups and shows sources, and says plainly that AI analysis is off.
- **Thin evidence = no answer.** Fewer than 3 relevant sources, or only one type of source, means it says
  "Evidence is thin" and won't guess.
- **Made-up citations are deleted.** If the AI cites a source number that doesn't exist, it's removed.
- **"Proven" has to be earned.** A claim the AI calls Proven is automatically downgraded unless it has 2+ supporting
  sources of 2+ different types and no contradicting sources.
- **Failures are shown.** If a source is down, the page says so.

## Run it (one command)
Needs Python 3.10+.
```
./run.sh
```
Then open http://127.0.0.1:5000

### Turn on AI analysis (optional)
Any OpenAI-compatible API works (OpenAI, Groq, OpenRouter, a local Ollama server, etc.):
```
export TF_API_KEY=your-key
export TF_BASE_URL=https://api.openai.com/v1   # or another provider's /v1 URL
export TF_MODEL=gpt-4o-mini                     # any model that provider offers
./run.sh
```
Free/local option: run [Ollama](https://ollama.com) and use `TF_BASE_URL=http://localhost:11434/v1 TF_API_KEY=ollama TF_MODEL=llama3.1`.

## Files
- `app.py` - backend: source fetchers, relevance filter, AI analysis, safety checks
- `static/index.html` - the whole web page
- `tests_mock_llm.py` - fake AI server for testing the display (its answers are canned, not real)
- `screenshots/` - example outputs

## Contribute
Everyone's welcome, programmer or not:
- **Add a source:** write a function in `app.py` that returns `[{title, url, snippet, source, kind}]` and add it to `SOURCES`.
- **Improve fairness:** fix or extend the `LEANING` table (cite where the rating came from).
- **Report bad answers:** open an issue with the question and what was wrong. These are the most valuable reports.
- **Non-coders:** test questions, improve wording, translate.
