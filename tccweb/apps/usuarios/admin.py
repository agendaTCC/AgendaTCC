# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from models import _User, CSVUsuario
from forms import _UserChangeForm,_UserCreationForm

def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)
deactivate.short_description = "Desativar Usuarios selecionados"

def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate.short_description = "Ativar Usuarios selecionados"


class _UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        (_(u'Informações Pessoais'), {'fields': ('nome_completo','email','numero_usp','curso','endereco',
                                        'numero','complemento','cidade','uf',
                                        'bairro','tel','cep',)}),
        (_(u'Permissões do Sistema'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       # 'groups', 
                                       'user_permissions'
                                       )}),
        (_(u'Funções'), {'fields': ('docente','doutorando', 'mestrando','aluno', 'funcionario','monitor','pae','supervisor','secretario')}),
        (_('Datas Importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'password1', 'password2')}
        ),
    )
    form = _UserChangeForm
    add_form = _UserCreationForm
    list_display = ('nome_completo', 'email', 'cpf', 'is_staff',)
    search_fields = ('nome_completo', 'email', 'cpf','numero_usp')
    ordering = ('nome_completo',)
    actions = [deactivate,activate]
    list_filter = ['docente','doutorando','mestrando','aluno','funcionario','supervisor','monitor','pae','secretario' , 'is_staff', 'is_superuser', 'is_active']

class CsvUsuarioAdmin(admin.ModelAdmin):
    # save_on_top = True
    # list_display = (['criada_em'])
    # list_display_links = (['criada_em'])
    # search_fields = ['criada_em']
    # date_hierarchy = 'criada_em'
    readonly_fields=('log',)

admin.site.register(CSVUsuario,CsvUsuarioAdmin)
admin.site.register(_User, _UserAdmin)

