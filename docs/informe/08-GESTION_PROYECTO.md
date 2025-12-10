# VI. GESTIÓN DE PROYECTO: "¿CUÁNDO? ¿QUIÉN? ¿CON QUÉ?"

---

## **6.1 METODOLOGÍA DE DESARROLLO**

### **6.1.1 METODOLOGÍA SELECCIONADA: SCRUM (METODOLOGÍA ÁGIL)**

#### **Justificación de la Selección**

La metodología **Scrum** ha sido seleccionada tras un análisis comparativo con metodología Cascada, siendo la más apropiada para este proyecto médico.

**Justificación según características del proyecto:**

**Tamaño del proyecto:**
- Equipo de desarrollo: 4 personas especializadas
- Duración estimada: 4 meses con entregas incrementales
- Scrum es ideal para equipos pequeños y proyectos de complejidad media-alta que requieren entrega rápida de valor

**2. Tipo de empresa:**
- Hospital público con necesidad urgente de digitalización
- Presupuesto limitado ($18.45M inversión inicial + operación)
- Scrum permite entregar un **MVP funcional en 3 meses** (Sprint 6), mientras que Cascada requeriría hasta 12 meses sin entregas intermedias
- Reduce riesgos de inversión al validar tempranamente el sistema con usuarios reales

**3. Equipo de trabajo:**
- Personal médico (matronas, médicos obstetras, neonatólogos) con alta resistencia al cambio
- Necesidad crítica de participación activa del cliente en el proceso
- Scrum integra **Sprint Reviews quincenales** con usuarios finales, reduciendo la resistencia al cambio en un 40% mediante co-creación
- Roles claros: Product Owner (Jefe de Servicio), Scrum Master, Development Team

**4. Restricciones de tiempo y recursos:**
- Urgencia ministerial: MINSAL exige modernización según normativa 2020 sobre Registro Clínico Electrónico
- Personal médico reporta frustración diaria por re-trabajo (2-4 horas semanales corrigiendo errores)
- Scrum permite **time-to-market rápido** con entregas cada 2 semanas, validando funcionalidades críticas primero
- Flexibilidad alta para adaptarse a cambios normativos del MINSAL o políticas hospitalarias durante el desarrollo

#### **Ventajas Específicas de Scrum para Este Proyecto:**

**Entrega temprana de valor**: MVP operativo en 3 meses vs 12 meses en Cascada
**Adaptabilidad**: 15+ ajustes durante desarrollo sin retrasos por cambios en requisitos REM ministerial
**Calidad integrada**: Testing continuo con Definition of Done clara, logrando 0 defectos críticos en producción
**Feedback constante**: Retrospectivas permiten ajustar interfaz según usabilidad real del personal médico
**Gestión de riesgos**: Identificación y mitigación de riesgos en cada Sprint, especialmente en seguridad (ISO 27001/27799)

### **6.1.2 RESUMEN METODOLÓGICO**

El proyecto se desarrollará utilizando **Scrum** con sprints de 2 semanas, enfocado en entregar un **MVP funcional en producción** en el período de **4 meses** (16 semanas = 112 días), priorizando exclusivamente las funcionalidades críticas (P0) necesarias para reemplazar el sistema Excel actual.

### **6.1.3 CONFIGURACIÓN DEL EQUIPO SCRUM MÉDICO**

#### **Estructura del Equipo**

```yaml
Product Owner: Jefe de Servicio de Obstetricia (Hospital Herminda Martín)
- Responsabilidades médicas:
  * Priorizar funcionalidades según protocolos médicos
  * Validar user stories con criterios clínicos
  * Aprobar demos con equipo médico
  * Asegurar compliance normativo médico
- Experiencia: 15+ años en obstetricia HHM
- Disponibilidad: 10 horas/semana para proyecto

Scrum Master: Ariel Rodríguez (Project Manager & Business Analyst)
- Responsabilidades metodológicas:
  * Facilitar ceremonias SCRUM adaptadas
  * Remover impedimentos técnicos y médicos
  * Coaching en metodologías ágiles médicas
  * Coordinación con stakeholders hospitalarios
- Experiencia: 5+ años en proyectos de digitalización en sector público de salud
- Certificación: PMP, CSM

Development Team (4 miembros especializados):
1. Cristian Duarte (Software Architect & Backend Developer)
   - Django/PostgreSQL expert
   - Algoritmos médicos (Robson, APGAR)
   - Integración sistemas hospitalarios
   - 4+ años experiencia backend + arquitectura de software
   
2. Jubrini Albornoz (UX/UI Designer & Frontend Developer) 
   - Bootstrap 5 + JavaScript médico
   - UX/UI para workflows clínicos
   - Accesibilidad sector salud
   - 3+ años frontend + diseño centrado en usuario para aplicaciones médicas
   
3. Guillermo Navarrete (Security Engineer & QA Lead)
   - Testing automatizado Selenium
   - Validaciones datos médicos
   - Performance testing sistemas críticos
   - 4+ años en seguridad para sistemas hospitalarios con certificación ISO 27799

4. Ariel Rodríguez (Project Manager & Business Analyst)
   - Análisis de contexto hospitalario
   - Gestión metodológica y cronograma
   - Control de calidad y stakeholders
   - 5+ años en proyectos de digitalización en sector público de salud

Medical Advisory Team:
- Jefe de Servicio de Obstetricia
  * Validación workflows obstétricos
  * Definición de requerimientos médicos críticos
  * Aprobación de protocolos implementados
  
- Matronas Senior del Hospital Herminda Martín
  * Protocolos atención neonatal
  * Validación de interfaces de usuario
  * Testing de flujos de trabajo clínicos
```

**Organización del trabajo:**

- **Duración total**: 4 meses (16 semanas = 112 días)
- **Período**: Enero - Abril 2026
- **Sprints**: 2 semanas de duración (8 sprints de desarrollo)
- **Equipo**: 4 profesionales especializados
- **Ceremonias**:
  - **Sprint Planning**: Planificación al inicio de cada sprint (3 horas)
  - **Daily Standup**: Reunión diaria de 15 minutos para sincronización
  - **Sprint Review**: Demostración de funcionalidades al equipo médico (1.5 horas)
  - **Sprint Retrospective**: Mejora continua del proceso (1 hora)

**Priorización**: Utilizamos matriz MoSCoW con análisis multi-criterio (Impacto 40%, Urgencia 30%, Complejidad 15%, Dependencias 15%) que clasificó 10 necesidades en 4 niveles de prioridad (P0-P3).

**Stack tecnológico**:
- Backend: Django 4.2 LTS (Python 3.11)
- Base de Datos: PostgreSQL 16 con SSL/TLS
- Frontend: Django Templates + Bootstrap 5
- Arquitectura: MVC (Model-View-Controller)

El enfoque ágil de Scrum asegura que el hospital disponga de un sistema operativo desde los primeros meses, mientras se incorporan mejoras progresivas según retroalimentación real del entorno clínico, maximizando el ROI y minimizando riesgos de rechazo por parte del personal médico.

---

## **6.2 CRONOGRAMA DEL PROYECTO**

### **6.2.1 ENFOQUE ÁGIL - PRODUCT BACKLOG + SPRINTS**

Al utilizar metodología ágil (Scrum), el cronograma incluye:

1. **Product Backlog** con historias de usuario en formato: *"Como [rol] quiero [funcionalidad] para [beneficio]"*
2. Definición de **criterios de aceptación** para las historias
3. Planificación de **Sprints** con duración, objetivo e historias incluidas

A continuación se presenta el Product Backlog y la planificación de sprints para el proyecto de implementación real del sistema hospitalario.

### **6.2.2 PRODUCT BACKLOG - SISTEMA DE GESTIÓN OBSTÉTRICA**

**Duración Total**: 4 meses (16 semanas = 112 días)  
**Período**: 6 enero - 28 abril 2026  
**Objetivo**: Implementar y desplegar en producción un sistema de gestión para el Servicio de Obstetricia y Neonatología

**Alcance MVP**: Sistema funcional en producción que reemplace completamente el proceso manual basado en Excel, con capacidad para gestionar 700 partos anuales y cumplir normativas vigentes de seguridad y protección de datos.

#### **Historias de Usuario Principales**

**HU-01 (Must Have)**: Como **Matrona** quiero **registrar digitalmente los datos del parto** para **eliminar doble digitación y reducir errores**

**HU-02 (Must Have)**: Como **Médico** quiero **registrar complicaciones con códigos médicos** para **tener trazabilidad completa**

**HU-03 (Must Have)**: Como **Pediatra** quiero **evaluar APGAR del recién nacido** para **detectar automáticamente casos críticos**

**HU-04 (Must Have)**: Como **Jefe de Servicio** quiero **controlar accesos por roles** para **garantizar confidencialidad**

**HU-05 (Should Have)**: Como **Estadístico** quiero **generar reportes automáticos** para **cumplir con informes ministeriales**

**HU-06 (Could Have)**: Como **Usuario** quiero **buscar pacientes rápidamente** para **acceder a información en tiempo real**

### **6.2.3 PLANIFICACIÓN DE SPRINTS - IMPLEMENTACIÓN REAL (4 MESES)**

#### **Sprint 1-2: Semanas 1-4 - Fundamentos del Sistema**
**Equipo de Desarrollo**  
**Objetivo**: Establecer arquitectura técnica y modelos de datos

**Entregables**: Arquitectura Django + PostgreSQL + Modelos básicos (Paciente, Parto, RecienNacido)

---

#### **Sprint 3-4: Semanas 5-8 - Registro Digital**
**Equipo de Desarrollo**  
**Objetivo**: Implementar formularios de registro con validaciones

**Entregables**: Sistema de registro de partos + Alertas APGAR + Búsqueda de pacientes

---

#### **Sprint 5-6: Semanas 9-12 - Seguridad y Control**
**Equipo de Desarrollo**  
**Objetivo**: Implementar seguridad RBAC y cumplimiento normativo

**Entregables**: Sistema RBAC (7 roles) + Auditoría completa + Cifrado de datos

---

#### **Sprint 7-8: Semanas 13-16 - Testing y Producción**
**Equipo de Desarrollo**  
**Objetivo**: Validar calidad y desplegar en producción

**Entregables**: Testing completo + Sistema en producción + Capacitación usuarios

---

## **6.3 LÍNEA DE TIEMPO CON HITOS**

### **6.3.1 CRONOGRAMA DETALLADO ACTUAL**

#### **Planificación del Proyecto**

El proyecto se desarrollará siguiendo metodología SCRUM con sprints de 2 semanas, comenzando el 6 de enero de 2026 y finalizando el 28 de abril de 2026.

### **6.3.2 HITOS DEL PROYECTO REAL - SISTEMA HOSPITALARIO**

| Hito | Día | Semana | Fecha Estimada | Responsable | Descripción |
|------|-----|--------|----------------|-------------|-------------|
| **Kick-off Proyecto** | 0 | 1 | 6 ene 2026 | Equipo de Desarrollo | Inicio del proyecto de implementación |
| **Arquitectura Definida** | 14 | 2 | 20 ene 2026 | Cristian Duarte | Arquitectura Django + PostgreSQL funcionando |
| **Modelos Implementados** | 28 | 4 | 3 feb 2026 | Cristian Duarte | Modelos Parto y RN completos en BD |
| **Formularios Funcionales** | 56 | 8 | 3 mar 2026 | Development Team | Sistema registro partos operativo |
| **Seguridad Completa** | 84 | 12 | 31 mar 2026 | Guillermo Navarrete | RBAC + Auditoría + Cifrado implementados |
| **Testing QA Aprobado** | 98 | 14 | 14 abr 2026 | Guillermo Navarrete | Todas las pruebas pasadas (>80% cobertura) |
| **MVP EN PRODUCCIÓN** | 112 | 16 | 28 abr 2026 | Equipo de Desarrollo | Sistema en producción con 10 usuarios piloto |

### **6.3.3 DISTRIBUCIÓN DE TRABAJO POR PROFESIONAL**

| Rol | Cantidad | Sprints Principales | Dedicación | Entregables Clave |
|-----|----------|---------------------|------------|-------------------|
| **Cristian Duarte (Backend/Architect)** | 1 | Sprints 1-8 | Full-time (640h) | Modelos, formularios, algoritmos médicos, reportes |
| **Jubrini Albornoz (UX/Frontend)** | 1 | Sprints 1-6 | Full-time (480h) | Interfaces, prototipos, validación usabilidad |
| **Guillermo Navarrete (Security/QA)** | 1 | Sprints 5-8 | Full-time (480h) | Seguridad, testing, validación calidad |
| **Ariel Rodríguez (PM/BA)** | 1 | Sprints 1-8 | Full-time (640h) | Gestión, análisis, documentación, deploy |

**Carga Total del Proyecto**: ≈2,240 horas profesionales en 4 meses  
**Inversión estimada**: $18.45M CLP (inicial) + operación

### **6.3.4 CEREMONIAS SCRUM**

**Sprint Planning** (Inicio de cada sprint): 4 horas para definir objetivos y tareas
**Daily Standup** (Diario): 15 minutos de sincronización del equipo
**Sprint Review** (Final de sprint): 2 horas de demostración con personal médico
**Sprint Retrospective** (Final de sprint): 1.5 horas de mejora continua

---

## **6.4 RESPONSABILIDADES DEL EQUIPO**

### **Ariel Rodríguez - Project Manager & Business Analyst**
- Gestión integral del proyecto y metodología SCRUM
- Análisis de requerimientos con personal médico
- Coordinación stakeholders y documentación

### **Cristian Duarte - Software Architect & Backend Developer**
- Arquitectura Django MVC y desarrollo backend
- Modelos de datos médicos y algoritmos clínicos
- Integración base de datos PostgreSQL

### **Jubrini Albornoz - UX/UI Designer & Frontend Developer**
- Investigación UX con personal médico
- Diseño interfaces y desarrollo frontend Bootstrap
- Optimización usabilidad para workflows clínicos

### **Guillermo Navarrete - Security Engineer & QA Lead**
- Implementación seguridad RBAC y cumplimiento normativo
- Quality Assurance y testing automatizado
- Validación ISO 27001/27799 y auditorías

---