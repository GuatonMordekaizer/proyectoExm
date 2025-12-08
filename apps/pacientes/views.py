from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from apps.administracion.decorators import rol_requerido
from .models import PacienteMadre
from .forms import BusquedaPacienteForm, PacienteMadreForm


@login_required
@rol_requerido('matrona', 'medico_obstetra', 'pediatra', 'enfermera_neonatal', 'puericultura', 'administrativo', 'jefe_servicio')
def buscar_paciente(request):
    """
    Vista para búsqueda de pacientes por RUT, nombre o fecha.
    Muestra los últimos 10 registros por defecto con paginación.
    """
    from django.core.paginator import Paginator
    from datetime import datetime
    
    form = BusquedaPacienteForm(request.GET or None)
    pacientes_list = None
    mostrar_resultados = False
    
    # Filtros
    query = request.GET.get('query', '').strip()
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    
    if query or fecha_desde or fecha_hasta:
        mostrar_resultados = True
        pacientes_list = PacienteMadre.objects.all()
        
        # Filtro por búsqueda de texto (RUT o nombre)
        if query:
            pacientes_list = pacientes_list.filter(
                Q(rut__icontains=query) |
                Q(nombre__icontains=query) |
                Q(apellido_paterno__icontains=query) |
                Q(apellido_materno__icontains=query)
            )
        
        # Filtro por fecha de registro
        if fecha_desde:
            try:
                fecha_desde_obj = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                pacientes_list = pacientes_list.filter(created_at__date__gte=fecha_desde_obj)
            except ValueError:
                messages.error(request, 'Formato de fecha inválido.')
        
        if fecha_hasta:
            try:
                fecha_hasta_obj = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                pacientes_list = pacientes_list.filter(created_at__date__lte=fecha_hasta_obj)
            except ValueError:
                messages.error(request, 'Formato de fecha inválido.')
        
        pacientes_list = pacientes_list.order_by('-created_at')
        
        if not pacientes_list.exists():
            messages.info(request, 'No se encontraron pacientes con los criterios especificados.')
    else:
        # Mostrar últimos 10 registros por defecto
        pacientes_list = PacienteMadre.objects.all().order_by('-created_at')[:10]
        mostrar_resultados = True
    
    # Paginación
    paginator = Paginator(pacientes_list, 10)  # 10 pacientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pacientes/buscar.html', {
        'form': form,
        'page_obj': page_obj,
        'mostrar_resultados': mostrar_resultados,
        'query': query,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    })


@login_required
@rol_requerido('matrona', 'medico_obstetra', 'pediatra', 'enfermera_neonatal', 'puericultura', 'administrativo', 'jefe_servicio')
def detalle_paciente(request, paciente_id):
    """
    Vista de detalle de un paciente.
    """
    paciente = get_object_or_404(PacienteMadre, pk=paciente_id)
    
    # Obtener partos con sus recién nacidos (relación OneToOne)
    partos = paciente.partos.select_related('recien_nacido').order_by('-fecha_parto')
    
    return render(request, 'pacientes/detalle.html', {
        'paciente': paciente,
        'partos': partos,
    })


@login_required
@rol_requerido('matrona', 'medico_obstetra', 'administrativo')
def crear_paciente(request):
    """
    Vista para crear un nuevo paciente.
    Solo matronas, médicos obstetras y administrativos pueden crear pacientes.
    """
    if request.method == 'POST':
        form = PacienteMadreForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f'Paciente {paciente.nombre_completo} creada exitosamente.')
            return redirect('detalle_paciente', paciente_id=paciente.pk)
    else:
        form = PacienteMadreForm()
    
    return render(request, 'pacientes/crear.html', {
        'form': form,
    })
