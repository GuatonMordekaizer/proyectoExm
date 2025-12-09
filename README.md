# Sistema de Gestión Obstétrica - Hospital Clínico Herminda Martín

![Status](https://img.shields.io/badge/Status-MVP%20Completo-success)
![Django](https://img.shields.io/badge/Django-4.2%20LTS-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-Proprietary-red)

Sistema de información web para la gestión digital de partos y neonatología, diseñado para reemplazar el registro manual en Excel y cumplir con la normativa chilena vigente.

## 📋 Documentación del Proyecto

### Informe Técnico Completo
La documentación completa del proyecto se encuentra en:
```
docs/informe/
├── 01-PORTADA.md                    # Portada académica del proyecto
├── 02-CONTENIDO.md                  # Índice y contenido del informe
├── 03-INTRODUCCION.md               # Introducción y contexto del proyecto
├── 04-PLANTEAMIENTO.md              # Planteamiento del problema y objetivos
├── 05-ANALISIS.md                   # Análisis del problema y requerimientos
├── 06-ENFOQUE_METODOLOGICO.md       # Metodología SCRUM aplicada
├── 07-ENFOQUE_TECNICO_1.md          # Arquitectura y tecnologías (con interfaces)
├── 07-ENFOQUE_TECNICO_2.md          # Tecnologias, diagramas UML del sistema
├── 07-ENFOQUE_TECNICO_3.md          # Implementación y desarrollo
├── 07-ENFOQUE_TECNICO_4.md          # Despliegue y infraestructura
├── 08-CRONOGRAMA.md                 # Cronograma y planificación
├── 09-RESULTADOS.md                 # Resultados obtenidos y métricas
└── 10-REFERENCIAS.md                # Referencias bibliográficas
```

## Funcionalidades Principales

### 1. Gestión de Pacientes
- Búsqueda rápida por RUT o nombre.
- Ficha clínica digital con antecedentes obstétricos.
- Validación automática de RUT chileno.

### 2. Registro de Parto (Obstetricia)
- **Formulario completo con 80+ campos clínicos** (actualizado a documentación).
- **Clasificación Robson Automática**: Algoritmo OMS implementado para clasificar partos en 10 grupos.
- Registro completo de complicaciones con códigos **CIE-10**.
- **Protocolo VIH Automático**: Se activa automáticamente al detectar VIH+.
- Registro de acompañamiento, tiempos de trabajo de parto, profesionales.
- Casos especiales: plan de parto, parto en agua, parto vertical, SAIP.

### 3. Atención Neonatal
- Registro de Recién Nacido vinculado al parto (35+ campos).
- **Evaluación APGAR Detallada**: 
  - Desglose de 5 componentes (frecuencia cardíaca, respiración, tono, reflejos, color).
  - Cálculo automático del total.
  - Alertas automáticas para APGAR < 7 a los 5 minutos.
- **Procedimientos inmediatos**: Pinzamiento cordón, apego piel a piel, lactancia.
- **Medicamentos**: Vitamina K, vacuna Hepatitis B, profilaxis ocular.
- Clasificación automática de peso (Bajo peso, Normal, Macrosómico).
- Registro de complicaciones neonatales con **CIE-10**.
- Seguimiento completo: signos vitales, alimentación, eliminaciones.

### 4. Seguridad y Auditoría (RBAC)
- **7 Roles Diferenciados**: Matrona, Médico Obstetra, Pediatra, Enfermera Neonatal, etc.
- **Autenticación con RUT**: Login seguro con validación de identidad.
- **Auditoría Inmutable**: Registro de todas las acciones (Decreto 7/2023) con retención de 5 años.
- Bloqueo automático de cuentas tras 5 intentos fallidos.

---

## Estructura del Proyecto

```
hospital_hhm/
├── apps/                  # Aplicaciones Django
│   ├── administracion/   # Gestión de usuarios, roles y auditoría
│   ├── admision/         # Admisión de pacientes
│   ├── neonatologia/     # Atención neonatal
│   ├── obstetricia/      # Registro de partos
│   ├── pacientes/        # Gestión de pacientes
│   └── reportes/         # Reportes y estadísticas
├── docs/                  # Documentación técnica
│   ├── ACTUALIZACION_MODELOS.md
│   ├── INSTRUCCIONES_MIGRACION.md
│   └── MODELOS_COMPLETOS.py
├── hospital_hhm/         # Configuración del proyecto
├── logs/                 # Logs del sistema
├── scripts/              # Scripts de utilidades
│   ├── migraciones/     # Scripts de migración de BD
│   ├── utilidades/      # Herramientas administrativas
│   └── README.md        # Documentación de scripts
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── templates/            # Plantillas HTML
├── tests/                # Pruebas automatizadas
│   ├── test_selenium_forms.py
│   └── README_SELENIUM.md
├── venv/                 # Entorno virtual (no incluido en repo)
├── db.sqlite3           # Base de datos SQLite
├── manage.py            # Gestor de Django
└── requirements.txt     # Dependencias Python
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.11+
- Virtualenv
- Google Chrome (para pruebas Selenium)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-repositorio>
   cd hospital_hhm
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   Crear archivo `.env` en la raíz:
   ```env
   SECRET_KEY=tu_clave_secreta_segura
   DEBUG=True
   DATABASE_NAME=hospital_hhm_db
   ```

5. **Aplicar migraciones de base de datos**
   
   **IMPORTANTE:** Los modelos han sido actualizados con 80+ campos nuevos.
   
   **Opción A - Usar script automatizado (RECOMENDADO):**
   ```bash
   # Windows
   .\aplicar_migraciones.bat
   
   # Linux/Mac
   chmod +x aplicar_migraciones.sh
   ./aplicar_migraciones.sh
   ```
   
   **Opción B - Manual:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   
   Ver documentación detallada en: `ACTUALIZACION_MODELOS.md`

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Iniciar servidor**
   ```bash
   python manage.py runserver
   ```
   Acceder a `http://127.0.0.1:8000/`

---

## Guía de Uso Rápida

### 1. Iniciar Sesión
- Use su RUT (ej: 12.345.678-9) o nombre de usuario.
- Si falla 5 veces, su cuenta se bloqueará por seguridad.

### 2. Registrar un Parto
1. Vaya a **"Buscar Paciente"**.
2. Encuentre a la paciente y haga clic en **"Ver Detalle"**.
3. Presione el botón verde **"Registrar Parto"**.
4. Complete los datos del parto. El Grupo Robson se calculará solo.
5. Al guardar, será redirigido automáticamente al registro del Recién Nacido.

### 3. Registrar Recién Nacido
1. Complete los datos antropométricos y APGAR.
2. Si el APGAR a los 5 min es < 7, aparecerá una **ALERTA CRÍTICA**.
3. Guarde el registro para finalizar el proceso.

---

## Testing

El proyecto incluye tests unitarios para validar la lógica médica crítica.

```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de obstetricia (Robson)
python manage.py test apps.obstetricia

# Ejecutar tests de neonatología (APGAR)
python manage.py test apps.neonatologia
```

---

## Licencia y Normativa

Desarrollado para el Hospital Clínico Herminda Martín.
Cumple con:
- Ley 19.628 (Protección de la Vida Privada)
- Ley 20.584 (Derechos y Deberes del Paciente)
- Decreto 7/2023 (Reglamento de Seguridad de la Información)
