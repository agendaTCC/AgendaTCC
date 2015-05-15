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
        hoje = datetime.datetime.now()
        hoje = datetime.date(hoje.year,hoje.month, hoje.day)
        if hoje.month > 6:
            semestre = 2
        else:
            semestre = 1
        try:
            datas = Data.objects.filter(semestre = semestre, ano = hoje.year)
        except:
            datas = None
        try:
        		datas_monografia = DatasMonografia.objects.filter(semestre = semestre, ano = hoje.year)
        except:
        		datas_monografia = None
        if datas != None:
            #Matricula:
            #Verificando Periodo de Matricula:
            periodo_matricula = [datetime.date(hoje.year,12,31), datetime.date(hoje.year,1,1)]
            for data in datas:
                if data.inic_inscricao != None and data.inic_inscricao < periodo_matricula[0]:
                    periodo_matricula[0] = data.inic_inscricao
                if data.max_inscricao != None and data.max_inscricao > periodo_matricula[1]:
                    periodo_matricula[1] = data.max_inscricao 
            #Periodo de Matricula Iniciado
            usuarios = User.objects.all()
            #Uma Semana Antes;
            if hoje + datetime.timedelta(days = 7) == periodo_matricula[0]:
                for usuario in usuarios:
                    if usuario.get_profile().funcao != '4':
                        continue
                    usuario.email_user(
                                   subject=u"Perido de Matricula será Iniciado em uma Semana.",
                                   message=u"Perido de Matricula será Iniciado em uma Semana.",
                                   from_email=u"noreply@tccweb.com",
                                )
            #No dia:
            if hoje == periodo_matricula[0]:
                for usuario in usuarios:
                    if usuario.get_profile().funcao != '4':
                        continue
                    usuario.email_user(
                                   subject=u"Perido de Matricula Iniciado.",
                                   message=u"Perido de Matricula Iniciado.",
                                   from_email=u"noreply@tccweb.com",
                                )
            #Uma semana antes de acabar para usuarios sem matricula:
            if hoje + datetime.timedelta(days = 7) == periodo_matricula[1]:
                for usuario in usuarios:
                    aux = 0
                    projeto = ProjetoDeGraduacao.objects.filter(user = usuario.id)
                    for projeto in projetos:
                        if projeto.disciplina.semestre == semestre and projeto.disciplina.ano == hoje.year:
                            aux = 1
                            break
                    if usuario.get_profile().funcao != '4' and aux == 0:
                        continue
                    usuario.email_user(
                                   subject=u"Perido de Matricula será finalizado em uma Semana.",
                                   message=u"Perido de Matricula será finalizado em uma Semana.",
                                   from_email=u"noreply@tccweb.com",
                                )
            #3 dias antes de acabar para usuarios sem matricula:
            if hoje + datetime.timedelta(days = 3) == periodo_matricula[1]:
                for usuario in usuarios:
                    aux = 0
                    projetos = ProjetoDeGraduacao.objects.filter(user = usuario.id)
                    for projeto in projetos:
                        if projeto.disciplina.semestre == semestre and projeto.disciplina.ano == hoje.year:
                            aux = 1
                            break
                    if usuario.get_profile().funcao != '4' and aux == 0:
                        continue
                    usuario.email_user(
                                   subject=u"Perido de Matricula será finalizado em 3 dias.",
                                   message=u"Perido de Matricula será finalizado em 3 dias.",
                                   from_email=u"noreply@tccweb.com",
                                )
            #3 dias antes de acabar para usuarios com matricula incompleta
            if hoje + datetime.timedelta(days = 7) == periodo_matricula[1]:
                for usuario in usuarios:
                    aux = 0
                    projetos = ProjetoDeGraduacao.objects.filter(user = usuario.id)
                    projeto_aluno = []
                    for projeto in projetos:
                        if projeto.disciplina.semestre == semestre and projeto.disciplina.ano == hoje.year:
                            projeto_aluno.append(projeto)
                    for item in projeto_aluno:
                        if item.rascunho:
                            aux = 0
                            break
                        if not item.rascunho:
                            aux = 1
                    if usuario.get_profile().funcao != '4' and aux == 0:
                        continue
                    usuario.email_user(
                                   subject=u"Perido de Matricula será finalizado em 3 dias.",
                                   message=u"Perido de Matricula será finalizado em 3 dias.",
                                   from_email=u"noreply@tccweb.com",
                                )
            #ultimo dia para usuarios sem matricula
            if hoje  == periodo_matricula[1]:
                for usuario in usuarios:
                    aux = 0
                    projetos = ProjetoDeGraduacao.objects.filter(user = usuario.id)
                    for projeto in projetos:
                        if projeto.disciplina.semestre == semestre and projeto.disciplina.ano == hoje.year:
                            aux = 1
                            break
                    if usuario.get_profile().funcao != '4' and aux == 0:
                        continue
                    usuario.email_user(
                                   subject=u"Perido de Matricula será finalizado hoje.",
                                   message=u"Perido de Matricula será finalizado hoje.",
                                   from_email=u"noreply@tccweb.com",
                                )
            #ultimo dia para usuarios com matricula imcompleta
            if hoje  == periodo_matricula[1]:
                for usuario in usuarios:
                    aux = 0
                    projetos = ProjetoDeGraduacao.objects.filter(user = usuario.id)
                    projeto_aluno = []
                    for projeto in projetos:
                        if projeto.disciplina.semestre == semestre and projeto.disciplina.ano == hoje.year:
                            projeto_aluno.append(projeto)
                    for item in projeto_aluno:
                        if item.rascunho:
                            aux = 0
                            break
                        if not item.rascunho:
                            aux = 1
                    if usuario.get_profile().funcao != '4' and aux == 0:
                        continue
                    usuario.email_user(
                                   subject=u"Perido de Matricula será finalizado hoje .",
                                   message=u"Perido de Matricula será finalizado hoje.",
                                   from_email=u"noreply@tccweb.com",
                                )
            #Bancas:
            #veridicando periodo de escolhas de bancas
            periodo_escolha_alunos = [datetime.date(hoje.year,12,31), datetime.date(hoje.year,1,1)]
            for data in datas:
                if data.inic_banca_alunos != None and data.inic_banca_alunos < periodo_escolha_alunos[0]:
                    periodo_escolha_alunos[0] = data.inic_banca_alunos
                if data.max_banca_alunos != None and data.max_banca_alunos > periodo_escolha_alunos[1]:
                    periodo_escolha_alunos[1] = data.max_banca_alunos
            disciplinas = Disciplina.objects.filter(semestre = semestre, ano = hoje.year)
            busca = Q()
            for disciplina in disciplinas:
                busca.add(Q(disciplina = disciplina.id), busca.OR)
            projetos = ProjetoDeGraduacao.objects.filter(busca)
            #Uma semana para inicio da escolha pelos alunos:
            if hoje + datetime.timedelta(days = 7) == periodo_escolha_alunos[0]:
                for projeto in projetos:
                    usuario = projeto.user
                    usuario.email_user(
                                   subject=u"Perido de escolha de banca será Iniciado em uma Semana.",
                                   message=u"Perido de escolha de banca será Iniciado em uma Semana.",
                                   from_email=u"noreply@tccweb.com",
                                )
            #3,2,1 dia(s) antes de acabar pra quem não tem horario reservado:
            if hoje + datetime.timedelta(days = 3) == periodo_escolha_alunos[1] \
            or hoje + datetime.timedelta(days = 2) == periodo_escolha_alunos[1] \
            or hoje + datetime.timedelta(days = 1) == periodo_escolha_alunos[1] \
            or hoje  == periodo_escolha_alunos[1]:
                for projeto in projetos:
                    try:
                        banca = Banca.objects.get(projeto = projeto)
                    except:
                        usuario = projeto.user
                        usuario.email_user(
                                       subject=u"Período de escolha de banca será Finalizado.",
                                       message=u"O período de escolha do dia e horário para realização de sua banca de Projeto/Estágio termina em %s/%s/%s.\n\nPara escolher seu hórario entre no sistema TCCWeb (http://tccweb.icmc.usp.br) usando seu nome de usuario: %s"%(str(periodo_escolha_alunos[1].day),str(periodo_escolha_alunos[1].month),str(periodo_escolha_alunos[1].year),str(usuario.username)),
                                       from_email=u"noreply@tccweb.com",
                                    )
            
            #Periodo inicio de banca para professores:
            periodo_banca2 = [datetime.date(hoje.year,12,31), datetime.date(hoje.year,1,1)]
            mestrando = False
            for data in datas:
                if data.inic_banca_convidado!= None and data.inic_banca_convidado <  periodo_banca2[0]:
                    periodo_banca2[0] = data.inic_banca_convidado
                if data.max_banca_convidado != None and data.max_banca_convidado > periodo_banca2[1]:
                    periodo_banca2[1] = data.max_banca_convidado
                if data.autorizacao_mestrando:
                    mestrando = True
            if hoje  == periodo_banca2[0]:
                busca = Q()
                busca.add(Q(groups = 1), busca.OR)
                busca.add(Q(groups = 2), busca.OR)
                if mestrando:
                    busca.add(Q(groups = 3), busca.OR)
                usuarios = User.objects.filter(busca)      
                for usuario in usuarios:
               	    usuario.email_user(
                                       subject=u"Perido de escolha de banca para convidado foi iniciado.",
                                       message=u"Período de escolha de banca para convidado foi iniciado.\n Para escolher uma apresentação para participar entre no Sistema TCCWeb (http://tccweb.icmc.usp.br) usando seu usuário %s, e entre em calendário, procure entre os Horários Reservados."%(str(usuario.username)),
		    from_email=u"noreply@tccweb.com",
                              )

	if datas_monografia != None:
            periodo_original =  datetime.date(hoje.year,1,1)
            for data in datas_monografia:
                if data.max_monografia != None and data.max_monografia > periodo_original:
                    periodo_original = data.max_monografia
            usuarios = User.objects.all()
            #Uma Semana Antes;
            if hoje + datetime.timedelta(days = 7) == periodo_original or hoje + datetime.timedelta(days = 3) == periodo_original or hoje == periodo_original:
                for usuario in usuarios:
                    projetos = ProjetoDeGraduacao.objects.filter(user = usuario.id)
                    projeto_aluno = []
                    for projeto in projetos:
                        if int(projeto.disciplina.semestre) == int(semestre) and int(projeto.disciplina.ano) == int(hoje.year):
			    if usuario.get_profile() in projeto.disciplina.alunos.all():
                            	projeto_aluno.append(projeto)
                    if len(projeto_aluno) != 0:
			if hoje != periodo_original:
                    	    usuario.email_user(
                                   subject=u"Entrega da Monografia Original.",
                                   message=u"Data máxima para entrega da monografia original é dia %s/%s/%s. \nPara submeter a monografia entre no Sistema TCCWeb (http://tccweb.icmc.usp.br) com o nome de usuário %s, na sua tela inicial procure a tabela monografias, e entre em Entregar na coluno Original. Submeta o arquivo com sua monografia."%(str(periodo_original.day),str(periodo_original.month),str(periodo_original.year),str(usuario.username)),
                                   from_email=u"noreply@tccweb.com",
                                )
			else:
			    usuario.email_user(
                                   subject=u"Entrega da Monografia Original.",
                                   message=u"Ultimo dia para entrega da Monografia Original. \nPara submeter a monografia entre no Sistema TCCWeb (http://tccweb.icmc.usp.br) com o nome de usuário %s, na sua tela inicial procure a tabela monografias, e entre em Entregar na coluno Original. Submeta o arquivo com sua monografia."%(str(periodo_original.day),str(periodo_original.month),str(periodo_original.year),str(usuario.username)),
                                   from_email=u"noreply@tccweb.com",
                                )
	        print "Aviso da data maxima para entraga da monografia enviado, data %s/%s/%s"%(str(hoje.day),str(hoje.month),str(hoje.year))
			    




