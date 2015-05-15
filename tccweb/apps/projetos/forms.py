# -*- coding: utf-8 -*-
from django.forms import ModelForm,  MultipleChoiceField, ValidationError, EmailField, CheckboxSelectMultiple
from django import forms
from models import ProjetoDeGraduacao, DeclaracaoDeHoras, AvaliacaoAluno


AREAS_RELACIONADAS = (
        ('a', u'Engenharia de Softtware e Sistemas de Informação'),
        ('b', u'Inteligencia Computacional'),
        ('c', u'Banco de Dados'),
        ('d', u'Computação Gráfica e Processamento de Imagens'),
        ('e', u'Hipermídia'),
        ('f', u'Computação Bioinspirada'),
        ('g', u'Otimização e Modelos Estocásticos'),
        ('h', u'Gerenciamento de Redes'),
        ('i', u'Mecânica dos Fluidos Computacionais'),
        ('j', u'Sistemas Distribuídos e Programaçãoo Concorrente'),
        ('k', u'Arquitetura de Computadores'),
        ('l', u'Outras'),
        )

class ProjetoDeGraduacaoAdminForm(ModelForm):
    area = MultipleChoiceField(label='Áreas Relacionadas',required=False, widget=CheckboxSelectMultiple, choices=AREAS_RELACIONADAS)

class ProjetoDeGraduacaoForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(ProjetoDeGraduacaoForm, self).__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('orientador') == None and cleaned_data.get('supervisor') == None:
            raise forms.ValidationError('Os campos Supervisor ou orientador devem ser preenchidos!')
        elif cleaned_data.get('orientador') != None and cleaned_data.get('supervisor') != None:
            raise forms.ValidationError('Somente um dos campos Supervisor ou orientador devem ser preenchidos!')
        return cleaned_data    
        
    required_css_class = 'required'
    error_css_class = 'error'
    area = MultipleChoiceField(label='Áreas Relacionadas',required=False, widget=CheckboxSelectMultiple, choices=AREAS_RELACIONADAS)
    class Meta:
        
        model = ProjetoDeGraduacao
        exclude = ('disciplina','aluno','validacao_docente','validacao_graduacao', 'validacao_supervisor_orientador', 'rascunho','justificativa','cancelado',)

class ProjetoDeGraduacaoFormReadOnly(ModelForm):
    class Meta:
        model = ProjetoDeGraduacao
        exclude = ('disciplina',
                   'aluno',
                   'validacao_docente',
                   'validacao_graduacao',
                   'validacao_supervisor_orientador',
                   'rascunho',
                   'orientador',
                   'supervisor',
                   'descricao',
                   'atividades',
                   'cronograma',
                   'justificativa',
                   'cancelado',
                    )
    area = MultipleChoiceField(label='Áreas Relacionadas',required=False, widget=CheckboxSelectMultiple, choices=AREAS_RELACIONADAS)

class DeclaracaoDeHorasForm(ModelForm):
    class Meta:
        model = DeclaracaoDeHoras
        exclude = ('projeto')

class AvaliacaoAlunoForm(ModelForm):
    class Meta:
        model = AvaliacaoAluno
        exclude = ('projeto')

