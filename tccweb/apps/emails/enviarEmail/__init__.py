from django.contrib.auth import get_user_model as User
from disciplinas.models import Disciplina
from semestre.models import Semestre
from django.db.models import Q
from ast import literal_eval

def alunosInscritosAtual(semestre):
	semestre = semestre.filter(atual = True)
	disciplinas = Disciplina.objects.filter(semestre = semestre)
	query = Q(aluno_disciplina__in=disciplinas)
	return query
def docentesResponsaveisAtual(semestre):
	semestre = semestre.filter(atual = True)
	disciplinas = Disciplina.objects.filter(semestre = semestre)
	query = Q(professor_disciplina__in = disciplinas)
	return query

def alunosInscritos(semestre):
	disciplinas = Disciplina.objects.filter(semestre = semestre)
	query = Q(aluno_disciplina__in=disciplinas)
	return query
def docentesResponsaveis(semestre):
	disciplinas = Disciplina.objects.filter(semestre = semestre)
	query = Q(professor_disciplina__in = disciplinas)
	return query

QUERYLIST = {
			'1':['Enviar e-mail para alunos Inscritos no semestre atual',alunosInscritosAtual],
			'2':['Enviar e-mail para docentes Responsaveis do semestre atual',docentesResponsaveisAtual],
			'3':['Enviar e-mail para alunos Inscritos(Todos)',alunosInscritos],
			'4':['Enviar e-mail para docentes Responsaveis(Todos)',docentesResponsaveis]
			}

def options():
	list =[]
	for key,option in QUERYLIST.iteritems():
		list.append((key,option[0]))

	OPCOES = tuple(list)
	return OPCOES

def send_emails(options,departamento, assunto = None,corpo = None):
	options = literal_eval(options)
	query = Q()
	semestre = Semestre.objects.filter(grupo = departamento)
	for item in options:
		f = QUERYLIST[item][1]
		print QUERYLIST[item][0]
		query.add(f(semestre), query.OR)
	usuarios = User().objects.filter(query)
	dispatch(usuarios,assunto, corpo)

def dispatch(usuarios, assunto, corpo):
	sended = []
	if usuarios:
		for item in usuarios:
			if not item in sended:
				item.email_user(assunto, corpo)
				sended.append(item)


