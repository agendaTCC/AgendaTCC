from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^monografia/original/projeto?id=(?P<projeto_id>\w+)/$', 'monografias.views.entrega_monografia_original', 
        name='entrega_monografia_original'),
    url(r'^monografia/revisada/projeto?id=(?P<projeto_id>\w+)/$', 'monografias.views.entrega_monografia_revisada', 
        name='entrega_monografia_revisada'),
    url(r'^download/monografia/revisada/projeto?id=(?P<projeto_id>\w+)/$', 'monografias.views.download_monografia_revisada', 
        name='download_monografia_revisada'),
    url(r'^download/monografia/original/projeto?id=(?P<projeto_id>\w+)/$', 'monografias.views.download_monografia_original', 
        name='download_monografia_original'),
    # url(r'^monografia/gerenciar/$', 'monografias.views.gerenciar_monografias', 
    #     name='gerenciar_monografias'),
    # url(r'^monografia/receber/impressa/(?P<aluno_id>\w+)/(?P<disciplina_id>\w+)/$', 'monografias.views.receber_monografia_impressa', 
    #     name='receber_monografia_impressa'),
    # url(r'^monografia/receber/emprestada/(?P<aluno_id>\w+)/(?P<disciplina_id>\w+)/$', 'monografias.views.receber_monografia_emprestada', 
    #     name='receber_monografia_emprestada'),
)
