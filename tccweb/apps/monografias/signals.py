# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, m2m_changed
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from models import CobrarMonografiaimpressa, CobrarMonografiaatrasada
from disciplinas.models import Disciplina
from emails.models import GerenciarEmails, EmailPadrao
from grupos_disciplinas.models import GrupoDisciplina

import datetime
data = datetime.datetime.now()
if data.month <= 7:
    semestre = 1
else:
    semestre = 2

def cobrar_alunos_devedores(sender, instance, action, reverse, model, pk_set,**kwargs):
    lista = instance
    disciplina = lista.disciplina
    grupo = GrupoDisciplina.objects.get(disciplinas = disciplina.titulo)
    gerencia = GerenciarEmails.objects.get(grupo = grupo, semestre = semestre, ano = data.year )
    padroes = EmailPadrao.objects.filter(gerencia = gerencia)
    try:
        reponsaveis = ResponsavelGrupo.objects.get(grupo=grupo)
        responsaveis = responsaveis[-1]
        responsavel = responsaveis.docentes.all()[0]
        enviado = responsavel.email
    except:
        enviado = "noreply@tccweb.com"
    alunos = lista.alunos.all()
    for aluno in alunos:
        if aluno.get_profile() not in disciplina.alunos.all():
            continue
        for padrao in padroes:
                if padrao.tipo == '19':
                    titulo = padrao.titulo
                    msg =  padrao.corpo
                    msg = msg.replace(u'{{disciplina}}',unicode(disciplina.titulo))
                    titulo = titulo.replace(u'{{disciplina}}',unicode(disciplina.titulo))
        if msg == None:
            titulo = "Monografia Atrasada",
            msg = render_to_string('emails/cobrar_monografia_impressa.txt',{'disciplina',disciplina.titulo})
        corpo_liso = strip_tags(msg) 
        mensagem = EmailMultiAlternatives(titulo, corpo_liso,enviado, [aluno.email],headers = {'Reply-To': enviado,})
        mensagem.attach_alternative(msg, "text/html")
        mensagem.send()
        
def cobrar_monografia_atrasada(sender, instance, action, reverse, model, pk_set,**kwargs):
    lista = instance
    disciplina = lista.disciplina
    grupo = GrupoDisciplina.objects.get(disciplinas = disciplina.titulo)
    gerencia = GerenciarEmails.objects.get(grupo = grupo, semestre = semestre, ano = data.year )
    padroes = EmailPadrao.objects.filter(gerencia = gerencia)
    try:
        reponsaveis = ResponsavelGrupo.objects.get(grupo=grupo)
        responsaveis = responsaveis[-1]
        responsavel = responsaveis.docentes.all()[0]
        enviado = responsavel.email
    except:
        enviado = "noreply@tccweb.com"
    alunos = lista.alunos.all()
    for aluno in alunos:
        if aluno.get_profile() not in disciplina.alunos.all():
            continue
        for padrao in padroes:
                if padrao.tipo == '19':
                    titulo = padrao.titulo
                    msg =  padrao.corpo
                    msg = msg.replace(u'{{disciplina}}',unicode(disciplina.titulo))
                    titulo = titulo.replace(u'{{disciplina}}',unicode(disciplina.titulo))
        if msg == None:
            titulo = "Monografia Atrasada",
            msg = render_to_string('emails/cobrar_monografia_atrasada.txt',{'disciplina',disciplina.titulo})
        corpo_liso = strip_tags(msg) 
        mensagem = EmailMultiAlternatives(titulo, corpo_liso,enviado, [aluno.email],headers = {'Reply-To': enviado,})
        mensagem.attach_alternative(msg, "text/html")
        mensagem.send()
        
m2m_changed.connect(cobrar_alunos_devedores,sender=CobrarMonografiaimpressa.alunos.through)
m2m_changed.connect(cobrar_monografia_atrasada,sender=CobrarMonografiaatrasada.alunos.through)