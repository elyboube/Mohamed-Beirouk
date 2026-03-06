# Script PowerShell pour lancer le serveur Django
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectPath = Join-Path $scriptPath "tourism_platform"
Set-Location -Path $projectPath
Write-Host "Lancement du serveur Django depuis: $projectPath" -ForegroundColor Green
python manage.py runserver
