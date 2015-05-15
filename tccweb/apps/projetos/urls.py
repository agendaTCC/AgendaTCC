# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^projeto/novo/(?P<usuario_id>\w+)/(?P<disciplina_id>\w+)/$', 'projetos.views.projetoDeGraduacao',name='novo_projeto_de_graduacao'),
	url(r'^projeto/editar/(?P<projeto_id>\w+)/$', 'projetos.views.EditProjetoDeGraduacao',name='editar_projeto_de_graduacao'),
	url(r'^projeto/(?P<projeto_id>\w+)/$', 'projetos.views.viewProjetoDeGraduacao',name='visualisar_projeto_de_graduacao'),
	url(r'^projeto/validar/(?P<projeto_id>\w+)/$', 'projetos.views.validarProjetoDeGraduacao',name='validar_projeto_de_graduacao'),
	url(r'^pendencias/projeto/$', 'projetos.views.pendencias_projeto',name='pendencias_projeto'),
	url(r'^relatorio/entrega/$', 'projetos.views.relatorio_entrega',name='relatorio_entrega'),
	url(r'^projeto/declaracao/horas/projeto=(?P<projeto_id>\w+)$', 'projetos.views.declarar_horas',name='declarar_horas'),
	url(r'^projeto/avaliacao/aluno/projeto=(?P<projeto_id>\w+)$', 'projetos.views.avaliacao_aluno',name='avaliacao_aluno'),
	url(r'^projeto/avaliacao/visualizar/id=(?P<projeto_id>\w+)$', 'projetos.views.visualizar_avaliacao',name='visualizar_avaliacao'),
	)