# Organización del Proyecto - Hospital Herminda Martín

## ✅ Cambios Realizados

Se ha reorganizado completamente la estructura de archivos del proyecto para mejorar la mantenibilidad y claridad.

## 📋 Estructura Actualizada

### Antes:
```
hospital_hhm/
├── aplicar_migraciones.bat
├── aplicar_migraciones.sh
├── aplicar_migraciones_verificar.py
├── calcular_rut_k.py
├── check_auditoria.py
├── create_superuser.py
├── listar_usuarios.py
├── reset_passwords.py
├── ejecutar_pruebas_selenium.bat
├── ejecutar_pruebas_selenium.sh
├── ACTUALIZACION_MODELOS.md
├── INSTRUCCIONES_MIGRACION.md
├── MODELOS_COMPLETOS.py
├── ... (muchos archivos en raíz)
```

### Después:
```
hospital_hhm/
├── .env                    # Configuración de entorno
├── db.sqlite3             # Base de datos
├── manage.py              # Gestor Django
├── README.md              # Documentación principal
├── requirements.txt       # Dependencias
│
├── apps/                  # Aplicaciones Django
├── hospital_hhm/         # Configuración del proyecto
├── logs/                 # Logs del sistema
├── static/               # Archivos estáticos
├── templates/            # Plantillas HTML
├── tests/                # Pruebas automatizadas
├── venv/                 # Entorno virtual
│
├── docs/                 # 📚 DOCUMENTACIÓN
│   ├── ACTUALIZACION_MODELOS.md
│   ├── INSTRUCCIONES_MIGRACION.md
│   └── MODELOS_COMPLETOS.py
│
└── scripts/              # 🔧 SCRIPTS Y UTILIDADES
    ├── README.md         # Documentación de scripts
    │
    ├── migraciones/      # Scripts de base de datos
    │   ├── aplicar_migraciones.bat
    │   ├── aplicar_migraciones.sh
    │   └── aplicar_migraciones_verificar.py
    │
    ├── utilidades/       # Herramientas administrativas
    │   ├── calcular_rut_k.py
    │   ├── check_auditoria.py
    │   ├── create_superuser.py
    │   ├── listar_usuarios.py
    │   └── reset_passwords.py
    │
    ├── ejecutar_pruebas_selenium.bat
    └── ejecutar_pruebas_selenium.sh
```

## 🗂️ Categorías de Archivos

### 1. **Raíz del Proyecto** (Solo archivos esenciales)
- ✅ `manage.py` - Gestor de Django
- ✅ `README.md` - Documentación principal
- ✅ `requirements.txt` - Dependencias Python
- ✅ `.env` - Configuración de entorno
- ✅ `db.sqlite3` - Base de datos

### 2. **`docs/`** - Documentación Técnica
- `ACTUALIZACION_MODELOS.md` - Guía de actualización de modelos
- `INSTRUCCIONES_MIGRACION.md` - Instrucciones de migración
- `MODELOS_COMPLETOS.py` - Referencia completa de modelos

### 3. **`scripts/`** - Scripts y Utilidades

#### 3.1. `scripts/migraciones/` - Gestión de Base de Datos
- `aplicar_migraciones.bat` - Aplicar migraciones (Windows)
- `aplicar_migraciones.sh` - Aplicar migraciones (Linux/Mac)
- `aplicar_migraciones_verificar.py` - Aplicar con verificación

#### 3.2. `scripts/utilidades/` - Herramientas Administrativas
- `create_superuser.py` - Crear superusuario
- `listar_usuarios.py` - Listar usuarios del sistema
- `reset_passwords.py` - Restablecer contraseñas
- `check_auditoria.py` - Revisar logs de auditoría
- `calcular_rut_k.py` - Validar RUT chileno

#### 3.3. `scripts/` - Pruebas Automatizadas
- `ejecutar_pruebas_selenium.bat` - Ejecutar pruebas (Windows)
- `ejecutar_pruebas_selenium.sh` - Ejecutar pruebas (Linux/Mac)

## 🚀 Cómo Usar los Scripts

### Desde cualquier ubicación:

Los scripts ahora detectan automáticamente la raíz del proyecto, por lo que puedes ejecutarlos desde cualquier lugar.

#### Windows:
```bash
# Migraciones
scripts\migraciones\aplicar_migraciones.bat

# Utilidades
scripts\utilidades\create_superuser.py
scripts\utilidades\listar_usuarios.py

# Pruebas
scripts\ejecutar_pruebas_selenium.bat
```

#### Linux/Mac:
```bash
# Migraciones
./scripts/migraciones/aplicar_migraciones.sh

# Utilidades
python scripts/utilidades/create_superuser.py
python scripts/utilidades/listar_usuarios.py

# Pruebas
./scripts/ejecutar_pruebas_selenium.sh
```

## 📝 Actualizaciones Realizadas

### Scripts Modificados:
1. ✅ `ejecutar_pruebas_selenium.bat` - Navega automáticamente a la raíz
2. ✅ `ejecutar_pruebas_selenium.sh` - Navega automáticamente a la raíz
3. ✅ `aplicar_migraciones.bat` - Navega automáticamente a la raíz
4. ✅ `aplicar_migraciones.sh` - Navega automáticamente a la raíz

### Documentación Creada:
1. ✅ `scripts/README.md` - Guía completa de scripts
2. ✅ `docs/` - Carpeta para documentación técnica
3. ✅ README principal actualizado con nueva estructura

## ✨ Beneficios

### Antes:
- ❌ 13+ archivos sueltos en la raíz
- ❌ Difícil encontrar scripts específicos
- ❌ Sin categorización clara
- ❌ Scripts debían ejecutarse desde raíz

### Ahora:
- ✅ Solo 5 archivos esenciales en raíz
- ✅ Scripts organizados por categoría
- ✅ Documentación centralizada en `docs/`
- ✅ Scripts se ejecutan desde cualquier ubicación
- ✅ README con estructura visual
- ✅ Fácil mantenimiento y escalabilidad

## 🔍 Búsqueda Rápida

**¿Necesitas crear un superusuario?**
→ `scripts/utilidades/create_superuser.py`

**¿Necesitas aplicar migraciones?**
→ `scripts/migraciones/aplicar_migraciones.bat` (Windows)
→ `scripts/migraciones/aplicar_migraciones.sh` (Linux/Mac)

**¿Necesitas ejecutar pruebas?**
→ `scripts/ejecutar_pruebas_selenium.bat` (Windows)
→ `scripts/ejecutar_pruebas_selenium.sh` (Linux/Mac)

**¿Necesitas ver documentación de modelos?**
→ `docs/MODELOS_COMPLETOS.py`

**¿Necesitas validar un RUT?**
→ `scripts/utilidades/calcular_rut_k.py`

## 📚 Más Información

- **Scripts**: Ver `scripts/README.md`
- **Pruebas Selenium**: Ver `tests/README_SELENIUM.md`
- **Documentación General**: Ver `README.md` en la raíz
