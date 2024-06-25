from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_voluntario/', views.cadastro_voluntario, name="cadastro_voluntario"),
    path('abrir_horario/', views.abrir_horario, name="abrir_horario"),
    path('atendimentos_voluntario/', views.atendimentos_voluntario, name="atendimentos_voluntario")
]
