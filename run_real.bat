@echo off
REM Free 3-model mode. First set your keys ONCE in a terminal (they are stored in your Windows user settings, not in this folder):
REM   setx TF_GEMINI_API_KEY "your-gemini-key"
REM   setx TF_GROQ_API_KEY "your-groq-key"
REM then close and reopen the terminal / double-click this file.
set "TF_MODELS=gemini-3.5-flash-lite|https://generativelanguage.googleapis.com/v1beta/openai|env:TF_GEMINI_API_KEY|gemini-3.5-flash-lite;gpt-oss-120b|https://api.groq.com/openai/v1|env:TF_GROQ_API_KEY|openai/gpt-oss-120b;qwen3.8-27b|https://api.groq.com/openai/v1|env:TF_GROQ_API_KEY|qwen/qwen3.8-27b"
call "%~dp0run.bat"
