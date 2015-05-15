# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from csv import reader, excel
from django.contrib.auth import get_user_model
from models import CSVUsuario
from random import choice

import os.path
import xlrd



#Testar para resolver problemas de unicode
def unicode_csv_reader(utf8_data, dialect=excel, **kwargs):
    csv_reader = reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def gera_senha(tamanho):
    """ -=-=-=- Funcao responsavel por gerar a senha..."""
    caracters = '0123456789abcdefghijlmnopqrstuwvxzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$'
    tamanho = int(tamanho)

    passwd = ''
    for char in range(tamanho):
        passwd += choice(caracters)

    return passwd

def csvAdd(sender,**kw):

	print 'aaaa'

	instance = kw["instance"]
	if kw["created"]:
		# file = reader(instance.file,delimiter = ';')

		#Verifica se o arquivo é CSV ou XLS
		#Caso seja XLS, utiliza o novo código do TCC Agenda para importar os dados de acordo com
		# o formato exportado pelo TIDIA.

		print instance
		print instance.file

		extensao = os.path.splitext(str(instance.file))[1]

		print extensao

		if extensao.lower() == '.xls':

			log = 'Log de entradas do arquivo XLS:\n'

			arquivo = instance.file.path

			print arquivo

			#Obtem o aruivo 
			wb = xlrd.open_workbook(arquivo)

			#Obtem a 'sheet' em questão
			s = wb.sheet_by_index(0);

			#Roda todas as linhas
			for linha in range(s.nrows):
				print 'Novo Aluno:'

				nome = s.cell(linha,0)
				nusp = s.cell(linha,1)
				email = s.cell(linha,3)

			a = 1/0


		elif extensao.lower() == '.csv':
			file = unicode_csv_reader(instance.file,delimiter = ';')
			log = 'Log de entradas do arquivo CSV:\n'
			for row in file:
				if(len(row) == 4):
					cpf = row[0]
					if len(cpf) != 11:
						log += 'Cpf invalido!\n'
						continue
					nome_completo = row[1]
					email = row[2]
					funcao = row[3]
					senha = gera_senha(10)
					try:
						usuario = get_user_model().objects.create_user(cpf,email,senha)
					except:
						log += u'Usuário '+nome_completo+u' não foi adicionado!\n'
						continue
					usuario.nome_completo = nome_completo
					usuario.aluno = False
					funcao = int(funcao)
					if funcao == 1:
						usuario.docente = True
					elif funcao == 2:
						usuario.doutorando = True
					elif funcao == 3:
						usuario.mestrando = True
					elif funcao == 4:
						usuario.aluno = True
					elif funcao == 5:
						usuario.funcionario = True
					elif funcao == 6:
						usuario.monitor = True
					elif funcao == 7:
						usuario.pae = True
					elif funcao == 8:
						usuario.supervisor = True
					elif funcao == 9:
						usuario.secretario = True
					usuario.save()

					log += u'Usuário '+nome_completo+u' adicionado com sucesso!\n'
					# usuario.email_user('tccweb@icmc.usp.br',
					# 	'Olá '+ nome_completo+', bem vindo ao tccweb \n\n\
					# 	Seu nome de usuario é seu cpf:\n\n'+cpf+'\n\n sua senha é:\n\n\
					# 	'+senha+'\n\nQulquer duvida entre em contato com duvidas@tccweb.icms.usp.br.')
				else:
					log += 'Formato Invalido!\n'
		else:
			log = 'Arquivo não identificado!\n'

		instance.log = log
		instance.save()

post_save.connect(csvAdd, sender=CSVUsuario, dispatch_uid="usuarios-csvusuario-signal")
