# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import forms, authenticate, views, login
# from haystack.forms import SearchForm
from django import http
from django.db import IntegrityError
from django.db.models import Q
from django.core.urlresolvers import reverse
from models import Dia_Agenda, Banca, Agenda
from forms import BancaForm, AgendamentoForm, dia_agenda_formset, EditarBancaForm
from disciplinas.models import Disciplina
from projetos.models import ProjetoDeGraduacao
from departamentos.models import Departamento
from salas.models import Sala
from semestre.models import Semestre
from empresa.models import Empresa
import datetime
import operator
import csv
from unicodedata import normalize

@login_required
def banca_liberar_aluno(request, banca_id):
    if banca_id:
        try:
            banca =  Banca.objects.get(pk = banca_id)
        except:
            messages.error(request, (u'Banca Invalida!'))
            return HttpResponseRedirect('/bancas/')
    else:
        messages.error(request, (u'Banca Invalida!'))
        return HttpResponseRedirect('/bancas/')
    if request.user == banca.projeto.aluno:
        banca.projeto = None
        banca.banca_docente = None
        banca.banca_convidado = None
        banca.reservada = False
        banca.save()
        messages.success(request, (u'Banca Liberada com sucesso!'))
    else:
        messages.error(request, (u'Banca não pertence a esse usuário'))
    return HttpResponseRedirect('/bancas/')

@login_required
def banca_liberar_professor(request, banca_id):
    if banca_id:
        try:
            banca =  Banca.objects.get(pk = banca_id)
        except:
            messages.error(request, (u'Banca Invalida!'))
            return HttpResponseRedirect('/bancas/')
    else:
        messages.error(request, (u'Banca Invalida!'))
        return HttpResponseRedirect('/bancas/')
    if not banca.banca_convidado and not banca.banca_docente:
        messages.error(request, (u'Nenhuma banca foi definida!'))
        return HttpResponseRedirect('/bancas/') 
    if banca.banca_convidado and banca.banca_convidado == request.user:
        banca.banca_convidado = None
    elif banca.banca_docente and banca.banca_docente == request.user:
        banca.banca_docente = None
    else:
        messages.error(request, (u'Usuário não pertence a essa banca!'))
        return HttpResponseRedirect(u'/bancas/')   
    banca.save()
    messages.success(request, ('Banca Liberada com sucesso!'))
    return HttpResponseRedirect('/bancas/')   
       

def banca_listar(request):
    usuario = request.user
    semestres = request.session.get("semestre")
    bancas = Banca.objects.filter(semestre__in = semestres, cancelada = False).order_by('data')
    matriculado = False
    hora_inicial = datetime.time(23)

    print bancas
    print semestres

    if(len(bancas)>0):
        print 'a'
        primeiro = bancas[0].data
        ultimo = bancas.reverse()[0].data
    else:
        print 'b'
        primeiro = datetime.datetime.now()
        ultimo = datetime.datetime.now()

    for banca in bancas:
        if banca.data == primeiro:
            if banca.hora_inicial <= hora_inicial:
                hora_inicial = banca.hora_inicial   
    for departamento,semestre in semestres.iteritems():
        disciplinas = semestre.disciplinas()
        for disciplina in disciplinas:
            matriculado = matriculado or disciplina.matriculado(usuario)
    return render_to_response('bancas/banca_listar.html', {
        'bancas': bancas,
        'primeiro':primeiro,
        'ultimo':ultimo,
        'hora_inicial':hora_inicial,
        'matriculado':matriculado,
        # 'form': form,
    }, context_instance=RequestContext(request))


# def banca_detalhe(request, banca_id):
    
#     banca = get_object_or_404(Banca, pk=banca_id)
#     aluno = banca.aluno
#     projeto = banca.projeto
#     return render_to_response('bancas/banca_detalhe.html', {
#         'banca': banca,
#         'aluno': aluno,
#         'projeto': projeto,
#     }, context_instance=RequestContext(request))

@login_required    
def banca_reserva(request, banca_id):
    if banca_id:
        try:
            banca =  Banca.objects.get(pk = banca_id)
        except:
            messages.error(request, (u'Banca Invalida!'))
            return HttpResponseRedirect('/bancas/')
    else:
        messages.error(request, (u'Banca Invalida!'))
        return HttpResponseRedirect('/bancas/')
    usuario = request.user
    semestre = banca.semestre
    #Verificar se esta em periodo de escolha de alunos
    if not semestre.emEscolhaAlunos():
        messages.error(request, (u'Fora do Periodo de escolha!'))
        return HttpResponseRedirect('/bancas/')
    
    if request.method == 'POST':
        form = BancaForm(request.POST, instance=banca)
        form.fields['projeto'].queryset = ProjetoDeGraduacao.objects.filter(aluno=usuario, disciplina__in = semestre.disciplinas())
        if form.is_valid():
            projeto  =  ProjetoDeGraduacao.objects.get(pk = form.cleaned_data['projeto'].id)
            if Banca.objects.filter(projeto_id = projeto).count() != 0:
                messages.error(request, (u'Usuário já tem banca reservada para esse projeto'))
                return HttpResponseRedirect('/bancas/')
            if banca.reservada:
                messages.error(request, (u'Já existe reserva para essa Banca '))
            else:
                save = form.save(commit=False)
                save.projeto = projeto
                save.reservada = True
                save.save()
                messages.success(request, (u'Banca salva com sucesso!'))
            return HttpResponseRedirect('/bancas/')
    else:
        form = BancaForm(instance=banca)
        form.fields['projeto'].queryset = ProjetoDeGraduacao.objects.filter(aluno=usuario, disciplina__in = semestre.disciplinas())

    return render_to_response('bancas/banca_reserva.html', {
        'banca': banca,
        'form' : form,
    }, context_instance=RequestContext(request))

@login_required
def banca_reserva_docente(request, banca_id):
    if banca_id:
        try:
            banca =  Banca.objects.get(pk = banca_id)
        except:
            messages.error(request, (u'Banca Invalida!'))
            return HttpResponseRedirect('/bancas/')
    else:
        messages.error(request, (u'Banca Invalida!'))
        return HttpResponseRedirect('/bancas/')
    usuario =  request.user
    if usuario.docente:
        #verificar se docente é responsavel ou convidado
        if banca.semestre.responsavel(usuario):
            if banca.semestre.emEscolhaDocenteResponsavel():
                if not banca.banca_docente:
                    banca.banca_docente = usuario
                    messages.success(request, (u'Banca reservada com sucesso!'))
                    banca.save()
                    return HttpResponseRedirect('/bancas/')
                else:
                    messages.error(request, (u'Vaga para docente responsavel já preenchida!'))
                    return HttpResponseRedirect('/bancas/')
            else:
                messages.error(request, (u'Fora do Periodo de escolha para docentes responsaveis!'))
                return HttpResponseRedirect('/bancas/')
        else:
            if banca.semestre.emEscolhaDocenteConvidado():
                if not banca.banca_convidado:
                    banca.banca_convidado = usuario
                    messages.success(request, (u'Banca reservada com sucesso!'))
                    banca.save()
                    return HttpResponseRedirect('/bancas/')
                else:
                    messages.error(request, (u'Vaga para convidado já preenchida!'))
                    return HttpResponseRedirect('/bancas/')
            else:
                messages.error(request, (u'Fora do Periodo de escolha para convidados!'))
                return HttpResponseRedirect('/bancas/')
    elif usuario.doutorando:
        if banca.semestre.emEscolhaDocenteConvidado():
            if not banca.banca_convidado:
                banca.banca_convidado = usuario
                messages.success(request, (u'Banca reservada com sucesso!'))
                banca.save()
                return HttpResponseRedirect('/bancas/')
            else:
                messages.error(request, (u'Vaga para convidado já preenchida!'))
                return HttpResponseRedirect('/bancas/')
        else:
            messages.error(request, (u'Fora do Periodo de escolha para convidados!'))
            return HttpResponseRedirect('/bancas/')
    elif usuario.mestrado:
        if banca.semestre.emEscolhaDocenteConvidado():
            if not banca.banca_convidado:
                    banca.banca_convidado = usuario
                    messages.success(request, (u'Banca reservada com sucesso!'))
                    banca.save()
                    return HttpResponseRedirect('/bancas/')
            else:
                messages.error(request, (u'Vaga para convidado já preenchida!'))
                return HttpResponseRedirect('/bancas/')
    else:
        messages.error(request, (u'Fora do Periodo de escolha para convidados!'))
        return HttpResponseRedirect('/bancas/')

def banca_relatorio(request):
    semestres = request.session.get("semestre")
    bancas = {}
    for departamento,semestre in semestres.iteritems():
        bancas_ = Banca.objects.filter(semestre = semestre, cancelada = False,reservada = True).order_by('data')
        bancas.update({departamento:bancas_})
    return render_to_response('bancas/banca_relatorio.html', {
        'bancas': bancas,
    }, context_instance=RequestContext(request))

def normalize_(str):
    if str == None:
        str=u''
    return normalize('NFKD',str).encode('utf-8')

def banca_relatorio_csv(request,departamento_id):
    departamento = Departamento.objects.get(pk = departamento_id)
    semestres = request.session.get("semestre")
    semestre = semestres.get(departamento)
    bancas = Banca.objects.filter(semestre = semestre, cancelada = False).order_by('data')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = u'attachment; filename="bancas_'+unicode(semestre.grupo)+'_'+unicode(semestre.ano)+'_'+unicode(semestre.semestre)+'.csv"'

    writer = csv.writer(response)
    writer.writerow([u'Nome do aluno', u'Disciplina', u'Curso', 'Título do trabalho',u' Nome do orientador ou supervisor', 'Data da apresentação',u'Sala',u'Hora de Inicio',u'Hora de Final', u'Nome Banca Convidada', u'CPF Banca Convidada','Email Banca Convidada', u'Nome da Banca responsavel'])
    for banca in bancas:
        if banca.reservada:
            if not banca.projeto.orientador:
                responsavel = banca.projeto.supervisor.nome_completo
            else:
                responsavel = banca.projeto.orientador.nome_completo
            if not banca.banca_convidado:
                convidado = u'';
                cpf_convidado = u'';
                email_convidado = u'';
            else:
                convidado = banca.banca_convidado.nome_completo
                cpf_convidado = banca.banca_convidado.cpf
                email_convidado = banca.banca_convidado.email
            if not banca.banca_docente:
                docente = u'';
            else:
                docente = banca.banca_docente.nome_completo

            writer.writerow([
                normalize_(banca.projeto.aluno.nome_completo) ,#Nome do aluno
                normalize_(banca.projeto.disciplina.titulo.codigo+' '+banca.projeto.disciplina.titulo.titulo),#Disciplina
                normalize_(banca.projeto.aluno.curso.nome), #Curso
                normalize_(banca.projeto.titulo),#Título do trabalho
                normalize_(responsavel), #Nome do orientador/supervisor
                normalize_(unicode(banca.data.strftime("%d/%m/%Y"))),# Data da apresentação
                normalize_(banca.sala.nome),# Sala
                normalize_(unicode(banca.hora_inicial.strftime("%H:%M"))),#Horario de Inicio
                normalize_(unicode(banca.hora_final.strftime("%H:%M"))),#Horario de Fim
                normalize_(convidado),#Noma banca convidado
                normalize_(cpf_convidado), #CPF banca CONvidado
                normalize_(email_convidado), #Email banca OCNvidado
                normalize_(docente)#Docente responsavel
                ])
    return response