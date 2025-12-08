from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from apps.obstetricia.models import Parto


class RecienNacido(models.Model):
    """
    Modelo para recién nacido.
    Relación 1:1 con Parto.
    Incluye APGAR, antropometría y datos vitales.
    """
    
    # Relación 1:1 con Parto
    parto = models.OneToOneField(
        Parto,
        on_delete=models.PROTECT,
        related_name='recien_nacido',
        primary_key=True
    )
    
    # === DATOS BÁSICOS ===
    
    SEXO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('intersexual', 'Intersexual'),
        ('no_determinado', 'No Determinado'),
    ]
    sexo = models.CharField(max_length=20, choices=SEXO_CHOICES)
    
    # === ANTROPOMETRÍA ===
    
    peso_gramos = models.IntegerField(
        validators=[MinValueValidator(400), MaxValueValidator(6000)],
        help_text='Peso al nacer en gramos'
    )
    
    talla_cm = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(30.0), MaxValueValidator(60.0)],
        help_text='Talla en centímetros'
    )
    
    circunferencia_craneana_cm = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(25.0), MaxValueValidator(45.0)],
        help_text='Circunferencia craneana en cm'
    )
    
    circunferencia_toracica_cm = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[MinValueValidator(20.0), MaxValueValidator(45.0)],
        help_text='Circunferencia torácica en cm'
    )
    
    circunferencia_abdominal_cm = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[MinValueValidator(20.0), MaxValueValidator(45.0)],
        help_text='Circunferencia abdominal en cm'
    )
    
    # === APGAR ===
    
    apgar_1_min = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text='APGAR al minuto 1'
    )
    
    apgar_5_min = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text='APGAR al minuto 5'
    )
    
    apgar_10_min = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text='APGAR al minuto 10 (si aplica)'
    )
    
    # === REANIMACIÓN ===
    
    reanimacion_requerida = models.BooleanField(default=False)
    
    TIPO_REANIMACION_CHOICES = [
        ('ninguna', 'Ninguna'),
        ('estimulacion', 'Estimulación Táctil'),
        ('oxigeno', 'Oxígeno'),
        ('vpp', 'Ventilación a Presión Positiva'),
        ('intubacion', 'Intubación'),
        ('masaje_cardiaco', 'Masaje Cardíaco'),
        ('adrenalina', 'Adrenalina'),
    ]
    tipo_reanimacion = models.CharField(
        max_length=30,
        choices=TIPO_REANIMACION_CHOICES,
        default='ninguna'
    )
    
    # === PROCEDIMIENTOS INMEDIATOS ===
    
    # Pinzamiento cordón
    tiempo_pinzamiento_cordon_segundos = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        help_text='Tiempo de pinzamiento del cordón en segundos'
    )
    
    # Apego precoz
    apego_piel_a_piel = models.BooleanField(
        default=False,
        help_text='Se realizó apego piel a piel'
    )
    tiempo_apego_minutos = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        help_text='Tiempo de apego piel a piel en minutos'
    )
    
    # Lactancia
    lactancia_inmediata = models.BooleanField(
        default=False,
        help_text='Lactancia materna inmediata en sala de parto'
    )
    hora_primera_lactancia = models.TimeField(
        blank=True,
        null=True,
        help_text='Hora de primera lactancia'
    )
    
    # Medicamentos
    vitamina_k_administrada = models.BooleanField(
        default=False,
        help_text='Vitamina K administrada'
    )
    hora_vitamina_k = models.TimeField(
        blank=True,
        null=True,
        help_text='Hora de administración de vitamina K'
    )
    
    vacuna_hepatitis_b = models.BooleanField(
        default=False,
        help_text='Vacuna Hepatitis B administrada'
    )
    hora_vacuna_hepatitis_b = models.TimeField(
        blank=True,
        null=True,
        help_text='Hora de administración de vacuna Hepatitis B'
    )
    
    # Profilaxis ocular
    profilaxis_ocular = models.BooleanField(
        default=False,
        help_text='Profilaxis ocular administrada (tetraciclina/eritromicina)'
    )
    
    # === DESTINO ===
    
    DESTINO_CHOICES = [
        ('alojamiento_conjunto', 'Alojamiento Conjunto'),
        ('neonatologia', 'Neonatología'),
        ('uci_neonatal', 'UCI Neonatal'),
        ('traslado', 'Traslado a Otro Centro'),
    ]
    destino = models.CharField(
        max_length=30,
        choices=DESTINO_CHOICES,
        default='alojamiento_conjunto'
    )
    motivo_traslado = models.TextField(
        blank=True,
        help_text='Motivo de traslado a otro centro o UCI'
    )
    
    # === ESTADO AL NACER ===
    
    ESTADO_CHOICES = [
        ('vivo', 'Vivo'),
        ('muerto', 'Muerto'),
        ('mortinato', 'Mortinato'),
    ]
    estado_al_nacer = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='vivo'
    )
    
    # Edad gestacional por Capurro
    edad_gestacional_capurro = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(24), MaxValueValidator(45)],
        help_text='Edad gestacional calculada por método Capurro'
    )
    
    # === MALFORMACIONES ===
    
    malformaciones = models.BooleanField(default=False)
    descripcion_malformaciones = models.TextField(blank=True)
    
    # === OBSERVACIONES ===
    
    observaciones = models.TextField(blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'recien_nacido'
        verbose_name = 'Recién Nacido'
        verbose_name_plural = 'Recién Nacidos'
        indexes = [
            # Índice para alertas APGAR crítico
            models.Index(
                fields=['apgar_5_min'],
                name='idx_rn_apgar5',
                condition=models.Q(apgar_5_min__lt=7)
            ),
            models.Index(fields=['destino'], name='idx_rn_destino'),
        ]
    
    def __str__(self):
        return f"RN de {self.parto.paciente.nombre_completo} - {self.parto.fecha_parto}"
    
    @property
    def clasificacion_peso(self):
        """Clasifica el peso del RN según estándares OMS"""
        if self.peso_gramos < 1500:
            return 'Muy Bajo Peso (<1500g)'
        elif self.peso_gramos < 2500:
            return 'Bajo Peso (1500-2499g)'
        elif self.peso_gramos <= 4000:
            return 'Peso Normal (2500-4000g)'
        else:
            return 'Macrosómico (>4000g)'
    
    @property
    def apgar_5_critico(self):
        """Determina si APGAR a los 5 min es crítico (<7)"""
        return self.apgar_5_min < 7
    
    @property
    def requiere_alerta_pediatra(self):
        """Determina si requiere alerta inmediata a pediatra"""
        return (
            self.apgar_5_critico or
            self.peso_gramos < 2500 or
            self.parto.edad_gestacional_semanas < 37 or
            self.malformaciones or
            self.reanimacion_requerida
        )
    
    def calcular_apgar_detallado(self, minuto):
        """
        Retorna desglose detallado del APGAR.
        Nota: Esto es un placeholder. En producción, se almacenarían
        los 5 componentes del APGAR por separado.
        """
        apgar_value = {
            1: self.apgar_1_min,
            5: self.apgar_5_min,
            10: self.apgar_10_min
        }.get(minuto, 0)
        
        if apgar_value >= 7:
            return 'APGAR Normal'
        elif apgar_value >= 4:
            return 'APGAR Moderadamente Anormal'
        else:
            return 'APGAR Severamente Anormal'


class APGARDetalle(models.Model):
    """
    Modelo para desglose detallado del APGAR (5 componentes).
    Permite cálculo automático y validación por componente.
    """
    
    recien_nacido = models.ForeignKey(
        RecienNacido,
        on_delete=models.CASCADE,
        related_name='apgar_detalles'
    )
    
    # Momento de evaluación
    MINUTO_CHOICES = [
        (1, '1 minuto'),
        (5, '5 minutos'),
        (10, '10 minutos'),
    ]
    minuto = models.IntegerField(choices=MINUTO_CHOICES)
    
    # Componentes APGAR (0-2 puntos cada uno)
    frecuencia_cardiaca = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text='0=Ausente, 1=<100 lpm, 2=>100 lpm'
    )
    
    esfuerzo_respiratorio = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text='0=Ausente, 1=Lento/irregular, 2=Bueno/llanto'
    )
    
    tono_muscular = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text='0=Flácido, 1=Flexión leve, 2=Movimiento activo'
    )
    
    irritabilidad_refleja = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text='0=Sin respuesta, 1=Mueca, 2=Llanto/tos'
    )
    
    color_piel = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text='0=Azul/pálido, 1=Cuerpo rosado/extremidades azules, 2=Rosado'
    )
    
    # Usuario que evalúa
    usuario_evaluador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        help_text='Profesional que realiza la evaluación'
    )
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'apgar_detalle'
        verbose_name = 'APGAR Detallado'
        verbose_name_plural = 'APGAR Detallados'
        ordering = ['minuto']
        unique_together = [['recien_nacido', 'minuto']]
        indexes = [
            models.Index(fields=['recien_nacido', 'minuto'], name='idx_apgar_rn_minuto'),
        ]
    
    def __str__(self):
        return f"APGAR {self.minuto}min - RN {self.recien_nacido.parto.paciente.nombre_completo} = {self.total}/10"
    
    @property
    def total(self):
        """Calcula el puntaje total del APGAR (suma de 5 componentes)"""
        return (
            self.frecuencia_cardiaca +
            self.esfuerzo_respiratorio +
            self.tono_muscular +
            self.irritabilidad_refleja +
            self.color_piel
        )
    
    @property
    def clasificacion(self):
        """Clasifica el APGAR según puntaje total"""
        total = self.total
        if total >= 7:
            return 'Normal'
        elif total >= 4:
            return 'Moderadamente Anormal'
        else:
            return 'Severamente Anormal - CRÍTICO'
    
    @property
    def requiere_alerta(self):
        """Determina si requiere alerta automática"""
        return self.total < 7
    
    def save(self, *args, **kwargs):
        """Override save para sincronizar con RecienNacido"""
        super().save(*args, **kwargs)
        
        # Actualizar campos en RecienNacido
        if self.minuto == 1:
            self.recien_nacido.apgar_1_min = self.total
            self.recien_nacido.save(update_fields=['apgar_1_min'])
        elif self.minuto == 5:
            self.recien_nacido.apgar_5_min = self.total
            self.recien_nacido.save(update_fields=['apgar_5_min'])
        elif self.minuto == 10:
            self.recien_nacido.apgar_10_min = self.total
            self.recien_nacido.save(update_fields=['apgar_10_min'])


class SeguimientoNeonatal(models.Model):
    """
    Modelo para seguimiento del recién nacido durante hospitalización.
    """
    
    recien_nacido = models.ForeignKey(
        RecienNacido,
        on_delete=models.CASCADE,
        related_name='seguimientos'
    )
    
    fecha_hora = models.DateTimeField()
    
    # Signos vitales
    temperatura_celsius = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(34.0), MaxValueValidator(40.0)]
    )
    
    frecuencia_cardiaca = models.IntegerField(
        validators=[MinValueValidator(60), MaxValueValidator(200)]
    )
    
    frecuencia_respiratoria = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(80)]
    )
    
    saturacion_oxigeno = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(70), MaxValueValidator(100)],
        help_text='Saturación de oxígeno en %'
    )
    
    # Alimentación
    TIPO_ALIMENTACION_CHOICES = [
        ('lactancia_materna', 'Lactancia Materna Exclusiva'),
        ('formula', 'Fórmula'),
        ('mixta', 'Mixta'),
        ('sonda', 'Sonda'),
        ('parenteral', 'Parenteral'),
    ]
    tipo_alimentacion = models.CharField(
        max_length=30,
        choices=TIPO_ALIMENTACION_CHOICES,
        blank=True
    )
    
    volumen_alimentacion_ml = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(200)],
        help_text='Volumen de alimentación en ml'
    )
    
    # Eliminaciones
    diuresis = models.BooleanField(
        default=False,
        help_text='Presenta diuresis'
    )
    numero_diuresis = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    
    deposiciones = models.BooleanField(
        default=False,
        help_text='Presenta deposiciones'
    )
    tipo_deposicion = models.CharField(
        max_length=50,
        blank=True,
        help_text='Tipo de deposición (meconio, transición, normal)'
    )
    
    # Observaciones
    observaciones = models.TextField(blank=True)
    
    # Usuario que registra
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    
    class Meta:
        db_table = 'seguimiento_neonatal'
        verbose_name = 'Seguimiento Neonatal'
        verbose_name_plural = 'Seguimientos Neonatales'
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"Seguimiento {self.recien_nacido} - {self.fecha_hora}"


class ComplicacionNeonatal(models.Model):
    """
    Modelo para registrar complicaciones neonatales
    con códigos CIE-10 para reportabilidad.
    """
    
    recien_nacido = models.ForeignKey(
        RecienNacido,
        on_delete=models.CASCADE,
        related_name='complicaciones_neonatales'
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
        ('distress_respiratorio', 'Síndrome Distress Respiratorio'),
        ('hipoglicemia', 'Hipoglicemia Neonatal'),
        ('ictericia', 'Ictericia/Hiperbilirrubinemia'),
        ('sepsis', 'Sepsis Neonatal'),
        ('asfixia', 'Asfixia Perinatal'),
        ('aspiracion_meconio', 'Aspiración de Meconio'),
        ('malformacion', 'Malformación Congénita'),
        ('prematurez', 'Complicación de Prematurez'),
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
        help_text='¿Requirió ingreso a UCI Neonatal?'
    )
    
    requirio_ventilacion = models.BooleanField(
        default=False,
        help_text='¿Requirió ventilación mecánica?'
    )
    
    requirio_fototerapia = models.BooleanField(
        default=False,
        help_text='¿Requirió fototerapia?'
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
        db_table = 'complicacion_neonatal'
        verbose_name = 'Complicación Neonatal'
        verbose_name_plural = 'Complicaciones Neonatales'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recien_nacido', 'tipo'], name='idx_complicacion_rn_tipo'),
            models.Index(fields=['codigo_cie10'], name='idx_complicacion_rn_cie10'),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.codigo_cie10} ({self.get_severidad_display()})"
