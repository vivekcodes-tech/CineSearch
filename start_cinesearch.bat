
@echo off
title CineSearch Launcher

echo =====================================
echo        STARTING CINESEARCH
echo =====================================

cd /d "%~dp0"

echo.
echo [1/3] Starting Flask Backend...

start "CineSearch Backend" /D "%~dp0" cmd /k python backend\app.py

echo Waiting for backend...
timeout /t 3 /nobreak >nul

echo.
echo [2/3] Starting Frontend Server...

start "CineSearch Frontend" /D "%~dp0frontend" cmd /k python -m http.server 5500

echo Waiting for frontend...
timeout /t 2 /nobreak >nul

echo.
echo [3/3] Opening CineSearch...

start "" http://127.0.0.1:5500/frontend/

echo.
echo =====================================
echo CineSearch startup initiated!
echo =====================================
echo.
echo Keep both server windows open.
echo Close both windows when finished.

pause
