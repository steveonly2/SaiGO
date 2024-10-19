@echo off
setlocal

:OSChoice
echo Choose your operating system:
echo 1. Windows
echo 2. Linux
echo 3. MacOS
set /p "os_choice=Enter your choice (1, 2, or 3): "

if "%os_choice%"=="1" goto Windows
if "%os_choice%"=="2" goto Linux
if "%os_choice%"=="3" goto MacOS
echo Invalid choice, exiting...
exit /b

:Windows
echo Downloading Python 3.13.0 for Windows...
start "" "https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe"
set "file_name=python-3.13.0-amd64.exe"
goto WaitInstall

:Linux
echo Downloading Python 3.13.0 for Linux...
start "" "https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe"
set "file_name=python-3.13.0-amd64.exe"
goto WaitInstall

:MacOS
echo Downloading Python 3.13.0 for MacOS...
start "" "https://www.python.org/ftp/python/3.13.0/python-3.13.0-macos11.pkg"
set "file_name=python-3.13.0-macos11.pkg"
goto WaitInstall

:WaitInstall
echo Waiting for download to complete...

:: Set the downloads path, adjust if necessary
set "downloads_path=%USERPROFILE%\Downloads"

:CheckFile
if exist "%downloads_path%\%file_name%" (
    echo Download complete! Opening installer...
    start "" "%downloads_path%\%file_name%"
) else (
    echo File not found yet. Waiting...
    timeout /t 5 /nobreak >nul
    goto CheckFile
)

:: Call PowerShell script to handle mouse clicks and install Python modules
powershell -ExecutionPolicy Bypass -File "mouse_click.ps1"

:: Wait for installation to finish and install modules
echo Waiting for installation to complete...
timeout /t 120 /nobreak >nul

echo Installing required Python modules...
python -m pip install customtkinter os keyboard threading pyautogui sys pillow ahk math json

echo All modules installed successfully!
pause
exit /b
