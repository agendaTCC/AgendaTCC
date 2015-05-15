from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^perfil/(?P<usuario_id>\w+)/$', 'usuarios.views.profile',name='visualizar_perfil'),
    url(r'^login/$', 'usuarios.views.mylogin', name='usuarios_login'),
    url(r'^logout/$', 'usuarios.views.logout', name='usuarios_logout'),
    url(r'^perfil/edit/(?P<usuario_id>\w+)/$', 'usuarios.views.editprofile',name='editar_perfil'),
    url(r'^cadastro/$', 'usuarios.views.cadastro', name='usuarios_cadastro'),
    url(r'^usuarios_autorizados/$', 'usuarios.views.usuarios_autorizados', name='usuarios_autorizados'),
    url(r'^usuarios_autorizados/importar/$', 'usuarios.views.cadastro_usuarios_tidia', name='cadastro_usuarios_tidia'),
    url(r'^usuarios_autorizados/novo/$', 'usuarios.views.usuarios_autorizados',{'novo':True}, name='cadastro_usuario_autorizado'),
    url(r'^usuarios_autorizados/remover/$', 'usuarios.views.remove_usuarios_autorizados',{'todos':True}, name='remover_usuarios_autorizados'),
    url(r'^usuarios_autorizados/(?P<nusp>[0-9]+)/remover/$', 'usuarios.views.remove_usuarios_autorizados', name='remover_usuario_autorizado'),
    url(r'^tidia/importar/$', 'usuarios.views.cadastro_usuarios_tidia', name='cadastro_usuarios_tidia'),
    url(r'^password/change/$', 'django.contrib.auth.views.password_change',{'template_name':'usuarios/password_change_form.html'}, name='auth_password_change'), 
    url(r'^password/change/done/$', 'django.contrib.auth.views.password_change_done',{'template_name':'usuarios/password_change_done.html'}, name='auth_password_change_done'), 

)


