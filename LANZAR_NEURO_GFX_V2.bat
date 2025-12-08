@echo off
REM ========================================================
REM 🎮 NEURO-OS VGA™ ADVANCED LAUNCHER V2.0
REM ========================================================

title NEURO-OS VGA Advanced Launcher v2.0

echo.
echo ========================================================
echo  🎮 NEURO-OS VGA™ ADVANCED LAUNCHER v2.0
echo ========================================================
echo.
echo Starting advanced capture system...
echo.

python NEURO_GFX_LAUNCHER_V2.py

if errorlevel 1 (
    echo.
    echo ❌ ERROR: El launcher falló
    echo.
    echo Posibles causas:
    echo   - Dependencias no instaladas
    echo   - Error en el código
    echo.
    echo Ejecuta SETUP_NEURO_GFX_ADVANCED.bat para instalar dependencias
    echo.
    pause
)
