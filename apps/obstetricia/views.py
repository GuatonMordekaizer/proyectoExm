from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.administracion.decorators import puede_registrar_parto
from apps.pacientes.models import PacienteMadre
from .models import Parto
from .forms import PartoForm, ControlPrenatalForm

@login_required
@puede_registrar_parto
def registrar_parto(request, paciente_id):
    """
    Vista para registrar un nuevo parto.
    Requiere rol de matrona o médico obstetra.
    """
    paciente = get_object_or_404(PacienteMadre, pk=paciente_id)
    
    if request.method == 'POST':
        form = PartoForm(request.POST, paciente_id=paciente_id)
        if form.is_valid():
            parto = form.save(commit=False)
            parto.paciente = paciente
            parto.usuario_registro = request.user
            parto.save()
            
            messages.success(request, 'Parto registrado exitosamente.')
            # Redirigir al registro de recién nacido
            return redirect('registrar_recien_nacido', parto_id=parto.pk)
        else:
            # Mostrar errores si el formulario no es válido
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # Pre-fill fecha/hora with current time
        initial_data = {
            'fecha_parto': timezone.now().date(),
            'hora_parto': timezone.now().time().strftime('%H:%M')
        }
        form = PartoForm(initial=initial_data, paciente_id=paciente_id)
    
    return render(request, 'obstetricia/registrar_parto.html', {
        'form': form,
        'paciente': paciente
    })

@login_required
def detalle_parto(request, parto_id):
    """
    Vista de detalle de un parto.
    Accesible por todos los roles autenticados.
    """
    parto = get_object_or_404(Parto, pk=parto_id)
    return render(request, 'obstetricia/detalle_parto.html', {
        'parto': parto
    })
