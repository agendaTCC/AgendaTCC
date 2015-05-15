# -*- coding: utf-8 -*-
from django.db import models
from departamentos.models import Departamento
import datetime

#Model Data, modelo do aplicativo data, Aplicativo para informar prazos ao sistema
#para cada disciplina:
#Data maxima para inscrição, max_inscricao;
#Data inicio da escolha dos horarios de banca pelos alunos, inic_banca_alunos;
#Data maxima da escolha dos horarios de banca pelos alunos, max_baca_alunos;
#Data maxima para mudanca de titulo e areas de concentracao, max_titulo_ares;
#Data inicio para escolha de bancas pelos convidados, inci_banca_convidado;
#Data maxima para escolha de bancas pelos convidados, max_banca_convidado;
#Data maxima para entrega da monografia original, max_monografia;
#Data maxima para para devolucao monografia impressa emprestada pela banca, max_monografia_emprestada;
#Data maxima para entrega de monografia emprestada, max_monografia_emprestada;

SEMESTRE = (
            ('1','1o Semestre'),
            ('2','2o Semestre')
            )
class SemestreManager(models.Manager):
    def semestreAtual(self,departamentos):
        if(type(departamentos) is not list):
            departamentos = [departamentos]  
        return self.get_query_set().filter(atual = True, grupo__in = departamentos)
    def semestreDepartamento(self,departamento,id = None, ano = None, semestre = None):
        return self.get_query_set().filter( grupo = departamento,id = id,ano=ano,semestre = semestre)


class Semestre(models.Model):
    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
    ano = models.IntegerField()
    grupo = models.ForeignKey(Departamento, verbose_name = 'Departamento')
    semestre = models.CharField(max_length = 1, default= 1, choices = SEMESTRE)
    inicio_semestre = models.DateField(verbose_name="Data Inicio do Semestre")
    fim_semestre = models.DateField(verbose_name="Data Fim do Semestre")
    atual = models.BooleanField(verbose_name="Semestre Atual?", default=False);  
    inic_inscricao = models.DateField(verbose_name='Data Inicial', null=True, blank=True)
    max_inscricao = models.DateField(verbose_name='Data final', null=True, blank=True)
    inic_banca_alunos = models.DateField(verbose_name='Data inicio', null=True, blank=True)
    max_banca_alunos = models.DateField(verbose_name='Data Final', null=True, blank=True)
    max_titulo_areas = models.DateField(verbose_name='Data final', null=True, blank=True)

    inic_banca_responsavel = models.DateField(verbose_name='Data inicio', null=True, blank=True)
    max_banca_responsavel = models.DateField(verbose_name='Data final', null=True, blank=True)

    inic_banca_convidado = models.DateField(verbose_name='Data inicio', null=True, blank=True)
    max_banca_convidado = models.DateField(verbose_name='Data final', null=True, blank=True)

    autorizacao_mestrando = models.BooleanField(verbose_name = 'Autorizar Mestrando', default = False)

    inic_apresentacao = models.DateField(verbose_name='Data inicial', null=True, blank=True)
    max_apresentacao = models.DateField(verbose_name='Data final', null=True, blank=True)

    max_autorizacao = models.DateField(verbose_name='Data maxima', null=True, blank=True)
    #Manager
    objects = SemestreManager()
    def __unicode__(self):
        
        if int(self.semestre) == 1:
            semestre = '1o Semestre'
        elif int(self.semestre) == 2:
            semestre = '2o Semestre'
        return unicode(self.grupo)+' - '+unicode(self.ano)+' - '+unicode(semestre)
    
    def isBancaDefined(self):
        if self.inic_apresentacao and self.max_apresentacao:
            return True
        else:
            return False

    def inBanca(self, data):
        if data < self.inic_apresentacao or data > self.max_apresentacao:
            return False
        else:
            return True
    
    def disciplinas(self):
        return self.disciplina_semestre.all()

    def emEscolhaAlunos(self):
        data = datetime.date.today()
        if data < self.inic_banca_alunos or data > self.max_banca_alunos:
            return False
        else:
            return True
    def emEscolhaDocenteResponsavel(self):
        data = datetime.date.today()
        if data < self.inic_banca_responsavel or data > self.max_banca_responsavel:
            return False
        else:
            return True
    def emEscolhaDocenteConvidado(self):
        data = datetime.date.today()
        if data < self.inic_banca_convidado or data > self.max_banca_convidado:
            return False
        else:
            return True
    def emSemestre(self):
        data = datetime.date.today()
        if data < self.inicio_semestre or data > self.fim_semestre:
            return False
        else:
            return True
    def responsavel(self, usuario):
        disciplinas = self.disciplinas()
        resp = False
        for disciplina in disciplinas:
            resp = resp or (usuario in disciplina.professores.all())
        return resp
    def matriculado(self,usuario):
        disciplinas = self.disciplinas()
        resp = False
        for disciplina in disciplinas:
            resp = resp or (usuario in disciplina.alunos.all())
        return resp