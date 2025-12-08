#!/bin/bash
# Script para aplicar las actualizaciones de modelos
# Sistema Obstétrico Hospital Herminda Martín

echo "=================================================="
echo "  Actualización de Modelos - Base de Datos"
echo "  Hospital Herminda Martín"
echo "=================================================="
echo ""

# 1. Ir al directorio raíz del proyecto
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/../.."

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: No se encuentra manage.py"
    echo "   Por favor ejecute este script desde la raíz del proyecto"
    exit 1
fi

# 2. Verificar entorno virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Advertencia: No hay entorno virtual activado"
    echo "   Activando entorno virtual..."
    
    if [ -d "venv" ]; then
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        echo "❌ Error: No se encuentra el entorno virtual"
        echo "   Cree uno con: python -m venv venv"
        exit 1
    fi
fi

echo "✅ Entorno virtual activo: $VIRTUAL_ENV"
echo ""

# 3. Verificar instalación de Django
python -c "import django" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: Django no está instalado"
    echo "   Instale dependencias con: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Django instalado correctamente"
echo ""

# 4. Verificar sintaxis de los modelos
echo "🔍 Verificando sintaxis de los modelos..."
python manage.py check
if [ $? -ne 0 ]; then
    echo "❌ Error: Hay errores de sintaxis en los modelos"
    exit 1
fi

echo "✅ Sintaxis correcta"
echo ""

# 5. Backup de base de datos (solo SQLite)
if [ -f "db.sqlite3" ]; then
    echo "💾 Creando backup de la base de datos..."
    BACKUP_FILE="db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
    cp db.sqlite3 "$BACKUP_FILE"
    echo "✅ Backup creado: $BACKUP_FILE"
    echo ""
fi

# 6. Generar migraciones
echo "🔨 Generando migraciones..."
python manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "❌ Error: No se pudieron generar las migraciones"
    exit 1
fi

echo "✅ Migraciones generadas"
echo ""

# 7. Mostrar plan de migración
echo "📋 Plan de migración:"
python manage.py showmigrations
echo ""

# 8. Aplicar migraciones
echo "⚙️  Aplicando migraciones..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Error: No se pudieron aplicar las migraciones"
    echo "   Revise los errores anteriores"
    exit 1
fi

echo "✅ Migraciones aplicadas correctamente"
echo ""

# 9. Verificar modelos en shell
echo "🔍 Verificando modelos actualizados..."
python manage.py shell << EOF
from apps.obstetricia.models import Parto, ComplicacionMaterna, ProtocoloVIH
from apps.neonatologia.models import RecienNacido, APGARDetalle, ComplicacionNeonatal

print("\n✅ Modelo Parto - Campos totales:", len([f for f in Parto._meta.get_fields()]))
print("✅ Modelo RecienNacido - Campos totales:", len([f for f in RecienNacido._meta.get_fields()]))
print("✅ Modelo APGARDetalle - Creado correctamente")
print("✅ Modelo ComplicacionMaterna - Creado correctamente")
print("✅ Modelo ProtocoloVIH - Creado correctamente")
print("✅ Modelo ComplicacionNeonatal - Creado correctamente\n")
EOF

if [ $? -ne 0 ]; then
    echo "⚠️  Advertencia: No se pudo verificar los modelos en shell"
fi

# 10. Resumen final
echo ""
echo "=================================================="
echo "  ✅ ACTUALIZACIÓN COMPLETADA CON ÉXITO"
echo "=================================================="
echo ""
echo "📊 Resumen de cambios:"
echo "   • Modelo Parto: +40 campos (ahora ~80 campos)"
echo "   • Modelo RecienNacido: +20 campos (ahora ~35 campos)"
echo "   • Nuevo modelo: APGARDetalle (5 componentes)"
echo "   • Nuevo modelo: ComplicacionMaterna (CIE-10)"
echo "   • Nuevo modelo: ProtocoloVIH (automático)"
echo "   • Nuevo modelo: ComplicacionNeonatal (CIE-10)"
echo ""
echo "📚 Documentación: Vea ACTUALIZACION_MODELOS.md"
echo ""
echo "🚀 Próximos pasos:"
echo "   1. Actualizar formularios en apps/*/forms.py"
echo "   2. Actualizar vistas en apps/*/views.py"
echo "   3. Actualizar templates en templates/*/*.html"
echo "   4. Configurar PostgreSQL para producción"
echo ""
echo "🎯 Para iniciar el servidor:"
echo "   python manage.py runserver"
echo ""
