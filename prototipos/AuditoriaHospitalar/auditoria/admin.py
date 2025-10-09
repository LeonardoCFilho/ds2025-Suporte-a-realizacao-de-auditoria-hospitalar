from django.contrib import admin
from .models import Internacao, ItemConta, Auditoria

@admin.register(Internacao)
class InternacaoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'patologia', 'data_entrada', 'status', 'setor', 'alerta_tempo']
    list_filter = ['status', 'setor', 'data_entrada']
    search_fields = ['paciente__nome']
    date_hierarchy = 'data_entrada'

@admin.register(ItemConta)
class ItemContaAdmin(admin.ModelAdmin):
    list_display = ['internacao', 'procedimento', 'quantidade', 'valor_total', 'status']
    list_filter = ['status', 'data_lancamento']
    search_fields = ['internacao__paciente__nome', 'procedimento__nome']

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ['internacao', 'tipo', 'auditor', 'data_auditoria', 'valor_glosado']
    list_filter = ['tipo', 'data_auditoria']
    search_fields = ['internacao__paciente__nome', 'auditor__username']
    date_hierarchy = 'data_auditoria'
