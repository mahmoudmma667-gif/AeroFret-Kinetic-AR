@echo off
chcp 65001 > nul
title AeroFret: Kinetic - Standalone Executable Builder
echo =========================================================
echo   AeroFret: Kinetic - Building Standalone Windows App
echo =========================================================
python tools/build_exe.py
echo.
pause
