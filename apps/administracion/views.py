from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .decorators import rol_requerido, puede_gestionar_usuarios, puede_ver_auditoria
from .models import Auditoria, Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm


def login_view(request):
    """
    Vista de login con autenticación por RUT o username.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticar usuario (usa RUTAuthenticationBackend)
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login exitoso
            login(request, user)
            
            # Registrar en auditoría
            Auditoria.objects.create(
                usuario=user,
                accion='login',
                descripcion=f'Inicio de sesión exitoso - Rol: {user.get_rol_display()}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Verificar si debe cambiar contraseña
            if user.requiere_cambio_password:
                messages.warning(request, 'Debe cambiar su contraseña temporal.')
                return redirect('forzar_cambio_password')
            
            messages.success(request, f'¡Bienvenido/a {user.get_full_name()}!')
            return redirect('dashboard')
        else:
            # Login fallido - registrar en auditoría
            # Intentar obtener el usuario para registrar intento fallido
            from apps.administracion.models import Usuario
            try:
                failed_user = Usuario.objects.get(rut=username) if '.' in username else Usuario.objects.get(username=username)
                Auditoria.objects.create(
                    usuario=failed_user,
                    accion='login_fallido',
                    descripcion=f'Intento de inicio de sesión fallido',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
            except Usuario.DoesNotExist:
                pass
            
            messages.error(request, 'RUT/Usuario o contraseña incorrectos.')
    
    return render(request, 'administracion/login.html')


def logout_view(request):
    """
    Vista de logout.
    """
    if request.user.is_authenticated:
        # Registrar en auditoría
        Auditoria.objects.create(
            usuario=request.user,
            accion='logout',
            descripcion='Cierre de sesión',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        logout(request)
        messages.success(request, 'Sesión cerrada exitosamente.')
    
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    Vista de dashboard principal.
    Redirige al dashboard específico según el rol del usuario.
    """
    user = request.user
    
    # Redirigir según rol
    dashboard_urls = {
        'matrona': 'dashboard_matrona',
        'medico_obstetra': 'dashboard_medico',
        'pediatra': 'dashboard_pediatra',
        'enfermera_neonatal': 'dashboard_enfermera',
        'puericultura': 'dashboard_puericultura',
        'administrativo': 'dashboard_administrativo',
        'jefe_servicio': 'dashboard_jefe',
    }
    
    dashboard_url = dashboard_urls.get(user.rol, 'dashboard_general')
    return redirect(dashboard_url)


@login_required
def dashboard_general(request):
    """
    Dashboard general con estadísticas en tiempo real.
    """
    from datetime import date, timedelta
    from django.db.models import Count, Q
    from apps.obstetricia.models import Parto
    from apps.neonatologia.models import RecienNacido
    from apps.pacientes.models import PacienteMadre
    
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    
    # Estadísticas del día
    partos_hoy = Parto.objects.filter(fecha_parto=hoy).count()
    rn_hoy = RecienNacido.objects.filter(created_at__date=hoy).count()
    pacientes_nuevos_hoy = PacienteMadre.objects.filter(created_at__date=hoy).count()
    
    # Alertas críticas (APGAR < 7 en las últimas 24 horas)
    alertas_criticas = RecienNacido.objects.filter(
        apgar_5_min__lt=7,
        created_at__gte=hoy
    ).count()
    
    # Estadísticas del mes
    partos_mes = Parto.objects.filter(fecha_parto__gte=inicio_mes).count()
    
    # Datos para gráficos
    # 1. Partos por tipo (mes actual)
    partos_vaginales = Parto.objects.filter(fecha_parto__gte=inicio_mes, tipo_parto='vaginal').count()
    cesareas = Parto.objects.filter(fecha_parto__gte=inicio_mes, tipo_parto__in=['cesarea_electiva', 'cesarea_urgencia']).count()
    
    # 2. Distribución de grupos Robson (mes actual)
    from django.db.models import Count
    grupos_robson = list(Parto.objects.filter(
        fecha_parto__gte=inicio_mes
    ).values('grupo_robson').annotate(
        total=Count('id')
    ).order_by('grupo_robson'))
    
    # 3. Peso de RN (mes actual)
    rn_peso_normal = RecienNacido.objects.filter(
        created_at__date__gte=inicio_mes,
        peso_gramos__gte=2500,
        peso_gramos__lt=4000
    ).count()
    rn_bajo_peso = RecienNacido.objects.filter(
        created_at__date__gte=inicio_mes,
        peso_gramos__lt=2500
    ).count()
    rn_macrosomico = RecienNacido.objects.filter(
        created_at__date__gte=inicio_mes,
        peso_gramos__gte=4000
    ).count()
    
    # 4. Últimos 7 días - partos por día
    from datetime import timedelta
    ultimos_7_dias = []
    partos_7_dias = []
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        ultimos_7_dias.append(dia.strftime('%d/%m'))
        count = Parto.objects.filter(fecha_parto=dia).count()
        partos_7_dias.append(count)
    
    # Últimos partos registrados - SOLO para roles clínicos
    ultimos_partos = None
    if request.user.rol in ['matrona', 'medico_obstetra', 'pediatra', 'enfermera_neonatal']:
        ultimos_partos = Parto.objects.select_related('paciente').order_by('-created_at')[:5]
    
    # Alertas recientes (RN con APGAR bajo o que requieren atención) - SOLO para roles clínicos
    alertas_recientes = None
    if request.user.rol in ['matrona', 'medico_obstetra', 'pediatra', 'enfermera_neonatal']:
        alertas_recientes = RecienNacido.objects.filter(
            Q(apgar_5_min__lt=7) | Q(peso_gramos__lt=2500) | Q(reanimacion_requerida=True)
        ).select_related('parto__paciente').order_by('-created_at')[:5]
    
    context = {
        'user': request.user,
        'partos_hoy': partos_hoy,
        'rn_hoy': rn_hoy,
        'pacientes_nuevos_hoy': pacientes_nuevos_hoy,
        'alertas_criticas': alertas_criticas,
        'partos_mes': partos_mes,
        'ultimos_partos': ultimos_partos,
        'alertas_recientes': alertas_recientes,
        # Datos para gráficos
        'partos_vaginales': partos_vaginales,
        'cesareas': cesareas,
        'grupos_robson': grupos_robson,
        'rn_peso_normal': rn_peso_normal,
        'rn_bajo_peso': rn_bajo_peso,
        'rn_macrosomico': rn_macrosomico,
        'ultimos_7_dias': ultimos_7_dias,
        'partos_7_dias': partos_7_dias,
    }
    
    return render(request, 'general/dashboard.html', context)


def get_client_ip(request):
    """
    Obtiene la IP del cliente desde el request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
@puede_ver_auditoria
def historial_auditoria(request):
    """
    Vista para ver el historial de auditoría (logs).
    Solo accesible para Jefe de Servicio.
    """
    from django.core.paginator import Paginator
    
    # Filtros
    logs = Auditoria.objects.select_related('usuario').all()
    
    usuario_id = request.GET.get('usuario')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    accion = request.GET.get('accion')
    
    if usuario_id:
        logs = logs.filter(usuario_id=usuario_id)
    
    if fecha_inicio:
        logs = logs.filter(timestamp__date__gte=fecha_inicio)
        
    if fecha_fin:
        logs = logs.filter(timestamp__date__lte=fecha_fin)
        
    if accion:
        logs = logs.filter(accion=accion)
    
    # Paginación (25 registros por página)
    paginator = Paginator(logs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    # Obtener lista de usuarios para el filtro
    usuarios = Usuario.objects.all().order_by('last_name')
    
    return render(request, 'administracion/auditoria_list.html', {
        'page_obj': page_obj,
        'logs': page_obj,  # Para compatibilidad con template actual
        'usuarios': usuarios,
        'ACCION_CHOICES': Auditoria.ACCION_CHOICES,
    })


@login_required
@puede_gestionar_usuarios
def lista_usuarios(request):
    """
    Lista de usuarios del sistema.
    Solo administrativos y jefe de servicio pueden gestionar usuarios.
    """
    usuarios = Usuario.objects.all()
    return render(request, 'administracion/lista_usuarios.html', {'usuarios': usuarios})


@login_required
@puede_gestionar_usuarios
@login_required
@puede_gestionar_usuarios
def crear_usuario(request):
    """
    Crear nuevo usuario.
    Solo administrativos y jefe de servicio pueden crear usuarios.
    """
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Auditoría
            Auditoria.objects.create(
                usuario=request.user,
                accion='crear',
                modelo='Usuario',
                objeto_id=user.id,
                descripcion=f'Creó usuario {user.username} ({user.get_rol_display()})',
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, f'Usuario {user.username} creado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioCreationForm()
        
    return render(request, 'administracion/form_usuario.html', {'form': form, 'titulo': 'Crear Usuario'})


@login_required
@puede_gestionar_usuarios
def editar_usuario(request, usuario_id):
    """
    Editar usuario existente.
    Solo administrativos y jefe de servicio pueden editar usuarios.
    """
    usuario_editar = get_object_or_404(Usuario, pk=usuario_id)
    
    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, instance=usuario_editar)
        if form.is_valid():
            user = form.save()
            
            # Auditoría
            Auditoria.objects.create(
                usuario=request.user,
                accion='editar',
                modelo='Usuario',
                objeto_id=user.id,
                descripcion=f'Editó usuario {user.username}',
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, f'Usuario {user.username} actualizado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioChangeForm(instance=usuario_editar)
        
    return render(request, 'administracion/form_usuario.html', {'form': form, 'titulo': 'Editar Usuario'})


@login_required
def perfil_usuario(request):
    """
    Vista de perfil del usuario actual.
    Permite editar nombre, username y contraseña.
    """
    if request.method == 'POST':
        # Actualizar datos básicos
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        
        # Validar que el username no esté en uso por otro usuario
        if username != request.user.username:
            if Usuario.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
                return redirect('perfil_usuario')
        
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.username = username
        
        # Cambiar contraseña si se proporcionó
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password:
            if password == password_confirm:
                request.user.set_password(password)
                messages.success(request, 'Contraseña actualizada. Por favor, inicie sesión nuevamente.')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect('perfil_usuario')
        
        request.user.save()
        
        # Auditoría
        Auditoria.objects.create(
            usuario=request.user,
            accion='editar',
            modelo='Usuario',
            objeto_id=request.user.id,
            descripcion='Actualizó su perfil',
            ip_address=get_client_ip(request)
        )
        
        if password:
            # Si cambió contraseña, cerrar sesión
            logout(request)
            return redirect('login')
        else:
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil_usuario')
    
    return render(request, 'administracion/perfil.html', {
        'user': request.user,
    })


@login_required
def cambiar_password(request, usuario_id):
    """
    Vista para cambiar la contraseña de un usuario.
    Solo accesible para usuarios con permisos de gestión.
    """
    if not request.user.puede_gestionar_usuarios() and not request.user.is_superuser:
        messages.error(request, 'No tiene permisos para cambiar contraseñas.')
        return redirect('dashboard')
        
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    
    if request.method == 'POST':
        nueva_password = request.POST.get('nueva_password')
        confirmar_password = request.POST.get('confirmar_password')
        
        if not nueva_password or not confirmar_password:
            messages.error(request, 'Debe completar todos los campos.')
            return render(request, 'administracion/cambiar_password.html', {'usuario_edit': usuario})
        
        if nueva_password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'administracion/cambiar_password.html', {'usuario_edit': usuario})
        
        if len(nueva_password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'administracion/cambiar_password.html', {'usuario_edit': usuario})
        
        # Cambiar contraseña
        usuario.set_password(nueva_password)
        usuario.save()
        
        # Auditoría
        Auditoria.objects.create(
            usuario=request.user,
            accion='cambiar_password',
            modelo='Usuario',
            objeto_id=usuario.id,
            descripcion=f'Cambió la contraseña del usuario {usuario.username}',
            ip_address=get_client_ip(request)
        )
        
        messages.success(request, f'Contraseña de {usuario.username} cambiada exitosamente.')
        return redirect('editar_usuario', usuario_id=usuario.id)
    
    return render(request, 'administracion/cambiar_password.html', {
        'usuario_edit': usuario,
    })


@login_required
def restablecer_password(request, usuario_id):
    """
    Genera una contraseña temporal aleatoria y obliga al usuario a cambiarla.
    """
    if not request.user.puede_gestionar_usuarios() and not request.user.is_superuser:
        messages.error(request, 'No tiene permisos para restablecer contraseñas.')
        return redirect('dashboard')
        
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    
    if request.method == 'POST':
        import secrets
        import string
        
        # Generar contraseña temporal segura (12 caracteres)
        caracteres = string.ascii_letters + string.digits + '!@#$%'
        password_temporal = ''.join(secrets.choice(caracteres) for _ in range(12))
        
        # Establecer contraseña temporal
        usuario.set_password(password_temporal)
        usuario.requiere_cambio_password = True
        usuario.save()
        
        # Auditoría
        Auditoria.objects.create(
            usuario=request.user,
            accion='restablecer_password',
            modelo='Usuario',
            objeto_id=usuario.id,
            descripcion=f'Generó contraseña temporal para {usuario.username}',
            ip_address=get_client_ip(request)
        )
        
        # Mostrar contraseña temporal en el template
        return render(request, 'administracion/password_temporal.html', {
            'usuario_edit': usuario,
            'password_temporal': password_temporal,
        })
    
    return redirect('editar_usuario', usuario_id=usuario.id)


@login_required
def forzar_cambio_password(request):
    """
    Vista que obliga al usuario a cambiar su contraseña temporal.
    """
    if not request.user.requiere_cambio_password:
        return redirect('dashboard')
    
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        nueva_password = request.POST.get('nueva_password')
        confirmar_password = request.POST.get('confirmar_password')
        
        # Verificar contraseña actual
        if not request.user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return render(request, 'administracion/forzar_cambio_password.html')
        
        if not nueva_password or not confirmar_password:
            messages.error(request, 'Debe completar todos los campos.')
            return render(request, 'administracion/forzar_cambio_password.html')
        
        if nueva_password != confirmar_password:
            messages.error(request, 'Las contraseñas nuevas no coinciden.')
            return render(request, 'administracion/forzar_cambio_password.html')
        
        if len(nueva_password) < 8:
            messages.error(request, 'La nueva contraseña debe tener al menos 8 caracteres.')
            return render(request, 'administracion/forzar_cambio_password.html')
        
        if password_actual == nueva_password:
            messages.error(request, 'La nueva contraseña debe ser diferente a la actual.')
            return render(request, 'administracion/forzar_cambio_password.html')
        
        # Cambiar contraseña
        request.user.set_password(nueva_password)
        request.user.requiere_cambio_password = False
        request.user.save()
        
        # Auditoría
        Auditoria.objects.create(
            usuario=request.user,
            accion='cambio_password_forzado',
            modelo='Usuario',
            objeto_id=request.user.id,
            descripcion='Usuario cambió su contraseña temporal',
            ip_address=get_client_ip(request)
        )
        
        # Actualizar sesión para que no se cierre
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Contraseña cambiada exitosamente. Ahora puede usar el sistema.')
        return redirect('dashboard')
    
    return render(request, 'administracion/forzar_cambio_password.html')


# ===================================================================
# VISTAS DE ERROR PERSONALIZADAS
# ===================================================================

def error_403(request, exception=None):
    """Vista personalizada para error 403 - Forbidden (Acceso Denegado)"""
    context = {
        'error_code': '403',
        'error_title': 'Acceso Denegado',
        'error_message': 'No tiene permisos para acceder a esta página.',
        'exception': exception
    }
    return render(request, '403.html', context, status=403)


def error_404(request, exception=None):
    """Vista personalizada para error 404 - Not Found (Página no encontrada)"""
    context = {
        'error_code': '404',
        'error_title': 'Página No Encontrada',
        'error_message': 'La página que busca no existe o ha sido movida.',
        'exception': exception
    }
    return render(request, '404.html', context, status=404)


def error_500(request):
    """Vista personalizada para error 500 - Internal Server Error"""
    context = {
        'error_code': '500',
        'error_title': 'Error Interno del Servidor',
        'error_message': 'Ha ocurrido un error inesperado. Por favor, intente nuevamente más tarde.'
    }
    return render(request, '500.html', context, status=500)
