#!/bin/sh
# One command: ./run.sh  then open http://127.0.0.1:5000
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
exec .venv/bin/python app.py
