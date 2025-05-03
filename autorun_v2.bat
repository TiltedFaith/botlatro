@echo off
setlocal

:: ===== CONFIG =====
:: change BOT_DIR to the file path of your bot folder
set "BOT_DIR=G:\Miko's folder\botlatro\botlatro" 
set "BOT_SCRIPT=main.py"
set "RETRY_DELAY=60"
set "NETWORK_RETRY_DELAY=30"
:: ========================

:check_connection
ping www.google.com -n 1 >nul 2>nul
if %errorlevel% neq 0 (
    echo No internet connection. Retrying in %NETWORK_RETRY_DELAY% seconds...
    timeout /t %NETWORK_RETRY_DELAY%
    goto check_connection
)

:loop
cd /D "%BOT_DIR%"
python "%BOT_SCRIPT%"

if %errorlevel% neq 0 (
    echo Script failed. Restarting in %RETRY_DELAY% seconds...
    timeout /t %RETRY_DELAY%
    goto loop
) else (
    echo Script completed successfully.
)

pause
endlocal