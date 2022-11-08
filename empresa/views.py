from django.shortcuts import render, HttpResponse

# Create your views here.

def nova_empresa(request):
    return HttpResponse('Estamos cadastrando nova empresa')
