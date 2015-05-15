from django.contrib import admin
from models import Disciplina, NomeDisciplina


class DisciplinaAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (['__unicode__'])
    list_display_links = (['__unicode__'])
    list_filter = ('semestre__grupo','semestre__ano','semestre__semestre', 'titulo__codigo', 'semestre__grupo')
    search_fields = ['semestre__grupo','semestre__ano','semestre__semestre', 'titulo__codigo']
    date_hierarchy = 'criada_em'
    filter_horizontal = ['alunos', 'professores', 'monitores']

admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(NomeDisciplina)