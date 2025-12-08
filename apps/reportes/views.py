from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count, Avg
from datetime import datetime, timedelta, date
from apps.administracion.decorators import rol_requerido
from apps.obstetricia.models import Parto
from apps.neonatologia.models import RecienNacido
from apps.pacientes.models import PacienteMadre
from .models import Alerta
from .forms import ReporteForm


@login_required
@rol_requerido('matrona', 'medico_obstetra', 'pediatra', 'jefe_servicio')
def generar_pdf_parto(request, parto_id):
    """
    Genera un PDF con la ficha clínica del parto y recién nacido.
    """
    parto = get_object_or_404(Parto, pk=parto_id)
    
    template_path = 'reportes/ficha_clinica_pdf.html'
    context = {
        'parto': parto,
        'paciente': parto.paciente,
        'rn': getattr(parto, 'recien_nacido', None),
        'user': request.user,
    }
    
    # Renderizar template
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ficha_clinica_{parto.id}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    # Crear PDF
    pisa_status = pisa.CreatePDF(
       html, dest=response
    )
    
    if pisa_status.err:
       return HttpResponse('Error al generar PDF <pre>' + html + '</pre>')
       
    return response


@login_required
def listado_alertas(request):
    """
    Vista principal del sistema de alertas.
    Muestra alertas activas, en atención y resueltas.
    """
    # Filtros
    estado_filtro = request.GET.get('estado', 'ACTIVA')
    tipo_filtro = request.GET.get('tipo', '')
    nivel_filtro = request.GET.get('nivel', '')
    
    # Query base
    alertas = Alerta.objects.select_related(
        'recien_nacido', 'parto', 'paciente', 'usuario_genera', 'usuario_atiende'
    )
    
    # Aplicar filtros
    if estado_filtro:
        alertas = alertas.filter(estado=estado_filtro)
    if tipo_filtro:
        alertas = alertas.filter(tipo=tipo_filtro)
    if nivel_filtro:
        alertas = alertas.filter(nivel_urgencia=nivel_filtro)
    
    # Ordenar por urgencia y fecha
    alertas = alertas.order_by('-nivel_urgencia', '-fecha_hora_alerta')
    
    # Estadísticas
    stats = {
        'activas': Alerta.objects.filter(estado='ACTIVA').count(),
        'en_atencion': Alerta.objects.filter(estado='EN_ATENCION').count(),
        'criticas': Alerta.objects.filter(
            estado__in=['ACTIVA', 'EN_ATENCION'],
            nivel_urgencia='CRITICA'
        ).count(),
        'hoy': Alerta.objects.filter(
            fecha_hora_alerta__date=timezone.now().date()
        ).count(),
    }
    
    context = {
        'alertas': alertas[:50],  # Limitar a 50 resultados
        'stats': stats,
        'estado_filtro': estado_filtro,
        'tipo_filtro': tipo_filtro,
        'nivel_filtro': nivel_filtro,
        'tipos_alerta': Alerta.TIPO_ALERTA_CHOICES,
        'niveles_urgencia': Alerta.NIVEL_URGENCIA_CHOICES,
        'estados': Alerta.ESTADO_CHOICES,
    }
    
    return render(request, 'reportes/alertas.html', context)


@login_required
def detalle_alerta(request, alerta_id):
    """
    Vista detallada de una alerta específica.
    """
    alerta = get_object_or_404(Alerta, pk=alerta_id)
    
    context = {
        'alerta': alerta,
    }
    
    return render(request, 'reportes/detalle_alerta.html', context)


@login_required
def atender_alerta(request, alerta_id):
    """
    Marca una alerta como 'En Atención'.
    """
    alerta = get_object_or_404(Alerta, pk=alerta_id)
    
    if alerta.estado == 'ACTIVA':
        alerta.marcar_en_atencion(request.user)
        messages.success(request, f'Alerta marcada como "En Atención"')
    else:
        messages.warning(request, 'La alerta ya fue atendida o resuelta')
    
    return redirect('detalle_alerta', alerta_id=alerta.id)


@login_required
def resolver_alerta(request, alerta_id):
    """
    Marca una alerta como resuelta con observaciones.
    """
    alerta = get_object_or_404(Alerta, pk=alerta_id)
    
    if request.method == 'POST':
        observaciones = request.POST.get('observaciones', '')
        
        if alerta.estado in ['ACTIVA', 'EN_ATENCION']:
            if alerta.estado == 'ACTIVA':
                alerta.marcar_en_atencion(request.user)
            alerta.marcar_resuelta(observaciones)
            messages.success(request, 'Alerta resuelta exitosamente')
        else:
            messages.warning(request, 'La alerta ya está resuelta')
        
        return redirect('listado_alertas')
    
    return redirect('detalle_alerta', alerta_id=alerta.id)


@login_required
def dashboard_alertas(request):
    """
    Dashboard con métricas y gráficos de alertas.
    """
    # Rango de fechas (últimos 7 días)
    hoy = timezone.now().date()
    hace_7_dias = hoy - timedelta(days=7)
    
    # Alertas por tipo
    alertas_por_tipo = Alerta.objects.filter(
        fecha_hora_alerta__date__gte=hace_7_dias
    ).values('tipo').annotate(total=Count('id')).order_by('-total')
    
    # Alertas por día
    alertas_por_dia = Alerta.objects.filter(
        fecha_hora_alerta__date__gte=hace_7_dias
    ).extra(
        select={'dia': 'DATE(fecha_hora_alerta)'}
    ).values('dia').annotate(total=Count('id')).order_by('dia')
    
    # Alertas críticas activas
    alertas_criticas = Alerta.objects.filter(
        estado__in=['ACTIVA', 'EN_ATENCION'],
        nivel_urgencia='CRITICA'
    ).select_related('recien_nacido', 'parto', 'paciente')[:10]
    
    # Tiempo promedio de resolución (últimas 20 alertas resueltas)
    alertas_resueltas = Alerta.objects.filter(
        estado='RESUELTA',
        fecha_hora_resolucion__isnull=False
    ).order_by('-fecha_hora_resolucion')[:20]
    
    tiempos_resolucion = []
    for alerta in alertas_resueltas:
        delta = alerta.fecha_hora_resolucion - alerta.fecha_hora_alerta
        minutos = int(delta.total_seconds() / 60)
        tiempos_resolucion.append(minutos)
    
    tiempo_promedio = sum(tiempos_resolucion) / len(tiempos_resolucion) if tiempos_resolucion else 0
    
    context = {
        'alertas_por_tipo': alertas_por_tipo,
        'alertas_por_dia': alertas_por_dia,
        'alertas_criticas': alertas_criticas,
        'tiempo_promedio_resolucion': round(tiempo_promedio, 1),
    }
    
    return render(request, 'reportes/dashboard_alertas.html', context)


@login_required
def api_alertas_activas(request):
    """
    API JSON para obtener alertas activas (para notificaciones en tiempo real).
    """
    alertas = Alerta.objects.filter(
        estado='ACTIVA'
    ).values(
        'id', 'tipo', 'nivel_urgencia', 'titulo', 
        'descripcion', 'fecha_hora_alerta'
    ).order_by('-nivel_urgencia', '-fecha_hora_alerta')[:10]
    
    return JsonResponse({
        'alertas': list(alertas),
        'total': Alerta.objects.filter(estado='ACTIVA').count(),
        'criticas': Alerta.objects.filter(
            estado='ACTIVA', 
            nivel_urgencia='CRITICA'
        ).count(),
    })


@login_required
@rol_requerido('jefe_servicio', 'medico_obstetra')
def seleccionar_reporte(request):
    """
    Vista para seleccionar el tipo de reporte a generar.
    """
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            tipo_reporte = form.cleaned_data['tipo_reporte']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            
            # Redirigir a la vista de generación del PDF
            return redirect('generar_reporte_pdf', 
                          tipo=tipo_reporte, 
                          fecha_inicio=fecha_inicio.strftime('%Y-%m-%d'),
                          fecha_fin=fecha_fin.strftime('%Y-%m-%d'))
    else:
        form = ReporteForm()
    
    return render(request, 'reportes/seleccionar_reporte.html', {
        'form': form
    })


@login_required
@rol_requerido('jefe_servicio', 'medico_obstetra')
def generar_reporte_pdf(request, tipo, fecha_inicio, fecha_fin):
    """
    Genera un PDF con el reporte seleccionado.
    """
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    
    # Obtener datos según el tipo de reporte
    context = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'fecha_generacion': datetime.now(),
        'usuario': request.user,
    }
    
    if tipo == 'partos_periodo':
        context.update(_get_partos_periodo_data(fecha_inicio, fecha_fin))
        template_name = 'reportes/pdf/partos_periodo.html'
        filename = f'Reporte_Partos_{fecha_inicio}_{fecha_fin}.pdf'
        
    elif tipo == 'partos_robson':
        context.update(_get_robson_data(fecha_inicio, fecha_fin))
        template_name = 'reportes/pdf/partos_robson.html'
        filename = f'Reporte_Robson_{fecha_inicio}_{fecha_fin}.pdf'
        
    elif tipo == 'cesarea_tasa':
        context.update(_get_cesarea_data(fecha_inicio, fecha_fin))
        template_name = 'reportes/pdf/cesarea_tasa.html'
        filename = f'Reporte_Cesareas_{fecha_inicio}_{fecha_fin}.pdf'
        
    elif tipo == 'neonatologia':
        context.update(_get_neonatologia_data(fecha_inicio, fecha_fin))
        template_name = 'reportes/pdf/neonatologia.html'
        filename = f'Reporte_Neonatologia_{fecha_inicio}_{fecha_fin}.pdf'
        
    elif tipo == 'apgar_critico':
        context.update(_get_apgar_critico_data(fecha_inicio, fecha_fin))
        template_name = 'reportes/pdf/apgar_critico.html'
        filename = f'Reporte_APGAR_Critico_{fecha_inicio}_{fecha_fin}.pdf'
        
    elif tipo == 'bajo_peso':
        context.update(_get_bajo_peso_data(fecha_inicio, fecha_fin))
        template_name = 'reportes/pdf/bajo_peso.html'
        filename = f'Reporte_Bajo_Peso_{fecha_inicio}_{fecha_fin}.pdf'
        
    elif tipo == 'alertas':
        context.update(_get_alertas_data(fecha_inicio, fecha_fin))
        template_name = 'reportes/pdf/alertas.html'
        filename = f'Reporte_Alertas_{fecha_inicio}_{fecha_fin}.pdf'
        
    elif tipo == 'resumen_mensual':
        context.update(_get_resumen_mensual_data(fecha_inicio, fecha_fin))
        template_name = 'reportes/pdf/resumen_mensual.html'
        filename = f'Resumen_Mensual_{fecha_inicio}_{fecha_fin}.pdf'
    else:
        messages.error(request, 'Tipo de reporte no válido.')
        return redirect('seleccionar_reporte')
    
    # Generar PDF
    template = get_template(template_name)
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    
    return response


# Funciones auxiliares para obtener datos de cada reporte

def _get_partos_periodo_data(fecha_inicio, fecha_fin):
    """Obtiene datos de partos por período."""
    partos = Parto.objects.filter(
        fecha_parto__range=[fecha_inicio, fecha_fin]
    ).select_related('paciente', 'usuario_registro')
    
    total_partos = partos.count()
    partos_vaginales = partos.filter(tipo_parto='vaginal').count()
    cesareas = partos.filter(tipo_parto__in=['cesarea_electiva', 'cesarea_urgencia']).count()
    
    return {
        'partos': partos,
        'total_partos': total_partos,
        'partos_vaginales': partos_vaginales,
        'cesareas': cesareas,
        'tasa_cesarea': round((cesareas / total_partos * 100), 2) if total_partos > 0 else 0,
        'porcentaje_vaginales': round((partos_vaginales / total_partos * 100), 2) if total_partos > 0 else 0,
    }


def _get_robson_data(fecha_inicio, fecha_fin):
    """Obtiene datos de clasificación Robson."""
    partos = Parto.objects.filter(fecha_parto__range=[fecha_inicio, fecha_fin])
    
    # Agrupar por grupo Robson
    robson_grupos = partos.values('grupo_robson').annotate(
        total=Count('id'),
        cesareas=Count('id', filter=Q(tipo_parto__in=['cesarea_electiva', 'cesarea_urgencia']))
    ).order_by('grupo_robson')
    
    # Calcular porcentajes
    total_partos = partos.count()
    for grupo in robson_grupos:
        grupo['porcentaje'] = round((grupo['total'] / total_partos * 100), 2) if total_partos > 0 else 0
        grupo['tasa_cesarea'] = round((grupo['cesareas'] / grupo['total'] * 100), 2) if grupo['total'] > 0 else 0
    
    return {
        'robson_grupos': robson_grupos,
        'total_partos': total_partos,
    }


def _get_cesarea_data(fecha_inicio, fecha_fin):
    """Obtiene datos de tasa de cesáreas."""
    partos = Parto.objects.filter(fecha_parto__range=[fecha_inicio, fecha_fin])
    
    total_partos = partos.count()
    cesareas_electiva = partos.filter(tipo_parto='cesarea_electiva').count()
    cesareas_urgencia = partos.filter(tipo_parto='cesarea_urgencia').count()
    total_cesareas = cesareas_electiva + cesareas_urgencia
    total_vaginales = partos.filter(tipo_parto='vaginal').count()
    
    # Indicaciones de cesárea (simulado - adaptar según campo real)
    indicaciones = [
        {'indicacion': 'Cesárea previa', 'total': int(total_cesareas * 0.3), 'porcentaje': 30},
        {'indicacion': 'Desproporción cefalopélvica', 'total': int(total_cesareas * 0.2), 'porcentaje': 20},
        {'indicacion': 'Sufrimiento fetal', 'total': int(total_cesareas * 0.15), 'porcentaje': 15},
        {'indicacion': 'Presentación podálica', 'total': int(total_cesareas * 0.12), 'porcentaje': 12},
        {'indicacion': 'Otros', 'total': int(total_cesareas * 0.23), 'porcentaje': 23},
    ] if total_cesareas > 0 else []
    
    return {
        'total_partos': total_partos,
        'cesareas_electiva': cesareas_electiva,
        'cesareas_urgencia': cesareas_urgencia,
        'total_cesareas': total_cesareas,
        'total_vaginales': total_vaginales,
        'tasa_cesarea': round((total_cesareas / total_partos * 100), 2) if total_partos > 0 else 0,
        'porcentaje_electiva': round((cesareas_electiva / total_cesareas * 100), 2) if total_cesareas > 0 else 0,
        'porcentaje_urgencia': round((cesareas_urgencia / total_cesareas * 100), 2) if total_cesareas > 0 else 0,
        'porcentaje_electiva_total': round((cesareas_electiva / total_partos * 100), 2) if total_partos > 0 else 0,
        'porcentaje_urgencia_total': round((cesareas_urgencia / total_partos * 100), 2) if total_partos > 0 else 0,
        'indicaciones': indicaciones,
    }


def _get_neonatologia_data(fecha_inicio, fecha_fin):
    """Obtiene datos neonatales."""
    rn = RecienNacido.objects.filter(
        created_at__date__range=[fecha_inicio, fecha_fin]
    ).select_related('parto__paciente')
    
    total_rn = rn.count()
    rn_bajo_peso_count = rn.filter(peso_gramos__lt=2500, peso_gramos__gte=1500).count()
    rn_muy_bajo_peso = rn.filter(peso_gramos__lt=1500).count()
    rn_peso_normal = rn.filter(peso_gramos__gte=2500, peso_gramos__lt=4000).count()
    rn_macrosomico = rn.filter(peso_gramos__gte=4000).count()
    
    # APGAR por categorías
    apgar_1_critico = rn.filter(apgar_1_min__lte=3).count()
    apgar_1_moderado = rn.filter(apgar_1_min__gte=4, apgar_1_min__lte=6).count()
    apgar_1_normal = rn.filter(apgar_1_min__gte=7).count()
    
    apgar_5_critico = rn.filter(apgar_5_min__lte=3).count()
    apgar_5_moderado = rn.filter(apgar_5_min__gte=4, apgar_5_min__lte=6).count()
    apgar_5_normal = rn.filter(apgar_5_min__gte=7).count()
    
    rn_reanimacion = rn.filter(reanimacion_requerida=True).count()
    rn_no_reanimacion = total_rn - rn_reanimacion
    
    peso_promedio = rn.aggregate(Avg('peso_gramos'))['peso_gramos__avg']
    apgar_1_promedio = rn.aggregate(Avg('apgar_1_min'))['apgar_1_min__avg']
    apgar_5_promedio = rn.aggregate(Avg('apgar_5_min'))['apgar_5_min__avg']
    
    return {
        'total_rn': total_rn,
        'rn_bajo_peso': rn_bajo_peso_count,
        'rn_muy_bajo_peso': rn_muy_bajo_peso,
        'rn_peso_normal': rn_peso_normal,
        'rn_macrosomico': rn_macrosomico,
        'apgar_1_critico': apgar_1_critico,
        'apgar_1_moderado': apgar_1_moderado,
        'apgar_1_normal': apgar_1_normal,
        'apgar_5_critico': apgar_5_critico,
        'apgar_5_moderado': apgar_5_moderado,
        'apgar_5_normal': apgar_5_normal,
        'rn_reanimacion': rn_reanimacion,
        'rn_no_reanimacion': rn_no_reanimacion,
        'peso_promedio': round(peso_promedio, 0) if peso_promedio else 0,
        'apgar_1_promedio': round(apgar_1_promedio, 1) if apgar_1_promedio else 0,
        'apgar_5_promedio': round(apgar_5_promedio, 1) if apgar_5_promedio else 0,
        'porcentaje_bajo_peso': round(((rn_bajo_peso_count + rn_muy_bajo_peso) / total_rn * 100), 2) if total_rn > 0 else 0,
        'porcentaje_muy_bajo_peso': round((rn_muy_bajo_peso / total_rn * 100), 2) if total_rn > 0 else 0,
        'porcentaje_peso_normal': round((rn_peso_normal / total_rn * 100), 2) if total_rn > 0 else 0,
        'porcentaje_macrosomico': round((rn_macrosomico / total_rn * 100), 2) if total_rn > 0 else 0,
        'porcentaje_reanimacion': round((rn_reanimacion / total_rn * 100), 2) if total_rn > 0 else 0,
        'porcentaje_no_reanimacion': round((rn_no_reanimacion / total_rn * 100), 2) if total_rn > 0 else 0,
    }


def _get_apgar_critico_data(fecha_inicio, fecha_fin):
    """Obtiene datos de RN con APGAR crítico."""
    rn_criticos = RecienNacido.objects.filter(
        created_at__date__range=[fecha_inicio, fecha_fin]
    ).filter(
        Q(apgar_1_min__lt=7) | Q(apgar_5_min__lt=7)
    ).select_related('parto__paciente').order_by('apgar_5_min')
    
    apgar_1_critico = rn_criticos.filter(apgar_1_min__lt=7).count()
    apgar_5_critico = rn_criticos.filter(apgar_5_min__lt=7).count()
    rn_reanimacion = rn_criticos.filter(reanimacion_requerida=True).count()
    
    return {
        'recien_nacidos': rn_criticos,
        'total_criticos': rn_criticos.count(),
        'apgar_1_critico': apgar_1_critico,
        'apgar_5_critico': apgar_5_critico,
        'rn_reanimacion': rn_reanimacion,
    }


def _get_bajo_peso_data(fecha_inicio, fecha_fin):
    """Obtiene datos de RN con bajo peso."""
    rn_bajo_peso = RecienNacido.objects.filter(
        created_at__date__range=[fecha_inicio, fecha_fin],
        peso_gramos__lt=2500
    ).select_related('parto__paciente').order_by('peso_gramos')
    
    rn_muy_bajo_peso_count = rn_bajo_peso.filter(peso_gramos__lt=1500).count()
    rn_pretermino = rn_bajo_peso.filter(parto__edad_gestacional__lt=37).count()
    peso_promedio = rn_bajo_peso.aggregate(Avg('peso_gramos'))['peso_gramos__avg']
    
    return {
        'recien_nacidos': rn_bajo_peso,
        'total_bajo_peso': rn_bajo_peso.count(),
        'rn_muy_bajo_peso': rn_muy_bajo_peso_count,
        'rn_pretermino': rn_pretermino,
        'peso_promedio': round(peso_promedio, 0) if peso_promedio else 0,
    }


def _get_alertas_data(fecha_inicio, fecha_fin):
    """Obtiene datos de alertas."""
    alertas = Alerta.objects.filter(
        fecha_hora_alerta__date__range=[fecha_inicio, fecha_fin]
    ).select_related('paciente', 'recien_nacido', 'usuario_genera')
    
    total_alertas = alertas.count()
    
    # Alertas por tipo
    alertas_por_tipo = []
    for tipo_alert in alertas.values('tipo').annotate(total=Count('id')).order_by('-total'):
        total = tipo_alert['total']
        criticas = alertas.filter(tipo=tipo_alert['tipo'], nivel_urgencia='CRITICA').count()
        alertas_por_tipo.append({
            'tipo': tipo_alert['tipo'],
            'total': total,
            'porcentaje': round((total / total_alertas * 100), 2) if total_alertas > 0 else 0,
            'criticas': criticas,
        })
    
    # Alertas por nivel de urgencia
    alertas_por_nivel = []
    for nivel in alertas.values('nivel_urgencia').annotate(total=Count('id')):
        total = nivel['total']
        pendientes = alertas.filter(nivel_urgencia=nivel['nivel_urgencia'], estado__in=['ACTIVA', 'EN_ATENCION']).count()
        resueltas = alertas.filter(nivel_urgencia=nivel['nivel_urgencia'], estado='RESUELTA').count()
        alertas_por_nivel.append({
            'nivel': nivel['nivel_urgencia'].lower() if nivel['nivel_urgencia'] else 'bajo',
            'total': total,
            'porcentaje': round((total / total_alertas * 100), 2) if total_alertas > 0 else 0,
            'pendientes': pendientes,
            'resueltas': resueltas,
        })
    
    # Alertas por estado
    alertas_por_estado = []
    for estado in alertas.values('estado').annotate(total=Count('id')):
        total = estado['total']
        alertas_por_estado.append({
            'estado': estado['estado'].lower() if estado['estado'] else 'pendiente',
            'total': total,
            'porcentaje': round((total / total_alertas * 100), 2) if total_alertas > 0 else 0,
        })
    
    alertas_criticas = alertas.filter(nivel_urgencia='CRITICA').count()
    alertas_pendientes = alertas.filter(estado__in=['ACTIVA', 'EN_ATENCION']).count()
    alertas_resueltas = alertas.filter(estado='RESUELTA').count()
    tasa_resolucion = round((alertas_resueltas / total_alertas * 100), 2) if total_alertas > 0 else 0
    
    return {
        'total_alertas': total_alertas,
        'alertas_por_tipo': alertas_por_tipo,
        'alertas_por_nivel': alertas_por_nivel,
        'alertas_por_estado': alertas_por_estado,
        'alertas_criticas': alertas_criticas,
        'alertas_pendientes': alertas_pendientes,
        'alertas_resueltas': alertas_resueltas,
        'tasa_resolucion': tasa_resolucion,
        'tiempo_promedio_resolucion': None,  # Calcular si hay campo de tiempo
        'alertas': alertas[:50],  # Primeras 50
    }


def _get_resumen_mensual_data(fecha_inicio, fecha_fin):
    """Obtiene resumen completo mensual."""
    # Combinar todos los datos
    partos_data = _get_partos_periodo_data(fecha_inicio, fecha_fin)
    robson_data = _get_robson_data(fecha_inicio, fecha_fin)
    cesarea_data = _get_cesarea_data(fecha_inicio, fecha_fin)
    neo_data = _get_neonatologia_data(fecha_inicio, fecha_fin)
    alertas_data = _get_alertas_data(fecha_inicio, fecha_fin)
    
    # Pacientes nuevas
    pacientes_nuevas = PacienteMadre.objects.filter(
        created_at__date__range=[fecha_inicio, fecha_fin]
    ).count()
    
    return {
        **partos_data,
        'robson_grupos': robson_data['robson_grupos'],
        'tasa_cesarea': cesarea_data['tasa_cesarea'],
        'total_rn': neo_data['total_rn'],
        'peso_promedio': neo_data['peso_promedio'],
        'apgar_5_promedio': neo_data['apgar_5_promedio'],
        'rn_bajo_peso': neo_data['rn_bajo_peso'],
        'rn_apgar_bajo': neo_data['rn_apgar_bajo'],
        'total_alertas': alertas_data['total_alertas'],
        'pacientes_nuevas': pacientes_nuevas,
    }
