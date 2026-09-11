@echo off
chcp 65001 > nul
title AeroFret: Kinetic - System Pre-Flight Diagnostics
echo ===================================================
echo   AeroFret: Kinetic - Running Health Doctor Check
echo ===================================================
python tools/doctor.py
pause
