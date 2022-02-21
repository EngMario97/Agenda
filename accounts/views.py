from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContact


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    user = request.POST.get('user')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=user, password=password)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Você fez login com sucesso.')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('index')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    name = request.POST.get('name')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    user = request.POST.get('user')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')

    if not name or not lastname or not email or not user or not password \
            or not password2:
        messages.error(request, 'Nenhum campo pode estar vazio.')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'accounts/register.html')

    if len(password) < 6:
        messages.error(request, 'Senha precisa ter 6 caracteres ou mais.')
        return render(request, 'accounts/register.html')

    if len(user) < 6:
        messages.error(request, 'Usuário precisa ter 6 caracteres ou mais.')
        return render(request, 'accounts/register.html')

    if password != password2:
        messages.error(request, 'Senhas não conferem.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=user).exists():
        messages.error(request, 'Usuário já existe.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já existe.')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Registrado com sucesso! Agora faça login.')

    user = User.objects.create_user(username=user, email=email,
                                    password=password, first_name=name,
                                    last_name=lastname)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContact()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContact(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar formulário.')
        form = FormContact(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    description = request.POST.get('description')

    if len(description) < 5:
        messages.error(request, 'Descrição precisa ter mais que 5 caracteres.')
        form = FormContact(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("name")} salvo com sucesso!')
    return redirect('dashboard')

