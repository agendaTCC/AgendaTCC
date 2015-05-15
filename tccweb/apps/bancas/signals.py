# -*- coding: utf-8 -*-
from models import Dia_Agenda, Agenda, Banca
from salas.models import Sala
from datetime import timedelta
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.db import models

def cria_banca(sender,**kwargs):
    dia = kwargs["instance"]
    agenda = dia.agenda
    sala = agenda.salas
    data = dia.data
    if dia.horarios != None:
        horarios = dia.horarios.split(';')
        for horario in horarios:
            horario = horario.split('-')
            banca_ = Banca.objects.filter(data = data, hora_inicial = horario[0], hora_final = horario[1], sala=sala.id, semestre = agenda.semestre)
            if banca_.count()==0:
                banca = Banca(data=data, hora_inicial = horario[0], hora_final = horario[1],sala_id = sala.id, semestre_id = agenda.semestre.id)
                banca.save()
    else:
        dia.delete()
post_save.connect(cria_banca, sender=Dia_Agenda, dispatch_uid="bancas.models.Agenda")

def cancela_banca(sender, **kwargs):
    banca = kwargs["instance"]
    if banca.cancelada:
        msg = render_to_string('emails/cancelamento_banca.txt',{'banca':banca,})
        banca1.email_user(
                               subject=u"Cancelamento de Apresentaçao",
                               message=msg,
                               from_email=u"noreply@tccweb.com",
                               )    