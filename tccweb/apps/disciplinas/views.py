# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import forms, authenticate, views, login
from django import http
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q 
from django.core.urlresolvers import reverse
from models import Disciplina

from projetos.models import ProjetoDeGraduacao
from departamentos.models import Departamento
import datetime


@login_required
def matricula(request,departamento_id):
	departamento = Departamento.objects.get(id = departamento_id)
	semestre = request.session['semestre'][departamento]
	if(request.session['hoje'] >= semestre.inic_inscricao and request.session['hoje'] <= semestre.max_inscricao):
	    disciplinas = Disciplina.objects.filter(esta_ativa=True, semestre = semestre.id)
	    return render(request,'disciplinas/disciplina_matricula.html', {
	        'disciplinas': disciplinas,
	    })
	else:
		return HttpResponseRedirect('/')
    
        
    
    
