from django.db import models

class Evento(models.Model):
    descricao = models.CharField(max_length=100)
    data = models.DateField()
    hr_ini = models.TimeField()
    hr_fim = models.TimeField()
    priori = models.BooleanField()

    def __str__(self):

        return self.descricao

