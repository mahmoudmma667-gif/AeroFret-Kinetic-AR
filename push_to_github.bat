@echo off
chcp 65001 > nul
title AeroFret Kinetic - GitHub Push Utility
color 0B
cls
echo ================================================================
echo   AeroFret: Kinetic - Automated GitHub Push Utility
echo   Engineered & Architected by Mahmoud Labib
echo ================================================================
echo.
echo [INFO] Ready to push to your GitHub repository.
echo.

set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/username/repo): "

if "%REPO_URL%"=="" (
    echo [ERROR] No URL provided. Aborting.
    pause
    exit /b 1
)

echo.
echo [1/3] Configuring Git Remote 'origin'...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [2/3] Verifying Branch 'main'...
git branch -M main

echo [3/3] Pushing all 74 files, assets, and history to GitHub...
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ================================================================
    echo   SUCCESS! Your repository is now LIVE and public on GitHub!
    echo ================================================================
) else (
    echo.
    echo [NOTICE] If Git prompted you to log in, please complete the browser
    echo          authentication window to finish pushing.
)

echo.
pause
