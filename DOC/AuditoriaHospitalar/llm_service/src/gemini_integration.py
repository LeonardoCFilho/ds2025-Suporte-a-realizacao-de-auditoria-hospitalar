"""
Integração com Google Gemini para análise de pacientes
"""

import os

# Adicionado type: ignore para silenciar o erro "PrivateImportUsage" do Pylance
import google.generativeai as genai  # type: ignore
from google.generativeai.types import HarmCategory, HarmBlockThreshold, GenerationConfig
from typing import Dict, Any, Optional, List
import logging
import re

logger = logging.getLogger(__name__)


class GeminiIntegration:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = None

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)  # type: ignore

                generation_config = GenerationConfig(
                    temperature=0.1,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048,  # Aumentado para garantir
                )

                # Configurações de segurança no mínimo para evitar bloqueios médicos
                safety_settings = [
                    {
                        "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
                        "threshold": HarmBlockThreshold.BLOCK_NONE,
                    },
                    {
                        "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        "threshold": HarmBlockThreshold.BLOCK_NONE,
                    },
                    {
                        "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        "threshold": HarmBlockThreshold.BLOCK_NONE,
                    },
                    {
                        "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        "threshold": HarmBlockThreshold.BLOCK_NONE,
                    },
                ]

                # --- MUDANÇA: USANDO A VERSÃO 2.0 (MAIS ESTÁVEL) ---
                model_name = "gemini-2.0-flash"

                self.model = genai.GenerativeModel(  # type: ignore
                    model_name=model_name,
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                )

                logger.info(f"Gemini ({model_name}) inicializado com sucesso")

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

            # Verifica se há conteúdo válido
            if response.candidates and response.candidates[0].content.parts:
                return response.text
            else:
                motivo = "Desconhecido"
                if response.candidates:
                    motivo = response.candidates[0].finish_reason

                logger.warning(f"Gemini retornou resposta vazia. Motivo: {motivo}")
                return self._resposta_mock(prompt)

        except Exception as e:
            logger.error(f"ERRO ao chamar Gemini: {e}")
            return self._resposta_mock(prompt)

    def analisar_paciente_estruturado(self, prompt: str) -> Dict[str, Any]:
        """Analisa paciente e retorna dados estruturados"""
        resposta_bruta = self.analisar_paciente(prompt)
        return self._parse_resposta_llm_corrigido(resposta_bruta)

    def _parse_resposta_llm_corrigido(self, resposta: str) -> Dict[str, Any]:
        """Parse da resposta do LLM"""
        try:
            print("PARSER: Iniciando parse...")
            resposta_limpa = resposta.strip()
            resposta_normalizada = self._normalizar_chaves_maiusculas(resposta_limpa)

            analise_inicial = self._extrair_secao_flexivel(
                resposta_normalizada, "analise_inicial"
            )
            razoes_alta = self._extrair_lista_flexivel(
                resposta_normalizada, "razoes_alta"
            )
            pendencias = self._extrair_lista_flexivel(
                resposta_normalizada, "pendencias"
            )
            recomendacao = self._extrair_secao_flexivel(
                resposta_normalizada, "recomendacao"
            )
            fontes = self._extrair_lista_flexivel(resposta_normalizada, "fontes")
            if not fontes:
                fontes = self._extrair_lista_flexivel(
                    resposta_normalizada, "fontes_informacao"
                )
            confianca = self._extrair_confianca_flexivel(resposta_normalizada)

            prioridade = self._mapear_recomendacao_para_prioridade(recomendacao)

            resultado = {
                "prioridade": prioridade,
                "razoes_alta": razoes_alta,
                "pendencias": pendencias,
                "fontes_informacao": fontes,
                "confianca": confianca,
                "resposta_bruta_llm": resposta_limpa,
                "analise_inicial": analise_inicial,
                "recomendacao_original": recomendacao,
            }
            return resultado

        except Exception as e:
            print(f"PARSER: Erro no parse: {e}")
            return self._estrutura_erro(resposta)

    def _normalizar_chaves_maiusculas(self, texto: str) -> str:
        mapeamento = {
            "ANALISE_INICIAL": "analise_inicial",
            "RAZÕES_ALTA": "razoes_alta",
            "RAZOES_ALTA": "razoes_alta",
            "PENDENCIAS": "pendencias",
            "RECOMENDACAO": "recomendacao",
            "RECOMENDAÇÃO": "recomendacao",
            "FONTES": "fontes",
            "FONTES_INFORMACAO": "fontes_informacao",
            "CONFIANCA": "confianca",
            "CONFIANÇA": "confianca",
        }
        texto_normalizado = texto
        for maiuscula, minuscula in mapeamento.items():
            texto_normalizado = texto_normalizado.replace(
                f"{maiuscula}:", f"{minuscula}:"
            )
        return texto_normalizado

    def _extrair_secao_flexivel(self, texto: str, secao: str) -> str:
        padrao = rf"{secao}:\s*(.*?)(?=\n[a-z_]+:|\n*$)"
        match = re.search(padrao, texto, re.IGNORECASE | re.DOTALL)
        if match:
            conteudo = match.group(1).strip()
            conteudo = re.sub(r"^\s*[\*\-\+]\s*", "", conteudo, flags=re.MULTILINE)
            return conteudo
        return ""

    def _extrair_lista_flexivel(self, texto: str, secao: str) -> list:
        conteudo = self._extrair_secao_flexivel(texto, secao)
        if not conteudo:
            return []
        linhas = [linha.strip() for linha in conteudo.split("\n") if linha.strip()]
        itens_limpos = []
        for linha in linhas:
            linha_limpa = re.sub(r"^\s*[\*\-\+•]\s*", "", linha).strip()
            if linha_limpa:
                itens_limpos.append(linha_limpa)
        return itens_limpos

    def _extrair_confianca_flexivel(self, texto: str) -> float:
        padrao = r"confianca:\s*([0-9.]+)"
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
        return 0.75

    def _mapear_recomendacao_para_prioridade(self, recomendacao: str) -> str:
        if not recomendacao:
            return "MEDIA"
        recomendacao = recomendacao.upper().strip()
        if "ALTA_PRIORIDADE_ALTA" in recomendacao:
            return "ALTA"
        elif "ALTA_PRIORIDADE_MEDIA" in recomendacao:
            return "MEDIA"
        elif "ALTA_PRIORIDADE_BAIXA" in recomendacao:
            return "BAIXA"
        elif "MANTER_INTERNACAO" in recomendacao:
            return "MANTER"
        else:
            if "ALTA" in recomendacao and "PRIORIDADE" not in recomendacao:
                return "ALTA"
            elif any(
                word in recomendacao for word in ["CONTINUAR", "MANTER", "PERMANECER"]
            ):
                return "MANTER"
            else:
                return "MEDIA"

    def _resposta_mock(self, prompt: str) -> str:
        return """
        ANALISE_INICIAL: Paciente em avaliação para possível alta.
        RAZÕES_ALTA: Tempo de internação adequado, Condições clínicas estáveis
        PENDENCIAS: Avaliação médica final pendente
        RECOMENDACAO: ALTA_PRIORIDADE_MEDIA
        FONTES: Prontuário eletrônico, Protocolos institucionais
        CONFIANCA: 0.78
        """

    def _estrutura_erro(self, resposta_bruta: str) -> Dict[str, Any]:
        return {
            "prioridade": "MEDIA",
            "razoes_alta": ["Erro/Fallback"],
            "pendencias": ["Verificar log"],
            "fontes_informacao": ["Sistema"],
            "confianca": 0.5,
            "resposta_bruta_llm": resposta_bruta,
            "analise_inicial": "Erro na análise",
            "recomendacao_original": "MANTER",
        }
