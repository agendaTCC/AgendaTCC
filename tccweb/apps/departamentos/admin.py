from django.contrib import admin
from models import Departamento


class DepartamentoAdmin(admin.ModelAdmin):
    filter_horizontal = ['docentes_responsaveis']
admin.site.register(Departamento,DepartamentoAdmin)
