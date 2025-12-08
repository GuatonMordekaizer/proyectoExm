from django import forms
from .models import RecienNacido, SeguimientoNeonatal

class RecienNacidoForm(forms.ModelForm):
    """
    Formulario para evaluación de recién nacido (APGAR, antropometría).
    """
    class Meta:
        model = RecienNacido
        exclude = ['parto', 'created_at', 'updated_at', 'usuario_registro'] # usuario_registro is in Seguimiento, not RecienNacido directly? Wait, let me check model.
        # RecienNacido model does NOT have usuario_registro directly, it's linked to Parto which has it.
        # But wait, RecienNacido might need one? 
        # Checking model from step 189: RecienNacido has 'parto', 'sexo', 'peso...', 'apgar...', 'reanimacion...', 'destino...', 'malformaciones...', 'observaciones'.
        # It does NOT have usuario_registro. Parto has it. SeguimientoNeonatal has it.
        
        widgets = {
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'peso_gramos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'g'}),
            'talla_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'cm'}),
            'circunferencia_craneana_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'cm'}),
            'apgar_1_min': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
            'apgar_5_min': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
            'apgar_10_min': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
            'tipo_reanimacion': forms.Select(attrs={'class': 'form-select'}),
            'destino': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_malformaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'reanimacion_requerida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'malformaciones': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'apgar_1_min': 'APGAR 1 min',
            'apgar_5_min': 'APGAR 5 min',
            'apgar_10_min': 'APGAR 10 min',
        }

class SeguimientoNeonatalForm(forms.ModelForm):
    class Meta:
        model = SeguimientoNeonatal
        exclude = ['recien_nacido', 'usuario_registro'] # Set in view
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'temperatura_celsius': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'frecuencia_cardiaca': forms.NumberInput(attrs={'class': 'form-control'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_alimentacion': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
