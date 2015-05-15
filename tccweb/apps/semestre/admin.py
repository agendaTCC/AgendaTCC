# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Semestre

#DataAdmin: Organiza a visualizacao do modelo Data na administracao;
#admin.site.register(Data,DataAdmin), coloca o modelo Data na adminstricao, respeitando o DataAdmin;

class SemestreAdmin(admin.ModelAdmin):
    fieldsets = (
                ('Configurações', {
                        'fields':['ano', 'semestre', 'grupo','inicio_semestre','fim_semestre','atual']
                        }),
                ('Inscrição de Alunos',{
                                       'fields':['inic_inscricao','max_inscricao']
                                       }),
                ('Mudança de Titulo e áreas de concentração',{
                                                              'fields':['max_titulo_areas']
                                                              } ),
                ('Escolha da Banca pelos Alunos',{
                                                  'fields':['inic_banca_alunos','max_banca_alunos']
                                                  } ),
                ('Escolha da Banca pelos Professores Responsaveis',{
                                                      'fields':['inic_banca_responsavel','max_banca_responsavel']
                                                      } ),
                ('Escolha da Banca pelos Convidados',{
                                                      'fields':['inic_banca_convidado','max_banca_convidado']
                                                      } ),
                ('Periodo de Apresentação das Bancas',{
                                                      'fields':['inic_apresentacao','max_apresentacao']
                                                      } ),
                )
    list_display = ('grupo', 'semestre', 'ano', 'inicio_semestre', 'fim_semestre')
    ordering = ('grupo',)
    list_filter = ['grupo','ano','semestre']
admin.site.register(Semestre,SemestreAdmin)