# -*- coding: utf-8 -*-
from django.forms import ModelForm,  MultipleChoiceField,CheckboxSelectMultiple, DateField, DateTimeInput, ValidationError
from django.forms.models import inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.admin.widgets import AdminDateWidget 
from models import Dia_Agenda, Banca, Agenda
from disciplinas.models import Disciplina
from projetos.models import ProjetoDeGraduacao
from semestre.models import Semestre
# from datas.models import Data
import datetime

hoje = datetime.datetime.now()
hoje = datetime.date(hoje.year, hoje.month, hoje.day)
if hoje.month <= 6:
    semestre = 1
else:
    semestre = 2

PERIODOS = (
            ('m','Manha'),
            ('t','Tarde'),
            ('n','Noite'),            
            )

class DiaForm(ModelForm):
    data = DateField(widget=AdminDateWidget())
    class Meta:
        model = Dia_Agenda
    def clean_horarios(self):
        horarios=self.cleaned_data['horarios']
        if horarios.endswith(';'):
            horarios = horarios[:-1]
        if not horarios:
            self.cleaned_data['horarios'] = None
            return self.cleaned_data['horarios']
        horarios = horarios.strip()
        if horarios.count(' ') != 0:
            raise ValidationError(u'Formato da entrada é incorreto, espaços não são permitidos')
        self.cleaned_data['horarios'] = horarios
        return self.cleaned_data['horarios']

    def clean_data(self):
        data = self.cleaned_data['data']
        agenda = self.cleaned_data['agenda']
        semestre = agenda.semestre
        if not semestre:
            raise ValidationError('Período de apresentações não definido')
        if semestre.isBancaDefined():
            if not semestre.inBanca(data):
                raise ValidationError('Data fora do Período de apresentações. Apresentações de '+semestre.inic_apresentacao.strftime('%d/%m/%Y')+', até '+semestre.max_apresentacao.strftime('%d/%m/%Y')+'.')
            else:
                return self.cleaned_data['data']
        else:
            raise ValidationError('Período de Apresentações não definido')
        
class BancaForm(ModelForm):
    class Meta:
        model = Banca
        exclude = ('data','hora_inicial','hora_final','semestre','aluno','sala','empresa','reservada','alteravel','banca_docente','banca_convidado','cancelada')
        
class AgendamentoForm(ModelForm):
    class Meta:
        model = Agenda
        exclude = ('grupo')
        
dia_agenda_formset = inlineformset_factory(Agenda,Dia_Agenda,form = DiaForm, extra = 365, can_delete=False)      

class EditarBancaForm(ModelForm):
    class Meta:
        model = Banca 
        exclude = ('hora_inicial','hora_final','data','grupo','sala','orientador','empresa','reservada','alteravel','projeto')
    
    
    def clean(self):
        cleaned_data = self.cleaned_data
        banca1 = cleaned_data.get('banca1')
        banca2 = cleaned_data.get('banca2')
        aluno = cleaned_data.get('aluno')
        disciplina = cleaned_data.get('disciplina')
        if aluno == None:
            return cleaned_data
        try:
            projeto =  ProjetoDeGraduacao.objects.get(user=aluno, disciplina = disciplina)  
        except:
            raise ValidationError('Usuário Não tem Projeto Preenchido para essa disciplina')   
        if banca1 == None:
            return cleaned_data
        if banca1 == projeto.orientador:
            raise ValidationError('Banca1 Não Pode Ser o Orientador do Aluno')
        if banca2 == None:
            return cleaned_data
        if banca2 == projeto.orientador:
            raise ValidationError('Banca2 Não Pode Ser o Orientador do Aluno')
        return cleaned_data
    
        
         
