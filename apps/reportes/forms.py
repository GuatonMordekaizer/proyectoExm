from django import forms
from datetime import date, timedelta


class ReporteForm(forms.Form):
    """
    Formulario para seleccionar tipo de reporte y rango de fechas.
    """
    TIPO_REPORTE_CHOICES = [
        ('', '-- Seleccione un tipo de reporte --'),
        ('partos_periodo', 'Partos por Período'),
        ('partos_robson', 'Clasificación Robson'),
        ('cesarea_tasa', 'Tasa de Cesáreas'),
        ('neonatologia', 'Estadísticas Neonatales'),
        ('apgar_critico', 'Recién Nacidos APGAR Crítico'),
        ('bajo_peso', 'Recién Nacidos Bajo Peso'),
        ('alertas', 'Reporte de Alertas'),
        ('resumen_mensual', 'Resumen Mensual Completo'),
    ]
    
    tipo_reporte = forms.ChoiceField(
        choices=TIPO_REPORTE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    fecha_inicio = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        initial=lambda: date.today() - timedelta(days=30)
    )
    
    fecha_fin = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        initial=date.today
    )
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                raise forms.ValidationError('La fecha de inicio no puede ser mayor que la fecha de fin.')
            
            # Validar que no sea un rango muy grande (más de 1 año)
            if (fecha_fin - fecha_inicio).days > 365:
                raise forms.ValidationError('El rango de fechas no puede ser mayor a 1 año.')
        
        return cleaned_data
