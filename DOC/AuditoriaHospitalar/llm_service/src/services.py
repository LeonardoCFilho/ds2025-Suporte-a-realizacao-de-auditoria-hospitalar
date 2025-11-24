import os
import logging
from typing import Dict, List, Optional
from src.rag import RAGSystem
from src.prompts import PromptTemplates
from src.gemini_integration import GeminiIntegration

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, api_key: str = None):
        self.rag = RAGSystem()
        self.prompts = PromptTemplates()
        self.gemini = GeminiIntegration(api_key)
    
    def analisar_paciente_alta(self, internacao_data: Dict) -> Dict:
        """
        Analisa se paciente tem potencial para alta usando Thinking + RAG + Gemini
        Versão corrigida com tratamento robusto de erros
        """
        try:
            # 1. Buscar contexto relevante com RAG
            contexto = self.rag.buscar_contexto_relevante(internacao_data)
            
            # 2. Construir prompt estruturado
            prompt = self.prompts.criar_prompt_analise_alta(internacao_data, contexto)
            
            # 3. Chamar Gemini com thinking model
            resposta_estruturada = self.gemini.analisar_paciente_estruturado(prompt)
            
            # 4. VALIDAÇÃO ROBUSTA da estrutura de resposta
            resposta_validada = self._validar_estrutura_resposta(resposta_estruturada)
            
            # 5. Adicionar metadados do contexto
            resposta_validada['contexto_utilizado'] = {
                'protocolo': contexto.get('knowledge_base', {}).get('protocolo_patologia', {}),
                'conformidade_pagador': contexto.get('knowledge_base', {}).get('conformidade_pagador', {}),
                'documentos_encontrados': len(contexto.get('vector_store', []))
            }
            
            return resposta_validada
            
        except Exception as e:
            logger.error(f"Erro na análise de alta: {e}")
            return self._resposta_erro_estruturada()
    
    def _validar_estrutura_resposta(self, resposta: Dict) -> Dict:
        """
        Valida e corrige a estrutura da resposta do Gemini
        """
        # Campos obrigatórios
        campos_obrigatorios = {
            'prioridade': 'MEDIA',  # valor padrão se faltar
            'razoes_alta': [],
            'pendencias': [],
            'fontes_informacao': [],
            'confianca': 0.5,
            'resposta_bruta_llm': '',
            'analise_inicial': 'Análise realizada',
            'recomendacao_original': 'MANTER_INTERNACAO'
        }
        
        resposta_validada = resposta.copy() if resposta else {}
        
        # Garantir que todos os campos obrigatórios existam
        for campo, valor_padrao in campos_obrigatorios.items():
            if campo not in resposta_validada or resposta_validada[campo] is None:
                resposta_validada[campo] = valor_padrao
                logger.warning(f"Campo '{campo}' não encontrado na resposta, usando padrão: {valor_padrao}")
        
        # Validar tipos
        if not isinstance(resposta_validada['razoes_alta'], list):
            resposta_validada['razoes_alta'] = [str(resposta_validada['razoes_alta'])]
        
        if not isinstance(resposta_validada['pendencias'], list):
            resposta_validada['pendencias'] = [str(resposta_validada['pendencias'])]
            
        if not isinstance(resposta_validada['fontes_informacao'], list):
            resposta_validada['fontes_informacao'] = [str(resposta_validada['fontes_informacao'])]
        
        # Validar prioridade
        prioridades_validas = ['ALTA', 'MEDIA', 'BAIXA', 'MANTER']
        if resposta_validada['prioridade'] not in prioridades_validas:
            resposta_validada['prioridade'] = 'MEDIA'
            logger.warning(f"Prioridade inválida: {resposta_validada['prioridade']}, usando 'MEDIA'")
        
        # Validar confiança
        try:
            confianca = float(resposta_validada['confianca'])
            if not 0 <= confianca <= 1:
                resposta_validada['confianca'] = 0.5
        except (ValueError, TypeError):
            resposta_validada['confianca'] = 0.5
        
        return resposta_validada
    
    def _resposta_erro_estruturada(self) -> Dict:
        """Resposta padrão em caso de erro - ESTRUTURADA CORRETAMENTE"""
        return {
            'prioridade': 'BAIXA',
            'razoes_alta': ['Erro na análise - avaliação manual necessária'],
            'pendencias': ['Sistema temporariamente indisponível'],
            'fontes_informacao': ['Sistema de auditoria'],
            'confianca': 0.0,
            'resposta_bruta_llm': '',
            'analise_inicial': 'Erro na análise automatizada',
            'recomendacao_original': 'MANTER_INTERNACAO',
            'contexto_utilizado': {}
        }