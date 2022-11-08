from django.db import models

class Empresa(models.Model):
    choice_nicho_mercado = (
        ('M', 'Marketing'),
        ('N', 'Nutrição'),
        ('D', 'Design'),
    )
    nome = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    cidade = models.CharField(max_length=40)
    endereco = models.CharField(max_length=40)
    caracteristicas_empresa = models.TextField()
    nicho_mercado= models.CharField(max_length=3, choices=choice_nicho_mercado)
