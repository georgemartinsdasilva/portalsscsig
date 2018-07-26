from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField
from cadastro.models import empresa_terc, funcionario, documento,docs_integracao, Solic_cad, docs, cad_resp, bloq_hse
from django.forms.widgets import Select

    
class empresaForm(ModelForm):
    class Meta:
        model = empresa_terc
        fields = ['nome_empresa', 'cnpj','telefone','email']

class funcionarioForm(ModelForm):
    resp = forms.ModelChoiceField(queryset=cad_resp.objects.all(), widget=Select(attrs={'class':'form-control', 'data-show-subtext':'true', 'data-live-search':'true'}))
    class Meta:
        model = funcionario
        fields = ['nome_funcionario', 'rg','cpf','funcao','resp']

class documentoForm(forms.ModelForm):
    validade_documento = forms.CharField(label="validade_documento", widget=forms.TextInput(attrs={ 'name': 'validade_documento','id': 'data'}))
    class Meta:
        model = documento
        fields = ['validade_documento','arquivo_documento',]
    
class doc_Int_Form(ModelForm):
    class Meta:
        model = docs_integracao
        fields = [ 'arquivo','funcionario']

class New_Solic_cad(ModelForm):
    class Meta:
        model = Solic_cad
        fields = ['Contato', 'Obs']

class docsF(ModelForm):
    class Meta:
        model = docs
        fields = ['nome', 'txt1','txt2','tipo','toolTip']

class cad_respF(ModelForm):
    class Meta:
        model = cad_resp
        fields = ['nome_resp', 'empresa_resp','funcao_resp','telefone_resp','email_resp']

class bloq_hse_FORM(ModelForm):
    class Meta:
        model = bloq_hse
        fields = ['fun', 'motivo']

    