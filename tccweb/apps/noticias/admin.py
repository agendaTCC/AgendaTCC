from django.contrib import admin
from models import Noticia

class NoticiaAdmin(admin.ModelAdmin):
    save_on_top = True
    date_hierarchy = 'criada_em'
    list_display = ['__unicode__', 'disciplina']
    list_display_links = (['__unicode__'])
    list_filter = ('titulo', 'disciplina')
    search_fields = ['titulo', 'disciplina']
    list_select_related = True
    # raw_id_fields = ("disciplina",)


admin.site.register(Noticia, NoticiaAdmin)