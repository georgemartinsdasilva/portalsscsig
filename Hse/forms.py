from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField
from Hse.models import chamado_hse, aux_table, msg, email_hse, dias_integracao
from cadastro.models import empresa_terc, cad_resp
from django.forms.widgets import Select
from django.db  import  models

TYPE_CHOICES = [
    ('1', "Trabalho em alta tensão e eletricidade"),
    ('2', "Trabalhos em altura "),
    ('3', "Espaços confinados "),
    ('4', "Operação de empilhadeira "),
    ('5', "Trabalhos com plataformas elevatórias"),
    ('6', "Operação de guindaste ou munk "),
    ('7', "Trabalhador autônomo - Firma individual "),
    ('8', " Assistência Técnica - mautenção "),
    ('9', " Soldador "),
]


class chamado_hseForm(ModelForm):
    tipo_servico = forms.MultipleChoiceField(choices=TYPE_CHOICES, 
    	                       widget=forms.CheckboxSelectMultiple(attrs={'class': 'flat', 'name': '','type': 'checkbox'}))
    empresa = forms.ModelChoiceField(queryset=empresa_terc.objects.all(), widget=Select(attrs={'class':'form-control', 'data-show-subtext':'true', 'data-live-search':'true'}))
    
    #resp_terc = forms.ModelChoiceField(queryset=cad_resp.objects.all(), widget=Select(attrs={'class':'form-control', 'data-show-subtext':'true', 'data-live-search':'true'}))
    

    nome_proj = forms.CharField(label="Nome Projeto / Serviço ", widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'vencimento','type': ''}))

    descricao = forms.CharField(label="Descricao", widget=forms.Textarea(attrs={'class': 'form-control', 'name': 'descricao','type': 'textarea'}))
    
    class Meta:
        model = chamado_hse
        fields = ['empresa','nome_proj','tipo_servico','descricao',]

class aux_tableForm(ModelForm):
    class Meta:
        model = aux_table
        fields = ['num_cham', 'tps','colab','id_col',]

class msgForm(ModelForm):
    class Meta:
        model = msg
        fields = ['num_cham', 'ator','msg',]


class email_hse_Form(ModelForm):
    class Meta:
        model = email_hse
        fields = ['Nome', 'email','ativo',]


class dias_integracao_FORM(ModelForm):
    class Meta:
        model = dias_integracao
        fields = ['Seg', 'Ter','Qua', 'Qui', 'Sex', 'Sab', 'Dom']