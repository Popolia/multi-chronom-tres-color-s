# build.ps1
# Nettoie, recompile et prépare le dossier dist/ complet (exe + assets)
# A lancer depuis le dossier du projet, avec le venv deja active.

Write-Host "=== Nettoyage des anciens fichiers de build ===" -ForegroundColor Cyan
Remove-Item -Recurse -Force dist, build, gestionnaire_lignes.spec -ErrorAction SilentlyContinue

Write-Host "=== Compilation avec PyInstaller ===" -ForegroundColor Cyan
python -m PyInstaller --onefile --icon=assets\logo.ico gestionnaire_lignes.py

if (-not (Test-Path "dist\gestionnaire_lignes.exe")) {
    Write-Host "Echec de la compilation, arret du script." -ForegroundColor Red
    exit 1
}

Write-Host "=== Copie du dossier assets a cote de l'exe ===" -ForegroundColor Cyan
New-Item -ItemType Directory -Path "dist\assets" -Force | Out-Null
Copy-Item "assets\logo.png" "dist\assets\logo.png" -Force
Copy-Item "assets\logo.ico" "dist\assets\logo.ico" -Force

Write-Host "=== Termine ! ===" -ForegroundColor Green
Write-Host "Executable pret dans : dist\gestionnaire_lignes.exe"
Write-Host "Structure finale :"
Get-ChildItem dist -Recurse | Select-Object FullName
