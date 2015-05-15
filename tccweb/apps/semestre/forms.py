# -*- coding: utf-8 -*-
from models import Data
from monografias.models import DatasMonografia
from django.forms import ModelForm
from django import forms
#Cria formulario a partir do Modelo Data

class DatasLimiteForm(ModelForm):
    class Meta:
        model = Data
        exclude = ('grupo', 'ano', 'semestre')
    def clean(self):
        cleaned_data = self.cleaned_data
        max_autorizacao = cleaned_data.get('max_autorizacao')
        max_inscricao = cleaned_data.get('max_inscricao')
        if max_autorizacao != None and max_inscricao != None:
            if max_autorizacao < max_inscricao:
                raise forms.ValidationError(u'Data maxima para o fechamento da matricula não pode ser anterior a data maxima para matricula dos alunos')
        return cleaned_data
class DatasMonografiaForm(ModelForm):
    class Meta:
        model = DatasMonografia
        exclude = ('grupo_de_disciplinas', 'ano', 'semestre')
        
    
        