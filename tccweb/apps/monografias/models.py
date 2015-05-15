# -*- coding: utf-8 -*-
from django.db import models
from projetos.models import ProjetoDeGraduacao
SEMESTRE = (
             ('1','1o Semestre'),
             ('2','2o Semestre'),
             )
# class DatasMonografia(models.Model):
#     grupo_de_disciplinas = models.ForeignKey(GrupoDisciplina, unique= True, verbose_name='Grupo de Dsiciplinas')
#     ano = models.IntegerField()
#     semestre = models.CharField(max_length = 1, default= 1, choices = SEMESTRE)
#     max_monografia = models.DateField(verbose_name='Original', null=True, blank=True)
#     max_monografia_emprestada = models.DateField(verbose_name='Emprestada', null=True, blank=True)
#     max_monografia_revisada = models.DateField(verbose_name='Revisada', null=True, blank=True)

# class ReceberMonografia(models.Model):
#     disciplina = models.ForeignKey(Disciplina, null = True, blank = True)
#     data_recebimento = models.DateField(verbose_name = "Data de Recebimento")
#     alunos = models.ForeignKey(User, null = True, limit_choices_to={'groups': 4},blank = True,related_name = 'receber_monografia_alunos')
    
    
# class CobrarMonografiaimpressa(models.Model):
#     disciplina = models.ForeignKey(Disciplina, null = True, blank = True)
#     data = models.DateTimeField()
#     alunos = models.ManyToManyField(User, null = True, limit_choices_to={'groups': 4},blank = True,related_name = 'cobrar_monografia_impressa_alunos')
    
class EntregaMonografiaRevisada(models.Model):
    class Meta:
        verbose_name = "Monografia Revisada"
        verbose_name_plural = "Monografias Revisadas"
    projeto = models.OneToOneField(ProjetoDeGraduacao, null = True, blank = True,related_name = "monografia_revisada_projeto")
    data = models.DateTimeField(auto_now=True,verbose_name="Data da Entraga")
    monografia = models.FileField(upload_to = "monografias_revisadas/%Y/%M")
    def __unicode__(self):
        return "Monografia Revisada de "+self.projeto.aluno.nome_completo
    def get_aluno_display(self):
        return self.projeto.aluno.nome_completo
    get_aluno_display.short_description = 'Aluno'

class EntregaMonografiaOriginal(models.Model):
    class Meta:
        verbose_name = "Monografia Original"
        verbose_name_plural = "Monografias Originais"
    projeto = models.OneToOneField(ProjetoDeGraduacao, null = True, blank = True, related_name = "monografia_original_projeto")
    data = models.DateTimeField(auto_now=True, verbose_name="Data da Entraga")
    monografia = models.FileField(upload_to = "monografias_original/%Y/%M")
    def __unicode__(self):
        return "Monografia Revisada de "+self.projeto.aluno.nome_completo
    def get_aluno_display(self):
        return self.projeto.aluno.nome_completo
    get_aluno_display.short_description = 'Aluno'

# class CobrarMonografiaatrasada(models.Model):
#     disciplina = models.ForeignKey(Disciplina, null = True, blank = True)
#     data = models.DateTimeField()
#     alunos = models.ManyToManyField(User, null = True, limit_choices_to={'groups': 4},blank = True,related_name = 'cobrar_monografia_atrasada_alunos')
    
# class DevolucaoMonografiaIMpressa(models.Model):
#     disciplina = models.ForeignKey(Disciplina, null = True, blank = True)
#     data = models.DateTimeField(verbose_name = "Data de Devolução")
#     alunos = models.ForeignKey(User, null = True, limit_choices_to={'groups': 4},blank = True,related_name = 'devolucao_monografia_alunos')
    
    

    
    
    
    
    
    
    