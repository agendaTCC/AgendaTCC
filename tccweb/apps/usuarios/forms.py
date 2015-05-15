# -*- coding: utf-8 -*-
from django.forms import ModelForm , EmailField
from django import forms
from django.core.validators import EMPTY_VALUES

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from usuarios.models import _User

class _UserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(_UserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = _User
        fields = ("cpf","email",)

class _UserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(_UserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = _User


#UserProfileForm, cria formulario a partir do Modelo para edicao pelo usario
#FormRegitro, cria formulario a partir do modelo para criacao de usuario, trata a existencia ea concistencia dos dados

class  UserProfileForm(ModelForm):
    class Meta:
        model = _User
        exclude = (
            'password','date_joined','docente','doutorando','mestrando',
            'aluno','funcionario','monitor','pae','supervisor','secretario',
            'last_login','is_staff', 'is_superuser','is_active','groups','user_permissions')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['cpf'].widget.attrs['readOnly'] = True

    def clean_cpf(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.cpf
        else:
            return self.cleaned_data['cpf']
 
def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0

            
class FormRegistro(ModelForm):
    class Meta:
        model=_User
        order_by = ['cpf','email', 'nome_completo', 'numero_usp', 'password']
        fields = ('cpf','email','nome_completo','numero_usp','password')
    confirme_a_senha = forms.CharField( max_length=30, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        self.base_fields['password'].help_text = ''
        self.base_fields['password'].widget = forms.PasswordInput()
        super(FormRegistro, self).__init__(*args, **kwargs)

    def clean_cpf(self):
        value = self.cleaned_data['cpf']
        if not value:
            raise forms.ValidationError('Este campo é obrigatório.')
        try:
            int(value)
        except ValueError:
            raise forms.ValidationError('Somente Digitos')
        if len(value) != 11:
            raise forms.ValidationError('Numero de Digitos Incorreto')
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise forms.ValidationError('Cpf Invalido')
        if _User.objects.filter(
            cpf=self.cleaned_data['cpf'],
            ).count():
            raise forms.ValidationError('Já existe um usuário com esse cpf')
        return self.cleaned_data['cpf']
    def clean_nome_completo(self):
        if not self.cleaned_data['nome_completo']:
            raise forms.ValidationError('Este campo é obrigatório.')
        return self.cleaned_data['nome_completo']
    def clean_numero_usp(self):
        if not self.cleaned_data['numero_usp']:
            raise forms.ValidationError('Este campo é obrigatório.')
        return self.cleaned_data['numero_usp']

    def clean_confirme_a_senha(self):
        if self.cleaned_data['confirme_a_senha'] != self.data['password']:
            raise forms.ValidationError(u'Confirmação da senha não confere!')

        return self.cleaned_data['confirme_a_senha']
    def save(self, commit=True):
        usuario = super(FormRegistro, self).save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        if commit:
            usuario.save()
        return usuario

