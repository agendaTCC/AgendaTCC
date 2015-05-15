# -*- coding: utf-8 -*-
from south.modelsinspector import add_introspection_rules
from django.db import models
from django.conf import settings
from widgets import ColorWidget
from django.db.models import Q 


# from disciplinas.models import Disciplina, NomeDisciplina
SEMESTRE = (
            ('1','1semestre'),
            ('2','2semestre'),
            )




class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)

add_introspection_rules([(
    (ColorField,),
    [],
    {
    },
  )], ["^departamentos\.models\.ColorField"])

class Departamento(models.Model):
#    modelo de grupos de disciplinas
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
    titulo = models.CharField(max_length=255, verbose_name='Nome do Grupo')
    watermark = models.FileField(upload_to = settings.MEDIA_ROOT+"/watermarks/", default=settings.MEDIA_ROOT+'/img/generico.gif')
    cor = ColorField(blank=True)
    docentes_responsaveis = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True,related_name="docentes_responsaveis_pelo_grupo", limit_choices_to={'docente':True})
    def __unicode__(self):
        #Modo como o Modelo e Exibido na Lista na Adminstracao
        return unicode(self.titulo)

# class Monitor(models.Model):
#     class Meta:
#         verbose_name = 'Monitor do Grupo'
#         verbose_name_plural = 'Monitores dos Grupos'
#     monitor = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="monitor_grupo", limit_choices_to={'docente': True})
        
# class ResponsavelGrupo(models.Model):
#     class Meta:
#         verbose_name = 'Docente Responsavel pelo Grupo'
#         verbose_name_plural = 'Docentes Responsaveis por Grupos'
#     docentes = models.ManyToManyField(settings.AUTH_USER_MODEL,through='Responsaveis', verbose_name = 'Docentes')
#     # monitores = models.ManyToManyField(settings.AUTH_USER_MODEL,through='Monitores',verbose_name = 'Monitores' )
#     grupo = models.ForeignKey(Departamento) 
#     def __unicode__(self):
#         #Modo como o Modelo e Exibido na Lista na Adminstracao
#         return unicode(self.grupo.titulo) + u' - ' + unicode(self.semestre)+ u' semestre de '+ unicode(self.ano)

# class Responsaveis(models.Model):
#     class Meta:
#         verbose_name = 'Responsavel'
#         verbose_name_plural = 'Responsaveis'
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,limit_choices_to={'docente':True})
#     responsavelgrupo = models.ForeignKey(ResponsavelGrupo)
#     lider = models.BooleanField(default = False)

