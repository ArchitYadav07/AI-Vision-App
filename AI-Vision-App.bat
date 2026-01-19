@echo off
set "PROJECT_DIR=C:\Python Programming\CV Projects\AI-Vision-App"
cd /d "%PROJECT_DIR%"

echo --- Activating Local VENV312 ---
:: We call the specific python.exe inside your local venv
set "PYTHON_EXE=%PROJECT_DIR%\venv312\Scripts\python.exe"

if exist "%PYTHON_EXE%" (
    echo [SUCCESS] Found local environment. Launching Dashboard...
    "%PYTHON_EXE%" main_menu.py
) else (
    echo [ERROR] Could not find venv312 at %PYTHON_EXE%
    echo Please check the path and try again.
    pause
)