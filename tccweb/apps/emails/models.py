# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from departamentos.models import Departamento
# from semestre.models import Semestre
from django.utils import timezone
from emails.sendmail import options
from django.template import loader, Context
# Create your models here.
TIPO_PADRAO = (
         ('1', 'Inscrição Aluno - Aluno'),
         ('2', 'Inscrição Aluno - Orientador'),
         ('3', 'Inscrição Aluno - Supervisor'),
         ('4', 'Inscrição aluno - Matricula Negada'),
         ('5', 'Inscrição aluno - Matricula Efetivada'),
         ('6', 'Disciplina - Matricula de aluno efetivada'),
         )

class emailTemplate:
    def __init__(self):
        self.corpo = ''
        self.titulo = ''
    def get_template(self, tipo):
        t = loader.render_to_string('emails/templates/'+tipo+'.txt', {'aluno': '{{ aluno }}', 'disciplina':'{{ disciplina }}'})
        self.corpo = t;
        self.titulo = "TCCWEB"



class EmailPadraoManager(models.Manager):
    def get_or_template(self,gerencia, tipo):
        query =   self.get_query_set().filter(gerencia = gerencia, tipo = tipo).order_by('-criado_em')
        if not query:
            template = emailTemplate()
            template.get_template(tipo)
            return template
        query = query[0]
        return query
    


class EnviaEmail(models.Model):
    class Meta:
        verbose_name = _(u'Enviar Email')
        verbose_name_plural  = _(u'Enviar Emails')
    departamento = models.ForeignKey(Departamento, verbose_name=_(u'Departamento'))
    filtro = models.CharField(verbose_name=_(u'Filtro'),max_length = 255,  null = True, blank = True)
    assunto = models.CharField(max_length = 255,null = True, blank = True)
    corpo  = models.TextField(null = True, blank = True)
    enviada_em = models.DateTimeField(verbose_name=_(u'Enviada Em'), default=timezone.now)
    def get_filtro_display(self):
    	options_str = ''
    	for option in self.filtro:
    		for item in options():
    			if item[0] == option:
    				options_str+= item[1]+'; '
    	return options_str
    get_filtro_display.short_description = 'Filtro'



# TIPO_AUTOMATICO = (
#          ('1','Matrícula - Antes de Iniciar'),
#          ('2','Matrícula - Iniciada'),
#          ('3','Matrícula - Antes de Finalizar'),
#          ('4','Apresentação - Antes de Iniciar'),
#          ('5','Apresentação - Iniciado'),
#          ('6','Apresentação - Antes de Finalizar'),
#          ('7','Banca Convidado - Antes de Iniciar'),
#          ('8','Banca Convidado - Iniciado'),
#          ('9','Banca Convidado - Antes de Finalizar'),
#          ('10','Monografia Original - Antes de Finalizar'),
#          ('11','Monografia Revisada - Antes de Finalizar'),
#          )
class GerenciarEmails(models.Model):
    class Meta:
        verbose_name = 'Gerenciar E-mails'
        verbose_name_plural = 'Gerenciar E-mails'
    departamento = models.ForeignKey(Departamento)
    def __unicode__(self):
        return self.departamento.titulo
    
class EmailPadrao(models.Model):
    class Meta:
        verbose_name = 'E-mail Padrão'
        verbose_name_plural = 'E-mails Padrão'
        unique_together = (("gerencia", "tipo"),)
    gerencia = models.ForeignKey(GerenciarEmails)
    tipo = models.CharField(max_length=2, verbose_name=u'Tipo', choices = TIPO_PADRAO)
    titulo = models.CharField(verbose_name=u'Assunto',max_length = 255,null = True, blank= True)
    corpo = models.TextField(null = True, blank= True)
    criado_em = models.DateTimeField(_(u'Criado Em'), default=timezone.now)
    objects = EmailPadraoManager()

    def __unicode__(self):
        return self.tipo
# class EmailAutomatico(models.Model):
#     class Meta:
#         verbose_name = 'E-mail Automatico'
#         verbose_name_plural = 'E-mails Automaticos'
#         unique_together = (("gerencia", "tipo"),)
#     gerencia = models.ForeignKey(GerenciarEmails)
#     tipo = models.CharField(max_length=1, verbose_name=u'Tipo', choices = TIPO_AUTOMATICO, null = True, blank= True)
#     periodo_antes = models.CharField(max_length = 255,null=True, blank=True)
#     periodo_depois = models.CharField(max_length = 255,null=True, blank=True)
#     data = models.DateField(auto_now=True, null=True, blank=True)
#     titulo = models.CharField(verbose_name=u'Título',max_length = 255,null = True, blank= True)
#     corpo = models.TextField(null = True, blank= True)