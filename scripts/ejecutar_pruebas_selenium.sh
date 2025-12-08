#!/bin/bash
# Script para ejecutar pruebas automatizadas con Selenium
# Hospital Herminda Martín

echo "============================================================"
echo " PRUEBAS AUTOMATIZADAS - SELENIUM"
echo " Hospital Herminda Martin"
echo "============================================================"
echo ""

# Obtener el directorio del script y ir a la raíz
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "ERROR: No se encuentra manage.py"
    exit 1
fi

# Activar entorno virtual
echo "[1/4] Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo activar el entorno virtual"
    echo "Asegurate que existe la carpeta venv"
    exit 1
fi

# Instalar dependencias si es necesario
echo ""
echo "[2/4] Verificando dependencias..."
if ! pip show selenium &> /dev/null; then
    echo "Instalando Selenium y WebDriver Manager..."
    pip install selenium webdriver-manager
fi

# Verificar que el servidor está corriendo
echo ""
echo "[3/4] Verificando servidor..."
if ! curl -s http://127.0.0.1:8000 &> /dev/null; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  ADVERTENCIA: El servidor no esta corriendo               ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Por favor, ejecuta en otra terminal:"
    echo "   python manage.py runserver"
    echo ""
    read -p "Presiona Enter cuando el servidor este listo..."
fi

# Ejecutar pruebas (ya estamos en la raíz)
echo ""
echo "[4/4] Ejecutando pruebas..."
echo ""
python tests/test_selenium_forms.py

echo ""
echo "============================================================"
echo " Ejecucion completada"
echo "============================================================"
