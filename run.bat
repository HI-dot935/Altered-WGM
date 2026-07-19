@echo off
if not exist "venv" python -m venv venv
call venv\Scripts\activate
pip install -r backend\requirements.txt
python backend\app\main.py
pause
