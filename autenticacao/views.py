from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth

# Cadastro de usuário
def cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated:  # Veirificar se usuário já está logado
            return redirect('/plataforma')
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('password')
        confirmar_senha = request.POST.get('confirm-password')

        # Varificar se senha é igual a confirmar senha
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')            
            return redirect('/auth/cadastro')

        # Checar se há espaços na criação da senha
        if len(username.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Nome de usuário e senha devem ser preenchidos') 
            return redirect('/auth/cadastro')

        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuáreo já existe, tente outra opção')
            return redirect('/auth/cadastro')
        
        try:
            user = User.objects.create_user(username=username, password=senha)
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            user.save()
            return redirect('/auth/logar')

        except:
            return redirect('/auth/cadastro')
        
# Login Usuário
def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated:  # Veirificar se usuário já está logado
            return redirect('/plataforma')
        return render(request, 'logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('password')

        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return redirect('/auth/logar')
        else:
            auth.login(request, usuario)
            return HttpResponse('MÃE TO NA GLOBO.')


def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')