from django.db import models
from departamentos.models import Departamento

class Curso(models.Model):
	departamento = models.ForeignKey(Departamento)
	nome = models.CharField(max_length = 255)
    
	def __unicode__(self):
		return unicode(self.nome)
