"""PortalSscSig URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path
from usuario.views import home
from usuario.forms import LoginForm
from django.conf.urls.static import static
from django.conf import settings
from Hse.views import hse, novo_chamado_hse, home_empresa, show_cham_sol, show_my_cham, meus_chamados, include_col, message, gestao, message_sol, documentosHse, view_cham_hse, message_hse, saveCham, action, portaria, message_fun, doc_integracao,alter, resp, colaborador, cad_email_hse_w, bloq_fun, configurate_hse, general_settings, blocked, dias_integracao_w, agendar_int, portaria_table
from cadastro.views import cadastro_empresa, solicita, colaboradores, novo_fun, documentacao, cad_docs, exlude_fun, cad_resp_view, exlude_doc
from usuario.views import perfil, configurate, usuarios, new_user, alt_perm, decide
from rest_framework.routers import DefaultRouter
from documentacao.views import base, my_view
router = DefaultRouter()
router.register(r'music', portaria_table)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', home, name='home'),
    path(r'hse/', hse, name='hse'),
    path(r'login/', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm,}, name='login'),
    path(r'logout', views.logout, {'next_page': '/login'}), 
    path(r'novo_chamado_hse', novo_chamado_hse, name='novo_chamado_hse'),
    path(r'home_empresa', home_empresa, name='home_empresa'),
    path(r'cadastro_empresa', cadastro_empresa, name='cadastro_empresa'),
    path(r'perfil', perfil, name='perfil'),
    path(r'show_cham_sol/<str:nr>', show_cham_sol, name='show_cham_sol'),
    path(r'solicita', solicita, name='solicita'),
    path(r'<str:num_chamG>/<str:idG>/show_my_cham', show_my_cham, name='show_my_cham'), 
    path(r'colaboradores', colaboradores, name='colaboradores'),  
    path(r'novo_fun', novo_fun, name='novo_fun'),
    path(r'<str:idG>/<str:empG>/documentacao', documentacao, name='documentacao'), 
    path(r'cad_docs', cad_docs, name='cad_docs'),
    path(r'exlude_fun/<int:id>', exlude_fun, name='exlude_fun'),
    path(r'meus_chamados', meus_chamados, name='meus_chamados'),
    path(r'<int:num>/<int:id>/include_col', include_col, name='include_col'),
    path(r'<int:num>/<int:id>/message', message, name='message'),
    path(r'gestao', gestao, name='gestao'),
    path(r'message_sol/<int:num>/<slug:orig>', message_sol, name='message_sol'),
    path(r'<str:idG>/documentosHse', documentosHse, name='documentosHse'),
    path(r'<str:numG>/<str:idG>/view_cham_hse', view_cham_hse, name='view_cham_hse'),
    path(r'<int:num>/<int:id>/message_hse', message_hse, name='message_hse'),
    path(r'<int:num>/<int:id>/saveCham', saveCham, name='saveCham'),
    path(r'<int:id>/action', action, name='action'),
    path(r'<int:id>/message_fun', message_fun, name='message_fun'),
    path(r'portaria', portaria, name='portaria'),
    path(r'doc_integracao/<int:id>', doc_integracao, name='doc_integracao'),
    path(r'<int:num>/<int:id>/alter', alter, name='alter'),
    path(r'cad_resp_view', cad_resp_view, name='cad_resp_view'),
    path(r'resp/<str:idG>', resp, name='resp'),
    path(r'colaborador/<str:id>', colaborador, name='colaborador'),
    path(r'configurate', configurate, name='configurate'),
    path(r'usuarios', usuarios, name='usuarios'),
    path(r'new_user', new_user, name='new_user'),
    path(r'alt_perm/<int:id>', alt_perm, name='alt_perm'),
    path(r'decide', decide, name='decide'),
    path(r'exlude_doc/<str:idG>', exlude_doc, name='exlude_doc'),
    path(r'bloq_fun/<str:idG>', bloq_fun, name='bloq_fun'),
    path(r'configurate_hse', configurate_hse, name='configurate_hse'),
    path(r'general_settings', general_settings, name='general_settings'),
    path(r'blocked', blocked, name='blocked'),
    path(r'dias_integracao_w', dias_integracao_w, name='dias_integracao_w'),
    path(r'<str:num_chamG>/<str:idG>/agendar_int', agendar_int, name='agendar_int'), 

    path(r'documentacao', base, name='base'),
    path(r'my_view', my_view, name='my_view'),



    
    

]+ static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
