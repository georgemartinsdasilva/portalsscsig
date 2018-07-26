from django.shortcuts import render
from django_ajax.decorators import ajax
from cadastro.models import cad_resp
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.core import serializers

# Create your views here.
def base(request):

    return render(request, 'DOCUMENTAÇÃO\doc_base.html')


#@ajax
def my_view(request):
    print(request.GET.get('data'))
    eventList = cad_resp.objects.all()
    lista = serializers.serialize('json', eventList)
    return JsonResponse(lista, safe=False) 