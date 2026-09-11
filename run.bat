@echo off
title AeroFret: Kinetic — Touchless Air Guitar
chcp 65001 > nul
cd /d "%~dp0"
color 0A
cls

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not added to PATH!
    echo Please install Python 3.10+ from python.org and add it to PATH.
    pause
    exit /b 1
)
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ====================================================================
    echo [NOTE] An issue occurred during execution.
    echo ====================================================================
    pause
)
