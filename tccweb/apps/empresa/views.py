# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Empresa

def listar_empresas(request):
    empresas = Empresa.objects.all()
    return render_to_response('empresa/listar_empresas.html', {
        'empresas': empresas,
    }, context_instance=RequestContext(request))
    
def empresa_detalhe(request, id):
    empresa = Empresa.objects.get(id=id)
    return render_to_response('empresa/detalhe_empresa.html', {
        'empresa': empresa,
    }, context_instance=RequestContext(request))

@login_required
def empresa_detalhe_supervisor(request, id):
    try:
        empresa = Empresa.objects.get(supervisores=id)
    except:
        empresa = None
    return render_to_response('empresa/detalhe_empresa.html', {
        'empresa': empresa,
    }, context_instance=RequestContext(request))
    

        
    