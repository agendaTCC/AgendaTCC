from django.db.models import Q
from ast import literal_eval
import re
from django.contrib.auth import get_user_model as User
from disciplinas.models import Disciplina
from semestre.models import Semestre
from projetos.models import ProjetoDeGraduacao
from departamentos.models import Departamento


def alunosMatriculadosAtual(semestre):
	semestre = semestre.filter(atual = True)
	disciplinas = Disciplina.objects.filter(semestre = semestre)
	query = Q(aluno_disciplina__in=disciplinas)
	return query
def docentesResponsaveisAtual(semestre):
	semestre = semestre.filter(atual = True)
	disciplinas = Disciplina.objects.filter(semestre = semestre)
	query = Q(professor_disciplina__in = disciplinas)
	return query
def alunosMatriculados(semestre):
	disciplinas = Disciplina.objects.filter(semestre = semestre)
	query = Q(aluno_disciplina__in=disciplinas)
	return query
def docentesResponsaveis(semestre):
	disciplinas = Disciplina.objects.filter(semestre = semestre)
	query = Q(professor_disciplina__in = disciplinas)
	return query
def alunosInscritosAtual(semestre):
	semestre = semestre.filter(atual = True)
	disciplina = Disciplina.objects.filter(semestre=semestre)
	projetos = ProjetoDeGraduacao.objects.filter(disciplina__in = disciplina)
	query = Q(projeto_aluno__in = projetos)
	return query

QUERYLIST = {
			'1':['Enviar e-mail para alunos Matriculados no semestre atual',alunosMatriculadosAtual],
			'2':['Enviar e-mail para docentes Responsaveis do semestre atual',docentesResponsaveisAtual],
			'3':['Enviar e-mail para alunos Matriculados(Todos)',alunosMatriculados],
			'4':['Enviar e-mail para docentes Responsaveis(Todos)',docentesResponsaveis],
			'5':['Enviar e-mail para alunos inscritos (projeto submetido)',alunosInscritosAtual]
			}

def options():
	list =[]
	for key,option in QUERYLIST.iteritems():
		list.append((key,option[0]))

	OPCOES = tuple(list)
	return OPCOES

def send_emails(options,departamento, assunto = None,corpo = None):
	if options != []:
		options = literal_eval(options)
		query = Q()
		semestre = Semestre.objects.filter(grupo = departamento)
		for item in options:
			f = QUERYLIST[item][1]
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


def compose_body(dict,body_text):
	if dict and body_text:
		string = body_text
		for key,value in dict.iteritems():
			string = re.sub(r"\{\{\s*\b"+key+r"\b\s*\}\}",value ,string)
		return string
	else:
		return None


