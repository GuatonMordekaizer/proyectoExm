# Scripts del Sistema Hospital Herminda Martín

Esta carpeta contiene scripts útiles para administración y pruebas del sistema.

## 📁 Estructura

```
scripts/
├── migraciones/           # Scripts relacionados con migraciones de base de datos
├── utilidades/           # Scripts de utilidades administrativas
├── ejecutar_pruebas_selenium.bat   # Ejecutar pruebas automatizadas (Windows)
└── ejecutar_pruebas_selenium.sh    # Ejecutar pruebas automatizadas (Linux/Mac)
```

## 🔧 Migraciones (`migraciones/`)

### `aplicar_migraciones.bat` / `aplicar_migraciones.sh`
Aplica todas las migraciones pendientes a la base de datos.

**Uso:**
```bash
# Windows
scripts\migraciones\aplicar_migraciones.bat

# Linux/Mac
./scripts/migraciones/aplicar_migraciones.sh
```

### `aplicar_migraciones_verificar.py`
Verifica y aplica migraciones con confirmación.

**Uso:**
```bash
python scripts/migraciones/aplicar_migraciones_verificar.py
```

## 🛠️ Utilidades (`utilidades/`)

### `create_superuser.py`
Crea un superusuario de forma automatizada.

**Uso:**
```bash
python scripts/utilidades/create_superuser.py
```

### `listar_usuarios.py`
Lista todos los usuarios del sistema con sus roles.

**Uso:**
```bash
python scripts/utilidades/listar_usuarios.py
```

### `reset_passwords.py`
Restablece contraseñas de usuarios a valores temporales.

**Uso:**
```bash
python scripts/utilidades/reset_passwords.py
```

### `check_auditoria.py`
Revisa los registros de auditoría del sistema.

**Uso:**
```bash
python scripts/utilidades/check_auditoria.py
```

### `calcular_rut_k.py`
Calcula y valida dígitos verificadores de RUT chileno.

**Uso:**
```bash
python scripts/utilidades/calcular_rut_k.py
```

## 🧪 Pruebas Automatizadas

### `ejecutar_pruebas_selenium.bat` / `ejecutar_pruebas_selenium.sh`
Ejecuta la suite completa de pruebas automatizadas con Selenium.

**Uso:**
```bash
# Windows
scripts\ejecutar_pruebas_selenium.bat

# Linux/Mac
./scripts/ejecutar_pruebas_selenium.sh
```

**Requisitos:**
- Selenium instalado: `pip install selenium webdriver-manager`
- Servidor Django corriendo en `http://127.0.0.1:8000`
- Google Chrome instalado

**Pruebas incluidas:**
1. Creación de usuario
2. Creación de paciente
3. Registro de parto

Ver `tests/README_SELENIUM.md` para más detalles.

## 📝 Notas

- Todos los scripts Python deben ejecutarse desde la raíz del proyecto
- Asegúrate de activar el entorno virtual antes de ejecutar los scripts
- Los scripts .bat son para Windows, los .sh para Linux/Mac
