@echo off

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version > nul 2>&1
if errorlevel 1 (
    echo Pip is not installed. Please install pip and try again.
    pause
    exit /b 1
)

REM Check if virtual environment exists, if not create it
if not exist venv (
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies from requirements.txt
pip install -r requirements.txt

REM Deactivate the virtual environment
deactivate

echo Dependencies installed successfully.
pause
exit /b 0
