import datetime
import base64
import os
from datetime import date
from django.utils import timezone
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from Hse.forms import chamado_hseForm, aux_tableForm, msgForm, email_hse_Form, dias_integracao_FORM
from cadastro.models import empresa_terc, documento, funcionario, docs, docs_integracao, cad_resp, bloq_hse
from usuario.models import Perfil
from Hse.models import chamado_hse, aux_table, logs, msg, email_hse, dias_integracao
from cadastro.forms import documentoForm, doc_Int_Form, bloq_hse_FORM
from django.http import HttpResponseRedirect
from datetime import date, datetime, time, timedelta
from django.contrib.auth.models import User
from django.core import serializers
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from mail_templated import send_mail
from mail_templated import EmailMessage
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from Hse.lib import decodif, encoder, dias
from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Q
from django.shortcuts import render
from django.conf import settings
from Hse.serializers import PortSerializer
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

scheduler = BackgroundScheduler()

def my_job():
    doc = documento.objects.all()
    datafk0 = datetime.strptime("11/01/2020", '%d/%m/%Y').date()
    datafk1 = datetime.strptime("03/01/2020", '%d/%m/%Y').date()
    datafk2 = datetime.strptime("01/01/2020", '%d/%m/%Y').date()
    Zero = (datafk2 - datafk2).days
    Dois = (datafk1 - datafk2).days
    Dez =  (datafk0 - datafk2).days

    for el in doc:
        data = datetime.strptime(el.validade_documento, '%d/%m/%Y').date()
        d1 = datetime.strptime(timezone.localtime().strftime('%Y-%m-%d'), "%Y-%m-%d").date()
        prazo = (data - d1).days
        if prazo < Dois:
            msg = "no limite do prazo da validade e faltam 2 dias para vencer"
            if prazo < Zero: #   SE VALIDADE DOCUMENTO REALMENTE VENCIDA
                fun = funcionario.objects.get(id=el.funcionario) # SELEÇÃO FUNCIONÁRIO
                fun.status = 'RP'  # ALTERAR STATUS FUNCIONÁRIO
                fun.save()  # SALVA FUNCIONÁRIO
                msg = "vencido, e colaborador tornou-se inapto para realizar trabalhos na Sig Combibloc"
                el.hse = "RP"
                el.save()
            verif = aux_table.objects.filter(~Q(status="Concluído"))
            array = ['eng_diego@live.com', 'gmartins86@gmail.com', el.email_emp, el.email_resp]
            for item in verif:
                if str(item.id_col).strip() == str(el.funcionario).strip():
                    array.append(item.email_resp_cham)
            context = {
                    'txt': 'verif automática',
                    'el':el,
                    'msg':msg,
                    }
            #print(set(array))
           
            #message = EmailMessage('Val_check_Mail.html', context, settings.EMAIL_HOST_USER, set(array), render=True )
            #f = '/SIG_1.png'
            #fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
            #msg_img = MIMEImage(fp.read())
            #fp.close()
            #msg_img.add_header('Content-ID', '<{}>'.format(f))
            #message.attach(msg_img)
            #message.send()
    qry = email_hse.objects.filter(ativo=True)
    fb = docs_integracao.objects.all()
    for doc in fb:
        data = doc.validade_documento
        val = data + timedelta(days=365)
        d1 = datetime.strptime(timezone.localtime().strftime('%Y-%m-%d'), "%Y-%m-%d").date()
        prazo = (val - d1).days
        if prazo < Dez:
            msg = "no limite do prazo da validade e faltam 10 dias para vencer"
            if prazo < Zero: #   SE VALIDADE DOCUMENTO REALMENTE VENCIDA
                fun = funcionario.objects.get(id=doc.funcionario) # SELEÇÃO FUNCIONÁRIO
                fun.status = 'RP'  # ALTERAR STATUS FUNCIONÁRIO
                fun.save()  # SALVA FUNCIONÁRIO
                msg = "vencido, e colaborador tornou-se inapto para realizar trabalhos na Sig Combibloc"
                doc.status = 0
                doc.save()
            ema = email_hse.objects.all()
            array = ['eng_diego@live.com', 'gmartins86@gmail.com', doc.email_emp, doc.email_resp]
            for item in ema:
                    array.append(item.email)
            context = {
                    'txt': 'verif automática',
                    'el':doc,
                    'msg':msg,
                    }
            print(set(array))
           
            #message = EmailMessage('Val_check_Mail.html', context, settings.EMAIL_HOST_USER, set(array), render=True )
            #f = '/SIG_1.png'
            #fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
            #msg_img = MIMEImage(fp.read())
            #fp.close()
            #msg_img.add_header('Content-ID', '<{}>'.format(f))
            #message.attach(msg_img)
            #message.send()
scheduler.add_job(my_job, 'interval', seconds=5)
scheduler.start()

def hse(request):
	return render(request, 'hse.html')

def novo_chamado_hse(request):
    args = Perfil.objects.filter(user=request.user.username)
    print(args)
    if args.count() > 0:
        if request.method == 'POST':
            form = chamado_hseForm(request.POST)
            print (form.errors)
            if form.is_valid():
                post = form.save(commit=False)
                Emp = empresa_terc.objects.filter(id=post.empresa_id)[0]
                post.setor_solicitante = request.POST.get('setor_solicitante')
                post.gestor_solicitante = request.POST.get('gestor_solicitante')
                post.fone_solicitante = request.POST.get('fone_solicitante')
                post.status = 'Aguardando Terceiro'
                post.tempo_estimado = request.POST.get('tempo_estimado')
                print(request.POST.get('tempo_estimado'))
                post.email_terc = Emp.email
                post.solicitante = request.user
                post.email_solicitante = request.user.email
                post.save()
                print(post.id)
                obj= chamado_hse.objects.get(id = post.id)
                log = logs(num_cham=str(obj.id), ator=request.user.username, acao= "Abertura Chamado", tipo="open")
                log.id = None
                log.save()
                data = datetime.strptime(request.POST.get('tempo_estimado'), '%m/%d/%Y')
                dt = datetime.combine(data, time(00, 00)) - timedelta(days=4)
                arr = []
                dict = {}
                cont = 0
                for x in request.POST.getlist('tipo_servico'):
                    if x == '1':
                        arr.insert(cont,'Trabalho em alta tensão e eletricidade')
                        dict = {'CURSO DE ELETRICISTA':'Trabalho em alta tensão e eletricidade','ASO ALTA TENSÃO':'Trabalho em alta tensão e eletricidade','CURSO NR 10 OU RECICLAGEM':'Trabalho em alta tensão e eletricidade',}
                    if x == '2':
                        arr.insert(cont,'Trabalhos em altura')
                        cont = cont + 1            
                        dict.update({'CERTIFICADO TREINAMENTO NR35':'Trabalhos em altura','ASO TRABALHOS EM ALTURA':'Trabalhos em altura','FICHA DE EPI':'Trabalhos em altura',})
                    if x == '3':
                        arr.insert(cont,'Espaços confinados') 
                        cont = cont + 1           
                        dict.update({'CERTIFICADO TREINAMENTO DE VIGIA':'Espaços confinados','ASO ESPAÇO CONFINADO':'Espaços confinados','FICHA DE EPI':'Espaços confinados',})
                    if x == '4':
                        arr.insert(cont,'Operação de empilhadeira') 
                        cont = cont + 1           
                        dict.update({'ASO DA ADMISSÃO':'Operação de empilhadeira','CERTIFICADO OPERADOR EMPILHADEIRA':'Operação de empilhadeira',})
                    if x == '5':
                        arr.insert(cont,'Trabalhos com plataformas elevatórias')
                        cont = cont + 1
                        dict.update({'CURSO OPERADOR PLATAFORMA ELEVATÓRIA':'Trabalhos com plataformas elevatórias','ASO DA ADMISSÃO':'Trabalhos com plataformas elevatórias',})
                    if x == '6':
                        arr.insert(cont,'Operação de guindaste ou munck')
                        cont = cont + 1
                        dict.update({'CURSO DE GUINDASTE E/OU MUNCK':'Operação de guindaste ou munck','ASO DA ADMISSÃO':'Operação de guindaste ou munck','RINGGING PARA GUINDASTES':'Operação de guindaste ou munck',})
                    if x == '7':
                        arr.insert(cont,'Trabalhador autônomo - Firma individual')
                        cont = cont + 1
                        dict.update({'REGISTRO DA PREFEITURA':'Trabalhador autônomo - Firma individual','ASO':'Trabalhador autônomo - Firma individual','NÚMERO DE MATRÍCULA INSS':'Trabalhador autônomo - Firma individual',})
                    if x == '8':
                        arr.insert(cont,'Assistência Técnica - mautenção')
                        cont = cont + 1
                        dict.update({'CRACHÁ OU CARTEIRA PROFISSIONAL':'Assistência Técnica - mautenção','ASO':'Assistência Técnica - mautenção',})
                    if x == '9':
                        arr.insert(cont,'Soldador')
                        cont = cont + 1
                        dict.update({'PPRA DE SOLDA':'Soldador','COMPROVANTE DE CURSO OU EXPERIÊNCIA':'Soldador','FICHA DE EPI SOLDA':'Soldador',})
                qx = empresa_terc.objects.all()
                context = {
                    'solicitante': request.user.username,
                    'emp': Emp.nome_empresa,
                    'nome_proj': request.POST.get('nome_proj'),
                    'data_term': dt,
                    'obs': request.POST.get('descricao'),
                    'dict':dict,
                    'arr':arr,
                    'obj':obj,
                    'emp_id': post.empresa_id,
                    'qx': qx,
                    }
                message = EmailMessage('novo_chamEMAIL.html', context, settings.EMAIL_HOST_USER, [Emp.email,'eng_diego@live.com', 'gmartins86@gmail.com',], render=True )
                f = '/SIG_1.png'
                fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
                msg_img = MIMEImage(fp.read())
                fp.close()
                msg_img.add_header('Content-ID', '<{}>'.format(f))
                message.attach(msg_img)
                message.send()
                return redirect('show_cham_sol', "None")
        else:        
            form = chamado_hseForm()
        args = Perfil.objects.all()
        return render(request, 'novo_chamdo_hse.html', {'form': form, 'dado':args})
    else:
        return redirect('perfil')
        


def home_empresa(request):
	return render(request, 'home_empresa.html')


def show_cham_sol(request, nr):
    if nr == 'None':
        obj= chamado_hse.objects.filter(solicitante = request.user).latest('data_abertura')
    else:
        nu = decodif(nr)
        obj= chamado_hse.objects.get(id = nu)        
    arr = []
    dict = {}
    cont = 0
    for x in obj.tipo_servico:
        if x == '1':
            arr.insert(cont,'Trabalho em alta tensão e eletricidade')
            dict = {'CURSO DE ELETRICISTA':'Trabalho em alta tensão e eletricidade','ASO ALTA TENSÃO':'Trabalho em alta tensão e eletricidade','CURSO NR 10 OU RECICLAGEM':'Trabalho em alta tensão e eletricidade',}
        if x == '2':
            arr.insert(cont,'Trabalhos em altura')
            cont = cont + 1            
            dict.update({'CERTIFICADO TREINAMENTO NR35':'Trabalhos em altura','ASO TRABALHOS EM ALTURA':'Trabalhos em altura','FICHA DE EPI':'Trabalhos em altura',})
        if x == '3':
            arr.insert(cont,'Espaços confinados') 
            cont = cont + 1           
            dict.update({'CERTIFICADO TREINAMENTO DE VIGIA':'Espaços confinados','ASO ESPAÇO CONFINADO':'Espaços confinados','FICHA DE EPI':'Espaços confinados',})
        if x == '4':
            arr.insert(cont,'Operação de empilhadeira') 
            cont = cont + 1           
            dict.update({'ASO DA ADMISSÃO':'Operação de empilhadeira','CERTIFICADO OPERADOR EMPILHADEIRA':'Operação de empilhadeira',})
        if x == '5':
            arr.insert(cont,'Trabalhos com plataformas elevatórias')
            cont = cont + 1
            dict.update({'CURSO OPERADOR PLATAFORMA ELEVATÓRIA':'Trabalhos com plataformas elevatórias','ASO DA ADMISSÃO':'Trabalhos com plataformas elevatórias',})
        if x == '6':
            arr.insert(cont,'Operação de guindaste ou munck')
            cont = cont + 1
            dict.update({'CURSO DE GUINDASTE E/OU MUNCK':'Operação de guindaste ou munck','ASO DA ADMISSÃO':'Operação de guindaste ou munck','RINGGING PARA GUINDASTES':'Operação de guindaste ou munck',})
        if x == '7':
            arr.insert(cont,'Trabalhador autônomo - Firma individual')
            cont = cont + 1
            dict.update({'REGISTRO DA PREFEITURA':'Trabalhador autônomo - Firma individual','ASO':'Trabalhador autônomo - Firma individual','NÚMERO DE MATRÍCULA INSS':'Trabalhador autônomo - Firma individual',})
        if x == '8':
            arr.insert(cont,'Assistência Técnica - mautenção')
            cont = cont + 1
            dict.update({'CRACHÁ OU CARTEIRA PROFISSIONAL':'Assistência Técnica - mautenção','ASO':'Assistência Técnica - mautenção',})
        if x == '9':
            arr.insert(cont,'Soldador')
            cont = cont + 1
            dict.update({'PPRA DE SOLDA':'Soldador','COMPROVANTE DE CURSO OU EXPERIÊNCIA':'Soldador','FICHA DE EPI SOLDA':'Soldador',})
    emp = empresa_terc.objects.all()
    N_CHM = '%0*d' % (5, obj.id)
    mycham= chamado_hse.objects.filter(solicitante = request.user)
    data = datetime.strptime(obj.tempo_estimado, '%m/%d/%Y')
    dt = datetime.combine(data, time(00, 00)) - timedelta(days=4)
    minus4 = dt.date() - timedelta(days=4) 
    minus6 = dt.date() - timedelta(days=6)  
    d1 = datetime.strptime(timezone.localtime().strftime('%Y-%m-%d'), "%Y-%m-%d").date()
    d2 = datetime.strptime(minus6.strftime('%Y-%m-%d'), "%Y-%m-%d").date()
    rest = (d2 - d1).days
    if rest > 0:
         rest = "RESTAM   " + str(abs((d1 - d2).days))
    elif rest == 0:
        rest = "VENCIMENTO HOJE !"
    else:
        
        rest = "ATRASADO !   " + str(abs((d1 - d2).days))
    print(minus6)
    obj.data  = minus6
    obj.save()
    colab = aux_table.objects.filter(num_cham = obj.id)
    msgs = msg.objects.filter(num_cham = obj.id)
    log = logs.objects.filter(num_cham = obj.id)
    #Us = User.objects.get(username=obj.gestor_solicitante)'Em_g':Us.email,
    resp = cad_resp.objects.all()
    return render(request, 'show_cham_sol.html', {'resp':resp, 'd1':d1,  'dw':data.date(), 'log':log,'msgs':msgs,'colab':colab,'obj':obj,'N_CHM':N_CHM,'emp':emp,'mycham':mycham,'minus4':minus4,'minus6':minus6,'rest':rest,'arr':arr,'dict':dict})

def show_my_cham(request, num_chamG, idG):
    if num_chamG == "None":
        try:
            obj= chamado_hse.objects.all().latest('data_abertura')
        except chamado_hse.DoesNotExist:
            raise Http404("Nenhum Chamado Existente para sua Empresa.")
    else:
        num_cham = decodif(num_chamG)
        obj= chamado_hse.objects.get(id = num_cham)
    id = decodif(idG)
    arr = []
    dict = {}
    cont = 0
    for x in obj.tipo_servico:
        if x == '1':
            arr.insert(cont,'Trabalho em alta tensão e eletricidade')
            dict = {'CURSO DE ELETRICISTA':'Trabalho em alta tensão e eletricidade','ASO ALTA TENSÃO':'Trabalho em alta tensão e eletricidade','CURSO NR 10 OU RECICLAGEM':'Trabalho em alta tensão e eletricidade',}
        if x == '2':
            arr.insert(cont,'Trabalhos em altura')
            cont = cont + 1            
            dict.update({'CERTIFICADO TREINAMENTO NR35':'Trabalhos em altura','ASO TRABALHOS EM ALTURA':'Trabalhos em altura','FICHA DE EPI':'Trabalhos em altura',})
        if x == '3':
            arr.insert(cont,'Espaços confinados') 
            cont = cont + 1           
            dict.update({'CERTIFICADO TREINAMENTO DE VIGIA':'Espaços confinados','ASO ESPAÇO CONFINADO':'Espaços confinados','FICHA DE EPI':'Espaços confinados',})
        if x == '4':
            arr.insert(cont,'Operação de empilhadeira') 
            cont = cont + 1           
            dict.update({'ASO DA ADMISSÃO':'Operação de empilhadeira','CERTIFICADO OPERADOR EMPILHADEIRA':'Operação de empilhadeira',})
        if x == '5':
            arr.insert(cont,'Trabalhos com plataformas elevatórias')
            cont = cont + 1
            dict.update({'CURSO OPERADOR PLATAFORMA ELEVATÓRIA':'Trabalhos com plataformas elevatórias','ASO DA ADMISSÃO':'Trabalhos com plataformas elevatórias',})
        if x == '6':
            arr.insert(cont,'Operação de guindaste ou munck')
            cont = cont + 1
            dict.update({'CURSO DE GUINDASTE E/OU MUNCK':'Operação de guindaste ou munck','ASO DA ADMISSÃO':'Operação de guindaste ou munck','RINGGING PARA GUINDASTES':'Operação de guindaste ou munck',})
        if x == '7':
            arr.insert(cont,'Trabalhador autônomo - Firma individual')
            cont = cont + 1
            dict.update({'REGISTRO DA PREFEITURA':'Trabalhador autônomo - Firma individual','ASO':'Trabalhador autônomo - Firma individual','NÚMERO DE MATRÍCULA INSS':'Trabalhador autônomo - Firma individual',})
        if x == '8':
            arr.insert(cont,'Assistência Técnica - mautenção')
            cont = cont + 1
            dict.update({'CRACHÁ OU CARTEIRA PROFISSIONAL':'Assistência Técnica - mautenção','ASO':'Assistência Técnica - mautenção',})
        if x == '9':
            arr.insert(cont,'Soldador')
            cont = cont + 1
            dict.update({'PPRA DE SOLDA':'Soldador','COMPROVANTE DE CURSO OU EXPERIÊNCIA':'Soldador','FICHA DE EPI SOLDA':'Soldador',})
    emp = empresa_terc.objects.all()
    N_CHM = '%0*d' % (5, obj.id)
    mycham= chamado_hse.objects.filter(empresa_id = id)
    data = datetime.strptime(obj.tempo_estimado, '%m/%d/%Y')
    dt = datetime.combine(data, time(00, 00)) - timedelta(days=4)
    minus4 = dt.date() - timedelta(days=4) 
    minus6 = dt.date() - timedelta(days=6)  
    d1 = datetime.strptime(timezone.localtime().strftime('%Y-%m-%d'), "%Y-%m-%d").date()
    d2 = datetime.strptime(minus6.strftime('%Y-%m-%d'), "%Y-%m-%d").date()



    qt = dias(data.date(), obj.data_abertura.date())
    alist = list(sorted(qt.keys()))



    rest = (d2 - d1).days
    if rest > 0:
         rest = "RESTAM   " + str(abs((d1 - d2).days))
    elif rest == 0:
        rest = "VENCIMENTO HOJE !"
    else:
        rest = "ATRASADO !   " + str(abs((d1 - d2).days))
    obj.data  = minus6
    obj.save()
    fun = funcionario.objects.filter(Q(empresa_id = id) & ~Q(rg="BLOQUEADO"))
    dc = chamado_hse.objects.filter(empresa_id = id)
    colab = aux_table.objects.filter(num_cham = obj.id)
    log = logs.objects.filter(num_cham = obj.id)
    msgs = msg.objects.filter(num_cham = obj.id)
    func = funcionario.objects.filter(empresa_id=id)
    #Us = User.objects.get(username=obj.gestor_solicitante)'Em_g':Us.email,
    respo = cad_resp.objects.filter(empresa_resp=id)
    return render(request, 'chamados.html', {'qt':alist, 'respo':respo, 'dw':data.date(), 'func':func, 'msgs':msgs,'log':log,'colab':colab,'id':id,'fun':fun,'obj':obj,'N_CHM':N_CHM,'emp':emp,'mycham':mycham,'minus4':minus4,'minus6':minus6,'rest':rest,'arr':arr,'dict':dict})


def meus_chamados(request):
    mycham= chamado_hse.objects.filter(solicitante = request.user)
    emp  = empresa_terc.objects.all()
    return render(request, 'meus_chamados.html', {'mycham':mycham, 'emp':emp})

def include_col(request, id, num):
    lm = request.POST.get('num_cham') #recebe o número do chamado
    fun = request.POST.getlist('colab[]') # recebe os colaboradores selecionados
    key = request.POST.get('tps')#recebe o tipo de serviço relacionado
    arr1 = []
    try:
        data = aux_table.objects.filter(num_cham = lm, tps = key)
    except:
        data = None
    if data:
        for rec in data:
            rec.delete()
        cont = 0
        num_cham = lm
        for fb in fun:
            x = fb
            a,b = x.split(",")
            arr1.append(a)
            action = ""
            aux = (a +";")
            action = action  + aux
            form = aux_tableForm(request.POST)
            print (form.errors)
            if form.is_valid():
                post = form.save(commit=False)
                post.colab = a
                post.id_col = b
                post.save()
                y =  action 
        log = logs(num_cham=str(lm), ator=request.user.username, acao= str(arr1), tipo="add_col")
        log.id = None
        log.save()
        ab = encoder(str(num_cham))
        cb = encoder(str(id))
        return redirect('show_my_cham', ab, cb)
    else:
        num_cham = lm
        for fb in fun:
            x = fb
            a,b = x.split(",")
            arr1.append(a)
            form = aux_tableForm(request.POST)
            print (form.errors)
            print("adding:"+a+", with id:"+b)
            if form.is_valid():
                post = form.save(commit=False)
                post.colab = a
                post.id_col = b
                post.save()
        log = logs(num_cham=str(lm), ator=request.user.username, acao= str(arr1), tipo="add_col")
        log.id = None
        log.save()
        ab = encoder(str(num_cham))
        cb = encoder(str(id))
        return redirect('show_my_cham', ab, cb)              

def cad_docs(request):
    if request.method == 'POST':
        form = docsF(request.POST)
        print (form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            
            post.save()
            return redirect('cad_docs')
    else:        
        form = docsF()
    return render(request, 'cad_docs.html', {'form': form})



def message(request, id, num):
    if request.method == 'POST':
        form = msgForm(request.POST)
        print (form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.data = timezone.now()
            post.ator = request.user.username
            post.save()
            log = logs(num_cham=str(num), ator=request.user.username, acao= request.POST.get("msg"), tipo="msg")
            log.id = None
            log.save()
            aux1 = encoder(str(num))
            aux2 = encoder(str(id))
            return redirect('show_my_cham', aux1, aux2)
    else:        
        form = msgForm()
        aux1 = encoder(str(num))
        aux2 = encoder(str(id))
    return redirect('show_my_cham', aux1, aux2)

def message_sol(request, num, orig):
    if request.method == 'POST':
        form = msgForm(request.POST)
        bas = request.POST.getlist('ema[]')
        bas = list(set(bas))
        for hn in bas:
            print(hn)
        print (form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.data = timezone.now()
            if request.POST.get('fun'):
                post.id_col = request.POST.get('fun')
                post.tipo = "lib"
            else:
                post.id_col = "123"
                post.tipo = "123"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
            post.ator = request.user.username
            post.save()
            log = logs(num_cham=str(num), ator=request.user.username, acao= request.POST.get("msg"), tipo="msg")
            log.id = None
            log.save()
            if orig == "f_terc":
                pass
            else:
                obj = chamado_hse.objects.get(id=num)
            emp = empresa_terc.objects.all()
            if bas:
                context = {
                        'solicitante': request.user.username,
                        'emp': 'qwedsa',
                        'nome_proj': request.POST.get('nome_proj'),
                        'msg': request.POST.get("msg"),
                        'num': num,
                        'obj':obj,
                        'emp':emp,
                        }
                message = EmailMessage('MSG_EMAIL.html', context, settings.EMAIL_HOST_USER, bas, render=True )
                f = '/SIG_1.png'
                fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
                msg_img = MIMEImage(fp.read())
                fp.close()
                msg_img.add_header('Content-ID', '<{}>'.format(f))
                message.attach(msg_img)
                message.send() 
            if orig == "ter":
                aux1 = encoder(str(num))
                aux2 = encoder(request.POST.get('emp'))
                return redirect('show_my_cham', aux1, aux2)
            elif orig == "sol":
                aux1 = encoder(str(num))
                return redirect('show_cham_sol', aux1)
            elif orig == "f_terc":
                aux1 = encoder(request.POST.get('fun'))
                aux2 = encoder(request.POST.get('empresa'))
                return redirect('documentacao', aux1, aux2)
    else:        
        form = msgForm()
        aux1 = encoder(str(num))
    return redirect('show_cham_sol', aux1)

def message_hse(request, id, num):
    if request.method == 'POST':
        form = msgForm(request.POST)
        print (form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.data = timezone.now()
            post.tipo = "123"
            post.id_col = "123"
            post.ator = request.user.username
            post.save()
            log = logs(num_cham=str(num), ator=request.user.username, acao= request.POST.get("msg"), tipo="msg")
            log.id = None
            log.save()
            aux1 = encoder(str(num))
            aux2 = encoder(str(id))
            return redirect('view_cham_hse', aux1, aux2)
    else:        
        form = msgForm()
        aux1 = encoder(str(num))
        aux2 = encoder(str(id))
    return redirect('view_cham_hse', aux1, aux2)



@permission_required('Hse.add_hse', login_url="/hse/")
def gestao(request):
    mycham= chamado_hse.objects.all()
    emp = empresa_terc.objects.all()
    fun = funcionario.objects.filter(~Q(rg="BLOQUEADO"))
    return render(request, 'gestão.html', {'fun':fun, 'mycham':mycham, 'emp':emp})


                       
# TODO: Add more useful commands here.



def view_cham_hse(request, numG, idG):
    num = decodif(numG)
    id = decodif(idG)
    obj= chamado_hse.objects.get(id = num)
    arr = []
    dict = {}
    cont = 0
    for x in obj.tipo_servico:
        if x == '1':
            arr.insert(cont,'Trabalho em alta tensão e eletricidade')
            dict = {'CURSO DE ELETRICISTA':'Trabalho em alta tensão e eletricidade','ASO ALTA TENSÃO':'Trabalho em alta tensão e eletricidade','CURSO NR 10 OU RECICLAGEM':'Trabalho em alta tensão e eletricidade',}
        if x == '2':
            arr.insert(cont,'Trabalhos em altura')
            cont = cont + 1            
            dict.update({'CERTIFICADO TREINAMENTO NR35':'Trabalhos em altura','ASO TRABALHOS EM ALTURA':'Trabalhos em altura','FICHA DE EPI':'Trabalhos em altura',})
        if x == '3':
            arr.insert(cont,'Espaços confinados') 
            cont = cont + 1           
            dict.update({'CERTIFICADO TREINAMENTO DE VIGIA':'Espaços confinados','ASO ESPAÇO CONFINADO':'Espaços confinados','FICHA DE EPI':'Espaços confinados',})
        if x == '4':
            arr.insert(cont,'Operação de empilhadeira') 
            cont = cont + 1           
            dict.update({'ASO DA ADMISSÃO':'Operação de empilhadeira','CERTIFICADO OPERADOR EMPILHADEIRA':'Operação de empilhadeira',})
        if x == '5':
            arr.insert(cont,'Trabalhos com plataformas elevatórias')
            cont = cont + 1
            dict.update({'CURSO OPERADOR PLATAFORMA ELEVATÓRIA':'Trabalhos com plataformas elevatórias','ASO DA ADMISSÃO':'Trabalhos com plataformas elevatórias',})
        if x == '6':
            arr.insert(cont,'Operação de guindaste ou munck')
            cont = cont + 1
            dict.update({'CURSO DE GUINDASTE E/OU MUNCK':'Operação de guindaste ou munck','ASO DA ADMISSÃO':'Operação de guindaste ou munck','RINGGING PARA GUINDASTES':'Operação de guindaste ou munck',})
        if x == '7':
            arr.insert(cont,'Trabalhador autônomo - Firma individual')
            cont = cont + 1
            dict.update({'REGISTRO DA PREFEITURA':'Trabalhador autônomo - Firma individual','ASO AUTONOMO':'Trabalhador autônomo - Firma individual','NÚMERO DE MATRÍCULA INSS':'Trabalhador autônomo - Firma individual',})
        if x == '8':
            arr.insert(cont,'Assistência Técnica - mautenção')
            cont = cont + 1
            dict.update({'CRACHÁ OU CARTEIRA PROFISSIONAL':'Assistência Técnica - mautenção','ASO ASSIST. TÉCNICA':'Assistência Técnica - mautenção',})
        if x == '9':
            arr.insert(cont,'Soldador')
            cont = cont + 1
            dict.update({'PPRA DE SOLDA':'Soldador','COMPROVANTE DE CURSO OU EXPERIÊNCIA':'Soldador','FICHA DE EPI SOLDA':'Soldador',})
    emp = empresa_terc.objects.all()
    N_CHM = '%0*d' % (5, obj.id)
    mycham= chamado_hse.objects.filter(solicitante = request.user)
    data = datetime.strptime(obj.tempo_estimado, '%m/%d/%Y')
    dt = datetime.combine(data, time(00, 00)) - timedelta(days=4)
    minus4 = dt.date() - timedelta(days=4) 
    minus6 = dt.date() - timedelta(days=6)  
    d1 = datetime.strptime(timezone.localtime().strftime('%Y-%m-%d'), "%Y-%m-%d").date()
    d2 = datetime.strptime(minus6.strftime('%Y-%m-%d'), "%Y-%m-%d").date()
    rest = abs((d1 - d2).days)
    colab = aux_table.objects.filter(num_cham = obj.id)
    func = funcionario.objects.filter(empresa_id=id)
    msgs = msg.objects.filter(num_cham = obj.id)
    log = logs.objects.filter(num_cham = obj.id)
    resp = cad_resp.objects.filter(empresa_resp=id)
    return render(request, 'view_cham_hse.html', {'resp':resp, 'dw':data.date(), 'func':func, 'log':log,'msgs':msgs,'colab':colab,'obj':obj,'N_CHM':N_CHM,'emp':emp,'mycham':mycham,'minus4':minus4,'minus6':minus6,'rest':rest,'arr':arr,'dict':dict,'id':id})


def documentosHse(request, idG):
    id = decodif(idG)
    fun = funcionario.objects.get(id=id)
    a_docs = docs.objects.filter(tipo = "B").values_list('nome', flat=True)
    c_docs = docs.objects.filter(tipo = "C").values_list('nome', flat=True)
    b_docs = docs.objects.all()
    aux = documento.objects.filter(funcionario = id)
    msgs = msg.objects.filter(tipo="lib", id_col=id)
    arr = []
    dict = {}
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
    arr1 = []
    dict1 = {}
    for dc in c_docs:
        arr1.append(dc)
    i = 0
    cont = 0
    while i < len(arr1):
        key = arr1[i]
        dict1.setdefault(key, [])
        for fb in aux:
            if fb.nome_documento == arr1[i]:
                cont = cont + 1
                dict1[key].append(fb.arquivo_documento)
        cont = 0
        i += 1
    try:
        el = docs_integracao.objects.get(funcionario=id)
    except:
        el = None
    print(id)
    return render(request, 'documentação1.html',{'fun_data':fun.data_int, 'el':el, 'msgs':msgs, 'fun':fun ,'arr': arr, 'dict': dict,'dict1': dict1, 'docs': b_docs, 'aux': aux,'id': id })


def saveCham(request, num, id):
    mycham= chamado_hse.objects.get(id=num)
    if mycham.resp_terc:
        wq = mycham.resp_terc
        respo = cad_resp.objects.get(id= str(wq))
        abc = respo.email_resp
    else:
        abc = "Res. não Informado" 
    print(abc)
    mycham.status = request.POST.get('gr')
    mycham.save()
    aux = aux_table.objects.filter(num_cham=num)
    for el in aux:
        el.status = request.POST.get('gr')
        el.email_resp_cham = abc
        el.save()
    mycham.save()
    emp = empresa_terc.objects.all()
    docs = documento.objects.filter(hse=1)
    gth = encoder(str(num))
    hhy = encoder(str(id))
    return redirect('view_cham_hse', gth, hhy)

def action(request, id):
    if request.POST.get('buton') == 'submeter':
        Forr = encoder(str(id))
        if request.POST.get('lib') == "BLOQ":
            return redirect('bloq_fun', Forr)
        fun = funcionario.objects.get(id=id)
        fun.status = request.POST.get('lib')
        fun.save()
        m1 = msg(num_cham=00, ator=request.user.username, msg=request.POST.get('messa'), tipo="lib", id_col=id)
        m1.id = None
        m1.save()
        #subject, from_email, to = 'Solicitação da Sig Combibloc para a '+ Contato, settings.EMAIL_HOST_USER, 'to@example.com'
        #text_content = 'This is an important message.'
        #msg = EmailMultiAlternatives(subject, text_content, from_email, ['eng_diego@live.com',post1.username])
        #         #msg.attach_alternative(html_content, "text/html")
        #msg.send()  
        Forr = encoder(str(id))
        print(Forr)
        print('111')
        return redirect('documentosHse', Forr)
    else:
        doc = request.POST.get('nome_documento')
        sel = request.POST.get('sel')
        validade = request.POST.get('Validade')
        if sel == "nada":
            Forr = encoder(str(id))
            print('222')
            return redirect('documentosHse', Forr)
        else:
            obj = documento.objects.get(funcionario=id, nome_documento=doc)
            obj.validade_documento = validade
            obj.hse = sel
            obj.save()
            Forr = encoder(str(id))
            print('333')
        return redirect('documentosHse', Forr)


@permission_required('Hse.add_portaria', login_url="/hse/")
def portaria(request):
    func = funcionario.objects.all()
    emp = empresa_terc.objects.all()
    return render(request, 'portaria.html', {'func':func, 'emp':emp})


def message_fun(request, id):
    if request.method == 'POST':
        form = msgForm(request.POST)
        print (form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.data = timezone.now()
            post.ator = request.user.username
            post.save()
            log = logs(num_cham=str(num), ator=request.user.username, acao= request.POST.get("msg"), tipo="msg")
            log.id = None
            log.save()
            Forr = encoder(str(id))
            return redirect('documentosHse', Forr)
    else:        
        form = msgForm()
        For = encoder(str(id))
    return redirect('documentosHse', For)



def doc_integracao(request, id):
    obj = funcionario.objects.get(id=id)
    emp = empresa_terc.objects.get(id=obj.empresa_id)
    resp = cad_resp.objects.get(id=obj.resp_id)
    try:
        el = docs_integracao.objects.get(funcionario=id)
    except:
        el = None
    if el:
        el.delete()
    if request.method == 'POST':
        form = doc_Int_Form(request.POST, request.FILES)
        print (form.errors)
        if form.is_valid():
            obj = funcionario.objects.get(id=id)
            post = form.save(commit=False)
            post.arquivo = request.FILES.get('arquivo')
            post.email_emp = emp.email
            post.email_resp = resp.email_resp
            post.funcionario = id
            post.validade_documento = datetime.strptime(request.POST.get('validade_documento'),"%d/%m/%Y").date()
            post.save()
            obj.data_int = datetime.strptime(request.POST.get('validade_documento'),"%d/%m/%Y").date()
            obj.save()
            print(datetime.strptime(request.POST.get('validade_documento'),"%d/%m/%Y").date())
            For = encoder(str(id))
            return redirect('documentosHse', For)
    else:
        For = encoder(str(id))
        return redirect('documentosHse', For)


def alter(request, num, id):
    el = chamado_hse.objects.get(id=num)
    el.status = "Aguardando HSE" 
    el.resp_terc = request.POST.get('resp') 
    if request.POST.get('cham') == "aaa":
        pass
    else:
        el.status = request.POST.get('cham')
    el.save()
    aux1 = encoder(str(num))
    aux2 = encoder(str(id))
    return redirect('show_my_cham', aux1,aux2)


def resp(request, idG):
    id = decodif(idG)
    respo = cad_resp.objects.get(id=id)
    emp = empresa_terc.objects.all()
    return render(request, 'resp.html', {'respo':respo,'emp':emp})

def colaborador(request, id):
    data = decodif(id)
    aux = aux_table.objects.filter(id_col=data)
    dist = aux_table.objects.values_list('num_cham', flat=True).distinct()
    obj = chamado_hse.objects.all()
    func = funcionario.objects.get(id=data)
    empw = empresa_terc.objects.all()
    return render(request, 'colaborador.html', {'data':data, 'aux':aux, 'obj':obj, 'dist':dist,'func':func,'empw':empw})       

def cad_email_hse_w(request):
    if request.method == 'POST':
        form = email_hse_Form(request.POST)
        print (form.errors)
        print(request.POST.get('Nome'))
        if form.is_valid():
            post = form.save(commit=False)
            post.Nome = request.POST.get('Nome')
            post.email = request.POST.get('email')
            post.ativo = request.POST.get('ativo')
            post.save()
            return redirect('cad_email_hse')
    else:        
        form = email_hse_Form()
    data = email_hse.objects.all()
    return render(request, 'cad_email_hse.html', {'data':data})       


def bloq_fun(request, idG):
    if request.method == 'POST':
        form = bloq_hse_FORM(request.POST)
        print (form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.fun = funcionario.objects.get(id=decodif(idG))
            post.motivo = request.POST.get('motivo')
            post.save()
            #message = EmailMessage('Val_check_Mail.html', context, settings.EMAIL_HOST_USER, set(array), render=True )
            #f = '/SIG_1.png'
            #fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
            #msg_img = MIMEImage(fp.read())
            #fp.close()
            #msg_img.add_header('Content-ID', '<{}>'.format(f))
            #message.attach(msg_img)
            #message.send()
            obj = funcionario.objects.get(id=decodif(idG))
            obj.rg = "BLOQUEADO"
            obj.status = "RP"
            obj.funcao = "BLOQUEADO PELO HSE"
            obj.save()
            mms = msg.objects.filter(id_col=decodif(idG))
            for el in mms:
                el.delete()
            mmg = msg(ator="Gestão HSE", msg= request.POST.get('motivo'), tipo="lib", id_col=decodif(idG))
            mmg.id = None
            mmg.save()
            dc = documento.objects.filter(funcionario=decodif(idG))
            for th in dc:
                th.delete()
            it = docs_integracao.objects.get(funcionario=decodif(idG))
            it.delete()
            return redirect('documentosHse', idG)
    else:        
        form = bloq_hse_FORM()
    data = bloq_hse.objects.all()
    return render(request, 'bloq_fun.html', {'data':data, 'form':form, 'fun': funcionario.objects.get(id=decodif(idG))})  

def configurate_hse(request):
    return render(request, 'configurate_hse.html')

def general_settings(request):
    form_dias = dias_integracao_FORM()
    data = bloq_hse.objects.all()
    dias = dias_integracao.objects.all()
    return render(request, 'general_settings.html', {'form_dias': form_dias, 'data':data, 'dias':dias})

def blocked(request):
    obj = bloq_hse.objects.all()
    fun = funcionario.objects.all()
    return render(request, 'blocked.html', {'obj':obj, 'fun':fun, 'time':timezone.localtime().date()})

def dias_integracao_w(request):
    if request.method == 'POST':
        form = dias_integracao_FORM(request.POST)
        print (form.errors)
        if form.is_valid():
            data = dias_integracao.objects.all()
            data.delete()
            post = form.save(commit=False)
            if request.POST.get('Seg'):
                post.Seg = "Monday"
            else:
                 post.Seg = " "
            if request.POST.get('Ter'):
                post.Ter = "Tuesday"
            else:
                 post.Ter = " "
            if request.POST.get('Qua'):
                post.Qua = "Wednesday"
            else:
                 post.Qua = " "
            if request.POST.get('Qui'):
                post.Qui = "Thursday"
            else:
                 post.Qui = " "
            if request.POST.get('Sex'):
                post.Sex = "Friday"
            else:
                 post.Sex = " "
            if request.POST.get('Sab'):
                post.Sab = "Saturday"
            else:
                 post.Sab = " "
            if request.POST.get('Dom'):
                post.Dom = "Sunday"
            else:
                 post.Dom = " "
            post.save()
    return redirect('general_settings')


def agendar_int(request, num_chamG, idG):
    data = request.POST.get('data')
    fun = request.POST.getlist('colab[]') # recebe os colaboradores selecionados
    print(data)
    print(fun)
    context = {
        'data':data,
        'fun':fun,
    }
    #message = EmailMessage('Val_check_Mail.html', context, settings.EMAIL_HOST_USER, set(array), render=True )
    #f = '/SIG_1.png'
    #fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
    #msg_img = MIMEImage(fp.read())
    #fp.close()
    #msg_img.add_header('Content-ID', '<{}>'.format(f))
    #message.attach(msg_img)
    #message.send()
    return redirect('show_my_cham', num_chamG, idG)



class portaria_table(viewsets.ModelViewSet):
    queryset = funcionario.objects.all()
    serializer_class = PortSerializer

    def list(self, request, **kwargs):
        try:
            music = query_musics_by_args(**request.query_params)
            serializer = MusicSerializer(music['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = music['draw']
            result['recordsTotal'] = music['total']
            result['recordsFiltered'] = music['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)