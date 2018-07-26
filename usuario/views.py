from django.shortcuts import render
from django.shortcuts import redirect 
from django.contrib.auth.decorators import login_required
from usuario.forms import PerfilForm
from usuario.models import Perfil
from django.contrib.auth.forms import UserCreationForm
from cadastro.models import empresa_terc
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import permission_required



#from Usuario.models import Perfil
# Create your views here.




@login_required(login_url="login/")
def home(request):
    emp = empresa_terc.objects.all()
    for el in emp:
        if el.usuario == request.user.username:
            return render(request, 'home_empresa.html',{'el':el})       
    if request.user.first_name == "first_access":
        return redirect('cadastro_empresa') 
    else:
        args = Perfil.objects.all()
        return render(request, 'index.html',{'args':args})

@login_required(login_url="login/")
def perfil(request):
    if request.method == 'POST':
        print("ok")
        form = PerfilForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            try:
                el = Perfil.objects.get(user = request.user.username)
            except:
                el = None
            if el:
                el.delete()
            post = form.save(commit=False)
            post.image = request.FILES.get('image')
            post.last_name = request.POST.get('last_name')
            post.user = request.POST.get('user')
            post.Setor = request.POST.get('Setor')
            post.Gestor = request.POST.get('Gestor')
            post.email = request.POST.get('email')
            post.perm = request.POST.get('perm')
            post.funcao = request.POST.get('funcao')
            post.num_tel = request.POST.get('num_tel')
            post.save()
            return redirect('perfil')
    try:
        el = Perfil.objects.get(user = request.user.username)
    except:
        el = None
    form = PerfilForm()
    return render(request, 'perfil.html', {'dado':el, 'form':form})  



@login_required(login_url="login/")
def configurate(request):
    if request.user.has_perm('Hse.add_hse'):
        return render(request, 'conf.html')
    else:
        if request.user.first_name:
            return redirect('home_empresa')
        else:
            return redirect('hse')

@login_required(login_url="login/")
def usuarios(request):
    users = User.objects.all()
    perfil = Perfil.objects.all()
    form = PerfilForm()
    return render(request, 'usuarios.html', {'form':form, 'users': users, 'perfil':perfil})


def new_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('perfil')
    else:
        form = UserCreationForm()
    return render(request, 'new_user.html', {'form': form})


@login_required(login_url="login/")
def alt_perm(request, id):
    print(id)
    print(request.POST.get('perm'))
    print(request.POST.get('diff'))
    el = Perfil.objects.get(id=id)
    el.perm = request.POST.get('perm')
    el.save()
    u = User.objects.get(username=request.POST.get('diff'))
    if request.POST.get('perm') == "HSE":
        permissions =  Permission.objects.get(codename='add_hse')
    if request.POST.get('perm') == "POR":
        permissions =  Permission.objects.get(codename='add_portaria')
    if request.POST.get('perm') == "SIG":
        permissions =  Permission.objects.get(codename='add_perfil')
    print(permissions)
    u.user_permissions.add(permissions)
    return redirect('usuarios')


def decide(request):
    bias = request.user.first_name
    if bias:
        return redirect('cadastro_empresa')
    else:
        return redirect('perfil')