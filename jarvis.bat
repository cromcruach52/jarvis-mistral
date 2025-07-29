@echo off
title Jarvis AI Assistant
echo.
echo  ╔══════════════════════════════════════╗
echo  ║        🤖 JARVIS AI ASSISTANT 🤖     ║
echo  ║              Starting...             ║
echo  ╚══════════════════════════════════════╝
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found!
    echo Make sure you're running this from the Jarvis directory.
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
if exist "requirements.txt" (
    echo 📦 Checking dependencies...
    pip show speechrecognition >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ⚠️  Missing required packages detected!
        echo.
        echo Jarvis needs to install some Python packages to work properly:
        echo   • speechrecognition (for voice input)
        echo   • pyttsx3 (for voice output)  
        echo   • requests (for AI communication)
        echo   • pyautogui (for screen control)
        echo   • and other dependencies...
        echo.
        set /p install_choice="📥 Install required packages now? (y/n): "
        
        if /i "%install_choice%"=="y" (
            echo.
            echo 📥 Installing packages... This may take a few minutes.
            pip install -r requirements.txt
            if errorlevel 1 (
                echo.
                echo ❌ Failed to install dependencies!
                echo.
                echo Manual installation:
                echo   pip install -r requirements.txt
                echo.
                echo Or install individually:
                echo   pip install speechrecognition pyttsx3 requests pyautogui
                echo.
                pause
                exit /b 1
            ) else (
                echo.
                echo ✅ All packages installed successfully!
                echo.
            )
        ) else if /i "%install_choice%"=="n" (
            echo.
            echo ⚠️  Jarvis may not work properly without required packages.
            echo.
            echo To install later, run: pip install -r requirements.txt
            echo.
            set /p continue_choice="Continue anyway? (y/n): "
            if /i not "%continue_choice%"=="y" (
                echo.
                echo 👋 Setup cancelled. Run jarvis.bat again when ready!
                pause
                exit /b 0
            )
        ) else (
            echo.
            echo ❌ Invalid choice. Please run jarvis.bat again and enter 'y' or 'n'
            pause
            exit /b 1
        )
    ) else (
        echo ✅ All dependencies are installed!
    )
)

REM Launch Jarvis
echo.
echo 🚀 Starting Jarvis AI Assistant...
echo.
echo ═══════════════════════════════════════════════════════════
echo  💡 Quick Commands:
echo     • "open word" / "open chrome" / "open vscode"
echo     • "what's on my screen" / "take screenshot"  
echo     • "text mode" / "fast mode" / "memory mode"
echo     • "exit" to quit / "stop" to interrupt speech
echo ═══════════════════════════════════════════════════════════
echo.

python main.py

REM Handle errors
if errorlevel 1 (
    echo.
    echo ❌ Jarvis encountered an error!
    echo.
    echo Common solutions:
    echo • Make sure Ollama is running: ollama serve
    echo • Check your microphone permissions
    echo • Try running in text mode first
    echo.
    pause
)

echo.
echo 👋 Jarvis has stopped. Goodbye!
pause
