# III. ENUNCIADO DEL DESAFÍO: EL "¿POR QUÉ?"

---

## **3.1 ANTECEDENTES DEL PROBLEMA**

### **3.1.1 CONTEXTO INSTITUCIONAL**

El **Hospital Herminda Martín** es un establecimiento de salud pública de la Región de Ñuble que atiende a la población de la zona. Su **Servicio de Obstetricia y Neonatología** representa uno de los servicios críticos del hospital, proporcionando atención materno-infantil las 24 horas del día, todos los días del año.

Este servicio atiende tanto partos de bajo riesgo como casos de alta complejidad, siendo un referente importante en la atención obstétrica de la región.

### **3.1.2 PROBLEMÁTICA CENTRAL**

El Servicio de Obstetricia y Neonatología enfrenta un **problema crítico de gestión de información clínica** debido al uso de un sistema completamente manual basado en **Microsoft Excel**, donde se registran múltiples campos de información por cada atención de parto en planillas locales.

Esta situación representa una **brecha tecnológica significativa**, cuando muchos establecimientos de salud han migrado a sistemas digitales, y contrasta con los estándares modernos de atención en salud que exigen trazabilidad, precisión y cumplimiento normativo.

---

## **3.2 PROBLEMÁTICAS ESPECÍFICAS IDENTIFICADAS**

### **3.2.1 ERRORES EN EL REGISTRO MANUAL**

**Descripción del Problema:**
El sistema manual basado en Excel presenta riesgo de errores en las fichas clínicas debido a la transcripción manual y falta de validaciones automáticas.

**Impacto Crítico:**
- **Calidad de datos comprometida:** Los errores afectan la confiabilidad de la información clínica
- **Seguimiento clínico deficiente:** Datos incorrectos pueden afectar decisiones médicas futuras
- **Riesgo médico-legal:** Inconsistencias en registros pueden generar problemas en casos de complicaciones
- **Pérdida de confiabilidad:** Personal médico puede perder confianza en datos históricos

**Ejemplos de Errores Frecuentes:**
- Transcripción incorrecta de datos antropométricos del recién nacido
- Errores en cálculo de datos gestacionales
- Inconsistencias en registro de complicaciones
- Duplicación o pérdida de registros por manipulación manual

---

### **3.2.2 TIEMPO EXCESIVO DE REGISTRO**

**Descripción del Problema:**
El proceso manual de registro y transcripción consume tiempo considerable por parto, restando tiempo valioso a la atención directa de pacientes.

**Impacto en la Operación:**
- **Sobrecarga laboral:** Personal médico debe dividir tiempo entre atención clínica y documentación administrativa
- **Ineficiencia operacional:** Tiempo de registro puede generar demoras en flujo de pacientes
- **Fatiga profesional:** Doble trabajo (atención + digitación) genera desgaste en personal
- **Costo de oportunidad:** Tiempo que podría destinarse a atención directa

**Proceso Actual:**
- Registro inicial durante la atención
- Transcripción posterior a Excel
- Validación y corrección de errores
- Tiempo total considerable por caso

---

### **3.2.3 GENERACIÓN MANUAL DE REPORTES**

**Descripción del Problema:**
La elaboración de reportes estadísticos se realiza de forma completamente manual, consumiendo tiempo considerable del personal clínico o administrativo, con alto riesgo de errores de consolidación.

**Impacto Administrativo:**
- **Ineficiencia operacional:** Tiempo considerable en consolidación manual
- **Errores de cálculo:** Riesgo de inconsistencias en totalizaciones y clasificaciones
- **Retrasos en reportería:** Posibles demoras en entrega de reportes requeridos
- **Recurso humano mal utilizado:** Personal médico especializado realizando tareas administrativas

**Complejidad de los Reportes:**
- Clasificación manual de diferentes tipos de parto
- Consolidación de complicaciones maternas y neonatales
- Cálculos estadísticos de indicadores hospitalarios
- Validación cruzada con otros reportes del servicio

---

### **3.2.4 FALTA DE TRAZABILIDAD**

**Descripción del Problema:**
No existe un registro confiable de **quién ingresó o modificó la información, ni cuándo**, lo que dificulta auditorías clínicas y genera riesgos significativos.

**Riesgos Asociados:**
- **Imposibilidad de auditoría:** No se puede rastrear cambios o responsabilidades
- **Vulnerabilidad legal:** Falta de evidencia en casos de consultas o demandas
- **Pérdida de accountability:** Ausencia de responsabilidad individual por errores
- **Incumplimiento de estándares:** Violación de requisitos de trazabilidad en salud

**Casos Críticos Sin Trazabilidad:**
- Modificaciones posteriores a registros de complicaciones
- Cambios en datos de recién nacidos después del alta
- Correcciones de datos sin justificación documentada
- Actualizaciones de información sin identificación de responsable

---

### **3.2.5 LIMITACIONES DE SEGURIDAD Y CUMPLIMIENTO**

**Descripción del Problema:**
El sistema actual presenta limitaciones en cuanto a seguridad y protección de datos que no cumplen con estándares modernos de sistemas de información de salud.

**Limitaciones Identificadas:**

#### **Protección de Datos Personales:**
- **Falta de cifrado:** Datos sensibles almacenados sin protección especial
- **Acceso no controlado:** Cualquier persona con acceso al archivo puede ver toda la información
- **Ausencia de controles:** No hay registro de autorización para tratamiento de datos

#### **Confidencialidad y Acceso:**
- **Control limitado:** Imposibilidad de controlar acceso a información específica
- **Acceso no granular:** No hay restricciones por tipo de información o rol
- **Falta de proceso formal:** No hay mecanismo estructurado para corrección de datos

#### **Seguridad de la Información:**
- **Ausencia de logs:** No hay registro de accesos o modificaciones
- **Falta de retención:** No se garantiza conservación segura de información
- **Sin backup estructurado:** Riesgo de pérdida de información
- **Vulnerabilidades no gestionadas:** Sistema sin actualizaciones de seguridad

---

### **3.2.6 AUSENCIA DE VALIDACIONES AUTOMÁTICAS**

**Descripción del Problema:**
El uso de Excel no incorpora validaciones médicas robustas, permitiendo errores que pueden afectar la calidad de la atención.

**Errores No Detectados:**

#### **Cálculo de Evaluaciones Médicas:**
- **Error frecuente:** Cálculos manuales incorrectos en evaluaciones
- **Impacto:** No detección automática de casos que requieren atención especial
- **Consecuencia:** Posible retraso en protocolos de atención

#### **Clasificación de Casos:**
- **Error frecuente:** Asignación manual incorrecta de clasificaciones
- **Impacto:** Estadísticas institucionales erróneas
- **Consecuencia:** Información de gestión basada en datos incorrectos

#### **Detección de Situaciones Especiales:**
- **Casos especiales:** Sin activación automática de protocolos
- **Controles insuficientes:** Sin alertas preventivas
- **Complicaciones:** Sin escalamiento automático

**Validaciones Ausentes:**
- Rangos de parámetros médicos importantes
- Coherencia entre fechas y datos clínicos
- Validación de identificación de pacientes y profesionales

---

### **3.2.7 ACCESO NO CONTROLADO Y SIN CIFRADO**

**Descripción del Problema:**
El archivo Excel utilizado presenta vulnerabilidades críticas de seguridad que exponen datos ultra-sensibles de salud.

**Vulnerabilidades Identificadas:**

#### **Falta de Cifrado:**
- **Datos en texto plano:** Información VIH, violencia intrafamiliar, salud mental sin protección
- **Facilidad de copia:** Archivo puede duplicarse sin control
- **Transmisión insegura:** Envío por correo sin cifrado end-to-end

#### **Acceso Sin Control:**
- **Sin roles diferenciados:** Todos los usuarios tienen acceso completo
- **Ausencia de permisos granulares:** No hay restricción por tipo de información
- **Sin logging de accesos:** Imposible rastrear quién accede y cuándo

#### **Riesgos de Ciberseguridad:**
- **Extracción no autorizada:** Posibilidad de robo de información sin detección
- **Modificación maliciosa:** Cambios no autorizados sin trazabilidad
- **Pérdida de integridad:** Corrupción accidental o intencional de datos

**Riesgos Específicos:**
- **Legal:** Multas hasta $500M por violación de Ley de Protección de Datos
- **Ético:** Violación de confidencialidad médica
- **Reputacional:** Daño a imagen institucional por filtración de datos
- **Operacional:** Pérdida de confianza del personal médico en el sistema

---

## **3.3 CARACTERÍSTICAS DEL GRUPO OBJETIVO**

### **3.3.1 UBICACIÓN Y CONTEXTO**

**Localización:**
- **Hospital:** Hospital Herminda Martín
- **Ciudad:** Chillán, Región de Ñuble, Chile
- **Tipo de hospital:** Hospital público de referencia regional

**Características de Pacientes:**
- Atención de partos durante todo el año
- Procedencia de la ciudad y comunas rurales de la región
- Diversidad socioeconómica en la población atendida
- Rango etario materno amplio
- Diferentes tipos de parto (vaginal y cesárea)

### **3.3.2 PERSONAL MÉDICO (USUARIOS DIRECTOS)**

**Equipo Multidisciplinario:** Personal especializado distribuido en diferentes roles

#### **Roles Principales:**
- **Matronas/Matrones:** Atención directa de partos, registro inicial
- **Médicos Obstetras:** Atención partos complejos, procedimientos especializados
- **Pediatras Neonatólogos:** Evaluación recién nacidos, atención neonatal
- **Enfermeras Neonatales:** Cuidado post-parto, procedimientos de enfermería
- **Personal de Apoyo:** Asistencia en atención y procedimientos
- **Personal Administrativo:** Consolidación reportes, estadísticas
- **Jefatura de Servicio:** Supervisión, gestión, reportería institucional

#### **Características de Usuarios:**
- **Experiencia tecnológica:** Variada, desde básica hasta intermedia
- **Disposición al cambio:** Variable, preferencia por métodos conocidos
- **Disponibilidad para capacitación:** Limitada por turnos y carga laboral
- **Expectativas:** Sistema simple, rápido, que no interfiera con atención clínica

### **3.3.3 LIMITACIONES Y RESTRICCIONES DEL GRUPO OBJETIVO**

#### **Limitaciones Operacionales:**
- **Tiempo limitado:** Personal en turnos de 12-24 horas, poco tiempo para capacitación
- **Estrés laboral:** Ambiente de alta presión con situaciones de emergencia
- **Trabajo 24/7:** Sistema debe funcionar sin interrupciones
- **Múltiples dispositivos:** Acceso desde computadores, tablets, estaciones móviles

#### **Limitaciones Tecnológicas:**
- **Conectividad variable:** WiFi hospitalario con interrupciones ocasionales
- **Dispositivos heterogéneos:** Mezcla de equipos antiguos y modernos
- **Conocimiento técnico limitado:** Usuarios no expertos en tecnología
- **Soporte técnico reducido:** Equipo TI hospitalario de 2 personas

#### **Limitaciones Regulatorias:**
- **Cumplimiento estricto:** Cero tolerancia a errores en datos de salud
- **Auditorías frecuentes:** Revisiones ministeriales trimestrales
- **Protección de datos:** Requisitos extremos de confidencialidad
- **Disponibilidad crítica:** Sistema no puede tener caídas durante atención

---

## **3.4 NECESIDAD DE SOLUCIÓN**

### **3.4.1 IMPACTO DE NO RESOLVER EL PROBLEMA**
- **Acumulación de errores:** Continuidad de inconsistencias en registros clínicos
- **Ineficiencia operacional:** Mantenimiento de procesos manuales que consumen tiempo
- **Riesgos de cumplimiento:** Posibles dificultades con estándares de calidad
- **Deterioro de datos:** Mayor inconsistencia en información hospitalaria

### **3.4.2 OPORTUNIDADES DE MEJORA**
- **Digitalización:** Transición a sistemas modernos de información
- **Eficiencia:** Reducción de tiempo en documentación manual
- **Calidad:** Mejora en precisión y confiabilidad de datos
- **Cumplimiento:** Alineación con estándares de sistemas de información en salud

---