@echo off
REM Script para ejecutar pruebas automatizadas con Selenium
REM Hospital Herminda Martín

echo ============================================================
echo  PRUEBAS AUTOMATIZADAS - SELENIUM
echo  Hospital Herminda Martin
echo ============================================================
echo.

REM Obtener el directorio del script
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%.."

REM Verificar que estamos en el directorio correcto
if not exist "manage.py" (
    echo ERROR: No se encuentra manage.py
    pause
    exit /b 1
)

REM Activar entorno virtual
echo [1/4] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    echo Asegurate que existe la carpeta venv
    pause
    exit /b 1
)

REM Instalar dependencias si es necesario
echo.
echo [2/4] Verificando dependencias...
pip show selenium >nul 2>&1
if errorlevel 1 (
    echo Instalando Selenium y WebDriver Manager...
    pip install selenium webdriver-manager
)

REM Verificar que el servidor está corriendo
echo.
echo [3/4] Verificando servidor...
powershell -Command "(Invoke-WebRequest -Uri 'http://127.0.0.1:8000' -UseBasicParsing -TimeoutSec 2).StatusCode" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║  ADVERTENCIA: El servidor no esta corriendo               ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo Por favor, ejecuta en otra terminal:
    echo    python manage.py runserver
    echo.
    echo Presiona Enter cuando el servidor este listo...
    pause >nul
)

REM Ir al directorio raíz del proyecto
cd ..

REM Ejecutar pruebas
echo.
echo [4/4] Ejecutando pruebas...
echo.
python tests\test_selenium_forms.py

echo.
echo ============================================================
echo  Ejecucion completada
echo ============================================================
pause
