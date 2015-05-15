from django.conf.urls import patterns, include, url
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tccweb.views.home', name='home'),
    # url(r'^tccweb/', include('tccweb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
        
    
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', 
        {'template_name':'usuarios/password_reset_form.html',
          }, name='password_reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', 
        {'template_name':'usuarios/password_reset_done.html'}),

    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', 
        {'template_name':'usuarios/password_reset_confirm.html'}),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', 
        {'template_name':'usuarios/password_reset_complete.html'}),
    (r'', include('website.urls')),
    (r'', include('usuarios.urls')),
    (r'', include('disciplinas.urls')),
    (r'', include('projetos.urls')),
    (r'', include('semestre.urls')),
    (r'', include('departamentos.urls')),
    (r'', include('noticias.urls')),
    # (r'', include('atividades.urls')),
    # (r'', include('eventos.urls')),
    # (r'', include('formularios.urls')),
    (r'', include('bancas.urls')),
    # (r'', include('datas.urls')),
    (r'', include('empresa.urls')),
    (r'', include('monografias.urls')),
    # (r'', include('emails.urls')),
    (r'', include('questionarios.urls')),
    # (r'^busca/', include('haystack.urls')),

    url('', include('social.apps.django_app.urls', namespace='social')),

    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

