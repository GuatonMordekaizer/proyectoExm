from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscar_paciente, name='buscar_paciente'),
    path('<int:paciente_id>/', views.detalle_paciente, name='detalle_paciente'),
    path('crear/', views.crear_paciente, name='crear_paciente'),
]
