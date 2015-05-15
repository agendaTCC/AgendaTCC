# -*- coding: utf-8 -*-
from django.db import models
from departamentos.models import Departamento
from projetos.models import ProjetoDeGraduacao
from django.conf import settings
# Create your models here.

class questionarioManager(models.Manager):
    def novo_questionario(self, departamento,titulo, tipo):
        questionario = self.create(departamento = departamento, titulo = titulo, tipo = tipo)
        return questionario

OPCOES = (
		('0','Questionario de Graduação'),
		('1','Questionário de Estagio'),
	)
FIELDOPTIONS = (
	('0', 'Campo de Texto'),
	('1','Sim ou Não'),
	('2','Multipla escolha'),
	('3','Selecionar Varios'),
	('4','Seção')
	)

class Questionario(models.Model):
	departamento = models.ForeignKey(Departamento, verbose_name = 'Departamento', related_name=u'questionario_departamento')
	titulo = models.CharField(max_length = 255,verbose_name='Título do Questionario', null=True, blank = True)
	tipo = models.CharField(max_length = 255,verbose_name='Tipo', null=True, blank = True,choices = OPCOES)
	descricao = models.TextField(null=True, blank = True, default=None)
	objects = questionarioManager()
	def __unicode__(self):
		return self.departamento.titulo + ' - ' + self.titulo



class perguntasManager(models.Manager):
    def nova_pergunta(self, questionario,pergunta):
        pergunta = self.create(questionario = questionario, pergunta = pergunta)
        return resposta

class Perguntas(models.Model):
	class Meta:
		verbose_name = u'Pergunta'
		verbose_name_plural = u'Perguntas'
	questionario =  models.ForeignKey(Questionario, verbose_name = 'Questionario', related_name=u'perguntas_questionario')
	numero =  models.IntegerField(null=True, blank = True)
	pergunta = models.TextField(verbose_name=u'Pergunta')
	tipo = models.CharField(max_length = 255,verbose_name='Tipo de Campo', null=True, blank = True,choices = FIELDOPTIONS, default='0')
	opcoes = models.CharField(max_length = 255,verbose_name='Opções',help_text=u'Caso seja um campo de multipla escolha, descreva as opções separando-as por uma virgula, exemplo: opção 1, opção2, ...', null=True, blank = True)
	objects = perguntasManager()
	def __unicode__(self):
		return self.pergunta



class questionarioRespostaManager(models.Manager):
	def novo_respondido(self, projeto, questionario):
		respondido = self.create(projeto = projeto, questionario = questionario)
		return respondido
	# def novo_respondido(self, usuario, questionario):
	# 	respondido = self.create(usuario = usuario, questionario = questionario)
	# 	return respondido


class QuestionarioRespondido(models.Model):
	class Meta:
		verbose_name= "Questionário Respondido"
		verbose_name_plural = "Questionários Respondidos"
		unique_together =('projeto', 'questionario')
	# usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'Usuário', related_name="questionario_respondido_usuario")
	projeto = models.ForeignKey(ProjetoDeGraduacao,verbose_name=u'Projeto de Graduação', related_name='questionario_respondido_projeto', default='1')
	questionario =  models.ForeignKey(Questionario, verbose_name = 'Questionario', related_name=u'resposta_projeto_questionario')
	data = models.DateTimeField(auto_now=True, verbose_name="Data da Entrega")
	objects = questionarioRespostaManager()
	def __unicode__(self):
		return self.questionario.titulo + ': '+self.projeto.__unicode__()
	def get_aluno_display(self):
		return self.projeto.aluno.nome_completo
	get_aluno_display.short_description = 'Aluno'
	def get_tipo_display(self):
		return self.questionario.get_tipo_display()
	get_tipo_display.short_description = 'Tipo de Questionário'
	def get_departamento_display(self):
		return self.questionario.departamento
	get_departamento_display.short_description = 'Departamento'



class respostaManager(models.Manager):
    def nova_resposta(self, respondido,pergunta,resposta):
        resposta = self.create(respondido = respondido, pergunta = pergunta, resposta = resposta)
        return resposta

class Respostas(models.Model):
	class Meta:
		verbose_name = u'Resposta'
		verbose_name_plural = u'Respostas'
	respondido = models.ForeignKey(QuestionarioRespondido, verbose_name = 'Questionario Respondido',related_name=u'resposta_respondido')
	pergunta =  models.ForeignKey(Perguntas, verbose_name = 'Pergunta',related_name=u'respostas_pergunta')
	resposta = models.TextField(verbose_name=u'Resposta')
	objects = respostaManager()
	def __unicode__(self):
		return 'Resposta de '+self.pergunta.questionario.titulo