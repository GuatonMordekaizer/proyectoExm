from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from apps.pacientes.models import PacienteMadre
from django.utils import timezone


class ControlPrenatal(models.Model):
    """
    Modelo para control prenatal de la paciente.
    Registra datos del embarazo actual y antecedentes obstétricos.
    """
    
    paciente = models.ForeignKey(
        PacienteMadre,
        on_delete=models.PROTECT,
        related_name='controles_prenatales'
    )
    
    # Fechas importantes
    fur = models.DateField(
        help_text='Fecha Última Regla'
    )
    fecha_primer_control = models.DateField(blank=True, null=True)
    num_controles_realizados = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    
    # Grupo sanguíneo
    GRUPO_SANGUINEO_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]
    grupo_sanguineo = models.CharField(
        max_length=5,
        choices=GRUPO_SANGUINEO_CHOICES,
        blank=True
    )
    
    FACTOR_RH_CHOICES = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
    ]
    factor_rh = models.CharField(
        max_length=10,
        choices=FACTOR_RH_CHOICES,
        blank=True
    )
    
    # Exámenes de laboratorio
    hemoglobina_g_dl = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[MinValueValidator(6.0), MaxValueValidator(20.0)],
        help_text='Hemoglobina en g/dL'
    )
    
    glicemia_mg_dl = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(50), MaxValueValidator(400)],
        help_text='Glicemia en mg/dL'
    )
    
    # Antecedentes obstétricos
    num_gestas_previas = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    num_partos_previos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    num_cesareas_previas = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    num_abortos_previos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    
    # Características del embarazo actual
    embarazo_gemelar = models.BooleanField(default=False)
    
    # Patologías del embarazo
    hipertension = models.BooleanField(default=False)
    diabetes_gestacional = models.BooleanField(default=False)
    preeclampsia = models.BooleanField(default=False)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'control_prenatal'
        verbose_name = 'Control Prenatal'
        verbose_name_plural = 'Controles Prenatales'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Control Prenatal - {self.paciente.nombre_completo} ({self.fur})"
    
    @property
    def edad_gestacional_semanas(self):
        """Calcula edad gestacional en semanas desde FUR"""
        from datetime import date
        today = date.today()
        dias = (today - self.fur).days
        return dias // 7


class ExamenPrenatal(models.Model):
    """
    Modelo para exámenes prenatales obligatorios.
    VIH, VDRL, Hepatitis B, Streptococo B, etc.
    """
    
    control_prenatal = models.ForeignKey(
        ControlPrenatal,
        on_delete=models.CASCADE,
        related_name='examenes'
    )
    
    # Tipo de examen
    TIPO_EXAMEN_CHOICES = [
        ('vih', 'VIH'),
        ('vdrl', 'VDRL (Sífilis)'),
        ('hepatitis_b', 'Hepatitis B'),
        ('streptococo_b', 'Streptococo Grupo B'),
        ('hemograma', 'Hemograma'),
        ('grupo_rh', 'Grupo y RH'),
        ('glicemia', 'Glicemia'),
        ('urocultivo', 'Urocultivo'),
    ]
    tipo_examen = models.CharField(
        max_length=30,
        choices=TIPO_EXAMEN_CHOICES
    )
    
    # Resultado del examen
    RESULTADO_CHOICES = [
        ('negativo', 'Negativo'),
        ('positivo', 'Positivo'),
        ('no_reactivo', 'No Reactivo'),
        ('reactivo', 'Reactivo'),
        ('no_realizado', 'No Realizado'),
        ('pendiente', 'Pendiente'),
    ]
    resultado = models.CharField(
        max_length=30,
        choices=RESULTADO_CHOICES
    )
    
    # Fecha del examen
    fecha_examen = models.DateField(blank=True, null=True)
    
    # Observaciones
    observaciones = models.TextField(blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'examen_prenatal'
        verbose_name = 'Examen Prenatal'
        verbose_name_plural = 'Exámenes Prenatales'
        ordering = ['-fecha_examen']
        indexes = [
            models.Index(fields=['tipo_examen', 'resultado'], name='idx_examen_tipo_resultado'),
            models.Index(fields=['-fecha_examen'], name='idx_examen_fecha'),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_examen_display()}: {self.get_resultado_display()}"
    
    @property
    def es_critico(self):
        """Determina si el resultado requiere protocolo especial"""
        examenes_criticos = {
            'vih': 'positivo',
            'vdrl': 'reactivo',
            'hepatitis_b': 'positivo',
            'streptococo_b': 'positivo',
        }
        
        if self.tipo_examen in examenes_criticos:
            return self.resultado == examenes_criticos[self.tipo_examen]
        
        return False


class Parto(models.Model):
    """
    Modelo principal para registro de parto.
    Contiene los 99 campos requeridos según documentación.
    """
    
    paciente = models.ForeignKey(
        PacienteMadre,
        on_delete=models.PROTECT,
        related_name='partos'
    )
    
    control_prenatal = models.ForeignKey(
        ControlPrenatal,
        on_delete=models.PROTECT,
        related_name='partos',
        blank=True,
        null=True
    )
    
    # Usuario que registra (matrona o médico)
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='partos_registrados'
    )
    
    # === SECCIÓN 1: DATOS DEL PARTO ===
    
    fecha_parto = models.DateField()
    hora_parto = models.TimeField()
    
    # Edad gestacional
    edad_gestacional_semanas = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(45)],
        help_text='Edad gestacional en semanas'
    )
    edad_gestacional_dias = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(6)]
    )
    
    # Profesional responsable
    profesional_atiende_rut = models.CharField(
        max_length=12,
        blank=True,
        help_text='RUT del profesional que atiende el parto'
    )
    profesional_atiende_nombre = models.CharField(
        max_length=200,
        blank=True,
        help_text='Nombre del profesional que atiende'
    )
    
    # Acompañamiento
    acompanamiento_prepartos = models.BooleanField(
        default=False,
        help_text='Acompañamiento durante prepartos'
    )
    acompanamiento_parto = models.BooleanField(
        default=False,
        help_text='Acompañamiento durante el parto'
    )
    acompanamiento_rn = models.BooleanField(
        default=False,
        help_text='Acompañamiento durante atención RN'
    )
    nombre_acompanante = models.CharField(
        max_length=200,
        blank=True,
        help_text='Nombre del acompañante'
    )
    parentesco_acompanante = models.CharField(
        max_length=100,
        blank=True,
        help_text='Parentesco del acompañante'
    )
    
    # Tipo de parto
    TIPO_PARTO_CHOICES = [
        ('eutocico', 'Eutócico (Vaginal Normal)'),
        ('cesarea_electiva', 'Cesárea Electiva'),
        ('cesarea_urgencia', 'Cesárea de Urgencia'),
        ('forceps', 'Fórceps'),
        ('ventosa', 'Ventosa'),
    ]
    tipo_parto = models.CharField(max_length=30, choices=TIPO_PARTO_CHOICES)
    
    # Presentación fetal
    PRESENTACION_CHOICES = [
        ('cefalica', 'Cefálica'),
        ('podalica', 'Podálica'),
        ('transversa', 'Transversa'),
    ]
    presentacion = models.CharField(max_length=20, choices=PRESENTACION_CHOICES)
    
    # Inicio del trabajo de parto
    INICIO_TRABAJO_PARTO_CHOICES = [
        ('espontaneo', 'Espontáneo'),
        ('inducido', 'Inducido'),
        ('cesarea_sin_trabajo', 'Cesárea sin Trabajo de Parto'),
    ]
    inicio_trabajo_parto = models.CharField(
        max_length=30,
        choices=INICIO_TRABAJO_PARTO_CHOICES
    )
    
    # Clasificación de Robson (1-10)
    grupo_robson = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Clasificación OMS Robson (1-10)'
    )
    
    # === SECCIÓN 2: DATOS MATERNOS ===
    
    # Paridad
    primigesta = models.BooleanField(default=False)
    multigesta = models.BooleanField(default=False)
    
    # Cicatriz uterina previa
    cicatriz_uterina = models.BooleanField(
        default=False,
        help_text='Cesárea previa u otra cirugía uterina'
    )
    
    # Rotura de membranas
    ROTURA_MEMBRANAS_CHOICES = [
        ('espontanea', 'Espontánea'),
        ('artificial', 'Artificial'),
        ('integras', 'Íntegras'),
    ]
    rotura_membranas = models.CharField(
        max_length=20,
        choices=ROTURA_MEMBRANAS_CHOICES,
        blank=True
    )
    hora_rotura_membranas = models.TimeField(
        blank=True,
        null=True,
        help_text='Hora de rotura de membranas'
    )
    
    # Tiempos del trabajo de parto
    duracion_trabajo_parto_minutos = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(2880)],
        help_text='Duración total del trabajo de parto en minutos'
    )
    duracion_periodo_expulsivo_minutos = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(240)],
        help_text='Duración del periodo expulsivo en minutos'
    )
    hora_inicio_trabajo_parto = models.TimeField(
        blank=True,
        null=True,
        help_text='Hora de inicio del trabajo de parto'
    )
    
    # Líquido amniótico
    LIQUIDO_AMNIOTICO_CHOICES = [
        ('claro', 'Claro'),
        ('meconial', 'Meconial'),
        ('sanguinolento', 'Sanguinolento'),
    ]
    liquido_amniotico = models.CharField(
        max_length=20,
        choices=LIQUIDO_AMNIOTICO_CHOICES,
        blank=True
    )
    
    # Analgesia/Anestesia
    ANESTESIA_CHOICES = [
        ('ninguna', 'Ninguna'),
        ('epidural', 'Epidural'),
        ('raquidea', 'Raquídea'),
        ('general', 'General'),
    ]
    anestesia = models.CharField(
        max_length=20,
        choices=ANESTESIA_CHOICES,
        blank=True
    )
    
    # === SECCIÓN 3: COMPLICACIONES ===
    
    # Hemorragia postparto
    hemorragia_postparto = models.BooleanField(default=False)
    hemorragia_ml = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(5000)]
    )
    
    # Desgarro perineal
    DESGARRO_CHOICES = [
        ('ninguno', 'Ninguno'),
        ('grado_1', 'Grado I'),
        ('grado_2', 'Grado II'),
        ('grado_3', 'Grado III'),
        ('grado_4', 'Grado IV'),
    ]
    desgarro_perineal = models.CharField(
        max_length=20,
        choices=DESGARRO_CHOICES,
        default='ninguno'
    )
    
    # Episiotomía
    episiotomia = models.BooleanField(default=False)
    
    # Alumbramiento
    ALUMBRAMIENTO_CHOICES = [
        ('completo', 'Completo'),
        ('incompleto', 'Incompleto'),
        ('manual', 'Manual'),
        ('instrumental', 'Instrumental'),
    ]
    alumbramiento = models.CharField(
        max_length=20,
        choices=ALUMBRAMIENTO_CHOICES,
        default='completo'
    )
    
    # Placenta
    peso_placenta_gramos = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(200), MaxValueValidator(1500)],
        help_text='Peso de la placenta en gramos'
    )
    placenta_completa = models.BooleanField(
        default=True,
        help_text='Placenta completa sin retención'
    )
    
    # Complicaciones adicionales
    retencion_placentaria = models.BooleanField(default=False)
    desgarro_cervical = models.BooleanField(default=False)
    ruptura_uterina = models.BooleanField(default=False)
    inversion_uterina = models.BooleanField(default=False)
    
    # === SECCIÓN 4: INDICACIÓN CESÁREA (si aplica) ===
    
    INDICACION_CESAREA_CHOICES = [
        ('no_aplica', 'No Aplica'),
        ('sufrimiento_fetal', 'Sufrimiento Fetal'),
        ('desproporcion_cefalopelvica', 'Desproporción Cefalopélvica'),
        ('distocia_trabajo_parto', 'Distocia de Trabajo de Parto'),
        ('cesarea_previa', 'Cesárea Previa'),
        ('presentacion_anomala', 'Presentación Anómala'),
        ('placenta_previa', 'Placenta Previa'),
        ('desprendimiento_placenta', 'Desprendimiento de Placenta'),
        ('preeclampsia_severa', 'Preeclampsia Severa'),
        ('otra', 'Otra'),
    ]
    indicacion_cesarea = models.CharField(
        max_length=40,
        choices=INDICACION_CESAREA_CHOICES,
        default='no_aplica'
    )
    indicacion_cesarea_otra = models.TextField(
        blank=True,
        help_text='Descripción si indicación es "otra"'
    )
    
    # === SECCIÓN 5: LUGAR Y CONTEXTO ===
    
    LUGAR_ATENCION_CHOICES = [
        ('sala_parto', 'Sala de Parto'),
        ('pabellon', 'Pabellón Quirúrgico'),
        ('urgencia', 'Servicio de Urgencia'),
        ('domicilio', 'Domicilio'),
        ('traslado', 'Durante Traslado'),
    ]
    lugar_atencion = models.CharField(
        max_length=20,
        choices=LUGAR_ATENCION_CHOICES,
        default='sala_parto'
    )
    
    # Plan de parto
    tiene_plan_parto = models.BooleanField(
        default=False,
        help_text='¿Paciente tiene plan de parto?'
    )
    plan_parto_respetado = models.BooleanField(
        default=True,
        help_text='¿Se respetó el plan de parto?'
    )
    plan_parto_observaciones = models.TextField(blank=True)
    
    # Casos especiales
    parto_agua = models.BooleanField(
        default=False,
        help_text='Parto en agua'
    )
    parto_vertical = models.BooleanField(
        default=False,
        help_text='Parto en posición vertical'
    )
    
    # Violencia obstétrica / SAIP
    sospecha_violencia = models.BooleanField(
        default=False,
        help_text='Sospecha de violencia intrafamiliar'
    )
    derivacion_saip = models.BooleanField(
        default=False,
        help_text='Derivación a SAIP (Sistema Atención Integral Violencia)'
    )
    
    # Observaciones generales
    observaciones = models.TextField(blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'parto'
        verbose_name = 'Parto'
        verbose_name_plural = 'Partos'
        ordering = ['-fecha_parto', '-hora_parto']
        indexes = [
            models.Index(fields=['-fecha_parto'], name='idx_parto_fecha'),
            models.Index(fields=['grupo_robson'], name='idx_parto_robson'),
            models.Index(fields=['tipo_parto'], name='idx_parto_tipo'),
        ]
    
    def __str__(self):
        return f"Parto {self.paciente.nombre_completo} - {self.fecha_parto}"
    
    def calcular_grupo_robson(self):
        """
        Calcula automáticamente el grupo Robson (1-10) según algoritmo OMS.
        
        Grupos Robson:
        1: Nulíparas, único, cefálico, ≥37 sem, trabajo espontáneo
        2: Nulíparas, único, cefálico, ≥37 sem, inducido o cesárea antes trabajo
        3: Multíparas sin cicatriz, único, cefálico, ≥37 sem, espontáneo
        4: Multíparas sin cicatriz, único, cefálico, ≥37 sem, inducido o cesárea antes
        5: Multíparas con cicatriz, único, cefálico, ≥37 sem
        6: Nulíparas, podálica
        7: Multíparas, podálica (incluye cicatriz)
        8: Embarazos múltiples (incluye cicatriz)
        9: Transversa/oblicua (incluye cicatriz)
        10: Únicos, cefálicos, <37 sem (incluye cicatriz)
        """
        
        # Grupo 8: Embarazos múltiples
        if self.control_prenatal and self.control_prenatal.embarazo_gemelar:
            return 8
        
        # Grupo 9: Presentación transversa
        if self.presentacion == 'transversa':
            return 9
        
        # Grupo 10: Prematuros (<37 semanas)
        if self.edad_gestacional_semanas < 37:
            return 10
        
        # Grupos 6-7: Presentación podálica
        if self.presentacion == 'podalica':
            if self.primigesta:
                return 6
            else:
                return 7
        
        # Grupos 1-5: Presentación cefálica, ≥37 semanas
        if self.presentacion == 'cefalica' and self.edad_gestacional_semanas >= 37:
            # Grupo 5: Multíparas con cicatriz
            if self.multigesta and self.cicatriz_uterina:
                return 5
            
            # Grupos 1-2: Nulíparas
            if self.primigesta:
                if self.inicio_trabajo_parto == 'espontaneo':
                    return 1
                else:
                    return 2
            
            # Grupos 3-4: Multíparas sin cicatriz
            if self.multigesta and not self.cicatriz_uterina:
                if self.inicio_trabajo_parto == 'espontaneo':
                    return 3
                else:
                    return 4
        
        # Por defecto, retornar grupo 10 (casos no clasificados)
        return 10
    
    def save(self, *args, **kwargs):
        """Override save para calcular Robson automáticamente"""
        if not self.grupo_robson:
            self.grupo_robson = self.calcular_grupo_robson()
        super().save(*args, **kwargs)


class ComplicacionMaterna(models.Model):
    """
    Modelo para registrar complicaciones maternas durante el parto
    con códigos CIE-10 para reportabilidad.
    """
    
    parto = models.ForeignKey(
        Parto,
        on_delete=models.CASCADE,
        related_name='complicaciones_maternas'
    )
    
    # Código CIE-10
    codigo_cie10 = models.CharField(
        max_length=10,
        help_text='Código CIE-10 de la complicación'
    )
    
    descripcion_cie10 = models.CharField(
        max_length=500,
        help_text='Descripción según CIE-10'
    )
    
    # Tipo de complicación
    TIPO_COMPLICACION_CHOICES = [
        ('hemorragia', 'Hemorragia Postparto'),
        ('preeclampsia', 'Preeclampsia/Eclampsia'),
        ('sepsis', 'Sepsis Puerperal'),
        ('ruptura_uterina', 'Ruptura Uterina'),
        ('embolia', 'Embolia'),
        ('shock', 'Shock Hipovolemicó/Séptico'),
        ('desgarro_grave', 'Desgarro Grado III-IV'),
        ('otra', 'Otra Complicación'),
    ]
    tipo = models.CharField(
        max_length=30,
        choices=TIPO_COMPLICACION_CHOICES
    )
    
    # Severidad
    SEVERIDAD_CHOICES = [
        ('leve', 'Leve'),
        ('moderada', 'Moderada'),
        ('grave', 'Grave'),
        ('critica', 'Crítica'),
    ]
    severidad = models.CharField(
        max_length=20,
        choices=SEVERIDAD_CHOICES,
        default='leve'
    )
    
    # Tratamiento
    tratamiento_realizado = models.TextField(
        blank=True,
        help_text='Descripción del tratamiento realizado'
    )
    
    # Resolución
    requirio_uci = models.BooleanField(
        default=False,
        help_text='¿Requirió ingreso a UCI?'
    )
    
    requirio_transfusion = models.BooleanField(
        default=False,
        help_text='¿Requirió transfusión sanguínea?'
    )
    
    requirio_cirugia = models.BooleanField(
        default=False,
        help_text='¿Requirió cirugía adicional?'
    )
    
    # Observaciones
    observaciones = models.TextField(blank=True)
    
    # Usuario que registra
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'complicacion_materna'
        verbose_name = 'Complicación Materna'
        verbose_name_plural = 'Complicaciones Maternas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['parto', 'tipo'], name='idx_complicacion_parto_tipo'),
            models.Index(fields=['codigo_cie10'], name='idx_complicacion_cie10'),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.codigo_cie10} ({self.get_severidad_display()})"


class ProtocoloVIH(models.Model):
    """
    Modelo para protocolo automático VIH perinatal.
    Se activa automáticamente cuando se detecta VIH+ en exámenes.
    """
    
    parto = models.OneToOneField(
        Parto,
        on_delete=models.CASCADE,
        related_name='protocolo_vih',
        primary_key=True
    )
    
    # Activación
    activado = models.BooleanField(
        default=False,
        help_text='Protocolo activado automáticamente'
    )
    
    fecha_activacion = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha y hora de activación del protocolo'
    )
    
    # Tratamiento ARV madre
    arv_madre_durante_parto = models.BooleanField(
        default=False,
        help_text='ARV administrado a madre durante parto'
    )
    
    # Protocolo RN
    arv_rn_administrado = models.BooleanField(
        default=False,
        help_text='ARV administrado a RN (profilaxis)'
    )
    
    lactancia_suspendida = models.BooleanField(
        default=False,
        help_text='Lactancia materna suspendida (reemplazo fórmula)'
    )
    
    # Tipo de parto recomendado
    cesarea_electiva_recomendada = models.BooleanField(
        default=False,
        help_text='Cesárea electiva recomendada según carga viral'
    )
    
    carga_viral_materna = models.IntegerField(
        blank=True,
        null=True,
        help_text='Carga viral materna (copias/ml)'
    )
    
    # Notificaciones
    notificado_infectologia = models.BooleanField(
        default=False,
        help_text='Servicio de infectología notificado'
    )
    
    notificado_neonatologia = models.BooleanField(
        default=False,
        help_text='Neonatología notificada para seguimiento RN'
    )
    
    # Seguimiento
    seguimiento_programado = models.BooleanField(
        default=False,
        help_text='Seguimiento programado para RN (test PCR, serología)'
    )
    
    # Observaciones
    observaciones = models.TextField(blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'protocolo_vih'
        verbose_name = 'Protocolo VIH Perinatal'
        verbose_name_plural = 'Protocolos VIH Perinatales'
    
    def __str__(self):
        estado = "ACTIVO" if self.activado else "INACTIVO"
        return f"Protocolo VIH - Parto {self.parto.id} [{estado}]"
    
    def activar_protocolo(self):
        """
        Activa el protocolo VIH automáticamente.
        Llamado desde señal cuando se detecta VIH+.
        """
        if not self.activado:
            self.activado = True
            self.fecha_activacion = timezone.now()
            self.cesarea_electiva_recomendada = True
            self.lactancia_suspendida = True
            self.save()
            
            # Aquí se pueden agregar notificaciones automáticas
            # enviar_notificacion_urgente_vih(self.parto)
