from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^noticias/$', 'noticias.views.noticia_listar', 
        name='listar_noticia'),
    url(r'^noticia/(?P<noticia_id>\w+)/$', 'noticias.views.noticia_detalhe', 
        name='detalhe_noticia'),
    url(r'^nova/noticia/$', 'noticias.views.noticia_criar', 
        name='nova_noticia'),
)
