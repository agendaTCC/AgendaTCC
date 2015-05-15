# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.conf import settings
#Modelo Empresa para cadastro de empresas no sistema

UF = (
      ('AC','AC'),
      ('AP','AP'),
      ('AM','AM'),
      ('BA','BA'),
      ('CE','CE'),
      ('DF','DF'),
      ('ES','ES'),
      ('GO','GO'),
      ('MA','MA'),
      ('MT','MT'),
      ('MS','MS'),
      ('MG','MG'),
      ('PA','PA'),
      ('PB','PB'),
      ('PR','PR'),
      ('PE','PE'),
      ('PI','PI'),
      ('RJ','RJ'),
      ('RN','RN'),
      ('RS','RS'),
      ('RO','RO'),
      ('RR','RR'),
      ('SC','SC'),
      ('SP','SP'),
      ('SE','SE'),
      ('TO','TO'),
                )
SITUACAO = (
            ('Ativa','Ativa'),
            ('Inativa','Inativa'),
            )

class Empresa(models.Model):
    #Modelo de empresa afiliada ao sistema
    email = models.CharField(max_length=255, verbose_name=u"E-mail", null=False)
    site = models.CharField(max_length=255, verbose_name=u"Site", null=False)
    area_de_atuacao = models.CharField(max_length=255, verbose_name=u"Area de Atuacao", null=False)
    nro_inscricao = models.CharField(max_length=255, unique=True, verbose_name=u"Numero de inscrição", null=False)
    data_inicio = models.DateField(verbose_name='Data da abertura', null=True, blank=True)
    nome_empresarial = models.CharField(max_length=255, verbose_name='Nome Empresarial', null=True, blank=True)
    nome_fantasia = models.CharField(max_length=255, verbose_name='Título do Estabelecimento (Nome Fantasia)', null=True, blank=True)
    end = models.CharField(max_length=255, verbose_name='Logradouro', null=True, blank=True)
    num = models.IntegerField(max_length=4, verbose_name='Numero',null=True, blank=True )
    comp = models.CharField(max_length=255, verbose_name='Complemento', null=True, blank=True)
    cep = models.IntegerField(max_length=8, verbose_name='CEP, somente Números', null=True, blank=True)
    bairro = models.CharField(max_length=255, verbose_name='Bairro/Distrito', null=True, blank=True)
    cidade = models.CharField(max_length=255, verbose_name='Município', null=True, blank=True)
    UF = models.CharField(max_length = 2,default = 'SP',  null = True, blank = True, choices = UF)
    data_inicio_convenio = models.DateField(verbose_name='Data de inicio de convénio', null=True, blank=True)
    data_final_convenio = models.DateField(verbose_name='Data de fim de convénio', null=True, blank=True)
    supervisores = models.ManyToManyField(settings.AUTH_USER_MODEL,limit_choices_to={'supervisor': True}, null = True, blank = True)
    def __unicode__(self):
        #Modo como o Modelo é Exibido na Lista na Adminstracao
        return unicode(self.nome_empresarial) 
    

