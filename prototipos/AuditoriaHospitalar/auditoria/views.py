from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Q
from .models import Internacao, ItemConta, Auditoria
from core.models import Paciente

@login_required
def dashboard(request):
    """Dashboard principal - HU04"""
    internacoes_ativas = Internacao.objects.filter(status='ATIVA').select_related('paciente', 'patologia')
    
    # Calcular alertas
    total_alertas = sum(1 for i in internacoes_ativas if i.excedeu_tempo_ideal())
    
    # Estatísticas
    total_internacoes = internacoes_ativas.count()
    por_setor = internacoes_ativas.values('setor').annotate(total=Count('id'))
    
    context = {
        'internacoes_ativas': internacoes_ativas,
        'total_internacoes': total_internacoes,
        'total_alertas': total_alertas,
        'por_setor': por_setor,
    }
    return render(request, 'auditoria/dashboard.html', context)


@login_required
def monitoramento_tempo_real(request):
    """Monitoramento em tempo real - HU01"""
    setor_filtro = request.GET.get('setor', None)
    
    internacoes = Internacao.objects.filter(status='ATIVA').select_related('paciente', 'patologia')
    
    if setor_filtro:
        internacoes = internacoes.filter(setor=setor_filtro)
    
    # Adicionar flag de alerta
    for internacao in internacoes:
        internacao.tem_alerta = internacao.excedeu_tempo_ideal()
    
    context = {
        'internacoes': internacoes,
        'setor_filtro': setor_filtro,
        'setores': Paciente.SETOR_CHOICES,
    }
    return render(request, 'auditoria/monitoramento.html', context)


@login_required
def controle_altas(request):
    """Controle de altas - HU03"""
    prontas_alta = Internacao.objects.filter(
        status='ATIVA'
    ).select_related('paciente', 'patologia')
    
    # Filtrar pacientes que excederam tempo ideal
    prontas_alta = [i for i in prontas_alta if i.excedeu_tempo_ideal()]
    
    context = {
        'prontas_alta': prontas_alta,
    }
    return render(request, 'auditoria/controle_altas.html', context)


@login_required
def efetivar_alta(request, internacao_id):
    """Efetivar alta - HU03"""
    internacao = get_object_or_404(Internacao, id=internacao_id)
    
    if request.method == 'POST':
        internacao.status = 'ALTA'
        internacao.data_saida = timezone.now()
        internacao.save()
        return redirect('auditoria:controle_altas')
    
    return render(request, 'auditoria/efetivar_alta.html', {'internacao': internacao})


@login_required
def analise_contas(request):
    """Análise de contas médicas - HU05"""
    internacoes_finalizadas = Internacao.objects.filter(
        status='ALTA'
    ).select_related('paciente', 'patologia').order_by('-data_saida')
    
    context = {
        'internacoes': internacoes_finalizadas,
    }
    return render(request, 'auditoria/analise_contas.html', context)


@login_required
def detalhe_conta(request, internacao_id):
    """Detalhe da conta para auditoria retrospectiva - HU06"""
    internacao = get_object_or_404(Internacao, id=internacao_id)
    itens = ItemConta.objects.filter(internacao=internacao).select_related('procedimento')
    
    # Calcular totais
    valor_total = itens.aggregate(total=Sum('valor_total'))['total'] or 0
    total_glosado = itens.filter(status='GLOSADO').aggregate(total=Sum('valor_total'))['total'] or 0
    
    context = {
        'internacao': internacao,
        'itens': itens,
        'valor_total': valor_total,
        'total_glosado': total_glosado,
    }
    return render(request, 'auditoria/detalhe_conta.html', context)


@login_required
def validar_item(request, item_id):
    """Aprovar ou glosar item - HU07, HU09"""
    item = get_object_or_404(ItemConta, id=item_id)
    
    if request.method == 'POST':
        acao = request.POST.get('acao')
        justificativa = request.POST.get('justificativa', '')
        
        if acao == 'aprovar':
            item.status = 'APROVADO'
        elif acao == 'glosar':
            item.status = 'GLOSADO'
        
        item.justificativa = justificativa
        item.save()
        
        return redirect('auditoria:detalhe_conta', internacao_id=item.internacao.id)
    
    return render(request, 'auditoria/validar_item.html', {'item': item})


@login_required
def historico_auditorias(request):
    """Histórico de auditorias - HU11"""
    auditorias = Auditoria.objects.all().select_related(
        'internacao__paciente', 'auditor'
    ).order_by('-data_auditoria')
    
    # Filtros
    termo_busca = request.GET.get('busca', '')
    if termo_busca:
        auditorias = auditorias.filter(
            Q(internacao__paciente__nome__icontains=termo_busca) |
            Q(observacoes__icontains=termo_busca)
        )
    
    context = {
        'auditorias': auditorias,
        'termo_busca': termo_busca,
    }
    return render(request, 'auditoria/historico.html', context)
