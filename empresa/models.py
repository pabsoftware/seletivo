from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    cidade = models.CharField(max_length=40)
    endereco = models.CharField(max_length=40)
    caracteristicas_empresa = models.TextField()
