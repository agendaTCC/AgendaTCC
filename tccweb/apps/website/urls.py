from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test


urlpatterns = patterns('',
    url(r'^$', 'website.views.index', name='website_index'),
    url(r'^termos/$',TemplateView.as_view(template_name='website/termos_de_uso.html'), name='website_termos'),
    url(r'^sobre/$', TemplateView.as_view(template_name='website/sobre.html'), name='website_sobre'),
    url(r'^relatorios/$', login_required(TemplateView.as_view(template_name='website/relatorios.html')), name='website_relatorios'),
)
