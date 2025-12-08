from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from apps.pacientes.models import validar_rut


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado para el sistema.
    Extiende AbstractUser de Django con campos específicos del hospital.
    """
    
    # Validador de formato RUT
    rut_validator = RegexValidator(
        regex=r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$',
        message='Formato RUT inválido. Use: 12.345.678-9'
    )
    
    # RUT del usuario (único)
    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[rut_validator, validar_rut],
        help_text='RUT del profesional. Formato: 12.345.678-9'
    )
    
    # Roles del sistema (7 roles según documentación)
    ROL_CHOICES = [
        ('matrona', 'Matrona/Matrón'),
        ('medico_obstetra', 'Médico Gineco-Obstetra'),
        ('pediatra', 'Médico Pediatra Neonatología'),
        ('enfermera_neonatal', 'Enfermera/o Neonatal'),
        ('puericultura', 'Técnico/a de Puericultura'),
        ('administrativo', 'Administrativo/a de Servicio'),
        ('jefe_servicio', 'Jefe/a de Servicio de Obstetricia'),
    ]
    rol = models.CharField(
        max_length=30,
        choices=ROL_CHOICES,
        help_text='Rol del usuario en el sistema'
    )
    
    # Estado del usuario
    activo = models.BooleanField(
        default=True,
        help_text='Usuario activo en el sistema'
    )
    
    # Último acceso
    ultimo_acceso = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha y hora del último acceso al sistema'
    )
    
    # Intentos de login fallidos (para bloqueo de cuenta)
    intentos_fallidos = models.IntegerField(
        default=0,
        help_text='Número de intentos de login fallidos consecutivos'
    )
    
    # Cuenta bloqueada
    cuenta_bloqueada = models.BooleanField(
        default=False,
        help_text='Cuenta bloqueada por intentos fallidos'
    )
    
    # Contraseña temporal (requiere cambio en primer login)
    requiere_cambio_password = models.BooleanField(
        default=False,
        help_text='Usuario debe cambiar su contraseña en el próximo login'
    )
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['rol', 'last_name', 'first_name']
        indexes = [
            models.Index(fields=['rut'], name='idx_usuario_rut'),
            models.Index(fields=['rol'], name='idx_usuario_rol'),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()}) - {self.rut}"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        return self.get_full_name() or self.username
    
    def puede_registrar_parto(self):
        """Determina si el usuario puede registrar partos"""
        return self.rol in ['matrona', 'medico_obstetra']
    
    def puede_evaluar_rn(self):
        """Determina si el usuario puede evaluar recién nacidos"""
        return self.rol in ['pediatra', 'enfermera_neonatal']
    
    def puede_ver_datos_sensibles(self):
        """Determina si el usuario puede ver datos sensibles"""
        return self.rol in ['matrona', 'medico_obstetra', 'pediatra', 'jefe_servicio']
    
    def puede_generar_reportes(self):
        """Determina si el usuario puede generar reportes"""
        return self.rol in ['super_admin', 'jefe_servicio', 'administrativo']
    
    def puede_gestionar_usuarios(self):
        """Determina si el usuario puede gestionar otros usuarios"""
        return self.rol in ['super_admin', 'jefe_servicio']
    
    def registrar_acceso(self):
        """Registra el último acceso del usuario y resetea intentos fallidos"""
        from django.utils import timezone
        self.ultimo_acceso = timezone.now()
        self.intentos_fallidos = 0  # Resetear intentos fallidos al acceder exitosamente
        self.save(update_fields=['ultimo_acceso', 'intentos_fallidos'])
    
    def bloquear_cuenta(self):
        """Bloquea la cuenta del usuario"""
        self.cuenta_bloqueada = True
        self.activo = False
        self.save(update_fields=['cuenta_bloqueada', 'activo'])
    
    def desbloquear_cuenta(self):
        """Desbloquea la cuenta del usuario"""
        self.cuenta_bloqueada = False
        self.activo = True
        self.intentos_fallidos = 0
        self.save(update_fields=['cuenta_bloqueada', 'activo', 'intentos_fallidos'])


class Auditoria(models.Model):
    """
    Modelo para auditoría inmutable de acciones en el sistema.
    Cumple con Decreto 7/2023 (retención 5 años).
    """
    
    # Usuario que realiza la acción
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='acciones_auditoria'
    )
    
    # Tipo de acción
    ACCION_CHOICES = [
        ('login', 'Inicio de Sesión'),
        ('logout', 'Cierre de Sesión'),
        ('login_fallido', 'Intento de Login Fallido'),
        ('crear', 'Crear Registro'),
        ('editar', 'Editar Registro'),
        ('ver', 'Ver Registro'),
        ('eliminar', 'Eliminar Registro'),
        ('exportar', 'Exportar Datos'),
        ('imprimir', 'Imprimir Documento'),
    ]
    accion = models.CharField(max_length=30, choices=ACCION_CHOICES)
    
    # Modelo afectado
    modelo = models.CharField(
        max_length=100,
        blank=True,
        help_text='Nombre del modelo afectado (ej: Parto, RecienNacido)'
    )
    
    # ID del objeto afectado
    objeto_id = models.IntegerField(
        null=True,
        blank=True,
        help_text='ID del objeto afectado'
    )
    
    # Descripción de la acción
    descripcion = models.TextField(
        help_text='Descripción detallada de la acción realizada'
    )
    
    # IP del usuario
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text='Dirección IP desde donde se realizó la acción'
    )
    
    # User agent
    user_agent = models.TextField(
        blank=True,
        help_text='Navegador y sistema operativo del usuario'
    )
    
    # Datos antes del cambio (JSON)
    datos_anteriores = models.JSONField(
        null=True,
        blank=True,
        help_text='Estado anterior del objeto (para ediciones)'
    )
    
    # Datos después del cambio (JSON)
    datos_nuevos = models.JSONField(
        null=True,
        blank=True,
        help_text='Estado nuevo del objeto (para ediciones)'
    )
    
    # Timestamp (inmutable)
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora exacta de la acción'
    )
    
    class Meta:
        db_table = 'auditoria'
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp'], name='idx_auditoria_timestamp'),
            models.Index(fields=['usuario', '-timestamp'], name='idx_auditoria_usuario'),
            models.Index(fields=['accion'], name='idx_auditoria_accion'),
            models.Index(fields=['modelo', 'objeto_id'], name='idx_auditoria_objeto'),
        ]
        # Permisos personalizados
        permissions = [
            ('view_all_auditoria', 'Puede ver todos los registros de auditoría'),
        ]
    
    def __str__(self):
        return f"{self.usuario.nombre_completo} - {self.get_accion_display()} - {self.timestamp}"
    
    def save(self, *args, **kwargs):
        """
        Override save para hacer el modelo inmutable después de creación.
        No se permite editar ni eliminar registros de auditoría.
        """
        if self.pk is not None:
            raise Exception('Los registros de auditoría no pueden ser modificados')
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        Override delete para prevenir eliminación de registros.
        """
        raise Exception('Los registros de auditoría no pueden ser eliminados')
