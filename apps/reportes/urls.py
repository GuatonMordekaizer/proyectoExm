from django.urls import path
from . import views

urlpatterns = [
    # PDFs
    path('pdf/parto/<int:parto_id>/', views.generar_pdf_parto, name='generar_pdf_parto'),
    
    # Sistema de Alertas
    path('alertas/', views.listado_alertas, name='listado_alertas'),
    path('alertas/<int:alerta_id>/', views.detalle_alerta, name='detalle_alerta'),
    path('alertas/<int:alerta_id>/atender/', views.atender_alerta, name='atender_alerta'),
    path('alertas/<int:alerta_id>/resolver/', views.resolver_alerta, name='resolver_alerta'),
    path('alertas/dashboard/', views.dashboard_alertas, name='dashboard_alertas'),
    
    # API
    path('api/alertas/activas/', views.api_alertas_activas, name='api_alertas_activas'),
    
    # Reportes estadísticos
    path('', views.seleccionar_reporte, name='seleccionar_reporte'),
    path('generar/<str:tipo>/<str:fecha_inicio>/<str:fecha_fin>/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
]
