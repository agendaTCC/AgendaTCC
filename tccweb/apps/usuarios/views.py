# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import forms, authenticate, views, login , logout as sair
from django import http
from django.core.urlresolvers import reverse
from forms import UserProfileForm, FormRegistro
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
# from empresa.models import Supervisor
# from formularios.models import ProjetoDeGraduacao, HorasCumpridas
# from monografias.models import EntregaMonografiaOriginal, EntregaMonografiaRevisada
import datetime
# from datas.models import Data

import xlrd
from django.shortcuts import redirect
from models import UsuarioAutorizado

import linecache, sys

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


def cadastro(request):
    #Cadastro, retorna para a url o formulario para cadastro existente no arquivos forms.py, verifica se o request  um 
    #metodo POST, se sim, cria um formulario novo com as informacoes recebidas pelo POST, caso essa informacoes sejam
    #validades o formulario e salvo, e a pagina volta ao inicio
    if request.method == 'POST' and 'registro' not in request.POST:
        form = FormRegistro(request.POST)
        if form.is_valid():
            novo_usuario = form.save()
            messages.success(request, ('Cadastro Feito com sucesso!'))
            return HttpResponseRedirect('/')
    else:
        form = FormRegistro(initial={'cpf': request.POST['cpf'], 'email':request.POST['email']})
        
    return render_to_response(
        'usuarios/cadastro.html',
        {'form':form},
        context_instance=RequestContext(request),
        )
    

@login_required
def editprofile(request, usuario_id=None):
    usuario = get_object_or_404(get_user_model(), pk=usuario_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, ('Perfil salvo com sucesso!'))
            return HttpResponseRedirect('/perfil/%d'%int(usuario_id))
    else:
        form = UserProfileForm(instance=usuario)
    return render_to_response('usuarios/edit.html', {
        'form': form, 'usuario':usuario,
    }, context_instance=RequestContext(request))


def _clean_next_url(request):
    """Taken from zamboni. Prevent us from redirecting outside of drumbeat."""
    gets = request.GET.copy()
    url = gets['next']
    if url and '://' in url:
        url = None
    gets['next'] = url
    request.GET = gets
    return request

@login_required
def profile(request, usuario_id):
    usuario = get_object_or_404(get_user_model(), pk=usuario_id)
    return render_to_response('usuarios/perfil.html', {
        'usuario': usuario,
    }, context_instance=RequestContext(request))
            
 
def mylogin(request):
    redirect_to = request.REQUEST.get('next', '/')
    if request.method == 'POST':
    
        user = authenticate(cpf=request.POST['cpf'], password=request.POST['password'])
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(redirect_to or request.META.get('HTTP_REFERER', None))
        else:          
            messages.error(request, ('Nome de usuario ou senha errados.'))  
    if redirect_to != '/':
        return render_to_response('usuarios/login.html', {
        'redirect_to': redirect_to,
        }, context_instance=RequestContext(request))
    else:
       return HttpResponseRedirect(redirect_to)      
 
@login_required()
def logout(request):
    """Destroy user session."""
    sair(request)
    messages.success(request, ('Saiu do sistema com sucesso.'))
    return http.HttpResponseRedirect(reverse('website_index'))

    
@login_required()
def cadastro_usuarios_tidia(request):
    '''
    Métodos: GET, POST

    GET: retorna a página de upload de XSL com a lista de alunos

    POST: recebe um arquivo XSL (vindo do Tidia) e salva os usuários permitidos
    '''
    context = RequestContext(request)
    user = request.user

    if not user.is_staff:
        return http.HttpResponse('403 Forbidden')
    else:

        if request.method == 'GET':
            return render_to_response('usuarios/uploadXSL.html', context_instance=context)

        elif request.method == 'POST':
            #obtem dados do POST
            #try:
            arquivo = request.FILES['xsl_file']
            #except:
            #    return http.HttpResponseBadRequest('<h1>Requisição inválida</h1>')

            log = 'Log de entradas do arquivo XLS:\n'

            #Obtem o aruivo 
            wb = xlrd.open_workbook(filename=None, file_contents=arquivo.read())

            #Obtem a 'sheet' em questão
            s = wb.sheet_by_index(0);

            #usuarios = []

            #Roda todas as linhas
            for linha in range(1,s.nrows):
                a = {}

                a['nome'] = s.cell(linha,0).value
                a['nusp'] = s.cell(linha,1).value
                a['email'] = s.cell(linha,2).value

                salva_usuario_autorizado(request,a['nome'],a['nusp'],a['email'])

                #usuarios.append(a)

            return redirect('/usuarios_autorizados/')        
            #return render_to_response('usuarios/uploadXSLconfirm.html',{'usuario': usuarios}, context_instance=context)


@login_required()
def usuarios_autorizados(request, novo=False):
    '''
    Métodos: GET, POST

    GET: retorna a página de usuários autorizados

    POST: recebe um novo usuário autorizado
    '''
    context = RequestContext(request)
    user = request.user

    if not user.is_staff:
        return http.HttpResponse('403 Forbidden')
    else:

        usuarios = [u for u in UsuarioAutorizado.objects.all()]
        print usuarios
        for u in usuarios:
            print u
            print u.nome_completo

        if request.method == 'GET':
            if novo:
                return render_to_response('usuarios/novo_usuario_autorizado.html',context_instance=context)
            else:
                return render_to_response('usuarios/usuarios_autorizados.html',{'usuarios': usuarios}, context_instance=context)

        elif request.method == 'POST':
            #obtem dados do POST
            try:
                nome = request.POST['nome']
                email = request.POST['nome']
                nusp = request.POST['nome']
            except:
                return http.HttpResponseBadRequest('<h1>Requisição inválida</h1>')

            salva_usuario_autorizado(request,nome,nusp,email)
        else:
            return HttpResponse('Método Não Permitido',status=405)

        return render_to_response('usuarios/usuarios_autorizados.html',{'usuarios': usuarios}, context_instance=context)

@login_required
def remove_usuarios_autorizados(request, nusp=False, todos=False):
    '''
    Métodos: GET

    GET: Recebe um parametro (um numero usp, ou todos) e exclui o ususario de acordo - caso 
    o usuário tenha permissão

    '''
    context = RequestContext(request)
    user = request.user

    if not user.is_staff:
        return http.HttpResponse('403 Forbidden')
    else:

        if request.method == 'GET':

            if nusp:
                try:
                    usuario = UsuarioAutorizado.objects.filter(nusp=nusp).delete();
                    messages.info(request, 'Usuário removido com sucesso')
                    return redirect('/usuarios_autorizados/')                
                except Exception, e:
                    return HttpResponse('Arquivo Não Encontrado',status=404)

            elif todos:
                try:
                    for u in UsuarioAutorizado.objects.all():
                        u.delete();
                except Exception, e:
                    messages.info(request, 'Erro desconhecido ao excluir usuários')

                messages.info(request, 'Usuários removidos com sucesso')

            return redirect('/usuarios_autorizados/')                

def salva_usuario_autorizado(request, nome, nusp, email):
    '''
    Salva um usuario autorizado no BD
    '''
    valid = True

    if not nome:
        valid = False
    if not nusp or nusp == '':
        valid = False

    if valid:
        #Tenta salvar o novo cliente no banco
        try:
            #Cria usuario
            usuario = UsuarioAutorizado.objects.create(nome_completo=nome,numero_usp=nusp)

            if email != '':
                usuario.email = email
        
            #Realiza um commit no bd
            usuario.save()

            messages.info(request, "Cadastro realizado com sucesso!")
        except Exception, e:
            #Para qualquer problema, retorna um erro interno   
            PrintException()             
            messages.error(request, 'Erro desconhecido ao cadastrar.')
