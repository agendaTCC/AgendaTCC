from django.contrib import admin
from models import EntregaMonografiaRevisada,  EntregaMonografiaOriginal

class RevisadaAdmin(admin.ModelAdmin):
	save_on_top = True
	list_display = ('get_aluno_display','projeto','data')
	list_display_links = ('get_aluno_display',)
	list_filter = ('projeto__disciplina__semestre__grupo','data')
	search_fields = ['projeto','projeto__disciplina','projeto__disciplina__semestre','projeto__disciplina__semestre__grupo','data']
	date_hierarchy = 'data'


class OriginalAdmin(admin.ModelAdmin):
	save_on_top = True
	list_display = ('get_aluno_display', 'projeto','data')
	list_display_links = ('get_aluno_display',)
	list_filter = ('projeto__disciplina__semestre__grupo','data')
	search_fields = ['projeto','data']
	date_hierarchy = 'data'

admin.site.register(EntregaMonografiaRevisada,RevisadaAdmin)
admin.site.register(EntregaMonografiaOriginal,OriginalAdmin)
    