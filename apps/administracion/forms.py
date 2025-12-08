from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    """
    Formulario para crear nuevos usuarios.
    """
    class Meta:
        model = Usuario
        fields = ('username', 'rut', 'first_name', 'last_name', 'email', 'rol')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

class UsuarioChangeForm(UserChangeForm):
    """
    Formulario para editar usuarios existentes.
    """
    password = None  # Excluir campo de contraseña
    
    class Meta:
        model = Usuario
        fields = ('username', 'rut', 'first_name', 'last_name', 'email', 'rol', 'activo', 'cuenta_bloqueada')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cuenta_bloqueada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
