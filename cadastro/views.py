from django.shortcuts import render
from cadastro.forms import empresaForm, New_Solic_cad,  funcionarioForm, documentoForm, docsF, cad_respF
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from mail_templated import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.template import Context
from django.shortcuts import redirect 
from cadastro.models import empresa_terc, funcionario, docs, documento, cad_resp
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from Hse.models import msg, aux_table
import os
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from Hse.lib import decodif, encoder





def cadastro_empresa(request):
    empr = empresa_terc.objects.filter(usuario=request.user.username)   
    if request.method == 'POST':
        form = empresaForm(request.POST)
        form1 = documentoForm(request.POST, request.FILES)
        print (form1.errors)
        print(request.FILES.get('arquivo_documento'))
        if empr.count() > 0:
            if form.is_valid():
                print("aaa")
                empr.nome_empresa = request.POST.get('nome_empresa')
                empr.cnpj = request.POST.get('cnpj')
                empr.telefone = request.POST.get('telefone')
                empr.email = request.POST.get('email')
                empr.save()
        else:
            print (form.errors)
            if form.is_valid():
                post = form.save(commit=False)
                post.usuario = request.user.username
                post.save()
                return redirect('cadastro_empresa')
        if form1.is_valid():
            empr = empresa_terc.objects.get(usuario=request.user.username)
            post = form1.save(commit=False)
            post.arquivo_documento = request.FILES.get('arquivo_documento')
            post.funcionario = 9999
            post.emp = empr.id
            post.enviado = request.POST.get('enviado')
            post.nome_documento = request.POST.get('nome_documento')
            post.save()
            return redirect('cadastro_empresa')
    else: 

        print("first load")
        
    a_docs = docs.objects.filter(tipo = "D").values_list('nome', flat=True)
    b_docs = docs.objects.all()
    dict = {}
    nome = '' 
    cnpj = ''
    telefone = ''
    email = ''
    eer = ''
    jv = ''
    if empr.count() > 0:
        empr = empresa_terc.objects.get(usuario=request.user.username)
        jv = empr.id
        aux = documento.objects.filter(emp = empr.id)
        arr = []
        for dc in a_docs:
            arr.append(dc)
        i = 0
        cont = 0
        while i < len(arr):
            key = arr[i]
            dict.setdefault(key, [])
            for fb in aux:
                if fb.nome_documento == arr[i]:
                    cont = cont + 1
                    dict[key].append(fb.arquivo_documento)
            cont = 0
            i += 1
        nome = empr.nome_empresa 
        cnpj = empr.cnpj
        telefone = empr.telefone
        email = empr.email
    form1 = documentoForm()
    form = empresaForm()
    resp = cad_resp.objects.all()
    return render(request, 'cadastro_empresa.html', {'resp':resp, 'empr_aux':jv , 'form': form,'form1': form1,'dict1': dict,'nome':nome, 'cnpj':cnpj, 'telefone':telefone, 'email':email})

def cad_resp_view(request):
     if request.method == 'POST': 
        form = cad_respF(request.POST)
        print (form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('cadastro_empresa')
        return redirect('cadastro_empresa')        


def solicita(request):
    if request.method == 'POST': 
        form = UserCreationForm(request.POST)
        form1 = New_Solic_cad(request.POST)
        print (form.errors)
        if form.is_valid():
            post1 = form.save(commit=False)
            post1.first_name = 'first_access'
            post1.save()
            if request.POST.get('Contato'):
                if form1.is_valid():
                    Contato = request.POST.get('Contato')
                    Obs = request.POST.get('Obs')
                    post = form1.save(commit=False)
                    post.Solicitante = request.user
                    post.save()
                    print(request.POST.get('username'))
                    context = {
                        'contato': Contato,
                        'emp': 'rrrr',
                        'solicitante': request.user.username,
                        'obs': Obs,
                        'rec': request.POST.get('username')
                        }
                    message = EmailMessage('SOLICTA_EMP_MAIL.html', context, settings.EMAIL_HOST_USER, ['eng_diego@live.com', 'gmartins86@gmail.com',], render=True )
                    f = '/SIG_1.png'
                    fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
                    msg_img = MIMEImage(fp.read())
                    fp.close()
                    msg_img.add_header('Content-ID', '<{}>'.format(f))
                    message.attach(msg_img)
                    message.send()
                    return render(request, 'success.html', {'Usmail':request.user.email, 'Solmail':post1.username})
            else:
                form = UserCreationForm()
                form1 = New_Solic_cad()
                return render(request, 'Nsuccess.html')
        else:
            form = UserCreationForm()
            form1 = New_Solic_cad()
            return render(request, 'Nsuccess.html')
    else:
            form = UserCreationForm()
            form1 = New_Solic_cad()
    return render(request, 'solicita.html', {'form': form,'form1':form1})


def colaboradores(request):
    emp = empresa_terc.objects.get(usuario=request.user.username)
    fun = funcionario.objects.filter(empresa_id=emp.id)
    return render(request, 'colaboradores.html',{'fun':fun,'emp':emp.id})

def exlude_fun(request, id):
    fun = funcionario.objects.get(id=id)
    aux = aux_table.objects.filter(id_col=id)
    for el in aux:
        aux.delete()
    fun.delete()

    return redirect('colaboradores',)

def exlude_doc(request, idG):
    id = decodif(idG)
    docu = docs.objects.get(id=id)
    docu.delete()
    return redirect('cad_docs',)



def novo_fun(request):
    emp = empresa_terc.objects.get(usuario=request.user.username)
    print(emp.id)
    if request.method == 'POST':
        form = funcionarioForm(request.POST)
        print (form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.empresa_id = emp.id
            #post.data_int = "None"
            post.save()
            return redirect('colaboradores')
    else:        
        form = funcionarioForm()
        resp = cad_resp.objects.filter(empresa_resp=emp.id)
        print(resp)
    return render(request, 'novo_fun.html', {'resp':resp, 'form': form})






def documentacao(request, idG, empG):
    id = decodif(idG) # id do funcionário
    emp = decodif(empG) # cód da empresa
    fun = funcionario.objects.get(id=id)
    resp = cad_resp.objects.get(id=fun.resp_id)
    print(resp)
    empr = empresa_terc.objects.get(id=emp)
    print(empr)
    print(fun.empresa_id)
    if request.method == 'POST':
        form = documentoForm(request.POST, request.FILES)
        print (form.errors)
        print(request.FILES.get('arquivo_documento'))
        if form.is_valid():
            post = form.save(commit=False)
            post.arquivo_documento = request.FILES.get('arquivo_documento')
            post.funcionario = id
            post.email_resp = resp.email_resp
            post.email_emp = empr.email
            post.enviado = request.POST.get('enviado')
            post.nome_documento = request.POST.get('nome_documento')
            post.emp = request.POST.get('emp')
            post.save()
            fun.status = "AG"
            fun.save()
            aux1 = encoder(id)
            aux2 = encoder(emp)
            return redirect('documentacao', aux1, aux2)
    else:
        form = documentoForm()
        a_docs = docs.objects.filter(tipo = "B").values_list('nome', flat=True)
        c_docs = docs.objects.filter(tipo = "C")
        b_docs = docs.objects.all()
        envs = documento.objects.filter(funcionario = id)
        msgs = msg.objects.filter(id_col=id, tipo="lib")
        print(fun.data_int)
        return render(request, 'documentacao.html',{'fun_data':fun.data_int, 'msgs':msgs, 'a_docs':a_docs,'c_docs':c_docs, 'fun':fun , 'envs':envs,  'form': form, 'id': id,'emp':emp })




def cad_docs(request):
    docu = docs.objects.all()
    if request.method == 'POST':
        form = docsF(request.POST)
        print (form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('cad_docs')
    else:        
        form = docsF()
    return render(request, 'cad_docs.html', {'docu':docu, 'form': form})