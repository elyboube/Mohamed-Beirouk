@echo off
REM Convenience wrapper to run the inner manage.py using the active Python
cd /d "%~dp0tourism_platform"
python manage.py runserver %*
