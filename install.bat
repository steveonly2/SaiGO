@echo off
setlocal

python --version 2>NUL
if errorlevel 1 goto errorNoPython

:: Define the list of modules
set modules=customtkinter os keyboard threading pyautogui sys pillow ahk math json

:: Loop through each module and check if it's installed
for %%m in (%modules%) do (
    python -c "import %%m" 2>NUL
    if errorlevel 1 (
        echo Installing %%m...
        pip install %%m
    ) else (
        echo %%m is already installed. Skipping...
    )
)

:: Show success message
echo Successfully installed all modules!

:: End script
set /p "confirmation=Press ENTER to Continue... "
goto 2>nul & del "%~f0"

:errorNoPython
cls
echo Error^: Python not installed
set /p "confirmation=Press ENTER to Continue... "