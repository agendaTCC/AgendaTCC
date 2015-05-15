# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^trocar_semestre/(?P<semestre_id>\w+)/$','semestre.views.trocarSemestre',name='trocar_semestre')
)
