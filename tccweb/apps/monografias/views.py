# -*- coding: utf-8 -*-
from forms import EntregaMonografiaRevisadaForm, EntregaMonografiaOriginalForm
from models import  EntregaMonografiaRevisada, EntregaMonografiaOriginal
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from projetos.models import ProjetoDeGraduacao
from django.conf import settings


import mimetypes, os
import datetime

@login_required
def entrega_monografia_revisada(request, projeto_id):
    projeto = ProjetoDeGraduacao.objects.get(pk = projeto_id)
    monografias = EntregaMonografiaRevisada.objects.filter(projeto = projeto)
    if monografias.count() != 0:
        messages.error(request, ('Você já entregou sua monografia revisada esse semestre!'))
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form  = EntregaMonografiaRevisadaForm(request.POST, request.FILES)
        if form.is_valid():
            save = form.save()
            save.projeto = projeto
            save.save()
            messages.success(request, ('Enviado com sucesso!'))
            return HttpResponseRedirect('/')
        else:
            messages.error(request, ('Erro ao enviar o arquivo!'))
    else:
        form = EntregaMonografiaRevisadaForm()
    return render_to_response('monografias/entrega_monografia_revisada.html', {
            'form': form,
        }, context_instance=RequestContext(request))
    
@login_required
def entrega_monografia_original(request, projeto_id):
    projeto = ProjetoDeGraduacao.objects.get(pk = projeto_id)
    monografias = EntregaMonografiaOriginal.objects.filter(projeto = projeto)
    if monografias.count() != 0:
        messages.error(request, ('Você já entregou sua monografia revisada esse semestre!'))
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form  = EntregaMonografiaOriginalForm(request.POST, request.FILES)
        if form.is_valid():
            save = form.save()
            save.projeto = projeto
            save.save()
            messages.success(request, ('Enviado com sucesso!'))
            return HttpResponseRedirect('/')
        else:
            messages.error(request, ('Erro ao enviar o arquivo!'))
    else:
        form = EntregaMonografiaOriginalForm()
    return render_to_response('monografias/entrega_monografia_original.html', {
            'form': form,
        }, context_instance=RequestContext(request))
@login_required
def download_monografia_original(request, projeto_id):
    projeto = ProjetoDeGraduacao.objects.get(pk = projeto_id)
    try:
        monografia = EntregaMonografiaOriginal.objects.get(projeto = projeto)
    except:
        messages.error(request, ('Monografia Original Ainda não foi entregue para esse projeto'))
        return HttpResponseRedirect('/')
    
    filename = settings.MEDIA_ROOT+ '/'  + str(monografia.monografia)
    
    file = open(filename,"r")
    mimetype = mimetypes.guess_type(filename)[0]
    if not mimetype: mimetype = "application/octet-stream"


    response = HttpResponse(file.read(), mimetype=mimetype)
    response["Content-Disposition"] = "attachment; filename=%s" % os.path.split(filename)[1]
    return response

@login_required
def download_monografia_revisada(request, projeto_id):
    projeto = ProjetoDeGraduacao.objects.get(pk = projeto_id)
    try:
        monografia = EntregaMonografiaRevisada.objects.get(projeto = projeto)
    except:
        messages.error(request, ('Monografia Original Ainda não foi entregue para esse projeto'))
        return HttpResponseRedirect('/')

    filename = settings.MEDIA_ROOT+ '/' + str(monografia.monografia)
    
    file = open(filename,"r")
    mimetype = mimetypes.guess_type(filename)[0]
    if not mimetype: mimetype = "application/octet-stream"


    response = HttpResponse(file.read(), mimetype=mimetype)
    response["Content-Disposition"] = "attachment; filename=%s" % os.path.split(filename)[1]
    return response

# @login_required
# def gerenciar_monografias(request):
#     estado = request.session.get('estado')
#     print request.session
#     grupos_ = estado.get('grupos')
#     busca_grupo = Q()
#     for grupo in grupos_:
#         busca_grupo.add(Q(id = grupo.get('grupo').id),busca_grupo.OR)
#     grupos = GrupoDisciplina.objects.filter(busca_grupo)
#     #grupos = GrupoDisciplina.objects.all()
#     disciplinas = estado.get('disciplinas')
#     semestre = estado.get('semestre')
#     ano = estado.get('ano')
#     hoje = estado.get('hoje')
#     busca = Q()
#     for disciplina in disciplinas:
#         busca.add(Q(disciplina = disciplina.id), busca.OR)
#     monografias_impressas = ReceberMonografia.objects.filter(busca)
#     monografias_emprestadas = DevolucaoMonografiaIMpressa.objects.filter(busca)
#     monografias_revisadas = EntregaMonografiaRevisada.objects.filter(busca)
#     monografias_originais = EntregaMonografiaOriginal.objects.filter(busca)
    
#     if request.method == 'POST':
#         form1 = CobrarMonografiaimpressaForm(request.POST)
#         form2 = CobrarMonografiaatrasadaForm(request.POST)
#         for disciplina in disciplinas:
#             if 'revisada_'+str(disciplina.id) in request.POST:
#                 if form1.is_valid():
#                     save = form1.save(commit = False)
#                     save.disciplina = disciplina
#                     save.data = hoje
#                     save.save()
#                     form1.save_m2m()
#                     messages.success(request, ('Enviado com sucesso!'))
#                     return HttpResponseRedirect('/monografia/gerenciar')
#             if 'atrasada_'+str(disciplina.id) in request.POST: 
#                 if form2.is_valid():
#                     save = form2.save(commit = False)
#                     save.disciplina = disciplina
#                     save.data = hoje
#                     save.save()
#                     form2.save_m2m()
#                     messages.success(request, ('Enviado com sucesso!'))
#                     return HttpResponseRedirect('/monografia/gerenciar')
#     else:
#         form1 = CobrarMonografiaimpressaForm()
#         form2 = CobrarMonografiaatrasadaForm()
#     return render_to_response('monografias/gerenciar_monografia.html', {
#             'grupos': grupos,
#             'disciplinas': disciplinas,
#             'hoje': hoje,
#             'semestre': semestre,
#             'form1':form1,
#             'form2':form2,
#             'monografias_originais':monografias_originais,
#             'monografias_emprestadas':monografias_emprestadas,
#             'monografias_impressas':monografias_impressas,
#             'monografias_revisadas':monografias_revisadas,
#         }, context_instance=RequestContext(request))
    
# def receber_monografia_impressa(request, aluno_id = None, disciplina_id = None):
#     disciplina = Disciplina.objects.get(id = disciplina_id)
#     aluno = User.objects.get(id = aluno_id)
#     try:
#         instance = ReceberMonografia.objects.get(disciplina = disciplina.id, alunos = aluno.id)
#     except:
#         instance = None
#     if request.method == 'POST':
#         form = ReceberMonografiaForm(request.POST, instance = instance)
#         if form.is_valid():
#             saving = form.save(commit = False)
#             saving.disciplina = disciplina
#             saving.alunos = aluno
#             saving.save()
#             messages.success(request, ('Enviado com sucesso!'))
#             return HttpResponseRedirect('/monografia/gerenciar')
#     else:
#         form = ReceberMonografiaForm(instance = instance)
#     return render_to_response('monografias/receber_monografia.html', {
#             'form': form,
#             'aluno':aluno,
#         }, context_instance=RequestContext(request))    

# def receber_monografia_emprestada(request, aluno_id = None, disciplina_id = None):
#     disciplina = Disciplina.objects.get(id = disciplina_id)
#     aluno = User.objects.get(id = aluno_id)
#     try:
#         instance = DevolucaoMonografiaIMpressa.objects.get(disciplina = disciplina.id, alunos = aluno.id)
#     except:
#         instance = None
#     if request.method == 'POST':
#         form = DevolucaoMonografiaIMpressaForm(request.POST, instance = instance)
#         if form.is_valid():
#             saving = form.save(commit = False)
#             saving.disciplina = disciplina
#             saving.alunos = aluno
#             saving.save()
#             messages.success(request, ('Enviado com sucesso!'))
#             return HttpResponseRedirect('/monografia/gerenciar')
#     else:
#         form = DevolucaoMonografiaIMpressaForm(instance = instance)
#     return render_to_response('monografias/receber_monografia.html', {
#             'form': form,
#             'aluno':aluno,
#         }, context_instance=RequestContext(request))    
    
