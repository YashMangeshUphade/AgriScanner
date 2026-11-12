@echo off
title AgriScanner Launcher
setlocal

:: Get the directory of the script
set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

echo ==========================================
echo       🌿 AgriScanner Launcher 🌿
echo ==========================================
echo.

:: Check if Streamlit is installed
where streamlit >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Streamlit not found in PATH.
    echo [!] Attempting to run via "python -m streamlit"...
    python -m streamlit run app.py
) else (
    echo [OK] Launching Streamlit app...
    streamlit run app.py
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start AgriScanner.
    echo Please ensure you have run "pip install -r requirements.txt"
    pause
)

endlocal
