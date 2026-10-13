@echo off
setlocal enabledelayedexpansion
title INQUIRY OT Tutor - System Troubleshooter & Health Check
color 0B

cd /d "%~dp0"

echo ====================================================================
echo         INQUIRY OT TUTOR - 1-CLICK SYSTEM TROUBLESHOOTER
echo ====================================================================
echo.
echo Running diagnostic health check...
echo.

set "PYCMD="

:: Check python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYCMD=python"
    goto :RUN_DIAG
)

:: Check py
py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYCMD=py -3"
    goto :RUN_DIAG
)

:: Check local AppData python
if exist "%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe" (
    set "PYCMD="%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe""
    goto :RUN_DIAG
)

echo [CRITICAL ERROR] Python was not found on your system!
echo Please install Python from https://www.python.org/
pause
exit /b 1

:RUN_DIAG
%PYCMD% troubleshoot.py
echo.
pause
