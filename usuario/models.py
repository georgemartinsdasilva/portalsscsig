from django.db import models
from django.contrib.auth.models import User
from cadastro.models import empresa_terc
# Create your models here.

default = 'default.png'

class Perfil(models.Model):
	Permissoes = (
        ('SIG', 'SIG'),
        ('HSE', 'HSE'),
		('POR', 'PORTARIA'),
	)
	first_name = models.CharField(max_length=10, null=True)
	last_name = models.CharField(max_length=10, null=True)
	user = models.CharField(max_length=50 , null=True)
	user_id = models.CharField(max_length=30 , null=True)
	Setor = models.CharField(max_length=30 , null=True)
	Gestor = models.CharField(max_length=30 , null=True)
	email = models.CharField(max_length=80, null=True)
	funcao = models.CharField(max_length=30 , null=True)
	num_tel = models.CharField(max_length=30 , null=True)
	perm = models.CharField(max_length=3, choices=Permissoes , default="SIG", null=True)


	class Meta:
		verbose_name_plural = "Perfis"

	def __str__(self):
		return '->>>: {}'.format(self.user)