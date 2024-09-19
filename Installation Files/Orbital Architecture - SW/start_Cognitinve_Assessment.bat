@echo off

REM Redirecting output to log.txt in append mode
python pss_pvt_nback.py
python main.py
python nasaTLX.py
python encryption_hybrid.py