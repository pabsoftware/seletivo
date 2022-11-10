from django.shortcuts import render, HttpResponse
from .models import Tecnologias, Empresa
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.

def nova_empresa(request):
    template_name = 'nova_empresa.html'

    if request.method =="GET":
        tecnologias = Tecnologias.objects.all()
        context = {'tecnologias': tecnologias}
        return render(request, template_name, context)


    elif request.method =='POST':
      
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cidade = request.POST.get('cidade')
        endereco = request.POST.get('endereco')
        nicho = request.POST.get('nicho')
        caracteristicas = request.POST.get('caracteristicas')
        tecnologias = request.POST.getlist('tecnologias') #getlist para pegar masi de um valor na lista
        logo = request.FILES.get('logo')

        if (len(nome.strip()) == 0) or (len(email.strip()) == 0) or(len(cidade.strip()) == 0) or(len(endereco.strip()) == 0) or (len(nicho.strip()) == 0) or (len(caracteristicas.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/home/nova_empresa')
        
        if logo.size > 100_000_000:
            messages.add_message(request, constants.ERROR, 'Sua logo não pode ter mais que 10 megas')
            return redirect('/home/nova_empresa')

        if nicho not in [i[0] for i in Empresa.choice_nicho_mercado]:
            messages.add_message(request, constants.ERROR, 'Nicho de mercado iválido')
            return redirect('/home/nova_empresa')

        empresa = Empresa(logo=logo,
                        nome=nome,
                        email=email,
                        cidade=cidade,
                        endereco=endereco,
                        nicho_mercado=nicho,
                        caracteristicas_empresa=caracteristicas)
        empresa.save()
        empresa.tecnologias.add(*tecnologias) #adiciona todas as tecnologias
        empresa.save()
        messages.add_message(request, constants.SUCCESS, 'Empresa cadastrada com sucesso')

        return redirect('/home/empresas')
    

def empresas(request):
    template_name= 'empresa.html'
    if request.method == "GET":
        nome = ''

    empresas = Empresa.objects.all()
    tecnologias = Tecnologias.objects.all()
    context = { 'empresas'      : empresas,
                'tecnologias'   : tecnologias
            }

    return render(request, template_name, context)


def excluir_empresa(request, id):
    template_name = 'empresa.html'

    empresa = Empresa.objects.get(id=id)
    empresa.delete()
    messages.add_message(request, constants.SUCCESS, 'Empresa excluida com sucesso')
    return redirect('/home/empresas')