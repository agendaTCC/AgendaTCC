# -*- coding: utf-8 -*-
from django.db import models

class Splash(models.Model):
    class Meta:
        verbose_name = 'Splash(Pagina Inicial)'
        verbose_name_plural = 'Splash(Pagina Inicial)'
    data =  models.DateTimeField(auto_now_add=True)
    texto = models.TextField(null = True, blank= True)
    exibir_noticias = models.BooleanField(verbose_name= 'Exibir Noticias')
    exibir_texto = models.BooleanField(verbose_name= 'Exibir Texto')
    exibir_imagens = models.BooleanField(verbose_name= 'Exibir Imagens')
    def __unicode__(self):
        dia = str(self.data.day)
        mes = str(self.data.month)
        ano = str(self.data.year)
        hora = str(self.data.hour)
        minuto = str(self.data.minute)
        segundo = str(self.data.second)
        if len(hora)== 1:
             hora = str(0)+hora
        if len(minuto)== 1:
             minuto = str(0)+minuto
        if len(segundo)== 1:
             segundo = str(0)+segundo    
        return u"Editar Aqui - Ultima alteração: "+dia+u"/"+mes+u"/"+ano+u" ás: "+hora+u":"+minuto+u":"+segundo
    
class Imagens(models.Model):
    data =  models.DateTimeField(auto_now_add=True)
    entrada = models.FileField(upload_to = "img/slide/")
    texto =  texto = models.TextField(null = True, blank= True)
    exibir = models.BooleanField()
    splash = models.ForeignKey(Splash)
    
