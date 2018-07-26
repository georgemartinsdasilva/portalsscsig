from django.conf import settings
from rest_framework import serializers

from cadastro.models import funcionario


class PortSerializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.

    data_int = serializers.DateField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = funcionario
        # fields = '__all__'
        fields = ('nome_funcionario', 'rg', 'cpf', 'status', 'data_int')