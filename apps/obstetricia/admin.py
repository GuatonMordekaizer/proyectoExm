from django.contrib import admin
from .models import ControlPrenatal, ExamenPrenatal, Parto


@admin.register(ControlPrenatal)
class ControlPrenatalAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fur', 'edad_gestacional_semanas', 'num_controles_realizados', 'embarazo_gemelar')
    list_filter = ('embarazo_gemelar', 'hipertension', 'diabetes_gestacional', 'preeclampsia')
    search_fields = ('paciente__rut', 'paciente__nombre')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Paciente', {
            'fields': ('paciente',)
        }),
        ('Datos del Embarazo', {
            'fields': ('fur', 'fecha_primer_control', 'num_controles_realizados', 'embarazo_gemelar')
        }),
        ('Grupo Sanguíneo', {
            'fields': ('grupo_sanguineo', 'factor_rh')
        }),
        ('Exámenes de Laboratorio', {
            'fields': ('hemoglobina_g_dl', 'glicemia_mg_dl')
        }),
        ('Antecedentes Obstétricos', {
            'fields': ('num_gestas_previas', 'num_partos_previos', 'num_cesareas_previas', 'num_abortos_previos')
        }),
        ('Patologías', {
            'fields': ('hipertension', 'diabetes_gestacional', 'preeclampsia')
        }),
    )


@admin.register(ExamenPrenatal)
class ExamenPrenatalAdmin(admin.ModelAdmin):
    list_display = ('control_prenatal', 'tipo_examen', 'resultado', 'fecha_examen', 'es_critico')
    list_filter = ('tipo_examen', 'resultado', 'fecha_examen')
    search_fields = ('control_prenatal__paciente__nombre',)
    readonly_fields = ('created_at',)


@admin.register(Parto)
class PartoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_parto', 'tipo_parto', 'grupo_robson', 'presentacion', 'usuario_registro')
    list_filter = ('tipo_parto', 'grupo_robson', 'presentacion', 'fecha_parto')
    search_fields = ('paciente__rut', 'paciente__nombre')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Datos Generales', {
            'fields': ('paciente', 'control_prenatal', 'usuario_registro')
        }),
        ('Datos del Parto', {
            'fields': ('fecha_parto', 'hora_parto', 'edad_gestacional_semanas', 'edad_gestacional_dias',
                      'tipo_parto', 'presentacion', 'inicio_trabajo_parto', 'grupo_robson')
        }),
        ('Datos Maternos', {
            'fields': ('primigesta', 'multigesta', 'cicatriz_uterina', 'rotura_membranas',
                      'liquido_amniotico', 'anestesia')
        }),
        ('Complicaciones', {
            'fields': ('hemorragia_postparto', 'hemorragia_ml', 'desgarro_perineal', 'episiotomia')
        }),
        ('Cesárea', {
            'fields': ('indicacion_cesarea',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
    )
