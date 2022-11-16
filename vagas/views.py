from django.shortcuts import render
from django.http import HttpResponse, Http404
from empresa.models import Vagas
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants

def nova_vaga(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        email = request.POST.get('email')
        tecnologias_domina = request.POST.getlist('tecnologias_domina')
        tecnologias_nao_domina = request.POST.getlist('tecnologias_nao_domina')
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
        vaga.tecnologias_dominadas.add(*tecnologias_domina)
        vaga.tecnologias_estudar.add(*tecnologias_nao_domina)
        vaga.save()
        messages.add_message(request, constants.SUCCESS, 'Vaga criada com sucesso.')
        return redirect(f'/home/empresa/{empresa}')
    elif request.method == 'GET':
        raise Http404()

def vaga(request, id):
    template_name= 'vaga.html'
    vaga = get_object_or_404(Vagas, id=id)
    context = {
        'vaga': vaga,
    }
    return render(request, template_name, context)