# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from forms import QuestionarioRespondidoForm
from models import Questionario, Perguntas, Respostas, QuestionarioRespondido
from projetos.models import ProjetoDeGraduacao
from departamentos.models import Departamento
import ast
import collections

def parseResposta(obj):
	if isinstance(obj, list):
		if obj:
			last = obj[-1]
			str = ''
			for item in obj:
				if item != last:
					str = str + item+', '
				else:
					str = str+ item
			return str
		else:
			return ""
	else:
		return obj

def responderQuestionario(request,projeto_id,questionario_id):
	#Buscando projeto e departamento baseado nos id, trantando erros
	selectmultiple = []
	try:
		projeto  = ProjetoDeGraduacao.objects.get(pk=projeto_id)
	except :
		messages.error(request, (u'Projeto Não Existe!'))
		return HttpResponseRedirect('/')		
	try:
		questionario = Questionario.objects.get(pk=questionario_id)
	except:
		messages.error(request, (u'Questionario Não Existe!'))
		return HttpResponseRedirect('/')
	perguntas = Perguntas.objects.filter(questionario = questionario).order_by('numero')
	try:
		respondido = QuestionarioRespondido.objects.get(projeto = projeto, questionario = questionario)
		respostas = Respostas.objects.filter(respondido = respondido).order_by('pergunta__numero')
	except:
		respondido = None
		respostas = None
	if request.POST:
		form = QuestionarioRespondidoForm(request.POST , perguntas = perguntas, respostas = respostas)
		if form.is_valid():
			if not respondido:
				respondido = QuestionarioRespondido.objects.novo_respondido(projeto = projeto, questionario = questionario)
				for (pergunta, resposta) in form.extra_answers():
					Respostas.objects.nova_resposta(respondido = respondido, pergunta = Perguntas.objects.get(pk = pergunta), resposta = parseResposta(resposta))
			else:
				for (pergunta, resposta) in form.extra_answers():
					try:
						_resposta = Respostas.objects.get(respondido = respondido, pergunta = Perguntas.objects.get(pk = pergunta))
						_resposta.resposta = parseResposta(resposta)
						_resposta.save()
					except:
						Respostas.objects.nova_resposta(respondido = respondido, pergunta = Perguntas.objects.get(pk = pergunta), resposta = parseResposta(resposta))
					
			messages.success(request, (u'Enviado com sucesso!'))
			return HttpResponseRedirect('/')		
	else:
		form = QuestionarioRespondidoForm(perguntas = perguntas, respostas = respostas)
		if respondido:
			respostas = Respostas.objects.filter(respondido = respondido)
			for resposta in respostas:
				if resposta.pergunta.tipo == "3":
					selectmultiple.append(("pergunta_"+str(resposta.pergunta.id),form.fields["pergunta_"+str(resposta.pergunta.id)].initial))
	return render(request,'questionarios/questionario_form.html',{
		'questionario':questionario,
		'form':form,
		'selectmultiple':selectmultiple,
	})
	
def visualizarQuestionario(request,projeto_id,questionario_id):
	try:
		projeto  = ProjetoDeGraduacao.objects.get(pk=projeto_id)
	except:
		messages.error(request, (u'Projeto Não Existe!'))
		return HttpResponseRedirect('/')		
	try:
		questionario = Questionario.objects.get(pk=questionario_id)
	except:
		messages.error(request, (u'Questionario Não Existe!'))
		return HttpResponseRedirect('/')
	respondido = QuestionarioRespondido.objects.filter(projeto = projeto, questionario = questionario)
	respostas = Respostas.objects.filter(respondido = respondido).order_by('pergunta__numero')
	return render(request, 'questionarios/visualizar_questionario.html',{
			'respostas':respostas,
			'questionario':questionario,
		})
