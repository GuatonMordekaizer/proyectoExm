from django import forms
from .models import Parto, ControlPrenatal

class PartoForm(forms.ModelForm):
    """
    Formulario para registro de parto.
    Maneja los 99 campos requeridos con widgets apropiados.
    """
    class Meta:
        model = Parto
        exclude = ['paciente', 'usuario_registro', 'grupo_robson', 'created_at', 'updated_at']
        widgets = {
            'alumbramiento': forms.Select(attrs={'class': 'form-select'}),
            'lugar_atencion': forms.Select(attrs={'class': 'form-select'}),
            'fecha_parto': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_parto': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'edad_gestacional_semanas': forms.NumberInput(attrs={'class': 'form-control', 'min': 20, 'max': 45}),
            'edad_gestacional_dias': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 6}),
            'tipo_parto': forms.Select(attrs={'class': 'form-select'}),
            'presentacion': forms.Select(attrs={'class': 'form-select'}),
            'inicio_trabajo_parto': forms.Select(attrs={'class': 'form-select'}),
            'rotura_membranas': forms.Select(attrs={'class': 'form-select'}),
            'liquido_amniotico': forms.Select(attrs={'class': 'form-select'}),
            'anestesia': forms.Select(attrs={'class': 'form-select'}),
            'hemorragia_ml': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ml'}),
            'desgarro_perineal': forms.Select(attrs={'class': 'form-select'}),
            'indicacion_cesarea': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # Checkboxes with custom classes if needed, or rely on crispy/bootstrap
            'primigesta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'multigesta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cicatriz_uterina': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hemorragia_postparto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'episiotomia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'hemorragia_ml': 'Volumen Hemorragia (ml)',
            'edad_gestacional_semanas': 'Edad Gestacional (Semanas)',
            'edad_gestacional_dias': 'Edad Gestacional (Días)',
        }

    def __init__(self, *args, **kwargs):
        paciente_id = kwargs.pop('paciente_id', None)
        super().__init__(*args, **kwargs)
        
        if paciente_id:
            # Filtrar controles prenatales por paciente
            self.fields['control_prenatal'].queryset = ControlPrenatal.objects.filter(
                paciente_id=paciente_id
            ).order_by('-fecha_primer_control')
            self.fields['control_prenatal'].empty_label = "Sin control prenatal registrado"
            self.fields['control_prenatal'].widget.attrs.update({'class': 'form-select'})
            
            # Set paciente field as hidden if we are handling it in the view
            # But the model needs it. We can set it in the instance before saving in the view.
            # Or include it as hidden field.
            # For now, we'll exclude 'paciente' from the form fields in the view logic usually, 
            # but here I excluded 'usuario_registro' etc. 
            # I should probably exclude 'paciente' too if it's passed via URL.
            pass

class ControlPrenatalForm(forms.ModelForm):
    class Meta:
        model = ControlPrenatal
        exclude = ['paciente', 'created_at', 'updated_at']
        widgets = {
            'fur': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_primer_control': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'num_controles_realizados': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo_sanguineo': forms.Select(attrs={'class': 'form-select'}),
            'factor_rh': forms.Select(attrs={'class': 'form-select'}),
            'hemoglobina_g_dl': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'glicemia_mg_dl': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'num_gestas_previas': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_partos_previos': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_cesareas_previas': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_abortos_previos': forms.NumberInput(attrs={'class': 'form-control'}),
            'embarazo_gemelar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hipertension': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diabetes_gestacional': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'preeclampsia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
