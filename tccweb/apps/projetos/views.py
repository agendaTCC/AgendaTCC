# -*- coding: utf-8 -*-
from disciplinas.models import Disciplina
from departamentos.models import Departamento
from django import http
from django.contrib import auth, messages
from django.contrib.auth import forms, authenticate, views, login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext

from forms import ProjetoDeGraduacaoForm, ProjetoDeGraduacaoFormReadOnly, DeclaracaoDeHorasForm, AvaliacaoAlunoForm
from models import ProjetoDeGraduacao, DeclaracaoDeHoras, AvaliacaoAluno

from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime
from emails.models import GerenciarEmails, EmailPadrao
from emails.sendmail import compose_body



def emails_inscricao(projeto):
	print "emails"
	try:
		gerente_emails = GerenciarEmails.objects.get(departamento = projeto.disciplina.semestre.grupo)
	except:
		return None

	#Email para ALuno
	template = EmailPadrao.objects.get_or_template(gerencia = gerente_emails, tipo = "1")
	corpo = compose_body({"disciplina":projeto.disciplina.titulo.titulo}, template.corpo)
	if corpo:
		projeto.aluno.email_user(template.titulo, corpo)
	#emails para Orientadores
	if projeto.orientador:
		template = EmailPadrao.objects.get_or_template(gerencia = gerente_emails, tipo = "2")
		corpo = compose_body({"aluno":projeto.aluno.nome_completo,"disciplina":projeto.disciplina.titulo.titulo}, template.corpo)
		if corpo:
			projeto.orientador.email_user(template.titulo, corpo)
	#emails para Supervisores
	if projeto.supervisor:
		template = EmailPadrao.objects.get_or_template(gerencia = gerente_emails, tipo = "3")
		corpo = compose_body({"aluno":projeto.aluno.nome_completo,"disciplina":projeto.disciplina.titulo.titulo}, template.corpo)
		if corpo:
			projeto.supervisor.email_user(template.titulo, corpo)


@login_required
def projetoDeGraduacao(request,usuario_id,disciplina_id = None):
	aluno = get_user_model().objects.get(pk=usuario_id)
	try:
	    disciplina = Disciplina.objects.get(id = disciplina_id)
	except:
	    messages.error(request, (u'Disciplina Não Existe!'))
	    return HttpResponseRedirect(request.session.get('last_visited'))
	if(ProjetoDeGraduacao.objects.filter(aluno = aluno, disciplina = disciplina).count() != 0):
		messages.error(request, (u'Ja existe projeto para essa Disciplina!'))
		return HttpResponseRedirect(request.session.get('last_visited'))
	if request.method == 'POST':
	    form = ProjetoDeGraduacaoForm(request.POST)
	    if form.is_valid():
	        save = form.save(commit=False)
	        if 'rascunho' not in request.POST:
	        	save.rascunho = False
	        	emails_inscricao(save)	
	        save.aluno = aluno
	        save.disciplina = disciplina 
	        save.save()
	        messages.success(request, (u'Enviado com sucesso!'))
	        return HttpResponseRedirect('/')
	else:
	    form = form = ProjetoDeGraduacaoForm()
	return render(request,'projetos/projeto_graduacao.html', {
	    'form': form,
	    'aluno':aluno,
	    'disciplina':disciplina,
	})
@login_required
def EditProjetoDeGraduacao(request,projeto_id = None):
	try:
	    projeto = ProjetoDeGraduacao.objects.get(pk = projeto_id)
	except:
	    messages.error(request, (u'Projeto Não Existe!'))
	    return HttpResponseRedirect(request.session.get('last_visited'))
	if request.method == 'POST':
		if not projeto.rascunho and request.user not in projeto.disciplina.professores.all() and request.user not in projeto.disciplina.monitores.all():
			form = ProjetoDeGraduacaoFormReadOnly(request.POST,instance = projeto)
		else:
			form = ProjetoDeGraduacaoForm(request.POST,instance = projeto)
		if form.is_valid():
			save = form.save(commit=False)
			if 'rascunho' not in request.POST:
				save.rascunho = False
				emails_inscricao(projeto)
			save.data = datetime.now()
			save.save()
			messages.success(request, (u'Enviado com sucesso!'))
			return HttpResponseRedirect('/')
	else:
		if not projeto.rascunho and request.user not in projeto.disciplina.professores.all() and request.user not in projeto.disciplina.monitores.all():
			form = ProjetoDeGraduacaoFormReadOnly(instance = projeto)
		else:
			form = form = ProjetoDeGraduacaoForm(instance = projeto)
	return render(request,'projetos/projeto_graduacao.html', {
	    'form': form,
	    'aluno':projeto.aluno,
	    'disciplina':projeto.disciplina,
	    'projeto':projeto,
	})

@login_required
def viewProjetoDeGraduacao(request,projeto_id):
	try:
		projeto = ProjetoDeGraduacao.objects.get(pk = projeto_id)
	except:
		messages.error(request, (u'Projeto Não Existe!'))
		return HttpResponseRedirect(request.session.get('last_visited'))
	return render(request,'projetos/visualisar_projeto_graduacao.html',{
			'projeto':projeto,
		})
	
@login_required
def validarProjetoDeGraduacao(request,projeto_id):
	try:
		projeto = ProjetoDeGraduacao.objects.get(pk = projeto_id)
	except:
		messages.error(request, (u'Projeto Não Existe!'))
		return HttpResponseRedirect(request.session.get('last_visited'))
	if request.method == 'POST':
		justificativa = ''
		opcaoJustificativa = ''
		validacao = request.POST['validacao']
		if 'justificativa' in request.POST:
			justificativa = request.POST['justificativa']
		if 'opcaoJustificativa' in request.POST:
			opcaoJustificativa = request.POST['opcaoJustificativa']
		if validacao == 'n':
			if not justificativa:
				messages.error(request,(u'Justificativa não Pode ser vazia'))
				return HttpResponseRedirect(request.session.get('last_visited'))
			else:
				projeto.justificativa = justificativa
			if opcaoJustificativa =='cancelar':
				projeto.cancelado = True
			elif opcaoJustificativa == 'rascunho':
				projeto.rascunho = True;
				projeto.validacao_supervisor_orientador = 'p'
				projeto.validacao_graduacao = 'p'
				projeto.validacao_docente = 'p'
			#Email projeto reprovado
			gerente_emails = GerenciarEmails.objects.get(departamento = projeto.disciplina.semestre.grupo)
			template = EmailPadrao.objects.get_or_template(gerencia = gerente_emails, tipo = "4")
			corpo = compose_body({"disciplina":projeto.disciplina.titulo.titulo}, template.corpo)
			if corpo:
				projeto.aluno.email_user(template.titulo, corpo)
		else:
			if(request.user.docente):
				if(request.user == projeto.orientador):
					if(projeto.validacao_supervisor_orientador == 'p'):
						projeto.validacao_supervisor_orientador = validacao
					else:
						messages.error(request,(u'Projeto já validado anteriormente!'))
						return HttpResponseRedirect(request.session.get('last_visited'))
				else:
					if(request.user in projeto.disciplina.professores.all()):
						if(projeto.validacao_docente == 'p'):
							projeto.validacao_docente = validacao
						else:
							messages.error(request,(u'Projeto já validado anteriormente!'))
							return HttpResponseRedirect(request.session.get('last_visited'))
			if(request.user.supervisor and request.user == projeto.supervisor):
				if(projeto.validacao_supervisor_orientador == 'p'):
					projeto.validacao_supervisor_orientador = validacao
				else:
					messages.error(request,(u'Projeto já validado anteriormente!'))
					return HttpResponseRedirect(request.session.get('last_visited'))
			if(request.user.funcionario):
				if(projeto.validacao_graduacao == 'p'):
					projeto.validacao_graduacao = validacao
				else:
					messages.error(request,(u'Projeto já validado anteriormente!'))
					return HttpResponseRedirect(request.session.get('last_visited'))
		projeto.save()

		if((projeto.validacao_supervisor_orientador == 's' and projeto.validacao_docente == 's') or (projeto.validacao_supervisor_orientador == 's' and  projeto.validacao_graduacao == 's') or (projeto.validacao_docente == 's' and  projeto.validacao_graduacao == 's')):
			projeto.disciplina.matricula_aluno(projeto.aluno)
			gerente_emails = GerenciarEmails.objects.get(departamento = projeto.disciplina.semestre.grupo)
			template = EmailPadrao.objects.get_or_template(gerencia = gerente_emails, tipo = "5")
			corpo = compose_body({"disciplina":projeto.disciplina.titulo.titulo}, template.corpo)
			if corpo:
				projeto.aluno.email_user(template.titulo, corpo)
			template = EmailPadrao.objects.get_or_template(gerencia = gerente_emails, tipo = "6")
			corpo = compose_body({"aluno":projeto.aluno.nome_completo,"disciplina":projeto.disciplina.titulo.titulo}, template.corpo)
			if corpo:
				for docente in projeto.disciplina.professores.all():
					docente.email_user(template.titulo, corpo)	
		messages.success(request,(u'Validação enviada com sucesso'))
	return HttpResponseRedirect(request.session.get('last_visited'))


	
@user_passes_test(lambda user: user.docente or user.funcionario or user.secretario, 'authorization')
@login_required       
def pendencias_projeto(request):
	usuario = request.user
	semestres = request.session.get("semestre")

	departamentos = Departamento.objects.all()
	list_semestre = []
	list_departamentos = []
	for departamento,semestre in semestres.iteritems():
		list_semestre.append(semestre)
		list_departamentos.append(departamento)
	#Query para disciplinas do semestre 
	disciplinas_semestre = Disciplina.objects.filter(esta_ativa=True,semestre__in = list_semestre)
	disc = {}
	if usuario.docente:
		for departamento,semestre in semestres.iteritems():
			disciplinas_dict = {}
			disciplinas_filter = disciplinas_semestre.filter(professores = usuario, semestre = semestre)
			for disciplina in disciplinas_filter:
				projetos = ProjetoDeGraduacao.objects.filter(disciplina = disciplina)
				disciplinas_dict.update({disciplina:projetos})
			disc.update({departamento:disciplinas_dict})
	if usuario.funcionario or usuario.secretario:
		for departamento,semestre in semestres.iteritems():
			disciplinas_dict = {}
			disciplinas = disciplinas_semestre.filter(semestre = semestre)
			for disciplina in disciplinas:
				projetos = ProjetoDeGraduacao.objects.filter(disciplina = disciplina)
				disciplinas_dict.update({disciplina:projetos})
			disc.update({departamento:disciplinas_dict})
	return render(request,'projetos/pendencias_projeto.html',{
	'disciplinas': disc,
	})

@login_required
def declarar_horas(request,projeto_id):
	semestres = request.session.get("semestre")
	try:
		projeto = ProjetoDeGraduacao.objects.get(pk = projeto_id)
	except:
		messages.error(request, (u'Projeto Não Existe!'))
		return HttpResponseRedirect(request.session.get('last_visited'))
	semestre = semestres[projeto.disciplina.semestre.grupo]
	if semestre.emSemestre():
		if request.user == projeto.supervisor or request.user == projeto.orientador:
			try:
				horas = DeclaracaoDeHoras.objects.get(projeto = projeto)
			except:
				horas = None
			form = DeclaracaoDeHorasForm(request.POST or None, instance = horas)
			if form.is_valid():
				save = form.save(commit=False)
				save.projeto = projeto
				save.save()
				messages.success(request, (u'Enviado com sucesso!'))
				return HttpResponseRedirect('/')
			return render(request,'projetos/declarar_horas.html',{
				'projeto':projeto,
				'form':form,
			})
		else:
			messages.error(request, (u'Você deve ser Supervisor ou Orientador do Projeto'))
			return HttpResponseRedirect('/')
	else:
		messages.error(request, (u'O semestre já foi encerrado!'))
		return HttpResponseRedirect('/')

@user_passes_test(lambda user: user.docente or user.funcionario or user.secretario, 'authorization')
@login_required       
def relatorio_entrega(request):
	usuario = request.user
	semestres = request.session.get("semestre")

	departamentos = Departamento.objects.all()
	list_semestre = []
	list_departamentos = []
	for departamento,semestre in semestres.iteritems():
		list_semestre.append(semestre)
		list_departamentos.append(departamento)
	#Query para disciplinas do semestre 
	disciplinas_semestre = Disciplina.objects.filter(esta_ativa=True,semestre__in = list_semestre)
	disc = {}
	if usuario.docente:
		for departamento,semestre in semestres.iteritems():
			disciplinas_dict = {}
			disciplinas_filter = disciplinas_semestre.filter(professores = usuario, semestre = semestre)
			for disciplina in disciplinas_filter:
				projetos = ProjetoDeGraduacao.objects.filter(disciplina = disciplina)
				disciplinas_dict.update({disciplina:projetos})
			disc.update({departamento:disciplinas_dict})
	if usuario.funcionario or usuario.secretario:
		for departamento,semestre in semestres.iteritems():
			disciplinas_dict = {}
			disciplinas = disciplinas_semestre.filter(semestre = semestre)
			for disciplina in disciplinas:
				projetos = ProjetoDeGraduacao.objects.filter(disciplina = disciplina)
				disciplinas_dict.update({disciplina:projetos})
			disc.update({departamento:disciplinas_dict})
	return render(request,'projetos/relatorio_entrega.html',{
	'disciplinas': disc,
	})

@login_required
def avaliacao_aluno(request,projeto_id):
	semestres = request.session.get("semestre")
	try:
		projeto = ProjetoDeGraduacao.objects.get(pk = projeto_id)
	except:
		messages.error(request, (u'Projeto Não Existe!'))
		return HttpResponseRedirect(request.session.get('last_visited'))
	semestre = semestres[projeto.disciplina.semestre.grupo]
	if semestre.emSemestre():
		if request.user == projeto.supervisor or request.user == projeto.orientador:
			try:
				avaliacao = AvaliacaoAluno.objects.get(projeto = projeto)
			except:
				avaliacao = None
			form = AvaliacaoAlunoForm(request.POST or None, instance = avaliacao)
			if form.is_valid():
				save = form.save(commit=False)
				save.projeto = projeto
				save.save()
				messages.success(request, (u'Enviado com sucesso!'))
				return HttpResponseRedirect('/')
			return render(request,'projetos/avaliacao_aluno.html',{
				'projeto':projeto,
				'form':form,
			})
		else:
			messages.error(request, (u'Você deve ser Supervisor ou Orientador do Projeto'))
			return HttpResponseRedirect('/')
	else:
		messages.error(request, (u'O semestre já foi encerrado!'))
		return HttpResponseRedirect('/')
@login_required
def visualizar_avaliacao(request,projeto_id):
	try:
		avaliacao =  ProjetoDeGraduacao.objects.get(pk = projeto_id).avaliacao_projeto
	except:
		messages.error(request, (u'Avaliação ainda não entregue!'))
		return HttpResponseRedirect('/')
	return render(request,'projetos/visualizar_avaliacao.html',{
				'avaliacao':avaliacao,
			})
