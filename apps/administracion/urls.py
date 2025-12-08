from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/general/', views.dashboard_general, name='dashboard_general'),
    path('auditoria/', views.historial_auditoria, name='historial_auditoria'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:usuario_id>/password/', views.cambiar_password, name='cambiar_password'),
    path('usuarios/<int:usuario_id>/restablecer/', views.restablecer_password, name='restablecer_password'),
    path('cambiar-password-obligatorio/', views.forzar_cambio_password, name='forzar_cambio_password'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    # Dashboards por rol (apuntan al general por ahora)
    path('dashboard/matrona/', views.dashboard_general, name='dashboard_matrona'),
    path('dashboard/medico/', views.dashboard_general, name='dashboard_medico'),
    path('dashboard/pediatra/', views.dashboard_general, name='dashboard_pediatra'),
    path('dashboard/enfermera/', views.dashboard_general, name='dashboard_enfermera'),
    path('dashboard/puericultura/', views.dashboard_general, name='dashboard_puericultura'),
    path('dashboard/administrativo/', views.dashboard_general, name='dashboard_administrativo'),
    path('dashboard/jefe/', views.dashboard_general, name='dashboard_jefe'),
    
    # Rutas de prueba para páginas de error (solo para desarrollo/testing)
    # Eliminar estas rutas en producción
    path('test/error/403/', views.error_403, name='test_error_403'),
    path('test/error/404/', views.error_404, name='test_error_404'),
    path('test/error/500/', views.error_500, name='test_error_500'),
]
