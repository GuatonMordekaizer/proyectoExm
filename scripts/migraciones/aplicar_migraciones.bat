@echo off
REM Script para aplicar las actualizaciones de modelos (Windows)
REM Sistema Obstétrico Hospital Herminda Martín

echo ==================================================
echo   Actualización de Modelos - Base de Datos
echo   Hospital Herminda Martín
echo ==================================================
echo.

REM 1. Ir al directorio raíz del proyecto
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%..\.."

REM Verificar que estamos en el directorio correcto
if not exist manage.py (
    echo ❌ Error: No se encuentra manage.py
    echo    Por favor ejecute este script desde la raíz del proyecto
    pause
    exit /b 1
)

REM 2. Verificar/Activar entorno virtual
if not defined VIRTUAL_ENV (
    echo ⚠️  Advertencia: No hay entorno virtual activado
    echo    Activando entorno virtual...
    
    if exist venv\Scripts\activate.bat (
        call venv\Scripts\activate.bat
    ) else if exist .venv\Scripts\activate.bat (
        call .venv\Scripts\activate.bat
    ) else (
        echo ❌ Error: No se encuentra el entorno virtual
        echo    Cree uno con: python -m venv venv
        pause
        exit /b 1
    )
)

echo ✅ Entorno virtual activo
echo.

REM 3. Verificar instalación de Django
python -c "import django" 2>nul
if errorlevel 1 (
    echo ❌ Error: Django no está instalado
    echo    Instale dependencias con: pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ Django instalado correctamente
echo.

REM 4. Verificar sintaxis de los modelos
echo 🔍 Verificando sintaxis de los modelos...
python manage.py check
if errorlevel 1 (
    echo ❌ Error: Hay errores de sintaxis en los modelos
    pause
    exit /b 1
)

echo ✅ Sintaxis correcta
echo.

REM 5. Backup de base de datos (solo SQLite)
if exist db.sqlite3 (
    echo 💾 Creando backup de la base de datos...
    set BACKUP_FILE=db.sqlite3.backup.%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    set BACKUP_FILE=%BACKUP_FILE: =0%
    copy db.sqlite3 "%BACKUP_FILE%" >nul
    echo ✅ Backup creado: %BACKUP_FILE%
    echo.
)

REM 6. Generar migraciones
echo 🔨 Generando migraciones...
python manage.py makemigrations
if errorlevel 1 (
    echo ❌ Error: No se pudieron generar las migraciones
    pause
    exit /b 1
)

echo ✅ Migraciones generadas
echo.

REM 7. Mostrar plan de migración
echo 📋 Plan de migración:
python manage.py showmigrations
echo.

REM 8. Aplicar migraciones
echo ⚙️  Aplicando migraciones...
python manage.py migrate
if errorlevel 1 (
    echo ❌ Error: No se pudieron aplicar las migraciones
    echo    Revise los errores anteriores
    pause
    exit /b 1
)

echo ✅ Migraciones aplicadas correctamente
echo.

REM 9. Verificar modelos en shell
echo 🔍 Verificando modelos actualizados...
python manage.py shell < aplicar_migraciones_verificar.py
if errorlevel 1 (
    echo ⚠️  Advertencia: No se pudo verificar los modelos en shell
)

REM 10. Resumen final
echo.
echo ==================================================
echo   ✅ ACTUALIZACIÓN COMPLETADA CON ÉXITO
echo ==================================================
echo.
echo 📊 Resumen de cambios:
echo    • Modelo Parto: +40 campos (ahora ~80 campos)
echo    • Modelo RecienNacido: +20 campos (ahora ~35 campos)
echo    • Nuevo modelo: APGARDetalle (5 componentes)
echo    • Nuevo modelo: ComplicacionMaterna (CIE-10)
echo    • Nuevo modelo: ProtocoloVIH (automático)
echo    • Nuevo modelo: ComplicacionNeonatal (CIE-10)
echo.
echo 📚 Documentación: Vea ACTUALIZACION_MODELOS.md
echo.
echo 🚀 Próximos pasos:
echo    1. Actualizar formularios en apps\*\forms.py
echo    2. Actualizar vistas en apps\*\views.py
echo    3. Actualizar templates en templates\*\*.html
echo    4. Configurar PostgreSQL para producción
echo.
echo 🎯 Para iniciar el servidor:
echo    python manage.py runserver
echo.
pause
