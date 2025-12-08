from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.administracion.decorators import rol_requerido
from apps.obstetricia.models import Parto
from apps.reportes.models import Alerta
from .models import RecienNacido
from .forms import RecienNacidoForm

@login_required
@rol_requerido('matrona', 'medico_obstetra', 'pediatra', 'enfermera_neonatal')
def registrar_recien_nacido(request, parto_id):
    """
    Vista para registrar evaluación de recién nacido (APGAR).
    Puede ser registrado por matronas, médicos obstetras, pediatras o enfermeras neonatales.
    """
    parto = get_object_or_404(Parto, pk=parto_id)
    
    # Verificar si ya existe RN para este parto
    if hasattr(parto, 'recien_nacido'):
        messages.warning(request, 'Este parto ya tiene un recién nacido registrado.')
        return redirect('detalle_recien_nacido', pk=parto.recien_nacido.pk)
    
    if request.method == 'POST':
        form = RecienNacidoForm(request.POST)
        if form.is_valid():
            rn = form.save(commit=False)
            rn.parto = parto
            rn.save()
            
            # Crear alertas automáticas según condiciones críticas
            alertas_creadas = []
            
            # Alerta por APGAR crítico
            alerta_apgar = Alerta.crear_alerta_apgar_critico(rn, request.user)
            if alerta_apgar:
                alertas_creadas.append('APGAR crítico')
            
            # Alerta por bajo peso
            alerta_peso = Alerta.crear_alerta_bajo_peso(rn, request.user)
            if alerta_peso:
                alertas_creadas.append('Bajo peso')
            
            # Alerta si requirió reanimación
            alerta_reanimacion = Alerta.crear_alerta_reanimacion(rn, request.user)
            if alerta_reanimacion:
                alertas_creadas.append('Reanimación')
            
            # Mostrar mensaje según alertas creadas
            if alertas_creadas:
                messages.warning(
                    request, 
                    f'¡ALERTA! Recién Nacido registrado con condiciones críticas: {", ".join(alertas_creadas)}. '
                    f'Se han generado alertas automáticas para atención prioritaria.'
                )
            else:
                messages.success(request, 'Recién Nacido registrado exitosamente.')
                
            return redirect('detalle_recien_nacido', pk=rn.pk)
    else:
        form = RecienNacidoForm()
    
    return render(request, 'neonatologia/registrar_rn.html', {
        'form': form,
        'parto': parto
    })

@login_required
@rol_requerido('matrona', 'medico_obstetra', 'pediatra', 'enfermera_neonatal', 'jefe_servicio')
def detalle_recien_nacido(request, pk):
    """
    Vista de detalle de un recién nacido.
    Accesible por personal clínico y jefe de servicio.
    """
    rn = get_object_or_404(RecienNacido, pk=pk)
    return render(request, 'neonatologia/detalle_rn.html', {
        'rn': rn
    })
