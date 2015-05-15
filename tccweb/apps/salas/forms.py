# -*- coding: utf-8 -*-
from django.forms import ModelForm, ValidationError
from models import Sala


class SalaForm(ModelForm):
    class Meta:
        model = Sala
        
        
    def clean_nome(self):
        if Sala.objects.filter(
            nome=self.cleaned_data['nome'],
            ).count():
            raise ValidationError('Já existe uma Sala com esse Nome')
        return self.cleaned_data['nome']