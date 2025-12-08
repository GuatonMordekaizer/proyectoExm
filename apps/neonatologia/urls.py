from django.urls import path
from . import views

urlpatterns = [
    path('registrar/<int:parto_id>/', views.registrar_recien_nacido, name='registrar_recien_nacido'),
    path('detalle/<int:pk>/', views.detalle_recien_nacido, name='detalle_recien_nacido'),
]
