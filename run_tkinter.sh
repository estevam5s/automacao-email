#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
export PYTHONPATH=.
python ui/desktop/app_tkinter.py
