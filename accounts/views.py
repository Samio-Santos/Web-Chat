from django.shortcuts import render
from django.shortcuts import render, redirect
from urllib.parse import urlparse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.contrib import messages, auth
from .models import ProfileUser


def login(request):
    # Salva o caminho do usuário antes de desativar as conversas
    current_url = urlparse(request.build_absolute_uri()).hostname
    port = urlparse(request.build_absolute_uri()).port

    if request.method != 'POST':

        if request.user.is_authenticated:
            token_user = ProfileUser.objects.get(username=request.user).token

            return redirect(f"http://{current_url}:{port}/chat/{token_user}/")

        return render(request, "accounts_app/login.html")
    
    usuario = request.POST.get('user')
    senha = request.POST.get('password')
    user = auth.authenticate(request, username=usuario, password=senha)
 
    modelUser = get_user_model()

    try:
        token_user = ProfileUser.objects.get(username=usuario).token

        if not user:
            # messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, 'accounts_app/login.html', {'invalid': 'invalid'})

        else:
            auth.login(request, user)
            # messages.success(request, f'Seja bem-vindo(a) {user.first_name} {user.last_name}!')
            return redirect(f"http://{current_url}:{port}/chat/{token_user}/")
                
 
    except modelUser.DoesNotExist:
        # messages.error(request, 'Usuário não está cadastrado!')
        # Renderiza o template com os dados
        return render(request, "accounts_app/login.html")


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts_app/register.html')