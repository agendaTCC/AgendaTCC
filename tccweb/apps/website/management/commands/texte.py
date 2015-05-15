# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand, CommandError
from django.core.mail import send_mail
from django.db.models import Q
from usuarios.models import MyUser as User
from datas.models import Data
from monografias.models import DatasMonografia
from formularios.models import ProjetoDeGraduacao
from disciplinas.models import Disciplina
from bancas.models import Banca
import datetime
# your custom commande must reference the base management classes like this:
class Command(NoArgsCommand):
    # it's useful to describe what the function does:
    help = u'Função de agendamento pelo cron, envia emails de acordo com datas definidas no sistema'
    def handle_noargs(self, **options):
	usuarios = User.objects.all()
	hoje = datetime.datetime.now()
        hoje = datetime.date(hoje.year,hoje.month, hoje.day)
        if hoje.month > 6:
            semestre = 2
        else:
            semestre = 1
	for usuario in usuarios:
    	    projetos = ProjetoDeGraduacao.objects.filter(user = usuario.id)
    	    projeto_aluno = []
            for projeto in projetos:
		if int(projeto.disciplina.semestre) == int(semestre) and int(projeto.disciplina.ano) == int(hoje.year):
	 	    if usuario.get_profile() in projeto.disciplina.alunos.all():
	                print "%s é aluno"%usuario
