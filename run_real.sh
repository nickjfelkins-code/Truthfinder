#!/bin/sh
# Real two-model cross-check: Gemini (free tier) + Groq (free tier).
# Keys are read from env vars TF_GEMINI_API_KEY and TF_GROQ_API_KEY - never put keys in this file.
export TF_MODELS="gemini-3.5-flash-lite|https://generativelanguage.googleapis.com/v1beta/openai|env:TF_GEMINI_API_KEY|gemini-3.5-flash-lite;groq-gpt-oss-120b|https://api.groq.com/openai/v1|env:TF_GROQ_API_KEY|openai/gpt-oss-120b|600"
exec "$(dirname "$0")/run.sh"
