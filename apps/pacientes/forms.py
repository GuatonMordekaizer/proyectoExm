from django import forms
from apps.pacientes.models import PacienteMadre


class BusquedaPacienteForm(forms.Form):
    """
    Formulario para búsqueda rápida de pacientes.
    Permite buscar por RUT o nombre.
    """
    query = forms.CharField(
        label='Buscar Paciente',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese RUT (12.345.678-9) o nombre del paciente',
            'autofocus': True
        })
    )
    
    def clean_query(self):
        query = self.cleaned_data.get('query')
        if query:
            query = query.strip()
        return query


class PacienteMadreForm(forms.ModelForm):
    """
    Formulario para crear/editar paciente madre.
    """
    class Meta:
        model = PacienteMadre
        fields = [
            'rut', 'nombre', 'apellido_paterno', 'apellido_materno',
            'fecha_nacimiento', 'estado_civil', 'escolaridad',
            'pueblo_originario', 'direccion', 'comuna', 'region',
            'prevision', 'consultorio_origen', 'telefono'
        ]
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12.345.678-9'
            }),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'escolaridad': forms.Select(attrs={'class': 'form-select'}),
            'pueblo_originario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'prevision': forms.Select(attrs={'class': 'form-select'}),
            'consultorio_origen': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
