# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from disciplinas.models import Disciplina
from departamentos.models import Departamento

class Noticia(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, blank = True, verbose_name="Autor")
    titulo = models.CharField(max_length=80, verbose_name='Titulo da Noticia')
    conteudo = models.TextField(verbose_name=u'Conteúdo da Noticia')
    disciplina = models.ForeignKey(Disciplina, null=True, blank=True, 
        verbose_name='Disciplina relacionada')
    departamento = models.ForeignKey(Departamento,null=True, blank=True,
        verbose_name = 'Departamento')
    criada_em = models.DateTimeField(auto_now_add=True, 
        verbose_name=u'Data de criação')
    
    class Meta:
        ordering = ['-criada_em']
        
    def __unicode__(self):
        return unicode(self.titulo)
        

