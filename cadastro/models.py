from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime




default = 'default.png'

class Solic_cad(models.Model):
	Solicitante = models.CharField(max_length=100)
	Contato = models.CharField(max_length=100)
	Obs = models.CharField(max_length=1000)

	def __str__(self):
		return '- {}'.format(self.Empresa)

class empresa_terc(models.Model):
	nome_empresa = models.CharField(max_length=100)
	cnpj = models.CharField(max_length=20)
	telefone = models.CharField(max_length=50, blank=True)
	email = models.CharField(max_length=50, blank=True)
	usuario = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return '- {}'.format(self.nome_empresa)

class cad_resp(models.Model):
	nome_resp = models.CharField(max_length=30)
	empresa_resp = models.CharField(max_length=30)
	funcao_resp = models.CharField(max_length=30)
	telefone_resp = models.CharField(max_length=30, blank=True)
	email_resp = models.CharField(max_length=500)

	def __str__(self):
		return '{}'.format(self.nome_resp)

class funcionario(models.Model):
	nome_funcionario = models.CharField(max_length=100)
	rg = models.CharField(max_length=20)
	cpf = models.CharField(max_length=20)
	empresa = models.ForeignKey(empresa_terc, on_delete=models.CASCADE)
	status = models.CharField(max_length=10, default="AG")
	funcao = models.CharField(max_length=100)
	data_int = models.DateField(null=True, blank=True)
	resp = models.ForeignKey(cad_resp, on_delete=models.CASCADE)

	def __str__(self):
		return '- {}'.format(self.nome_funcionario)
	

class documento(models.Model):
	nome_documento = models.CharField(max_length=100)
	validade_documento = models.CharField(max_length=30)
	arquivo_documento = models.FileField(upload_to='documents/')
	data_envio = models.DateTimeField(auto_now_add=True)
	funcionario = models.IntegerField()
	status = models.BooleanField(default=False)
	enviado = models.BooleanField(default=False)
	hse = models.CharField(max_length=2, default="AG")
	emp = models.CharField(max_length=100, default="none")
	email_resp =  models.CharField(max_length=100, default="none")
	email_emp =  models.CharField(max_length=100, default="none")

	def __str__(self):
		return '- {}'.format(self.nome_documento)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class docs_integracao(models.Model):
	validade_documento = models.DateField(auto_now=False)
	arquivo = models.FileField(upload_to='documents/')
	data_envio = models.DateTimeField(auto_now_add=True)
	funcionario = models.CharField(max_length=10)
	status = models.BooleanField(default=True)
	email_emp = models.CharField(max_length=100, default="none")
	email_resp = models.CharField(max_length=100, default="none")

	def __str__(self):
		return '- {}'.format(self.nome_documento)

class docs(models.Model):
	nome = models.CharField(max_length=30)
	txt1 = models.CharField(max_length=30)
	txt2 = models.CharField(max_length=30)
	tipo = models.CharField(max_length=30)
	toolTip = models.CharField(max_length=500)

	def __str__(self):
		return '{}'.format(self.nome)
	
class bloq_hse(models.Model):
	fun = models.OneToOneField(
        funcionario,
        on_delete=models.PROTECT,
        primary_key=True,
    )
	motivo = models.CharField(max_length=1000)
	data_bloq = models.DateField(auto_now=True)

	def __str__(self):
		return '{}'.format(self.nome)












