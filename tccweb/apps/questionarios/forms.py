# -*- coding: utf-8 -*-
from django import forms
import re


class QuestionarioRespondidoForm(forms.Form):
 	pass
	def __init__(self, *args, **kwargs):
		perguntas = kwargs.pop('perguntas')
		respostas = kwargs.pop('respostas')
		super(QuestionarioRespondidoForm, self).__init__(*args, **kwargs)
		if not respostas:
			for pergunta in perguntas:
				self.fields['pergunta_'+str(pergunta.id)] = self.correctField(pergunta.pergunta,pergunta.opcoes,pergunta.tipo)
		else:
			for resposta in respostas:
				if resposta.pergunta.tipo == "3":
					_resposta = re.sub('[,][ ]+', ',',resposta.resposta)
					_resposta = _resposta.split(',')
				else:
					_resposta = resposta.resposta
				self.fields['pergunta_'+str(resposta.pergunta.id)] = self.correctField(resposta.pergunta.pergunta,resposta.pergunta.opcoes,resposta.pergunta.tipo,_resposta)
	def clean(self):
		return self.cleaned_data
			
	def extra_answers(self):
		for name, value in self.cleaned_data.items():
			if name.startswith('pergunta_'):
				yield (name[9:], value)

	def cleanOptions(self,optionlist):
		tpl = ()
		optionlist = re.sub('[,][ ]+',',', optionlist)
		optionlist = optionlist.split(',')
		for index,item in enumerate(optionlist):
			tpl = tpl + ((item,item),)
		return tpl
	def correctField(self,label, opcoes,tipo = 0, initial = None):
		if tipo =='0':
			return forms.CharField(label=label,required=False,  widget=forms.Textarea, initial = initial)
		elif tipo =='1':
			return forms.ChoiceField(label = label,required=False, choices = ((u'sim',u'sim'),(u'não',u'não')), widget= forms.RadioSelect, initial = initial)
		elif tipo=='2':
			if opcoes:
				return forms.ChoiceField(label = label,required=False, choices = self.cleanOptions(opcoes), widget= forms.RadioSelect, initial = initial)
			else:
				return forms.CharField(label=label,required=False, widget=forms.Textarea, initial = initial)
		elif tipo=='3':
			if opcoes:
				return forms.MultipleChoiceField(label=label,required=False, widget=forms.CheckboxSelectMultiple, choices=self.cleanOptions(opcoes), initial = initial)
			else:
				return forms.CharField(label=label,required=False, widget=forms.Textarea, initial = initial)
		elif tipo=='4':	
			return forms.CharField(label='<h3>'+label+'</h3>',required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
		else:
			return forms.CharField(label=label,required=False, widget=forms.Textarea)
