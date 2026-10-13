@echo off
setlocal enabledelayedexpansion
title INQUIRY OT Tutor - AI Mentor for Occupational Therapy Students
color 0A

:: Always switch to the directory where this script is located
cd /d "%~dp0"

echo ====================================================================
echo             INQUIRY OT TUTOR - CLINICAL AI MENTOR
echo       Aligned with TN Dr. M.G.R. Medical University Syllabus
echo ====================================================================
echo.
echo [1/2] Checking Python installation...

set "PYCMD="

:: Check standard 'python'
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYCMD=python"
    goto :PYTHON_FOUND
)

:: Check Python Launcher 'py'
py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYCMD=py -3"
    goto :PYTHON_FOUND
)

:: Check User Local AppData Python (Windows Python 3.14)
if exist "%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe" (
    set "PYCMD="%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe""
    goto :PYTHON_FOUND
)

:: Check standard Local Programs Python
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if exist "%%D\python.exe" (
        set "PYCMD="%%D\python.exe""
        goto :PYTHON_FOUND
    )
)

:PYTHON_NOT_FOUND
color 0C
echo.
echo [ERROR] Python was not detected on your computer!
echo.
echo To fix this:
echo 1. Download and install Python from: https://www.python.org/downloads/
echo 2. During installation, make sure to CHECK the box:
echo    "Add Python to PATH"
echo.
pause
exit /b 1

:PYTHON_FOUND
echo Python found: %PYCMD%
echo.
echo [2/2] Starting INQUIRY OT Tutor Server...
echo The web browser will open automatically once the server is ready!
echo.
echo Tip: Keep this window open while using the tutor.
echo      To stop the server, press Ctrl + C or simply close this window.
echo ====================================================================
echo.

%PYCMD% app.py

if %errorlevel% neq 0 (
    echo.
    echo Server exited with an error code. 
    echo Running Troubleshooter...
    pause
)
