from django.contrib import admin
from .models import Alerta


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'nivel_urgencia', 'estado', 'paciente', 'recien_nacido', 
                    'fecha_hora_alerta', 'usuario_genera', 'tiempo_sin_atencion_display']
    list_filter = ['tipo', 'nivel_urgencia', 'estado', 'fecha_hora_alerta']
    search_fields = ['titulo', 'descripcion', 'paciente__nombre', 'paciente__apellido_paterno']
    readonly_fields = ['fecha_hora_alerta', 'fecha_hora_atencion', 'fecha_hora_resolucion', 
                       'tiempo_sin_atencion']
    
    fieldsets = (
        ('Información de la Alerta', {
            'fields': ('tipo', 'nivel_urgencia', 'estado', 'titulo', 'descripcion')
        }),
        ('Referencias', {
            'fields': ('recien_nacido', 'parto', 'paciente')
        }),
        ('Gestión', {
            'fields': ('usuario_genera', 'usuario_atiende', 'observaciones')
        }),
        ('Timestamps', {
            'fields': ('fecha_hora_alerta', 'fecha_hora_atencion', 'fecha_hora_resolucion'),
            'classes': ('collapse',)
        }),
    )
    
    def tiempo_sin_atencion_display(self, obj):
        if obj.estado == 'ACTIVA' and obj.tiempo_sin_atencion:
            return f"{obj.tiempo_sin_atencion} min"
        return "-"
    tiempo_sin_atencion_display.short_description = 'Tiempo sin atención'
