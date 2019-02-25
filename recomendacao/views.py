from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Evento
from .form import Evento_form
from django.contrib import messages, auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def logout(request):
    auth.logout(request)
    messages.info(request, 'Logout efetuado com sucessor.')
    return redirect('url_login')

def login(request):
    if request.user.is_authenticated:
        return redirect('url_index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            messages.success(request, 'Login efetuado com sucessor.')
            auth.login(request, user)
            return redirect('url_index')

        else:
            messages.warning(request, 'Erro! Usuario é/ou senha inválido(s)')
    
    return render(request, 'recomendacao/login.html')

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario cadastrado com sucessor.')
            return redirect('url_login')

    else:
        form = UserCreationForm()

    return render(request, 'recomendacao/sign_up.html', {'form': form})

def index(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Por favor efetue o login.')
        return redirect('url_login')

    dados = {}
    dados['eventos'] = Evento.objects.all()
    form = Evento_form(request.POST or None)

    if form.is_valid():
        messages.success(request, 'Evento adicionado na lista.')
        form.save()
        return redirect('url_index')

    dados['form'] = form
    
    return render(request, 'recomendacao/index.html',dados)

def delete(request, pk):
    dados = Evento.objects.get(pk=pk)
    dados.delete()
    messages.warning(request, 'Evento removido da lista.')
    
    return redirect('url_index')

def lista(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Por favor efetue o login.')
        return redirect('url_login')

    dados_b = list(Evento.objects.order_by('data','hr_fim'))

    if not dados_b:
        messages.warning(request, 'Lista de evetos vazia.')
        return redirect('url_index')

    else:
        dados_f = [dados_b[0]]
        for i in range(1,len(dados_b)):
            if dados_f[-1].data == dados_b[i].data:
                if dados_b[i].priori:
                    if dados_f[-1].hr_fim > dados_b[i].hr_ini:
                        dados_f[-1] = dados_b[i]
                    else:
                        dados_f.append(dados_b[i])
                else:
                    if dados_f[-1].hr_fim < dados_b[i].hr_ini:
                        dados_f.append(dados_b[i])
            else:
                dados_f.append(dados_b[i])
        
        dados = {}
        dados['eventos'] = dados_f
        
        #Evento.objects.all().delete()

        return render(request, 'recomendacao/lista.html', dados)