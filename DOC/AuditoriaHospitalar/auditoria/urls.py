from django.urls import path
from . import views

app_name = 'auditoria'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('monitoramento/', views.monitoramento_tempo_real, name='monitoramento'),
    path('controle-altas/', views.controle_altas, name='controle_altas'),
    path('efetivar-alta/<int:internacao_id>/', views.efetivar_alta, name='efetivar_alta'),
    path('analise-contas/', views.analise_contas, name='analise_contas'),
    path('conta/<int:internacao_id>/', views.detalhe_conta, name='detalhe_conta'),
    path('validar-item/<int:item_id>/', views.validar_item, name='validar_item'),
    path('historico/', views.historico_auditorias, name='historico'),
]
