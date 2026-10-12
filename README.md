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

### Turn on AI analysis (optional) - use 2+ models for a cross-check
Any OpenAI-compatible API works. List models in `TF_MODELS`, separated by `;`, each as
`label|base_url|api_key|model[|max_chars_per_source]`:
```
export TF_MODELS="gemini|https://generativelanguage.googleapis.com/v1beta/openai|YOUR_GEMINI_KEY|gemini-2.5-flash-lite;groq|https://api.groq.com/openai/v1|YOUR_GROQ_KEY|openai/gpt-oss-120b|700"
./run.sh
```
(One model only? `TF_API_KEY`, `TF_BASE_URL`, `TF_MODEL` still work, but answers are marked "not cross-checked".)
Optional: `TF_GOOGLE_FACTCHECK_KEY` (free Google API key) adds the Google Fact Check Tools database.
Free/local: [Ollama](https://ollama.com) at `http://localhost:11434/v1` with any key text, e.g. `llama3.1:8b`.

### Free three-model setup (Gemini + gpt-oss + Qwen)
Put your free keys in environment variables (never in files): `TF_GEMINI_API_KEY` and `TF_GROQ_API_KEY`, then run
`./run_real.sh` (Mac/Linux) or double-click `run_real.bat` (Windows; the comments inside show how to set keys once with `setx`).
In `TF_MODELS`, a key written as `env:NAME` is read from that environment variable.

### How an AI answer is built
1. Gather sources (encyclopedia, research, PubMed, official, news, fact-checkers, web, plus an **opposing-framing search**), filter off-topic, dedupe.
2. Read the **full article text** of up to 8 web/news/official pages; pick up publish dates where available.
3. Model #1 splits the question into 2-5 checkable claims (including the opposite claim).
4. All models get the **same compact evidence pack** (top sentences per source). Every model judges every claim independently, citing **exact quotes**. Quotes that only report a belief ('proponents claim...') don't count as support.
5. **Self-check in code:** each quote must literally appear in that source, or it's thrown out.
6. Code rules: Proven needs 2+ verified quotes (and "Proven false" needs 2+ verified contradicting quotes) from 2+ source types and no contradiction; Disputed needs verified quotes on both sides.
7. **Cross-check:** all agree = 'strong'. A clear majority (2 of 3) is used but shown in yellow, naming the dissenting model. No majority = red warning and the *weaker* verdict is used.
8. Results cached 24h (with a "re-check now" button) so repeat questions are free and instant.

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
