# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from models import Semestre

@login_required
def trocarSemestre(request,semestre_id):
	try:
		semestre = Semestre.objects.get(pk = semestre_id)
	except:
		messages.error(request, u'Semestre Não enconstrado')
		return HttpResponseRedirect(request.session.get('last_visited'))
	if 'semestre' in request.session:
		semestres = request.session['semestre']
		semestres[semestre.grupo] = semestre
		request.session['semestre'] = semestres
	return HttpResponseRedirect('/')



    
