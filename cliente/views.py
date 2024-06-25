
from django.shortcuts import render, redirect
from voluntario.models import  Especialidades, is_voluntario, DadosVoluntario, DatasAbertas
from . models import Doacao
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.method == "GET":
        voluntario_filtrar = request.GET.get('voluntario')
        especialidade_filtrar = request.GET.getlist('especialidades')
        voluntarios = DadosVoluntario.objects.all()
    
    if voluntario_filtrar:
        voluntarios = voluntarios.filter(nome__icontains=voluntario_filtrar)
        
    if especialidade_filtrar:
        voluntarios = voluntarios.filter(especialidade_id__in=especialidade_filtrar)
        
    especialidades = Especialidades.objects.all()
    return render(request, 'home.html', {'voluntarios': voluntarios, 'especialidades': especialidades, 'is_voluntario': is_voluntario(request.user)})

@login_required
def escolher_horario(request, id_dados_voluntarios):
    if request.method == "GET":
        voluntario = DadosVoluntario.objects.get(id=id_dados_voluntarios)
        datas_abertas = DatasAbertas.objects.filter(user=voluntario.user).filter(data__gte=datetime.now()).filter(agendado=False)
        return render(request,'escolher_horario.html', {'voluntario': voluntario, 'datas_abertas': datas_abertas, 'is_voluntario': is_voluntario(request.user)})

@login_required
def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)
        
        horario_agendado = Doacao(cliente=request.user, data_aberta=data_aberta)
        
        horario_agendado.save()
        
        data_aberta.agendado = True
        data_aberta.save()
        messages.add_message(request, constants.SUCCESS, 'Data Agendada')
        return redirect('/cliente/meus_atendimentos')

@login_required
def meus_atendimentos(request):
    data = request.GET.get("data")
    especialidade = request.GET.get("especialidade")
    
    meus_atendimentos = Doacao.objects.filter(cliente=request.user).filter(data_aberta__data__gte=datetime.now())
    
    if data:
        meus_atendimentos = meus_atendimentos.filter(data_aberta__data__gte=data)
    
    if especialidade:
        meus_atendimentos = meus_atendimentos.filter(data_aberta__user__dadosvoluntario__especialidade__id=especialidade)
        
    especialidades = Especialidades.objects.all()
        
    return render(request, 'meus_atendimentos.html', {'meus_atendimentos': meus_atendimentos, 'especialidades': especialidades, 'is_voluntario': is_voluntario(request.user)})


@login_required
def doacao(request, id_doacao):
    if request.method == 'GET':
        doacao = Doacao.objects.get(id=id_doacao)
        dado_voluntario = DadosVoluntario.objects.get(user=doacao.data_aberta.user)
        voluntarios = DadosVoluntario.objects.all()
        return render(request, 'doacao.html', {'doacao': doacao, 'dado_voluntario': dado_voluntario, 'voluntarios': voluntarios})
        
    