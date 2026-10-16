@echo off
chcp 65001 >nul
cd /d %~dp0
where python >nul 2>nul
if %errorlevel%==0 (
    python pet_qt.py
) else (
    "C:\Users\lenovo\.workbuddy\binaries\python\envs\default\Scripts\python.exe" pet_qt.py
)
if errorlevel 1 pause
