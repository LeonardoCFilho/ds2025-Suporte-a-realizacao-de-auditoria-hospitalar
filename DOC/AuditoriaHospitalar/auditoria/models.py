from django.db import models
from django.utils import timezone
from core.models import Paciente, Patologia, Procedimento

class Internacao(models.Model):
    STATUS_CHOICES = [
        ('ATIVA', 'Ativa'),
        ('ALTA', 'Alta'),
        ('TRANSFERENCIA', 'Transferência'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='internacoes')
    patologia = models.ForeignKey(Patologia, on_delete=models.PROTECT)
    data_entrada = models.DateTimeField(default=timezone.now)
    data_saida = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVA')
    setor = models.CharField(max_length=20, choices=Paciente.SETOR_CHOICES)
    observacoes = models.TextField(blank=True)
    alerta_tempo = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Internação"
        verbose_name_plural = "Internações"
    
    def __str__(self):
        return f"{self.paciente.nome} - {self.data_entrada.strftime('%d/%m/%Y')}"
    
    def tempo_permanencia(self):
        """Retorna tempo de permanência em dias"""
        if self.data_saida:
            delta = self.data_saida - self.data_entrada
        else:
            delta = timezone.now() - self.data_entrada
        return delta.days
    
    def excedeu_tempo_ideal(self):
        """Verifica se ultrapassou tempo ideal"""
        return self.tempo_permanencia() > self.patologia.tempo_internacao_ideal
    
    def dias_excesso(self):
        """Retorna quantos dias excedeu o tempo ideal"""
        excesso = self.tempo_permanencia() - self.patologia.tempo_internacao_ideal
        return excesso if excesso > 0 else 0


class ItemConta(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('GLOSADO', 'Glosado'),
    ]
    
    internacao = models.ForeignKey(Internacao, on_delete=models.CASCADE, related_name='itens_conta')
    procedimento = models.ForeignKey(Procedimento, on_delete=models.PROTECT)
    quantidade = models.IntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    data_lancamento = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    justificativa = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Item da Conta"
        verbose_name_plural = "Itens da Conta"
    
    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.procedimento.nome} - {self.quantidade}x"


class Auditoria(models.Model):
    TIPO_CHOICES = [
        ('CONCORRENTE', 'Concorrente'),
        ('RETROSPECTIVA', 'Retrospectiva'),
    ]
    
    internacao = models.ForeignKey(Internacao, on_delete=models.CASCADE, related_name='auditorias')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    auditor = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    data_auditoria = models.DateTimeField(default=timezone.now)
    observacoes = models.TextField()
    itens_glosados = models.IntegerField(default=0)
    valor_glosado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = "Auditoria"
        verbose_name_plural = "Auditorias"
    
    def __str__(self):
        return f"{self.tipo} - {self.internacao.paciente.nome} - {self.data_auditoria.strftime('%d/%m/%Y')}"

