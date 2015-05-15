from django.db import models

class Sala(models.Model):
    nome =  models.CharField(max_length = 255)
    ativa = models.BooleanField()
    def __unicode__(self):
        if self.ativa:
            return unicode(self.nome) + ' - Ativa'
        else:
            return unicode(self.nome) + ' - Inativa'
