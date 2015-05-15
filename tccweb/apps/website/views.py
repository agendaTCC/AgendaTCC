# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, render
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth import forms, authenticate, views, login
from django.contrib.auth.decorators import login_required
from django import http
from django.core.urlresolvers import reverse
from django.db.models import Q
from datetime import date
from itertools import chain
from django.contrib.auth.models import Group
from models import Splash, Imagens

from semestre.models import Semestre
from projetos.models import ProjetoDeGraduacao

from disciplinas.models import Disciplina
from departamentos.models import Departamento
from noticias.models import Noticia
from bancas.models import Banca
from questionarios.models import Questionario
    



def splash(request):
    modelo = Splash.objects.get(id = 1)
    imagens = Imagens.objects.filter(splash = 1)
    noticias = Noticia.objects.all()[:8]
    texto = modelo.texto
    exibir_noticias = modelo.exibir_noticias
    exibir_texto = modelo.exibir_texto
    exibir_imagens = modelo.exibir_imagens
    return render_to_response('website/splash.html', {
        'imagens':imagens,
        'texto': texto,
        'exibir_noticias':exibir_noticias,
        'exibir_texto': exibir_texto,
        'exibir_imagens':exibir_imagens,
        # 'noticias': noticias,
    }, context_instance=RequestContext(request))


@login_required
def dashboard(request):
    usuario = request.user
    semestres = request.session.get("semestre")
    
    departamentos = Departamento.objects.all()
    todos_semestres = {}
    for departamento in departamentos:
        todos_semestres.update({departamento:Semestre.objects.filter(grupo = departamento)})

    list_semestre = []
    list_departamentos = []
    for departamento,semestre in semestres.iteritems():
        list_semestre.append(semestre)
        list_departamentos.append(departamento)
    #Query para disciplinas do semestre 
    disciplinas_semestre = Disciplina.objects.filter(esta_ativa=True,semestre__in = list_semestre)
    noticias = Noticia.objects.all()[:8]
    dicionario = {'todos_semestres':todos_semestres, 'noticias':noticias};
    if not usuario.is_superuser or usuario.docente or usuario.funcionario or usuario.secretario:
        #
        # ALUNO
        #
        if usuario.aluno and usuario.curso:
            #Disciplinas Matriculadas
            #Filtra disciplinas do semestre para as matriculadas pelo aluno
            disciplinas_aluno = {usuario.curso.departamento:disciplinas_semestre.filter(alunos=usuario.id)}
            dicionario.update({'disiplinas_aluno':disciplinas_aluno})
            #Projetos do semestre
            #Query projetos para projetos pertencentes ao aluno e a disciplinas do semestre
            projetos = ProjetoDeGraduacao.objects.filter(aluno = usuario, disciplina__in = disciplinas_semestre)
            projetos_aluno = {usuario.curso.departamento:projetos}
            dicionario.update({'projetos_aluno':projetos_aluno})
            #Questionarios
            questionarios = Questionario.objects.filter(departamento = usuario.curso.departamento)
            dicionario.update({'questionarios':questionarios})
        #
        # DOCENTE
        #    
        if usuario.docente:
            #Disciplinas Docente
            #Filtra todos as disciplinas nas quais o docente é responsavel para todos os departamentos, então
            #lista todos os projetos para tais disciplinas
            disciplinas_docente = {}
            for departamento,semestre in semestres.iteritems():
                disciplinas_dict = {}
                disciplinas = disciplinas_semestre.filter(professores = usuario, semestre = semestre)
                for disciplina in disciplinas:
                    projetos = ProjetoDeGraduacao.objects.filter(disciplina = disciplina)
                    disciplinas_dict.update({disciplina:projetos})
                disciplinas_docente.update({departamento:disciplinas_dict})
            dicionario.update({'disciplinas_docente':disciplinas_docente})
            projetos_docente = {}
            for departamento,semestre in semestres.iteritems():
                disciplinas = disciplinas_semestre.filter(semestre = semestre)
                projetos = ProjetoDeGraduacao.objects.filter(orientador = usuario, disciplina__in  = disciplinas)
                projetos_docente.update({departamento:projetos})
            dicionario.update({'projetos_docente':projetos_docente})
            bancas_docente_responsavel = {}
            for departamento,semestre in semestres.iteritems():
                bancas = Banca.objects.filter(banca_docente = usuario, semestre = semestre)
                bancas_docente_responsavel.update({departamento:bancas})
            dicionario.update({'bancas_docente_responsavel':bancas_docente_responsavel})
            bancas_docente_convidado = {}
            for departamento,semestre in semestres.iteritems():
                bancas = Banca.objects.filter(banca_convidado = usuario, semestre = semestre)
                bancas_docente_convidado.update({departamento:bancas})
            dicionario.update({'bancas_docente_convidado':bancas_docente_convidado})
        #
        # SUPERVISOR
        #
        if usuario.supervisor:
            projetos_supervisor = {}
            for departamento,semestre in semestres.iteritems():
                disciplinas = disciplinas_semestre.filter(semestre = semestre)
                projetos = ProjetoDeGraduacao.objects.filter(supervisor = usuario, disciplina__in  = disciplinas)
                projetos_supervisor.update({departamento:projetos})
            dicionario.update({'projetos_supervisor':projetos_supervisor})
        #
        # FUNCIONARIO
        #
        if usuario.funcionario or usuario.secretario:
            disciplinas_funcionario = {}
            for departamento,semestre in semestres.iteritems():
                disciplinas_dict = {}
                disciplinas = disciplinas_semestre.filter(semestre = semestre)
                for disciplina in disciplinas:
                    projetos = ProjetoDeGraduacao.objects.filter(disciplina = disciplina)
                    disciplinas_dict.update({disciplina:projetos})
                disciplinas_funcionario.update({departamento:disciplinas_dict})
            dicionario.update({'disciplinas_funcionario':disciplinas_funcionario})
        if usuario.doutorando:
            bancas_doutorando_convidado = {}
            for departamento,semestre in semestres.iteritems():
                bancas = Banca.objects.filter(banca_convidado = usuario, semestre = semestre)
                bancas_doutorando_convidado.update({departamento:bancas})
            dicionario.update({'bancas_doutorando_convidado':bancas_doutorando_convidado})
        if usuario.mestrando:
            bancas_mestrando_convidado = {}
            for departamento,semestre in semestres.iteritems():
                bancas = Banca.objects.filter(banca_convidado = usuario, semestre = semestre)
                bancas_mestrando_convidado.update({departamento:bancas})
            dicionario.update({'bancas_mestrando_convidado':bancas_mestrando_convidado})

    return render(request,'website/dashboard.html', dicionario)


def index(request):
    if request.user.is_authenticated():
        #Ao se autenticar o sistema busca os semestres atuais(atual = true) releventes para cada tipo de usuario
        #Cada departamento no sistema tem sua configuração de semestre propria, cada objeto de semestre é pareado 
        #com se departamento em um dicionario e salvo na seção do usuario
        semestres = []
        if not request.user.is_superuser:
            if request.user.aluno:
                if request.user.curso:
                    semestres = Semestre.objects.semestreAtual(request.user.curso.departamento)
            if request.user.docente:
                semestres = Semestre.objects.filter(atual = True)
            if request.user.doutorando:
                semestres = Semestre.objects.filter(atual = True)
            if request.user.mestrando:
                semestres = Semestre.objects.filter(atual = True)
            if request.user.supervisor:
                semestres = Semestre.objects.filter(atual = True)
            if request.user.funcionario or request.user.secretario:
                semestres = Semestre.objects.filter(atual = True)
        else:
            semestres = Semestre.objects.filter(atual = True)

        # if 'semestre' not in request.session:
        dict_semestre = {}
        for semestre in semestres:
            dict_semestre.update({semestre.grupo:semestre})

        #if not 'semestre' in request.session:
        #    print 'a-'
        request.session['semestre'] = dict_semestre
        request.session['hoje'] = date.today()

        return dashboard(request)
    return splash(request)
