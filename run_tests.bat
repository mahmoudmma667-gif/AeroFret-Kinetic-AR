@echo off
chcp 65001 > nul
title AeroFret: Kinetic - Automated Verification Suite
echo ===================================================
echo   AeroFret: Kinetic - Running Automated Tests
echo ===================================================
python -m unittest discover tests
echo.
pause
