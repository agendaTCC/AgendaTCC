from django.contrib import admin
from models import ProjetoDeGraduacao, DeclaracaoDeHoras, AvaliacaoAluno
from forms import ProjetoDeGraduacaoAdminForm

class ProjetoDeGraduacaoAdmin(admin.ModelAdmin):
	form = ProjetoDeGraduacaoAdminForm
	ordering = ['aluno']
	list_display = ('aluno','titulo','disciplina','data')
	list_filter = ('disciplina__semestre__ano','disciplina__semestre__semestre', 'disciplina__titulo__codigo','disciplina__semestre__grupo')
	search_fields = ['aluno__nome_completo', 'disciplina__titulo__titulo', 'disciplina__titulo__codigo','disciplina__semestre__ano','disciplina__semestre__semestre']


class DeclaracaoDeHorasAdmin(admin.ModelAdmin):
	list_display = ('get_aluno_display','get_titulo_display','get_semestre_display')
	list_display_links = ('get_aluno_display',)
	list_filter = ('projeto__disciplina__semestre__grupo',)
	search_fields = ['projeto__aluno','projeto__disciplina','projeto__disciplina__semestre','projeto__disciplina__semestre__grupo',]

class AvaliacaoAlunoAdmin(admin.ModelAdmin):
	list_display = ('get_aluno_display','get_titulo_display','get_semestre_display')
	list_display_links = ('get_aluno_display',)
	list_filter = ('projeto__disciplina__semestre__grupo',)
	search_fields = ['projeto__aluno','projeto__disciplina','projeto__disciplina__semestre','projeto__disciplina__semestre__grupo',]



admin.site.register(ProjetoDeGraduacao, ProjetoDeGraduacaoAdmin)
admin.site.register(DeclaracaoDeHoras,DeclaracaoDeHorasAdmin)
admin.site.register(AvaliacaoAluno,AvaliacaoAlunoAdmin)