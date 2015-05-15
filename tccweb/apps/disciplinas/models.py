# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.encoding import force_unicode
from semestre.models import Semestre


TURMA = (
         ('01','01'),
         ('02','02'),
         ('03','03'),
         ('04','04'),
         ('05','05'),
         ('06','06'),
         ('07','07'),
         ('08','08'),
         ('09','09'),
         ('10','10'),
         )

class NomeDisciplina(models.Model):
    titulo = models.CharField(max_length=80, verbose_name=u'Nome da disciplina')
    codigo = models.CharField(max_length=80, verbose_name=u'Código da disciplina')
    ementa = models.TextField(verbose_name = u'Ementa da Disciplina')
    link = models.CharField(max_length = 1000, verbose_name = u'Link do Jupiter', help_text=u"Links devem sempre começar com http://")
    def __unicode__(self):
        return unicode(self.codigo) + ' - '+ unicode(self.titulo)

class Disciplina(models.Model):
    titulo = models.ForeignKey(NomeDisciplina, verbose_name=u'Nome da disciplina' )
    ano = models.IntegerField(verbose_name=u'Ano', null = True ,blank = True) 
    turma = models.CharField(max_length=2, verbose_name=u'Turma', choices = TURMA)
    criada_em = models.DateTimeField(auto_now_add=True, 
        verbose_name=u'Data da criacao')
    semestre = models.ForeignKey(Semestre,verbose_name=u'Semestre', related_name=u'disciplina_semestre')
    esta_ativa = models.BooleanField(verbose_name=u'Ativa')  
    alunos = models.ManyToManyField(settings.AUTH_USER_MODEL,null=True, blank=True, 
        related_name=u'aluno_disciplina', verbose_name=u'Alunos Matriculados')
    professores = models.ManyToManyField(settings.AUTH_USER_MODEL,limit_choices_to={'docente': True}, null=True, blank=True, 
        related_name=u'professor_disciplina', verbose_name=u'Professores Responsáveis')
    monitores = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'monitor': True,'pae':True},null=True, blank=True,
        related_name=u'monitor_disciplina', verbose_name=u'Monitores da disciplina')
    def __unicode__(self):
        return  unicode(self.semestre.ano)+self.semestre.semestre + '0' + self.turma + ' - ' + unicode(self.titulo.codigo) + ' - '+ unicode(self.titulo.titulo)
    
    class Meta:
        ordering = ['-semestre']
        
    def matricula_aluno(self,aluno):
        self.alunos.add(aluno)
        self.save()
    def retira_aluno(self,aluno):
        try:
            self.alunos.remove(aluno)
        except:
            pass
    
    def matriculado(self,aluno):
        if aluno in self.alunos.all():
            return True
        else:
            return False