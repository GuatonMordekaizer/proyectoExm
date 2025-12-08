from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Auditoria


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    """
    Admin personalizado para el modelo Usuario.
    Extiende UserAdmin de Django con campos personalizados.
    """
    
    list_display = ('username', 'rut', 'get_full_name', 'rol', 'activo', 'cuenta_bloqueada', 'ultimo_acceso')
    list_filter = ('rol', 'activo', 'cuenta_bloqueada', 'is_staff', 'is_superuser')
    search_fields = ('username', 'rut', 'first_name', 'last_name', 'email')
    readonly_fields = ('ultimo_acceso', 'intentos_fallidos', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('username', 'password', 'rut', 'first_name', 'last_name', 'email')
        }),
        ('Rol y Permisos', {
            'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Estado de la Cuenta', {
            'fields': ('activo', 'cuenta_bloqueada', 'intentos_fallidos', 'ultimo_acceso')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Información Básica', {
            'classes': ('wide',),
            'fields': ('username', 'rut', 'password1', 'password2', 'first_name', 'last_name', 'email')
        }),
        ('Rol', {
            'fields': ('rol',)
        }),
    )
    
    actions = ['desbloquear_cuentas']
    
    def desbloquear_cuentas(self, request, queryset):
        """Acción para desbloquear cuentas seleccionadas"""
        count = 0
        for usuario in queryset:
            if usuario.cuenta_bloqueada:
                usuario.desbloquear_cuenta()
                count += 1
        
        self.message_user(request, f'{count} cuenta(s) desbloqueada(s) exitosamente.')
    
    desbloquear_cuentas.short_description = 'Desbloquear cuentas seleccionadas'


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    """
    Admin para el modelo Auditoria.
    Solo lectura - no se pueden editar ni eliminar registros.
    """
    
    list_display = ('timestamp', 'usuario', 'accion', 'modelo', 'objeto_id', 'ip_address')
    list_filter = ('accion', 'modelo', 'timestamp')
    search_fields = ('usuario__username', 'usuario__rut', 'descripcion', 'ip_address')
    readonly_fields = ('usuario', 'accion', 'modelo', 'objeto_id', 'descripcion', 
                       'ip_address', 'user_agent', 'datos_anteriores', 'datos_nuevos', 'timestamp')
    
    # Deshabilitar edición y eliminación
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = (
        ('Información de la Acción', {
            'fields': ('timestamp', 'usuario', 'accion', 'descripcion')
        }),
        ('Objeto Afectado', {
            'fields': ('modelo', 'objeto_id')
        }),
        ('Información Técnica', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Cambios Realizados', {
            'fields': ('datos_anteriores', 'datos_nuevos'),
            'classes': ('collapse',)
        }),
    )
