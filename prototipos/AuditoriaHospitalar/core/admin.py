from django.contrib import admin
from .models import Patologia, Procedimento, ProcedimentoPadrao, Paciente

@admin.register(Patologia)
class PatologiaAdmin(admin.ModelAdmin):
    list_display = ['codigo_cid', 'nome', 'tempo_internacao_ideal']
    search_fields = ['nome', 'codigo_cid']

@admin.register(Procedimento)
class ProcedimentoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'valor_padrao']
    search_fields = ['nome', 'codigo']

@admin.register(ProcedimentoPadrao)
class ProcedimentoPadraoAdmin(admin.ModelAdmin):
    list_display = ['patologia', 'procedimento', 'quantidade_maxima', 'obrigatorio']
    list_filter = ['patologia', 'obrigatorio']

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'data_nascimento', 'setor_atual']
    search_fields = ['nome', 'cpf']
    list_filter = ['setor_atual']

