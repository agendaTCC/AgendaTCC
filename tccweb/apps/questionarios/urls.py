from django.conf.urls import patterns, url


urlpatterns = patterns('',
		url(r'^questionario/responder/projeto/questionario/(?P<projeto_id>\w+)/(?P<questionario_id>\w+)/$', 'questionarios.views.responderQuestionario',name='responderQuestionario'),
		url(r'^questionario/respondido/projeto/questionario/(?P<projeto_id>\w+)/(?P<questionario_id>\w+)/$', 'questionarios.views.visualizarQuestionario',name='visualizarQuestionario'),
    )