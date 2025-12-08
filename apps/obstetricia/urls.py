from django.urls import path
from . import views

urlpatterns = [
    path('parto/registrar/<int:paciente_id>/', views.registrar_parto, name='registrar_parto'),
    path('parto/detalle/<int:parto_id>/', views.detalle_parto, name='detalle_parto'),
]
