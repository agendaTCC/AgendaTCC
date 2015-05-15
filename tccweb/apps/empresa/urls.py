from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^empresas/$', 'empresa.views.listar_empresas',name='listar_empresas'),
    url(r'^empresa/(?P<id>\w+)/$', 'empresa.views.empresa_detalhe',name='empresa_detalhe'),
    url(r'^empresa/supervisor/(?P<id>\w+)/$', 'empresa.views.empresa_detalhe_supervisor',name='empresa_detalhe_supervisor'),
    )