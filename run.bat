@echo off
REM Lance le serveur Django
cd /d "%~dp0tourism_platform"
python manage.py runserver %*
