@echo off
title AeroFret: Kinetic — Studio Control Center
chcp 65001 > nul
cd /d "%~dp0"
color 0B
cls
python launcher.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ====================================================================
    echo [NOTE] Studio Control Center closed.
    echo ====================================================================
    pause
)
