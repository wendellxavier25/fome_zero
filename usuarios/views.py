from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

    if senha != confirmar_senha:
        messages.add_message(request, constants.WARNING, 'Senha e confirmar senha devem ser iguais')
        return redirect('/usuarios/cadastro/')
    
    if len(senha) < 4:
        messages.add_message(request, constants.WARNING, 'Senha deve ter mais de 4 caracteres')
        return redirect('/usuarios/cadastro/')
    
    users = User.objects.filter(username=username, email=email)
    
    
    if users.exists():
        messages.add_message(request, constants.ERROR, 'Já existe um usúario com esse username ou email')
        return redirect('/usuarios/cadastro/')
    
    try:
        user = User.objects.create_user(username=username, email=email, password=senha)
        messages.add_message(request, constants.SUCCESS, 'Usúario criado com sucesso')
        return redirect('/usuarios/login/')
    except:
        messages.add_message(request, constants.ERROR, 'Falha ao se cadastrar')
        return redirect('/usuarios/cadastro/')


def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)
            return redirect('/cliente/home')
        
        messages.add_message(request, constants.ERROR, 'Usúario ou senha inválidos')
        return redirect('/usuarios/login/')
    

def sair(request):
    auth.logout(request)
    return redirect('/usuarios/login')
    