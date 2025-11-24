"""
Integração com Google Gemini para análise de pacientes
"""
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from typing import Dict, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)

class GeminiIntegration:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        
        if self.api_key:
            try:
                # Configurar Gemini
                genai.configure(api_key=self.api_key)
                
                # Configurar o modelo Gemini
                generation_config = {
                    "temperature": 0.1,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1024,
                }

                safety_settings = [
                        {
                            "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
                            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                        },
                        {
                            "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH, 
                            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                        },
                        {
                            "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                        },
                        {
                            "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                        },
                        #  CATEGORIA DE SAÚDE CORRIGIDA
                        {
                            # Usa o objeto Enum correto
                            "category": HarmCategory.MEDICAL_HEALTH, 
                            # Limiar de bloqueio mais baixo para permitir sua análise administrativa
                            "threshold": HarmBlockThreshold.BLOCK_NONE 
                        },
                    ]

                self.model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )
                
                logger.info("Gemini inicializado com sucesso")
                
            except Exception as e:
                logger.error(f"Erro ao inicializar Gemini: {e}")
                self.model = None
        else:
            logger.warning("API key do Gemini não encontrada. Usando modo mock.")
    
    def analisar_paciente(self, prompt: str) -> str:
        """Analisa paciente usando Gemini"""
        if not self.model:
            return self._resposta_mock(prompt)
        
        try:
            # Chamada REAL para Gemini
            response = self.model.generate_content(prompt)
            
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                logger.error(f"Prompt bloqueado: {response.prompt_feedback}")
                return self._resposta_mock(prompt)
            
            return response.text
            
        except Exception as e:
            logger.error(f"ERRO ao chamar Gemini: {e}")
            return self._resposta_mock(prompt)
    
    def analisar_paciente_estruturado(self, prompt: str) -> Dict[str, Any]:
        """Analisa paciente e retorna dados estruturados"""
        resposta_bruta = self.analisar_paciente(prompt)
        return self._parse_resposta_llm_corrigido(resposta_bruta)
    
    def _parse_resposta_llm_corrigido(self, resposta: str) -> Dict[str, Any]:
        """
        Parse CORRIGIDO - lida com chaves em MAIÚSCULAS do Gemini e converte para minúsculas
        """
        try:
            print("PARSER: Iniciando parse da resposta do Gemini...")
            
            # Limpar a resposta
            resposta_limpa = resposta.strip()
            
            # PRIMEIRO: Normalizar todas as chaves para minúsculas
            resposta_normalizada = self._normalizar_chaves_maiusculas(resposta_limpa)
            
            # EXTRAIR seções da resposta normalizada
            analise_inicial = self._extrair_secao_flexivel(resposta_normalizada, "analise_inicial")
            razoes_alta = self._extrair_lista_flexivel(resposta_normalizada, "razoes_alta")
            pendencias = self._extrair_lista_flexivel(resposta_normalizada, "pendencias")
            recomendacao = self._extrair_secao_flexivel(resposta_normalizada, "recomendacao")
            fontes = self._extrair_lista_flexivel(resposta_normalizada, "fontes")
            confianca = self._extrair_confianca_flexivel(resposta_normalizada)
            
            # Se não encontrou fontes, tentar fontes_informacao
            if not fontes:
                fontes = self._extrair_lista_flexivel(resposta_normalizada, "fontes_informacao")
            
            print(f"Seções encontradas: analise_inicial={bool(analise_inicial)}, razoes_alta={len(razoes_alta)}, pendencias={len(pendencias)}, recomendacao={bool(recomendacao)}, fontes={len(fontes)}, confianca={confianca}")
            
            # Mapear recomendação para prioridade
            prioridade = self._mapear_recomendacao_para_prioridade(recomendacao)
            
            # ESTRUTURA FINAL com todos os campos necessários
            resultado = {
                'prioridade': prioridade,
                'razoes_alta': razoes_alta,
                'pendencias': pendencias,
                'fontes_informacao': fontes,  # CAMPO CORRETO
                'confianca': confianca,
                'resposta_bruta_llm': resposta_limpa,
                'analise_inicial': analise_inicial,
                'recomendacao_original': recomendacao  # CAMPO CORRETO
            }
            
            print(f"PARSER: Parse concluído - Prioridade: {prioridade}, Fontes: {len(fontes)}, Confiança: {confianca}")
            return resultado
            
        except Exception as e:
            print(f"PARSER: Erro no parse: {e}")
            import traceback
            traceback.print_exc()
            return self._estrutura_erro(resposta)
    
    def _normalizar_chaves_maiusculas(self, texto: str) -> str:
        """Converte chaves MAIÚSCULAS para minúsculas no texto"""
        # Mapeamento de chaves maiúsculas para minúsculas
        mapeamento = {
            'ANALISE_INICIAL': 'analise_inicial',
            'RAZÕES_ALTA': 'razoes_alta', 
            'RAZOES_ALTA': 'razoes_alta',
            'PENDENCIAS': 'pendencias',
            'RECOMENDACAO': 'recomendacao',
            'RECOMENDAÇÃO': 'recomendacao',
            'FONTES': 'fontes',
            'FONTES_INFORMACAO': 'fontes_informacao',
            'CONFIANCA': 'confianca',
            'CONFIANÇA': 'confianca'
        }
        
        texto_normalizado = texto
        for maiuscula, minuscula in mapeamento.items():
            texto_normalizado = texto_normalizado.replace(f"{maiuscula}:", f"{minuscula}:")
        
        return texto_normalizado
    
    def _extrair_secao_flexivel(self, texto: str, secao: str) -> str:
        """Extrai conteúdo de uma seção - FLEXÍVEL (maiúsculas/minúsculas)"""
        # Padrão flexível
        padrao = f"{secao}:\s*(.*?)(?=\n[a-z_]+:|\n*$)"
        match = re.search(padrao, texto, re.IGNORECASE | re.DOTALL)
        
        if match:
            conteudo = match.group(1).strip()
            # Remover marcadores de lista se existirem
            conteudo = re.sub(r'^\s*[\*\-\+]\s*', '', conteudo, flags=re.MULTILINE)
            return conteudo
        return ""
    
    def _extrair_lista_flexivel(self, texto: str, secao: str) -> list:
        """Extrai lista de uma seção - FLEXÍVEL"""
        conteudo = self._extrair_secao_flexivel(texto, secao)
        if not conteudo:
            return []
        
        # Dividir por linhas e limpar
        linhas = [linha.strip() for linha in conteudo.split('\n') if linha.strip()]
        
        # Remover marcadores de lista e limpar
        itens_limpos = []
        for linha in linhas:
            # Remover marcadores *, -, • etc.
            linha_limpa = re.sub(r'^\s*[\*\-\+•]\s*', '', linha).strip()
            if linha_limpa:
                itens_limpos.append(linha_limpa)
        
        return itens_limpos
    
    def _extrair_confianca_flexivel(self, texto: str) -> float:
        """Extrai valor de confiança - FLEXÍVEL"""
        # Tenta padrão confianca
        padrao = r"confianca:\s*([0-9.]+)"
        match = re.search(padrao, texto, re.IGNORECASE)
        
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
        return 0.75  # Default
    
    def _mapear_recomendacao_para_prioridade(self, recomendacao: str) -> str:
        """Mapeia recomendação para prioridade"""
        if not recomendacao:
            return 'MEDIA'
        
        recomendacao = recomendacao.upper().strip()
        
        if 'ALTA_PRIORIDADE_ALTA' in recomendacao:
            return 'ALTA'
        elif 'ALTA_PRIORIDADE_MEDIA' in recomendacao:
            return 'MEDIA'
        elif 'ALTA_PRIORIDADE_BAIXA' in recomendacao:
            return 'BAIXA'
        elif 'MANTER_INTERNACAO' in recomendacao:
            return 'MANTER'
        else:
            # Fallback por análise de texto
            if 'ALTA' in recomendacao and 'PRIORIDADE' not in recomendacao:
                return 'ALTA'
            elif any(word in recomendacao for word in ['CONTINUAR', 'MANTER', 'PERMANECER']):
                return 'MANTER'
            else:
                return 'MEDIA'
    
    def _resposta_mock(self, prompt: str) -> str:
        """Fallback para mock quando Gemini não está disponível"""
        return """
        ANALISE_INICIAL: Paciente em avaliação para possível alta.
        RAZÕES_ALTA: Tempo de internação adequado, Condições clínicas estáveis
        PENDENCIAS: Avaliação médica final pendente
        RECOMENDACAO: ALTA_PRIORIDADE_MEDIA
        FONTES: Prontuário eletrônico, Protocolos institucionais
        CONFIANCA: 0.78
        """
    
    def _estrutura_erro(self, resposta_bruta: str) -> Dict[str, Any]:
        """Estrutura de fallback em caso de erro"""
        return {
            'prioridade': 'MEDIA',
            'razoes_alta': ['Análise automática realizada'],
            'pendencias': ['Validação médica necessária'],
            'fontes_informacao': ['Sistema de auditoria'],
            'confianca': 0.5,
            'resposta_bruta_llm': resposta_bruta,
            'analise_inicial': 'Erro na análise automatizada',
            'recomendacao_original': 'MANTER_INTERNACAO'
        }