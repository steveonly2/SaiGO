python --version 2>NUL
if errorlevel 1 goto errorNoPython

cls

set list=customtkinter pyautogui tkinter os sys time thisdoesnotnotexists threading keyboard PIL

cls

(for %%a in (%list%) do (
   pip install %%a
   echo/
)) > log.txt

cls

@echo off
set /p "confirmation=Press Enter to Continue... "

goto 2>nul & del "%~f0"

:errorNoPython
echo.
echo Error^: Python not installed
@echo off
set /p "confirmation=Press Enter to Continue... "