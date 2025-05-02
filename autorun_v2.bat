@echo off
:check_connection
ping www.google.com -n 1 >nul 2>nul
if %errorlevel% neq 0 (
    echo No internet connection. Retrying in 30 seconds...
    timeout /t 30
    goto check_connection
)

:loop
cd C:\gian_saucebot
python sauce_bot_2.0.py
if %errorlevel% neq 0 (
    echo Script failed. Restarting in 60 seconds...
    timeout /t 60
    goto loop
) else (
    echo Script completed successfully.
)
pause