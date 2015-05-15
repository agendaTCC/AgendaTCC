# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from django.contrib import admin
from models import Banca, Apresentacao, Agenda, Dia_Agenda
from forms import DiaForm
from django.http import HttpResponseRedirect
from django.contrib import messages

def cancel(modeladmin, request, queryset):
    queryset.update(cancelada=True)
cancel.short_description = "Cancelar bancas selecionadas"

def activate(modeladmin, request, queryset):
    queryset.update(cancelada=False)
activate.short_description = "Ativar bancas selecionadas"


class DiaAdmin(admin.StackedInline):
    model = Dia_Agenda
    form = DiaForm
    extra = 7
    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an edit
            return ['data','horarios'] # Return a list or tuple of readonly fields' names
        else: # This is an addition
            return []

class AgendaAdmin(admin.ModelAdmin):
    inlines = [DiaAdmin,]
    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an edit
	    return ['salas','semestre'] # Return a list or tuple of readonly fields' names
        else: # This is an addition
	    return []
class BancaAdmin(admin.ModelAdmin):
    list_display = ('sala', 'data', 'hora_inicial', 'hora_final', 'semestre', 'reservada','cancelada', 'projeto',)
    ordering = ('data',)
    list_filter = ['semestre','sala','reservada']
    actions = [cancel,activate]
    def get_urls(self):
        urls = super(BancaAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^cancelar/bancas/$', self.cancelarNaoUtilizadas )
        )
        return my_urls + urls

    def cancelarNaoUtilizadas(self,request):
        try:
            bancas =  Banca.objects.all()
        except:
            messages.error(request, (u'Bancas não puderam ser selecionadas!'))
            return HttpResponseRedirect('/bancas/')
        for banca in bancas:
            if not banca.reservada and banca.semestre.atual:
                banca.cancelada = True
                banca.save()
        messages.success(request, (u'Bancas canceladas com sucesso!'))
        return HttpResponseRedirect('/admin/bancas/banca/')





admin.site.register(Banca, BancaAdmin)
admin.site.register(Agenda,AgendaAdmin)
