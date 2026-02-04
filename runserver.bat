@echo off
REM Convenience wrapper to run the inner manage.py using the active Python
python "%~dp0tourism_platform\manage.py" runserver %*
