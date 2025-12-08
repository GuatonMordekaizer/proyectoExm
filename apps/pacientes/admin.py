from django.contrib import admin
from .models import PacienteMadre


@admin.register(PacienteMadre)
class PacienteMadreAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre_completo', 'fecha_nacimiento', 'edad', 'prevision', 'created_at')
    list_filter = ('estado_civil', 'prevision', 'pueblo_originario')
    search_fields = ('rut', 'nombre', 'apellido_paterno', 'apellido_materno')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Identificación', {
            'fields': ('rut', 'nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento')
        }),
        ('Datos Demográficos', {
            'fields': ('estado_civil', 'escolaridad', 'pueblo_originario')
        }),
        ('Dirección', {
            'fields': ('direccion', 'comuna', 'region')
        }),
        ('Previsión y Salud', {
            'fields': ('prevision', 'consultorio_origen')
        }),
        ('Contacto', {
            'fields': ('telefono',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
