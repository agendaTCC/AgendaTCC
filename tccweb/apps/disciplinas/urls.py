from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^matricula/(?P<departamento_id>\w+)/$','disciplinas.views.matricula',name='matricula'),
)
