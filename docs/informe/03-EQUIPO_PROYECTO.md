# I. EQUIPO LÍDER DEL PROYECTO

---

## **1.1 DESCRIPCIÓN DEL PERSONAL DEL PROYECTO**

El equipo está conformado por 4 profesionales especializados en desarrollo de software para el sector salud. Cada miembro desempeñó roles específicos para la implementación del Sistema de Gestión Obstétrica y Neonatología del Hospital Herminda Martín.

---

## **1.2 ROLES INDIVIDUALES Y CALIFICACIONES**

### **🎯 ARIEL RODRÍGUEZ - PROJECT MANAGER & BUSINESS ANALYST**

**Rol en el Proyecto:** Gestión integral del proyecto, análisis de contexto hospitalario y definición metodológica

**Calificaciones Relevantes:**
- **Formación:** Ingeniería en Sistemas
- **Rol en el Proyecto:** Gestión de proyecto y análisis de requerimientos

**Funciones Desempeñadas:**
- **Análisis de Contexto:** Levantamiento de requerimientos con personal médico del Hospital Herminda Martín para identificar necesidades del sistema obstétrico y neonatal
- **Metodología de Trabajo:** Coordinación del desarrollo utilizando metodología ágil para entregas incrementales
- **Planificación:** Organización del cronograma del proyecto y establecimiento de hitos de desarrollo
- **Comunicación:** Facilitó la coordinación entre el equipo técnico y personal médico (matronas, obstetras, pediatras)
- **Control de Calidad:** Establecimiento de criterios de aceptación para las funcionalidades del sistema

**Contribución al Proyecto:** Coordinación general del proyecto y aseguramiento del cumplimiento de requerimientos médicos.

---

### **🏗️ CRISTIAN DUARTE - SOFTWARE ARCHITECT & BACKEND DEVELOPER**

**Rol en el Proyecto:** Arquitectura del sistema, diseño de base de datos y desarrollo backend

**Calificaciones Relevantes:**
- **Formación:** Ingeniería en Informática
- **Expertise Técnico:** Django 4.2, PostgreSQL, Python, Bootstrap 5
- **Rol en el Proyecto:** Arquitectura del sistema y desarrollo backend

**Funciones Desempeñadas:**
- **Arquitectura del Sistema:** Diseño de la arquitectura Django siguiendo patrones Model-View-Controller
- **Modelos de Datos:** Implementación de modelos principales:
  - PacienteMadre (datos demográficos y contacto)
  - ControlPrenatal (seguimiento prenatal)
  - Parto (registro del proceso de parto)
  - RecienNacido (datos neonatales y APGAR)
  - Sistema de auditoría
- **Base de Datos:** Diseño e implementación del modelo entidad-relación con PostgreSQL
- **Backend Django:** Desarrollo de vistas, forms y validaciones para los procesos obstétricos y neonatales
- **Validaciones:** Implementación de validaciones automáticas para campos médicos (rangos APGAR, peso RN, etc.)

**Contribución al Proyecto:** Desarrollo de la estructura técnica completa del sistema utilizando Django 4.2 y PostgreSQL.

---

### **🎨 JUBRINI ALBORNOZ - UX/UI DESIGNER & FRONTEND DEVELOPER**

**Rol en el Proyecto:** Experiencia de usuario, prototipado de interfaces y modelo de datos

**Calificaciones Relevantes:**
- **Formación:** Diseño Gráfico
- **Herramientas:** Figma, Bootstrap 5, CSS3, JavaScript
- **Rol en el Proyecto:** Diseño de interfaces y experiencia de usuario

**Funciones Desempeñadas:**
- **Diseño UX/UI:** Análisis de flujos de trabajo del personal médico para diseñar interfaces intuitivas
- **Prototipado:** Desarrollo de wireframes y prototipos para las principales interfaces del sistema
- **Frontend Responsivo:** Implementación de interfaces utilizando Bootstrap 5 para compatibilidad con diferentes dispositivos
- **Templates Django:** Desarrollo de templates HTML para:
  - Registro de pacientes
  - Formularios de control prenatal
  - Registro de partos
  - Evaluación APGAR
  - Dashboard principal
- **Usabilidad:** Diseño centrado en facilitar el trabajo del personal médico
- **Sistema Visual:** Establecimiento de guía de estilo coherente para toda la aplicación

**Contribución al Proyecto:** Diseño e implementación de todas las interfaces de usuario del sistema, priorizando usabilidad médica.

---

### **🔐 GUILLERMO NAVARRETE - SECURITY ENGINEER & QA LEAD**

**Rol en el Proyecto:** Seguridad del sistema, plan de pruebas e integración de componentes

**Calificaciones Relevantes:**
- **Formación:** Ingeniería en Ciberseguridad
- **Rol en el Proyecto:** Seguridad del sistema y plan de pruebas
- **Enfoque:** Sistemas de salud y protección de datos médicos

**Funciones Desempeñadas:**
- **Seguridad del Sistema:** Implementación de sistema de control de acceso basado en roles para diferentes tipos de usuarios médicos
- **Cumplimiento Normativo:** Asegurar compliance con normativas chilenas de protección de datos (Ley 19.628) y seguridad en salud
- **Plan de Pruebas:** Diseño y ejecución de casos de prueba para validar funcionalidad, seguridad y rendimiento
- **Testing Automatizado:** Implementación de pruebas Selenium para testing automatizado de flujos críticos
- **Auditoría:** Sistema de auditoría para tracking de cambios en registros médicos
- **Validación de Datos:** Verificación de protección adecuada para datos sensibles de salud

**Contribución al Proyecto:** Implementación del framework de seguridad y sistema de pruebas para garantizar la protección de datos médicos.

---

## **1.3 COLABORACIÓN Y METODOLOGÍA DEL EQUIPO**

### **Organización del Trabajo:**
El equipo trabajó de forma colaborativa para desarrollar el Sistema de Gestión Obstétrica y Neonatología, con cada miembro aportando desde su área de especialización.

### **División de Responsabilidades:**
- **Ariel Rodríguez:** Coordinación general, análisis de requerimientos y comunicación con stakeholders médicos
- **Cristian Duarte:** Arquitectura técnica, modelado de datos y desarrollo backend con Django
- **Jubrini Albornoz:** Diseño de interfaces, experiencia de usuario y implementación frontend
- **Guillermo Navarrete:** Seguridad del sistema, control de calidad y testing

### **Tecnologías Implementadas:**
El proyecto se desarrolló utilizando:
- **Backend:** Django 4.2 con PostgreSQL
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Seguridad:** django-guardian para control de acceso, django-auditlog para auditoría
- **Testing:** Selenium 4.15.2 para pruebas automatizadas
- **Herramientas:** Figma para prototipado, Git para control de versiones

### **Resultados del Trabajo en Equipo:**
El equipo logró desarrollar un sistema funcional que incluye:
- Registro completo de pacientes obstétricas
- Control prenatal digitalizado
- Registro detallado de procesos de parto
- Evaluación neonatal con escala APGAR
- Sistema de auditoría y seguridad
- Interfaces responsive para diferentes dispositivos

---