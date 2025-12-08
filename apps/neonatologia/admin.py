from django.contrib import admin
from .models import RecienNacido, SeguimientoNeonatal


@admin.register(RecienNacido)
class RecienNacidoAdmin(admin.ModelAdmin):
    list_display = ('parto', 'sexo', 'peso_gramos', 'clasificacion_peso', 'apgar_1_min', 
                    'apgar_5_min', 'apgar_5_critico', 'destino')
    list_filter = ('sexo', 'destino', 'reanimacion_requerida', 'malformaciones')
    search_fields = ('parto__paciente__nombre', 'parto__paciente__rut')
    readonly_fields = ('created_at', 'updated_at', 'clasificacion_peso', 'apgar_5_critico', 
                       'requiere_alerta_pediatra')
    
    fieldsets = (
        ('Parto', {
            'fields': ('parto',)
        }),
        ('Datos Básicos', {
            'fields': ('sexo',)
        }),
        ('Antropometría', {
            'fields': ('peso_gramos', 'talla_cm', 'circunferencia_craneana_cm', 'clasificacion_peso')
        }),
        ('APGAR', {
            'fields': ('apgar_1_min', 'apgar_5_min', 'apgar_10_min', 'apgar_5_critico')
        }),
        ('Reanimación', {
            'fields': ('reanimacion_requerida', 'tipo_reanimacion')
        }),
        ('Destino', {
            'fields': ('destino',)
        }),
        ('Malformaciones', {
            'fields': ('malformaciones', 'descripcion_malformaciones')
        }),
        ('Alertas', {
            'fields': ('requiere_alerta_pediatra',),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
    )


@admin.register(SeguimientoNeonatal)
class SeguimientoNeonatalAdmin(admin.ModelAdmin):
    list_display = ('recien_nacido', 'fecha_hora', 'temperatura_celsius', 'frecuencia_cardiaca',
                    'frecuencia_respiratoria', 'tipo_alimentacion', 'usuario_registro')
    list_filter = ('tipo_alimentacion', 'fecha_hora')
    search_fields = ('recien_nacido__parto__paciente__nombre',)
    readonly_fields = ('fecha_hora',)
