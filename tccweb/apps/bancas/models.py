# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from disciplinas.models import Disciplina
from empresa.models import Empresa
from departamentos.models import Departamento
from semestre.models import Semestre
from projetos.models import ProjetoDeGraduacao
from salas.models import Sala
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

class Banca(models.Model):
    hora_inicial = models.TimeField( null=True, blank = True)
    hora_final = models.TimeField( null=True, blank = True)
    data = models.DateField(null = True, blank = True, verbose_name = "Data")
    semestre = models.ForeignKey(Semestre,verbose_name = 'Semestre', related_name='banca_semestre', null=True, blank = True)
    banca_docente= models.ForeignKey(settings.AUTH_USER_MODEL,related_name= 'banca1',limit_choices_to={'docente': True}, null=True, blank=True)
    banca_convidado = models.ForeignKey(settings.AUTH_USER_MODEL,related_name= 'banca2',limit_choices_to=Q(docente = True) | Q(doutorando = True) | Q(mestrando = True), null=True, blank=True)
    sala = models.ForeignKey(Sala, null=True, blank = True)
    reservada = models.BooleanField()
    alteravel = models.BooleanField(default = True)
    projeto = models.ForeignKey(ProjetoDeGraduacao, related_name = u'banca_projeto', null = True, blank = True)
    cancelada = models.BooleanField(default = False)
    def __unicode__(self):
        if self.reservada:
            reservada = 'Reservada'
        else:
            reservada = ''
        return unicode(self.sala)+ ', Dia: '+str(self.data)+u' Horário: '+ str(self.hora_inicial)+' - '+str(self.hora_final)+ ' '+reservada
   

    
class Agenda(models.Model):
    class Meta:
        verbose_name = _(u'Agendamento')
        verbose_name_plural = _(u'Agendamento')
    semestre = models.ForeignKey(Semestre, related_name='agenda_departamento')
    salas = models.ForeignKey(Sala, related_name= 'agenda_sala',limit_choices_to={'ativa': True})
    def __unicode__(self):
        return u'Sala: '+unicode(self.salas.nome) + u' - ' +unicode(self.semestre)
    
DIAS_DA_SEMANA = (
                  ('seg','Segunda-feira'),
                  ('ter','Terça-feira'),
                  ('qua','Quarta-feira'),
                  ('qui','Quinta-feira'),
                  ('sex','Sexta-feira'),
                  ('sab','Sabado'),
                  )    

class Dia_Agenda(models.Model):
    class Meta:
        verbose_name = _(u'Dia agendamento')
        verbose_name_plural = _(u'Dias agendamento')
    agenda = models.ForeignKey(Agenda)
    data  =  models.DateField(null = True, blank = True, verbose_name = "Data")
    horarios = models.CharField(max_length = 255,help_text = "Exemplo:  8:00-8:40;8:40-9:20;9:20-10:00;10:00-10:40;10:40-11:20;11:20-12:00;12:00-12:40;12:40-13:20;13:20-14:00;14:00-14:40;14:40-15:20;15:20-16:00;16:00-16:40;16:40-17:20;17:20-18:00;19:00-19:40;19:40-20:20;20:20-21:00",null = True, blank = True)


    


class Apresentacao(models.Model):
    data = models.DateTimeField(verbose_name='Data da apresentação')
    sala = models.CharField(max_length=80,verbose_name='Sala')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário')
    banca = models.ForeignKey(Banca, verbose_name='Banca')




        
        
        
        
        
