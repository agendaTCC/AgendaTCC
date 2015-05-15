# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import forms, authenticate, views, login
from django.db.models import Q 
from django import http
from django.core.urlresolvers import reverse
from disciplinas.models import Disciplina
from models import Noticia
from forms import NoticiaForm
from departamentos.models import Departamento
import datetime
from django.http import HttpResponse, HttpResponseRedirect


def noticia_listar(request):
    
    noticias = Noticia.objects.all()
    
    return render_to_response('noticias/noticia_listar.html', {
        'noticias': noticias,
    }, context_instance=RequestContext(request))


def noticia_detalhe(request, noticia_id):
    
    noticia = get_object_or_404(Noticia, pk=noticia_id)

    return render_to_response('noticias/noticia_detalhe.html', {
        'noticia': noticia,
    }, context_instance=RequestContext(request))

@login_required
def noticia_criar(request):
    if request.user.docente or request.user.monitor or request.user.pae or request.user.funcionario or request.user.secretario:
        semestres = request.session['semestre']
        departamentos = []
        semestres = []
        for departamento,semestre in semestres:
            departamentos.append(departamento.id)
            semestres.append(semestre)
        autor = request.user
        if request.method == 'POST':
            form = NoticiaForm(request.POST)
            if form.is_valid():
                noticia = form.save(commit=False)
                noticia.autor = autor
                noticia.save()
                messages.success(request, ('Nova noticia incluida.'))
                return redirect(reverse('listar_noticia'))
            else:
                messages.error(request, ("Problemas ao criar a noticia."))
        else:
            form = NoticiaForm()
            disciplinas = Disciplina.objects.filter(Q(professores = autor)| Q(monitores = autor))
            departamentos = []
            for disciplina in disciplinas:
                if disciplina.semestre.atual:
                    departamentos.append(disciplina.semestre.grupo.id)

            form.fields['disciplina'].queryset = disciplinas
            form.fields['departamento'].queryset = Departamento.objects.filter(id__in = departamentos)
        return render_to_response('noticias/noticia_criar.html', {
            'form': form,
        }, context_instance=RequestContext(request))
    else:
        message.error(request,u'Você não tem autorização para acessar essa pagina')
        return HttpResponseRedirect('/')

