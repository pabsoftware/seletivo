from django.shortcuts import render
from django.http import HttpResponse, Http404
from empresa.models import Vagas
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants
from .models import Tarefa
# 03 imports para envio de emails com template html
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from django.conf import settings

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
    tarefa = Tarefa.objects.filter(vaga = vaga).filter(realizada=False)
    tarefa_realizada = Tarefa.objects.filter(vaga = vaga).filter(realizada=True)
    context = {
        'vaga'      : vaga,
        'tarefas'    : tarefa,
        'tarefas_realizadas'    : tarefa_realizada
    }
    return render(request, template_name, context)


def nova_tarefa(request, id_vaga):

    titulo = request.POST.get('titulo')
    prioridade = request.POST.get('prioridade')
    data = request.POST.get('data')
    #TODO: realizar validações
    try:
        tarefa = Tarefa(
            vaga_id     = id_vaga,
            titulo      = titulo,
            prioridade  = prioridade,
            data        = data
            )
        tarefa.save()
        messages.add_message(request, constants.SUCCESS, 'Tarefa adicionada com sucesso')
        return redirect(f'/vagas/vaga/{id_vaga}')
    except:
        messages.add_message(request, constants.ERROR, 'Houve um erro ao cadastrar tarefa')

        return redirect(f'/vagas/vaga/{id_vaga}')


def realizar_tarefa(request, id):
    tarefa_list = Tarefa.objects.filter(id=id).filter(realizada=False)
    if not tarefa_list.exists():
        messages.add_message(request, constants.ERROR, 'Realise apenas uma tarefa válida')
        return redirect(f'/home/empresas/')
    else:
        tarefa = tarefa_list.first()
        print(tarefa.titulo)
        tarefa.realizada = True
        tarefa.save()
        messages.add_message(request, constants.SUCCESS, 'Tarefa finalizada com sucesso')
        return redirect(f'/vagas/vaga/{tarefa.vaga.id}')

def enviar_email(request, id):
   
    vaga = Vagas.objects.get(id=id)
    assunto = request.POST.get('assunto')
    corpo = request.POST.get('corpo')

    html_content = render_to_string('emails/template_email.html', {'corpo':corpo})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
                                    assunto, 
                                    text_content, 
                                    settings.EMAIL_HOST_USER,
                                    [vaga.email,]
                                    )
    email.attach_alternative(html_content, "text/html")
    email.send()

    return HttpResponse(assunto)