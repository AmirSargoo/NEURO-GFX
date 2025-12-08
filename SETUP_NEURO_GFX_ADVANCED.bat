@echo off
REM ========================================================
REM 🎮 NEURO-GFX ADVANCED CAPTURE - DEPENDENCY INSTALLER
REM ========================================================
REM Instala todas las dependencias necesarias para el
REM sistema de captura avanzado con soporte GPU.
REM ========================================================

echo.
echo ========================================================
echo  🎮 NEURO-GFX ADVANCED CAPTURE - SETUP
echo ========================================================
echo.

echo [1/4] Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ ERROR: Python no encontrado
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

echo.
echo [2/4] Instalando dependencias base...
pip install --upgrade pip
pip install PySide6
pip install mss
pip install numpy

echo.
echo [3/4] Instalando D3DShot (GPU Capture)...
echo ⚠️  Si falla, el sistema usará MSS (CPU) como fallback
pip install d3dshot
if errorlevel 1 (
    echo ⚠️  D3DShot no disponible - usando MSS fallback
) else (
    echo ✅ D3DShot instalado correctamente
)

echo.
echo [4/4] Verificando instalación...
python -c "import PySide6; print('✅ PySide6 OK')"
python -c "import mss; print('✅ MSS OK')"
python -c "import numpy; print('✅ NumPy OK')"
python -c "try: import d3dshot; print('✅ D3DShot OK (GPU Capture Enabled)'); except: print('⚠️  D3DShot not available (CPU only)')"

echo.
echo ========================================================
echo  ✅ INSTALACIÓN COMPLETADA
echo ========================================================
echo.
echo Puedes ejecutar el launcher con:
echo   python NEURO_GFX_LAUNCHER_V2.py
echo.
echo Controles:
echo   F1  - Toggle metrics overlay
echo   F2  - Reload launcher
echo   ESC - Exit
echo.
pause
