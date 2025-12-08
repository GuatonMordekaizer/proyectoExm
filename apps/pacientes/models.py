from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


def validar_rut(rut):
    """
    Valida formato y dígito verificador de RUT chileno.
    Formato esperado: 12.345.678-9 o 12345678-9
    """
    # Remover puntos y guión
    rut_limpio = rut.replace('.', '').replace('-', '')
    
    if len(rut_limpio) < 2:
        raise ValidationError('RUT inválido')
    
    # Separar número y dígito verificador
    numero = rut_limpio[:-1]
    dv = rut_limpio[-1].upper()
    
    # Calcular dígito verificador
    suma = 0
    multiplo = 2
    
    for digito in reversed(numero):
        suma += int(digito) * multiplo
        multiplo += 1
        if multiplo == 8:
            multiplo = 2
    
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        dv_esperado = '0'
    elif dv_calculado == 10:
        dv_esperado = 'K'
    else:
        dv_esperado = str(dv_calculado)
    
    if dv != dv_esperado:
        raise ValidationError(f'RUT inválido. Dígito verificador incorrecto.')


class PacienteMadre(models.Model):
    """
    Modelo para pacientes madres del servicio de obstetricia.
    Almacena datos demográficos y de contacto.
    """
    
    # Validador de formato RUT
    rut_validator = RegexValidator(
        regex=r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$',
        message='Formato RUT inválido. Use: 12.345.678-9'
    )
    
    # Datos de identificación
    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[rut_validator, validar_rut],
        help_text='Formato: 12.345.678-9'
    )
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    
    # Estado civil
    ESTADO_CIVIL_CHOICES = [
        ('soltera', 'Soltera'),
        ('casada', 'Casada'),
        ('conviviente', 'Conviviente'),
        ('viuda', 'Viuda'),
        ('divorciada', 'Divorciada'),
    ]
    estado_civil = models.CharField(
        max_length=20,
        choices=ESTADO_CIVIL_CHOICES,
        blank=True
    )
    
    # Escolaridad
    ESCOLARIDAD_CHOICES = [
        ('basica_incompleta', 'Básica Incompleta'),
        ('basica_completa', 'Básica Completa'),
        ('media_incompleta', 'Media Incompleta'),
        ('media_completa', 'Media Completa'),
        ('tecnica', 'Técnica'),
        ('universitaria_incompleta', 'Universitaria Incompleta'),
        ('universitaria_completa', 'Universitaria Completa'),
    ]
    escolaridad = models.CharField(
        max_length=30,
        choices=ESCOLARIDAD_CHOICES,
        blank=True
    )
    
    # Pueblo originario
    pueblo_originario = models.BooleanField(
        default=False,
        help_text='¿Pertenece a algún pueblo originario?'
    )
    
    # Dirección
    direccion = models.TextField(blank=True)
    comuna = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    
    # Previsión
    PREVISION_CHOICES = [
        ('fonasa_A', 'FONASA A'),
        ('fonasa_B', 'FONASA B'),
        ('fonasa_C', 'FONASA C'),
        ('fonasa_D', 'FONASA D'),
        ('isapre', 'ISAPRE'),
        ('particular', 'Particular'),
    ]
    prevision = models.CharField(
        max_length=20,
        choices=PREVISION_CHOICES,
        blank=True
    )
    
    # Consultorio de origen
    consultorio_origen = models.CharField(
        max_length=200,
        blank=True,
        help_text='Consultorio APS de origen'
    )
    
    # Contacto
    telefono = models.CharField(max_length=20, blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'paciente_madre'
        verbose_name = 'Paciente Madre'
        verbose_name_plural = 'Pacientes Madres'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rut'], name='idx_paciente_rut'),
            models.Index(fields=['nombre', 'apellido_paterno'], name='idx_paciente_nombre'),
            models.Index(fields=['comuna'], name='idx_paciente_comuna'),
        ]
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} ({self.rut})"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo de la paciente"""
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    
    @property
    def edad(self):
        """Calcula la edad actual de la paciente"""
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    def clean(self):
        """Validaciones adicionales del modelo"""
        super().clean()
        
        # Validar edad razonable (10-60 años)
        if self.fecha_nacimiento:
            edad = self.edad
            if edad < 10 or edad > 60:
                raise ValidationError({
                    'fecha_nacimiento': 'La edad debe estar entre 10 y 60 años'
                })
