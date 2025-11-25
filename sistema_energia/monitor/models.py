from django.db import models

class Leitura(models.Model):
    tensao = models.FloatField()
    corrente = models.FloatField()
    potencia = models.FloatField()
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.data_hora} - {self.potencia}mW"