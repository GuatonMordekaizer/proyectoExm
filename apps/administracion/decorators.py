from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def rol_requerido(*roles_permitidos):
    """
    Decorador para restringir acceso a vistas según rol del usuario.
    
    Uso:
        @rol_requerido('matrona', 'medico_obstetra')
        def registrar_parto(request):
            ...
    
    Args:
        *roles_permitidos: Lista de roles que pueden acceder a la vista
    
    Raises:
        PermissionDenied: Si el usuario no tiene el rol requerido
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Verificar que el usuario esté autenticado
            if not request.user.is_authenticated:
                messages.error(request, 'Debe iniciar sesión para acceder a esta página.')
                return redirect('login')
            
            # Verificar que el usuario tenga el rol requerido
            if request.user.rol not in roles_permitidos:
                raise PermissionDenied(
                    f'No tiene permisos para acceder a esta página. '
                    f'Roles permitidos: {", ".join(roles_permitidos)}'
                )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def puede_registrar_parto(view_func):
    """
    Decorador específico para vistas de registro de parto.
    Solo matronas y médicos obstetras pueden registrar partos.
    """
    return rol_requerido('matrona', 'medico_obstetra')(view_func)


def puede_evaluar_rn(view_func):
    """
    Decorador específico para vistas de evaluación de recién nacidos.
    Solo pediatras y enfermeras neonatales pueden evaluar RN.
    """
    return rol_requerido('pediatra', 'enfermera_neonatal')(view_func)


def puede_generar_reportes(view_func):
    """
    Decorador específico para vistas de generación de reportes.
    Solo jefe de servicio y médicos obstetras pueden generar reportes.
    """
    return rol_requerido('jefe_servicio', 'medico_obstetra')(view_func)


def puede_gestionar_usuarios(view_func):
    """
    Decorador específico para vistas de gestión de usuarios.
    Solo administrativos y jefe de servicio pueden gestionar usuarios.
    """
    return rol_requerido('administrativo', 'jefe_servicio')(view_func)


def puede_ver_auditoria(view_func):
    """
    Decorador específico para vistas de auditoría.
    Solo jefe de servicio puede ver auditoría completa.
    """
    return rol_requerido('jefe_servicio')(view_func)
