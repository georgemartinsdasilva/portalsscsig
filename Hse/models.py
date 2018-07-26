from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from cadastro.models import empresa_terc, cad_resp
from model_utils import Choices

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'song'),
    ('2', 'singer'),
    ('3', 'last_modify_date'),
    ('4', 'created'),
)

default = 'default.png'

class chamado_hse(models.Model):
	solicitante = models.CharField(max_length=100)
	data_abertura = models.DateTimeField(auto_now_add=True)
	empresa = models.ForeignKey(empresa_terc, on_delete=models.CASCADE)
	tempo_estimado = models.CharField(max_length=100)
	nome_proj = models.CharField(max_length=100)
	setor_solicitante = models.CharField(max_length=100)
	gestor_solicitante = models.CharField(max_length=100)
	tipo_servico = models.CharField(max_length=50, blank=True)
	descricao = models.CharField(max_length=1000, blank=True)
	email_terc = models.CharField(max_length=500)
	email_solicitante = models.CharField(max_length=100)
	fone_solicitante = models.CharField(max_length=100)
	status = models.CharField(max_length=100)
	data = models.DateField(auto_now=True)
	resp_terc = models.CharField(max_length=100)

	def __str__(self):
		return '{}'.format(self.id)

class aux_table(models.Model):
	num_cham = models.IntegerField()
	email_resp_cham = models.CharField(max_length=100, blank=True)
	tps = models.CharField(max_length=100)
	colab = models.CharField(max_length=100)
	id_col = models.CharField(max_length=55)
	status = models.CharField(max_length=55)

	def __str__(self):
		return '{}'.format(self.id)

"""
class Solic_cad(models.Model):
	solicitante = models.CharField(max_length=100)
	nome_empresa = models.CharField(max_length=100)
	obs = models.CharField(max_length=500)
	first_access = models.IntegerField()

	def __str__(self):
		return '- {}'.format(self.Empresa)"""


class logs(models.Model):
	num_cham = models.CharField(max_length=100)
	ator = models.CharField(max_length=100)
	acao = models.CharField(max_length=10000)
	data = models.DateTimeField(default=datetime.now)
	tipo = models.CharField(max_length=100, default=None)

	def __str__(self):
		return '{}'.format(self.id)

class msg(models.Model):
	num_cham = models.CharField(max_length=100)
	ator = models.CharField(max_length=100)
	msg = models.CharField(max_length=10000)
	data = models.DateTimeField(default=datetime.now)
	tipo = models.CharField(max_length=10, default=None)
	id_col = models.CharField(max_length=10, default=None)

	def __str__(self):
		return '{}'.format(self.id)


class Hse(models.Model):
	Nome = models.CharField(max_length=10, default=None)

	def __str__(self):
		return '{}'.format(self.Nome)


class portaria(models.Model):
	Nome = models.CharField(max_length=10, default=None)

	def __str__(self):
		return '{}'.format(self.Nome)

class email_hse(models.Model):
	Nome = models.CharField(max_length=10, default=None)
	email = models.EmailField()
	ativo = models.BooleanField(default=True)

	def __str__(self):
		return '{}'.format(self.Nome)

class dias_integracao(models.Model):
	Seg = models.CharField(max_length=100, null=True, blank=True)
	Ter = models.CharField(max_length=100, null=True, blank=True)
	Qua = models.CharField(max_length=100, null=True, blank=True)
	Qui = models.CharField(max_length=100, null=True, blank=True)
	Sex = models.CharField(max_length=100, null=True, blank=True)
	Sab = models.CharField(max_length=100, null=True, blank=True)
	Dom = models.CharField(max_length=100, null=True, blank=True)


def query_musics_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Music.objects.all()
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) |
                                        Q(song__icontains=search_value) |
                                        Q(singer__icontains=search_value) |
                                        Q(last_modify_date__icontains=search_value) |
                                        Q(created__icontains=search_value))

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }
