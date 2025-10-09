from django.db import models
from django.contrib.auth.models import User

class Patologia(models.Model):
    nome = models.CharField(max_length=200)
    codigo_cid = models.CharField(max_length=10, unique=True)
    tempo_internacao_ideal = models.IntegerField(help_text="Tempo em dias")
    descricao = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Patologias"
    
    def __str__(self):
        return f"{self.codigo_cid} - {self.nome}"


class Procedimento(models.Model):
    nome = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20, unique=True)
    valor_padrao = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class ProcedimentoPadrao(models.Model):
    """Base de conhecimento: procedimentos esperados por patologia"""
    patologia = models.ForeignKey(Patologia, on_delete=models.CASCADE, related_name='procedimentos_padrao')
    procedimento = models.ForeignKey(Procedimento, on_delete=models.CASCADE)
    quantidade_maxima = models.IntegerField(default=1)
    obrigatorio = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Procedimentos Padrão"
        unique_together = ['patologia', 'procedimento']
    
    def __str__(self):
        return f"{self.patologia.nome} - {self.procedimento.nome}"


class Paciente(models.Model):
    SETOR_CHOICES = [
        ('UTI', 'UTI'),
        ('ENFERMARIA', 'Enfermaria'),
        ('APARTAMENTO', 'Apartamento'),
    ]
    
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    setor_atual = models.CharField(max_length=20, choices=SETOR_CHOICES, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Pacientes"
    
    def __str__(self):
        return f"{self.nome} - {self.cpf}"

