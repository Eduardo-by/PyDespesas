from django.db import models
from django.urls import reverse


class Despesas(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    valor = models.FloatField()
    data = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name = ("Despesas")
        verbose_name_plural = ("Despesass")

    def __str__(self):
        return self.titulo

class Caixa(models.Model):
    data = models.DateField(auto_now_add=True)
    valor_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    valor_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
