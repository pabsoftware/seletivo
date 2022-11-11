from django.shortcuts import render
from django.http import HttpResponse, Http404
from empresa.models import Vagas

def nova_vaga(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        email = request.POST.get('email')
        tecnologias_domina = request.POST.get('tecnologias_domina')
        tecnologias_nao_domina = request.POST.get('tecnologias_nao_domina')
        experiencia = request.POST.get('experiencia')
        data_final = request.POST.get('data_final')
        empresa = request.POST.get('empresa')
        status = request.POST.get('status')
        vaga = Vagas(
                    titulo=titulo,
                    email=email,
                    nivel_experiencia=experiencia,
                    data_final=data_final,
                    empresa_id=empresa,
                    status=status,
        )
        vaga.save()
        
    elif request.method == 'GET':
        raise Http404()
    return HttpResponse('Nova vaga')
