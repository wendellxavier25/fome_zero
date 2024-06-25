from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('escolher_horario/<int:id_dados_voluntarios>', views.escolher_horario, name="escolher_horario"),
    path('agendar_horario/<int:id_data_aberta>/', views.agendar_horario, name="agendar_horario"),
    path('meus_atendimentos/', views.meus_atendimentos, name="meus_atendimentos"),
    path('doacao/<int:id_doacao>/', views.doacao, name="doacao"),

]
