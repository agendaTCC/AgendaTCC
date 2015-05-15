# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from disciplinas.models import Disciplina

VALIDACAO = (
             ('s','Aprovado'),
             ('n',u'Não Aprovado'),
             ('p','Pendente'),
             )
AREAS_RELACIONADAS = (
        ('a', u'Engenharia de Softtware e Sistemas de Informação'),
        ('b', u'Inteligencia Computacional'),
        ('c', u'Banco de Dados'),
        ('d', u'Computação Gráfica e Processamento de Imagens'),
        ('e', u'Hipermídia'),
        ('f', u'Computação Bioinspirada'),
        ('g', u'Otimização e Modelos Estocásticos'),
        ('h', u'Gerenciamento de Redes'),
        ('i', u'Mecânica dos Fluidos Computacionais'),
        ('j', u'Sistemas Distribuídos e Programaçãoo Concorrente'),
        ('k', u'Arquitetura de Computadores'),
        ('l', u'Outras'),
        )
class ProjetoDeGraduacao(models.Model):
    #Modelo do formulario de matricula em disciplina
    class Meta:
        verbose_name = 'Projeto de Graduação'
        verbose_name_plural = 'Projetos de Graduação'
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,limit_choices_to={'aluno': True}, related_name="projeto_aluno")
    disciplina = models.ForeignKey(Disciplina,verbose_name='Disciplina', related_name="projeto_disciplina")
    orientador = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Orientador',related_name='projeto_orientador', limit_choices_to={'docente': True},null=True, blank = True)
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'ou Supervisor', related_name='projeto_supervisor',limit_choices_to={'supervisor': True}, null = True, blank = True, )
    titulo = models.CharField(max_length = 255,verbose_name='Título do Trabalho', null=True, blank = True)
    area = models.CharField(max_length = 255,null=True, blank=True)
    espc = models.CharField(max_length = 255,verbose_name='Se Outras, Especificar', null=True, blank = True)
    subarea = models.CharField(max_length = 255, verbose_name='Sub-Area Especifica',null=True, blank = True)
    descricao = models.TextField( verbose_name=u'Descriçao',null=True, blank = True)
    atividades = models.TextField(verbose_name='Atividades a serem Desempenhadas', null=True, blank = True)
    cronograma = models.TextField(verbose_name='Cronograma', null=True, blank = True)
    data = models.DateTimeField (verbose_name = u'Ultima modificação',auto_now=True, null=True, blank=True)
    validacao_docente = models.CharField(max_length = 1,verbose_name = u'Validação do Docente',default = 'p',choices = VALIDACAO , null=True, blank = True)
    validacao_supervisor_orientador = models.CharField(max_length = 1,verbose_name = u'Validação do Supervisor Orientador',default = 'p',choices = VALIDACAO , null=True, blank = True)
    validacao_graduacao = models.CharField(max_length = 1,verbose_name = u'Validação do Funcionario de Graduação',default = 'p',choices = VALIDACAO , null=True, blank = True)
    rascunho = models.BooleanField(default=True)
    cancelado = models.BooleanField(default=False)
    justificativa = models.TextField(verbose_name=u'Justificativa', null = True, blank=True)
    def __unicode__(self):
        return unicode(self.titulo) 
    


class DeclaracaoDeHoras(models.Model):
    class Meta:
        verbose_name = u'Declaração de Hora'
        verbose_name = u'Declarações de Hora'
    projeto = models.OneToOneField(ProjetoDeGraduacao, related_name='declaracao_projeto')
    horas = models.IntegerField(verbose_name = 'Horas Trabalhadas', null = True, blank=True)
    def __unicode__(self):
        return unicode(self.projeto) + u' - ' + unicode(self.horas)

    def get_aluno_display(self):
        return self.projeto.aluno.nome_completo
    get_aluno_display.short_description = 'Aluno'

    def get_titulo_display(self):
        return self.projeto.titulo
    get_titulo_display.short_description = 'Título' 

    def get_semestre_display(self):
        return self.projeto.disciplina.semestre.__unicode__()
    get_semestre_display.short_description = 'Semestre'

class AvaliacaoAluno(models.Model):
    class Meta:
        verbose_name = u'Avaliação Supervisor/Orientador'
        verbose_name_plural = u'Avaliações Supervisor/Orientador'

    projeto = models.OneToOneField(ProjetoDeGraduacao, related_name='avaliacao_projeto')
    data = models.DateTimeField(auto_now=True, verbose_name="Data Preenchimento")

    capacidade_de_aprendizagem = models.DecimalField(verbose_name = "1. Capacidade de Apredizagem", max_digits=4, decimal_places=2, null = True, blank = True)
    qualidade_do_trabalho = models.DecimalField(verbose_name = "2. Qualidade do Trabalho Realizado", max_digits=4, decimal_places=2, null = True, blank = True)
    produtividade = models.DecimalField(verbose_name = "3. Produtividade", max_digits=4, decimal_places=2, null = True, blank = True)
    responsabilidade = models.DecimalField(verbose_name = "4. Responsabilidade", max_digits=4, decimal_places=2, null = True, blank = True)
    assiduidade = models.DecimalField(verbose_name = "5. Assiduidade", max_digits=4, decimal_places=2, null = True, blank = True)
    iniciativa = models.DecimalField(verbose_name = "6. Iniciativa", max_digits=4, decimal_places=2, null = True, blank = True)
    relacionamento_no_trabalho = models.DecimalField(verbose_name = "7. Relacionamento no Trabalho", max_digits=4, decimal_places=2, null = True, blank = True)
    cooperacao = models.DecimalField(verbose_name = "8. Cooperação", max_digits=4, decimal_places=2, null = True, blank = True)
    conhecimentos_previos = models.DecimalField(verbose_name = "9. Conhecimentos Pŕevios", max_digits=4, decimal_places=2, null = True, blank = True)
    observacoes = models.TextField(verbose_name='Observaçãoes/ Justificativa da avaliação', null=True, blank = True)
    def __unicode__(self):
        return u"Questionario de desempenho referente ao projeto "+unicode(self.projeto)
    def get_aluno_display(self):
        return self.projeto.aluno.nome_completo
    get_aluno_display.short_description = 'Aluno'

    def get_titulo_display(self):
        return self.projeto.titulo
    get_titulo_display.short_description = 'Título' 

    def get_semestre_display(self):
        return self.projeto.disciplina.semestre.__unicode__()
    get_semestre_display.short_description = 'Semestre'