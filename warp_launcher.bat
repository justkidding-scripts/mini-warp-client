@echo off
REM WARP Terminal Universal Windows Launcher
REM Automatically detects Python and launches appropriate interface

setlocal enabledelayedexpansion

echo.
echo 🚀 WARP Terminal Universal Launcher (Windows)
echo ================================================

REM Check for Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8 or newer.
    echo 📥 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 🐍 Python %PYTHON_VERSION% detected

REM Check if GUI is available (always true on Windows)
echo 🖼️  GUI environment: Available

REM Parse command line arguments
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=gui

echo 🎯 Launching WARP Terminal in %COMMAND% mode...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Execute appropriate command
if "%COMMAND%"=="gui" (
    echo 🚀 Starting GUI interface...
    python warp_launcher.py gui
) else if "%COMMAND%"=="cli" (
    echo 💻 Starting CLI interface...
    python warp_launcher.py cli
) else if "%COMMAND%"=="setup" (
    echo 🔧 Running complete setup...
    python warp_launcher.py setup
) else if "%COMMAND%"=="status" (
    echo 📊 Showing system status...
    python warp_launcher.py status
) else if "%COMMAND%"=="config" (
    echo ⚙️ Opening configuration...
    python warp_launcher.py config
) else if "%COMMAND%"=="backup" (
    echo 💾 Creating backup...
    python warp_launcher.py backup
) else if "%COMMAND%"=="install" (
    echo 📦 Installing dependencies...
    python warp_launcher.py install
) else (
    echo ❌ Unknown command: %COMMAND%
    echo.
    echo Available commands:
    echo   gui     - Launch GUI interface ^(default^)
    echo   cli     - Launch CLI interface
    echo   setup   - Complete system setup
    echo   status  - Show system status
    echo   config  - Configure launcher
    echo   backup  - Create backup
    echo   install - Install dependencies
    echo.
    echo Usage: %~nx0 [command]
    echo Example: %~nx0 gui
)

echo.
if errorlevel 1 (
    echo ❌ Command failed with error level %errorlevel%
) else (
    echo ✅ Command completed successfully
)

pause
