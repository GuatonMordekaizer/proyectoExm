"""
Modelos para el sistema de alertas y notificaciones críticas
Hospital Herminda Martín
"""

from django.db import models
from django.utils import timezone
from apps.neonatologia.models import RecienNacido
from apps.obstetricia.models import Parto
from apps.pacientes.models import PacienteMadre
from apps.administracion.models import Usuario


class Alerta(models.Model):
    """
    Sistema de alertas para situaciones críticas que requieren atención inmediata
    """
    
    TIPO_ALERTA_CHOICES = [
        ('APGAR_CRITICO', 'APGAR Crítico (< 7)'),
        ('BAJO_PESO', 'Recién Nacido Bajo Peso (< 2500g)'),
        ('REANIMACION', 'Reanimación Requerida'),
        ('HEMORRAGIA', 'Hemorragia Materna'),
        ('PREECLAMPSIA', 'Pre-eclampsia/Eclampsia'),
        ('SUFRIMIENTO_FETAL', 'Sufrimiento Fetal'),
        ('CESAREA_EMERGENCIA', 'Cesárea de Emergencia'),
        ('UCI_NEONATAL', 'Derivación UCI Neonatal'),
        ('COMPLICACION_MADRE', 'Complicación Materna Grave'),
        ('COMPLICACION_RN', 'Complicación RN Grave'),
    ]
    
    NIVEL_URGENCIA_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]
    
    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('EN_ATENCION', 'En Atención'),
        ('RESUELTA', 'Resuelta'),
        ('DESCARTADA', 'Descartada'),
    ]
    
    # Información de la alerta
    tipo = models.CharField('Tipo de Alerta', max_length=30, choices=TIPO_ALERTA_CHOICES)
    nivel_urgencia = models.CharField('Nivel de Urgencia', max_length=10, choices=NIVEL_URGENCIA_CHOICES)
    estado = models.CharField('Estado', max_length=15, choices=ESTADO_CHOICES, default='ACTIVA')
    
    # Descripción
    titulo = models.CharField('Título', max_length=200)
    descripcion = models.TextField('Descripción')
    observaciones = models.TextField('Observaciones', blank=True)
    
    # Relaciones (opcional - puede ser de RN, Parto o Paciente)
    recien_nacido = models.ForeignKey(
        RecienNacido,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alertas'
    )
    parto = models.ForeignKey(
        Parto,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alertas'
    )
    paciente = models.ForeignKey(
        PacienteMadre,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alertas'
    )
    
    # Usuarios
    usuario_genera = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='alertas_generadas',
        verbose_name='Usuario que genera'
    )
    usuario_atiende = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alertas_atendidas',
        verbose_name='Usuario que atiende'
    )
    
    # Tiempos
    fecha_hora_alerta = models.DateTimeField('Fecha y Hora de Alerta', default=timezone.now)
    fecha_hora_atencion = models.DateTimeField('Fecha y Hora de Atención', null=True, blank=True)
    fecha_hora_resolucion = models.DateTimeField('Fecha y Hora de Resolución', null=True, blank=True)
    
    # Auditoría
    created_at = models.DateTimeField('Fecha Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha Actualización', auto_now=True)
    
    class Meta:
        db_table = 'alertas'
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-fecha_hora_alerta', '-nivel_urgencia']
        indexes = [
            models.Index(fields=['estado', '-fecha_hora_alerta']),
            models.Index(fields=['nivel_urgencia', 'estado']),
            models.Index(fields=['tipo', 'estado']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo} ({self.get_estado_display()})"
    
    @property
    def tiempo_sin_atencion(self):
        """Calcula el tiempo sin atención en minutos"""
        if self.estado == 'ACTIVA':
            delta = timezone.now() - self.fecha_hora_alerta
            return int(delta.total_seconds() / 60)
        return 0
    
    @property
    def es_critica(self):
        """Determina si la alerta es crítica"""
        return self.nivel_urgencia == 'CRITICA'
    
    @property
    def css_class(self):
        """Retorna la clase CSS según el nivel de urgencia"""
        return {
            'BAJA': 'info',
            'MEDIA': 'warning',
            'ALTA': 'danger',
            'CRITICA': 'danger',
        }.get(self.nivel_urgencia, 'secondary')
    
    def marcar_en_atencion(self, usuario):
        """Marca la alerta como en atención"""
        self.estado = 'EN_ATENCION'
        self.usuario_atiende = usuario
        self.fecha_hora_atencion = timezone.now()
        self.save()
    
    def marcar_resuelta(self, observaciones=''):
        """Marca la alerta como resuelta"""
        self.estado = 'RESUELTA'
        self.fecha_hora_resolucion = timezone.now()
        if observaciones:
            self.observaciones = observaciones
        self.save()
    
    @classmethod
    def crear_alerta_apgar_critico(cls, recien_nacido, usuario):
        """Crea una alerta automática por APGAR crítico"""
        if recien_nacido.apgar_5_min and recien_nacido.apgar_5_min < 7:
            return cls.objects.create(
                tipo='APGAR_CRITICO',
                nivel_urgencia='CRITICA',
                titulo=f'APGAR Crítico: {recien_nacido.apgar_5_min} puntos',
                descripcion=f'Recién nacido con APGAR a los 5 minutos de {recien_nacido.apgar_5_min} puntos. Requiere atención inmediata.',
                recien_nacido=recien_nacido,
                parto=recien_nacido.parto,
                paciente=recien_nacido.parto.paciente,
                usuario_genera=usuario,
            )
        return None
    
    @classmethod
    def crear_alerta_bajo_peso(cls, recien_nacido, usuario):
        """Crea una alerta por bajo peso al nacer"""
        if recien_nacido.peso_gramos and recien_nacido.peso_gramos < 2500:
            nivel = 'CRITICA' if recien_nacido.peso_gramos < 1500 else 'ALTA'
            return cls.objects.create(
                tipo='BAJO_PESO',
                nivel_urgencia=nivel,
                titulo=f'Bajo Peso al Nacer: {recien_nacido.peso_gramos}g',
                descripcion=f'Recién nacido con peso de {recien_nacido.peso_gramos}g. Requiere seguimiento especial.',
                recien_nacido=recien_nacido,
                parto=recien_nacido.parto,
                paciente=recien_nacido.parto.paciente,
                usuario_genera=usuario,
            )
        return None
    
    @classmethod
    def crear_alerta_reanimacion(cls, recien_nacido, usuario):
        """Crea una alerta por reanimación requerida"""
        if recien_nacido.reanimacion_requerida:
            return cls.objects.create(
                tipo='REANIMACION',
                nivel_urgencia='CRITICA',
                titulo='Reanimación Neonatal Requerida',
                descripcion='Recién nacido requirió maniobras de reanimación.',
                recien_nacido=recien_nacido,
                parto=recien_nacido.parto,
                paciente=recien_nacido.parto.paciente,
                usuario_genera=usuario,
            )
        return None
