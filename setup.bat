@echo off

python --version 2>NUL
if errorlevel 1 (
    echo Python is not installed. Please install Python before running this script.
    exit /b 1
)

pip --version 2>NUL
if errorlevel 1 (
    echo pip is not installed. Please install pip before running this script.
    exit /b 1
)

rem Install Pygame
pip install pygame==2.0.1

echo Setup completed successfully.

