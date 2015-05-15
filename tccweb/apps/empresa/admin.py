from django.contrib import admin
from models import Empresa
class EmpresaAdmin(admin.ModelAdmin):
	save_on_top = True
	list_display = ('nome_fantasia','nro_inscricao','data_inicio_convenio','data_final_convenio')
	list_display_links = ('nome_fantasia','nro_inscricao')
	search_fields = ['nome_fantasia','nro_inscricao']
	date_hierarchy = 'data_inicio'
	filter_horizontal = ['supervisores']
    
admin.site.register(Empresa,EmpresaAdmin)