"""
URL configuration for hospital_hhm project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login')),
    path('auth/', include('apps.administracion.urls')),
    path('pacientes/', include('apps.pacientes.urls')),
    path('obstetricia/', include('apps.obstetricia.urls')),
    path('neonatologia/', include('apps.neonatologia.urls')),
    path('reportes/', include('apps.reportes.urls')),
]

# Handlers para páginas de error personalizadas
# Nota: Solo funcionan cuando DEBUG=False
handler403 = 'apps.administracion.views.error_403'
handler404 = 'apps.administracion.views.error_404'
handler500 = 'apps.administracion.views.error_500'
