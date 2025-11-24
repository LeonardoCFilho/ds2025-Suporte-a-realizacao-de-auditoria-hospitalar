from typing import Dict, Any, List
import json
from datetime import datetime

class PromptTemplates:
    """Templates de prompts para o Thinking Model"""
    
    def __init__(self):
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Prompt do sistema - VERSÃO SEGURA E GENÉRICA (AJUSTADO)"""
        return """
        Você é um assistente para análise **logística e de conformidade financeira** de Casos em Acompanhamento.
        SUA FUNÇÃO: Analisar dados básicos de **permanência do Caso** e sugerir prioridade para avaliação de **encerramento/liberação de recurso**.
        
        LIMITAÇÕES IMPORTANTES:
        - Você NÃO faz avaliações clínicas ou de saúde.
        - Você NÃO avalia o estado do indivíduo, apenas o status do processo.
        - Você NÃO prescreve ações de tratamento.
        - Sua análise é **APENAS LOGÍSTICA E DE CONFORMIDADE COM REGRAS**.

        CRITÉRIOS PARA ANÁLISE (Logística e Conformidade):
        1. Duração atual do Caso vs. Tempo Padrão de Referência.
        2. Conformidade com regras de tempo máximo do Pagador/Regulador.
        3. Dados básicos do Processo (setor, idade do participante, comorbidades).

        FORMATO DE RESPOSTA OBRIGATÓRIO:
        ANALISE_INICIAL: [resumo baseado apenas nos dados fornecidos]
        RAZÕES_ALTA: [razões administrativas/logísticas para considerar encerramento]
        PENDENCIAS: [informações faltantes para decisão]
        RECOMENDACAO: [ALTA_PRIORIDADE_ALTA | ALTA_PRIORIDADE_MEDIA | ALTA_PRIORIDADE_BAIXA | MANTER_INTERNACAO]
        FONTES: [fontes usadas da lista fornecida]
        CONFIANCA: [0.0-1.0]
        """
    
    def criar_prompt_analise_alta(self, internacao_data: Dict[str, Any], contexto: Dict[str, Any]) -> str:
        """Cria prompt SEGURO para análise de alta"""
        
        # Dados básicos apenas
        patologia = internacao_data.get('patologia', 'Desconhecida')
        tempo_permanencia = internacao_data.get('tempo_permanencia', 0)
        tempo_ideal = internacao_data.get('tempo_ideal_patologia', 0)
        setor = internacao_data.get('setor', '')
        
        # Contexto simplificado
        protocolo = contexto.get('knowledge_base', {}).get('protocolo_patologia', {})
        conformidade = contexto.get('knowledge_base', {}).get('conformidade_pagador', {})
        
        prompt = f"""
        {self._get_system_prompt()}

        DADOS DO CASO:
        - Motivo Principal: {patologia}
        - Duração da Permanência: {tempo_permanencia} dias
        - Tempo de Referência: {tempo_ideal} dias
        - Setor: {setor}

        INFORMAÇÕES DE REFERÊNCIA:
        - Tempo máximo permitido: {conformidade.get('max_allowed_stay', 'N/A')} dias
        - Status conformidade: {'DENTRO DO LIMITE' if conformidade.get('is_compliant') else 'FORA DO LIMITE'}

        ANÁLISE REQUERIDA:
        Baseado apenas nos dados acima, avalie a prioridade para avaliação de alta (encerramento logístico/financeiro).

        RESPOSTA (formato exato):
        ANALISE_INICIAL: [resumo administrativo]
        RAZÕES_ALTA: [lista de razões administrativas/logísticas]
        PENDENCIAS: [lista de informações faltantes]
        RECOMENDACAO: [ALTA_PRIORIDADE_ALTA | ALTA_PRIORIDADE_MEDIA | ALTA_PRIORIDADE_BAIXA | MANTER_INTERNACAO]
        FONTES: [DADOS DA INTERNAÇÃO, INFORMAÇÕES DE REFERÊNCIA]
        CONFIANCA: [0.0-1.0]
        """
        
        return prompt
    
    def _formatar_contexto_clinico(self, protocolo: Dict, conformidade: Dict, contexto_vector: List) -> str:
        """Formata o contexto para o prompt - VERSÃO SEM TERMOS CLÍNICOS"""
        
        # MUDANÇA AQUI: "PROTOCOLO MÉDICO" -> "PROTOCOLO DE REFERÊNCIA"
        contexto_texto = "PROTOCOLO DE REFERÊNCIA (Tempo/Documentos):\n"
        
        if protocolo and protocolo.get('description'): 
            contexto_texto += f"- Tempo médio de processo: {protocolo.get('avg_length_of_stay', 'N/A')} dias\n"
            
            criterios = protocolo.get('discharge_criteria', [])
            if criterios:
                # MUDANÇA AQUI: "Critérios alta" -> "Requisitos de Encerramento"
                contexto_texto += f"- Requisitos de Encerramento: {', '.join(criterios[:3])}"
                if len(criterios) > 3:
                    contexto_texto += f" ... (+{len(criterios)-3} mais)"
                contexto_texto += "\n"
            
            exames = protocolo.get('required_exams', [])
            if exames:
                # MUDANÇA AQUI: "Exames necessários" -> "Documentos/Testes Obrigatórios"
                contexto_texto += f"- Documentos/Testes Obrigatórios: {', '.join(exames)}\n"
        else:
            contexto_texto += "- Protocolo não carregado corretamente\n"
        
        contexto_texto += f"\nCONFORMIDADE PAGADOR:\n"
        if conformidade:
            contexto_texto += f"- Tempo máximo permitido: {conformidade.get('max_allowed_stay', 'N/A')} dias\n"
            contexto_texto += f"- Dias em excesso: {conformidade.get('excess_days', 0)} dias\n"
            contexto_texto += f"- Alerta: {'SIM' if conformidade.get('alert_triggered', False) else 'NÃO'}\n"
        else:
            contexto_texto += "- Dados de conformidade não disponíveis\n"
        
        if contexto_vector:
            contexto_texto += f"\nCONTEXTO ADICIONAL ({len(contexto_vector)} fontes):\n"
            for i, ctx in enumerate(contexto_vector[:2]):
                conteudo = ctx.get('conteudo', '').replace('\n', ' ').strip()
                if len(conteudo) > 100:
                    conteudo = conteudo[:100] + "..."
                contexto_texto += f"- Fonte {i+1}: {conteudo}\n"
        
        return contexto_texto
    
    def criar_prompt_validacao(self, recomendacao: Dict[str, Any], decisao_humana: str) -> str:
        """Cria prompt para validação e aprendizado do modelo"""
        
        return f"""
        VALIDAÇÃO DE RECOMENDAÇÃO:
        
        Recomendação original da IA:
        - Prioridade: {recomendacao.get('prioridade', 'N/A')}
        - Razões: {recomendacao.get('razoes_alta', [])}
        - Pendências: {recomendacao.get('pendencias', [])}
        
        Decisão humana: {decisao_humana}
        
        Análise de discrepância:
        1. O que a IA considerou que deveria ser diferente?
        2. Quais fatores humanos pesaram na decisão?
        3. Como melhorar futuras recomendações?
        """