from django.contrib import admin
from models import Sala

def deactivate(modeladmin, request, queryset):
    queryset.update(ativa=False)
deactivate.short_description = "Desativar selecionados"

def activate(modeladmin, request, queryset):
    queryset.update(ativa=True)
activate.short_description = "Ativar selecionados"

class SalaAdmin(admin.ModelAdmin):
    list_display = (['__unicode__'])
    list_display_links = (['__unicode__'])
    list_filter = ('ativa',)
    actions = [deactivate,activate]


admin.site.register(Sala,SalaAdmin)