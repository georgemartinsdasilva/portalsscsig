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
from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Q
from django.shortcuts import render
from django.conf import settings

def decodif(value): 
    b = base64.b64decode(value.encode('utf-8')).decode("utf-8", "ignore")
    c = base64.b64decode(b).decode("utf-8", "ignore")
    d = base64.b64decode(c).decode("utf-8", "ignore")
    return d

def encoder(value): 
    a = base64.b64encode(bytes(value, "utf-8"))
    b = base64.b64encode(bytes(a.decode('utf-8'), "utf-8"))
    c = base64.b64encode(bytes(b.decode('utf-8'), "utf-8"))
    return c.decode('utf-8')

def dias(data1, data2):
    intg = dias_integracao.objects.all().last()
    dict = {'Seg':intg.Seg, 'Ter':intg.Ter, 'Qua':intg.Qua , 'Qui':intg.Qui , 'Sex':intg.Sex , 'Sab':intg.Sab , 'Dom':intg.Dom}
    sel = []
    for key, values in dict.items():
        if len(values) >> 2 :
            print(key, values)
            sel.append(values)
    qt_days = (data1 - data2).days
    aux = 0
    diict = {}
    aux_date = data2
    while aux < qt_days:
        more1 = aux_date + timedelta(days=1)
        for el in sel:
            if more1.strftime('%A') == el:
                diict.update({more1:more1.strftime('%A')})
        aux_date = more1
        aux = aux + 1        
    return diict
        
        
 #       if qt_days < 0:
  #      return "out"
   # elif qt_days == 0:
   #     return "out"
   # else:
   #     aux = 0