from django.shortcuts import render, redirect
from .models import Especialidades, DadosVoluntario, is_voluntario, DatasAbertas
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from cliente.models import Doacao

@login_required
def cadastro_voluntario(request):
    if is_voluntario(request.user):
        messages.add_message(request, constants.WARNING, 'Você já está cadastrado')
        return redirect('/voluntario/abrir_horario/')
    
    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        return render(request, 'cadastro_voluntario.html', {'especialidades': especialidades})
    
    elif request.method == "POST":
        if request.user.is_authenticated:
            user_id = request.user.id
            anos_de_experiencia = request.POST.get('anos_de_experiencia')
            nome = request.POST.get('nome')
            cep = request.POST.get('cep')
            rua = request.POST.get('rua')
            bairro = request.POST.get('bairro')
            numero = request.POST.get('numero')
            rg = request.FILES.get('rg')
            foto = request.FILES.get('foto')
            especialidade = request.POST.get('especialidade')
            descricao = request.POST.get('descricao')
        
        dados_voluntario = DadosVoluntario(
            user_id=user_id,
            anos_de_experiencia=anos_de_experiencia,
            nome=nome,
            cep=cep,
            rua=rua,
            bairro=bairro,
            numero=numero,
            rg=rg,
            foto=foto,
            especialidade_id=especialidade,
            descricao=descricao
        )
        dados_voluntario.save()
        
        messages.add_message(request, constants.SUCCESS, 'Dados salvos com sucesso')
        return redirect('/voluntario/abrir_horario/')
    else:
        return redirect('/voluntario/cadastro_voluntario/')
    
@login_required
def abrir_horario(request):
    if not is_voluntario(request.user):
        messages.add_message(request, constants.WARNING, 'Só voluntários cadastrados podem abrir horários')
        return redirect('/usuarios/sair/')
    
    if request.method == "GET":
        dados_voluntarios = DadosVoluntario.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user)
        return render(request, 'abrir_horario.html', {'dados_voluntarios': dados_voluntarios, 'datas_abertas': datas_abertas})
    
    elif request.method == "POST":
        data = request.POST.get('data')
        data_formatada = datetime.strptime(data, "%Y-%m-%dT%H:%M")
        
        if data_formatada <= datetime.now():
            messages.add_message(request, constants.ERROR, 'A data não pode ser anterior à data atual.')
            return redirect('/voluntario/abrir_horario/')
        
        horario_abrir = DatasAbertas(data=data, user=request.user)
        horario_abrir.save()
        messages.add_message(request, constants.SUCCESS, 'Horário salvo com sucesso')
        return redirect('/voluntario/abrir_horario/')

@login_required
def atendimentos_voluntario(request):
    if not is_voluntario(request.user):
        messages.add_message(request, constants.WARNING, 'Só voluntários cadastrados podem abrir horários')
        return redirect('/usuarios/sair/')
    
    hoje = datetime.now().date()
    atendimentos_hoje = Doacao.objects.filter(data_aberta__user=request.user).filter(data_aberta__data__gte=hoje).filter(data_aberta__data__lt=hoje + timedelta(days=1))
    atendimentos_restantes = Doacao.objects.exclude(id__in=atendimentos_hoje.values('id'))
    
    return render(request, 'atendimentos_voluntario.html', {'atendimentos_hoje': atendimentos_hoje, 'atendimentos_restantes': atendimentos_restantes})


