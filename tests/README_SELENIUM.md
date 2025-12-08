# Pruebas Automatizadas con Selenium

Este directorio contiene scripts de Selenium para automatizar las pruebas de los formularios del sistema.

## 📋 Requisitos

### 1. Instalar Selenium
```bash
pip install selenium
```

### 2. Instalar ChromeDriver

**Opción A - Automática (Recomendado):**
```bash
pip install webdriver-manager
```

**Opción B - Manual:**
1. Descargar ChromeDriver desde: https://chromedriver.chromium.org/downloads
2. Descargar la versión que coincida con tu Chrome
3. Agregar chromedriver.exe al PATH del sistema

### 3. Verificar instalación de Chrome
- Asegúrate de tener Google Chrome instalado
- Si prefieres Firefox, cambia `webdriver.Chrome()` por `webdriver.Firefox()` y descarga geckodriver

## 🚀 Uso

### Ejecutar todas las pruebas:

```bash
# Activar entorno virtual
.\venv\Scripts\activate

# Asegurarse que el servidor está corriendo
python manage.py runserver

# En otra terminal, ejecutar las pruebas
python tests\test_selenium_forms.py
```

### Configuración personalizada:

Edita las variables en `test_selenium_forms.py`:

```python
BASE_URL = "http://127.0.0.1:8000"  # URL del servidor
USERNAME = "admin"                   # Usuario para login
PASSWORD = "admin"                   # Contraseña
```

## 🧪 Scripts de Prueba Disponibles

### 📋 `test_selenium_forms.py` - Jefe de Servicio
**Rol:** Jefe de Servicio / Administrador
**Funcionalidades:**
- ✅ Login como administrador
- ✅ Crear usuarios (según permisos RBAC)
- ✅ Auditoría y gestión del sistema

**Uso:**
```bash
python tests\test_selenium_forms.py
```

---

### 🤰 `test_selenium_matrona.py` - Matrona
**Rol:** Matrona/Matrón
**Funcionalidades según `roles_permisos.md`:**
- ✅ Buscar pacientes
- ✅ Registrar parto completo (99 campos)
- ✅ Registrar datos del recién nacido
- ✅ Editar registros propios (24 horas)
- ✅ Consultar historial obstétrico
- ✅ Ver clasificación Robson automática

**Uso:**
```bash
python tests\test_selenium_matrona.py
```

**Pruebas incluidas:**
1. **Buscar Paciente** - Búsqueda por RUT o listado
2. **Registrar Parto** - Wizard de 4 pasos con 99 campos
3. **Registrar RN** - Datos del recién nacido vinculados al parto

---

### 👨‍⚕️ `test_selenium_medico.py` - Médico Obstetra
**Rol:** Médico Gineco-Obstetra
**Funcionalidades según `roles_permisos.md`:**
- ✅ Buscar pacientes
- ✅ Registrar cesáreas y partos complejos
- ✅ Agregar complicaciones con códigos CIE-10
- ✅ Modificar clasificación Robson en casos atípicos
- ✅ Consultar estadísticas clínicas (tasa cesáreas por Robson)
- ✅ Emitir certificados y gestionar egresos

**Uso:**
```bash
python tests\test_selenium_medico.py
```

**Pruebas incluidas:**
1. **Buscar Paciente** - Búsqueda por RUT o listado
2. **Registrar Cesárea** - Parto tipo CESAREA con complicaciones
3. **Ver Estadísticas** - Dashboard con KPIs y reportes
4. **Modificar Clasificación Robson** - Ajuste en casos atípicos

## 📊 Datos de prueba

### Usuario de prueba:
- Username: `usuario_test_YYYYMMDDHHMMSS`
- RUT: `12345678-9`
- Email: `test_YYYYMMDDHHMMSS@hospital.cl`
- Rol: `enfermera`
- Password: `TestPass123!`

### Paciente de prueba:
- Nombre: `María Isabel González Pérez`
- RUT: `1234567X-Y` (generado con timestamp)
- Fecha nacimiento: `1990-05-15`
- Sexo: `Femenino`
- Previsión: `FONASA`
- Grupo sanguíneo: `O+`

### Parto de prueba:
- Tipo: `Vaginal`
- Presentación: `Cefálica`
- Inicio: `Espontáneo`
- Lugar: `Hospital`
- Alumbramiento: `Espontáneo`
- Líquido amniótico: `Claro`
- Anestesia: `Epidural`
- Edad gestacional: `39 semanas, 3 días`

## 🎯 Características

### ✨ Funcionalidades:
- ✅ Login automático al sistema
- ✅ Relleno completo de formularios
- ✅ Navegación entre pasos del wizard
- ✅ Selección de campos select/dropdown
- ✅ Generación de datos únicos con timestamps
- ✅ Capturas de pantalla en caso de error
- ✅ Esperas inteligentes (WebDriverWait)
- ✅ Logs detallados en consola
- ✅ Navegador maximizado para mejor visualización

### 📸 Capturas de error:
Si ocurre un error, se guardan capturas en:
- `error_crear_usuario.png`
- `error_crear_paciente.png`
- `error_registrar_parto.png`

## 🔧 Personalización

### Ejecutar pruebas individuales:

```python
from tests.test_selenium_forms import HospitalFormTester

tester = HospitalFormTester()
tester.login("admin", "admin")

# Solo crear usuario
tester.test_crear_usuario()

# Solo crear paciente
tester.test_crear_paciente()

# Solo registrar parto (requiere ID de paciente)
tester.test_registrar_parto(paciente_id=1)

tester.driver.quit()
```

### Cambiar navegador a Firefox:

```python
# En la línea 27 de test_selenium_forms.py
self.driver = webdriver.Firefox()  # En vez de Chrome()
```

### Ajustar tiempos de espera:

```python
# En la línea 29 de test_selenium_forms.py
self.wait = WebDriverWait(self.driver, 20)  # Aumentar de 10 a 20 segundos
```

## ⚠️ Solución de problemas

### Error: "selenium module not found"
```bash
pip install selenium
```

### Error: "chromedriver not found"
```bash
pip install webdriver-manager
```
Y cambiar en el código:
```python
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### Error: "element not found"
- Aumentar tiempo de espera (line 29)
- Verificar que los nombres de campos coincidan con el HTML
- Verificar que el servidor está corriendo

### Error de login
- Verificar username/password en las variables de configuración
- Verificar que existe un superusuario en la BD

## 📝 Notas importantes

1. **Servidor debe estar corriendo**: El script asume que el servidor Django está en `http://127.0.0.1:8000`

2. **Base de datos**: Las pruebas crean datos reales en la BD. Ejecutar en ambiente de desarrollo.

3. **Navegador abierto**: El navegador permanece abierto al finalizar para que veas los resultados. Presiona Enter en la consola para cerrarlo.

4. **Tiempos de espera**: Los `time.sleep()` pueden ajustarse según la velocidad de tu sistema.

5. **Permisos**: Asegúrate que el usuario de login tiene permisos para crear usuarios, pacientes y registrar partos.

## 🚦 Estado de las pruebas

Al ejecutar, verás salida como:

```
============================================================
INICIANDO SESIÓN
============================================================
✓ Sesión iniciada como: admin

============================================================
PRUEBA 1: CREAR USUARIO
============================================================
Creando usuario: usuario_test_20231208143025
  ✓ username: usuario_test_20231208143025
  ✓ rut: 12345678-9
  ✓ email: test_20231208143025@hospital.cl
  ...
✓ Usuario creado exitosamente

============================================================
PRUEBA 2: CREAR PACIENTE
============================================================
...
```

## 📚 Recursos adicionales

- [Documentación Selenium Python](https://selenium-python.readthedocs.io/)
- [Localizadores de elementos](https://selenium-python.readthedocs.io/locating-elements.html)
- [WebDriverWait](https://selenium-python.readthedocs.io/waits.html)
