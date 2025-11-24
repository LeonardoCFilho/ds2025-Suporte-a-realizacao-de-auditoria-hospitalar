"""
Processador em lote para analisar múltiplas internações com Gemini
"""
import pandas as pd
import json
import logging
from typing import List, Dict, Any
from src.services import LLMService
from src.knowledge_base import medical_kb

logger = logging.getLogger(__name__)

class BatchProcessor:
    def __init__(self, api_key: str = None):
        self.llm_service = LLMService(api_key)
    
    def carregar_dataset(self, arquivo_csv: str) -> pd.DataFrame:
        """Carrega dataset de internações"""
        try:
            df = pd.read_csv(arquivo_csv)
            logger.info(f"Dataset carregado: {len(df)} registros")
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar dataset: {e}")
            raise
    
    def preparar_dados_internacao(self, linha: pd.Series) -> Dict[str, Any]:
        """Prepara dados de uma internação para análise do LLM"""
        return {
            'patologia': linha.get('patologia', 'DESCONHECIDA'),
            'tempo_permanencia': int(linha.get('tempo_permanencia', 0)),
            'setor': linha.get('setor', 'ENFERMARIA'),
            'idade': int(linha.get('idade', 0)),
            'comorbidades': self._parse_comorbidades(linha.get('comorbidades', '[]')),
            'tempo_ideal_patologia': int(linha.get('tempo_ideal_patologia', 5)),
            'paciente_id': linha.get('paciente_id', ''),
            'internacao_id': linha.get('internacao_id', ''),
            'alerta_tempo': bool(linha.get('alerta_tempo', False)),
            'dias_excesso': int(linha.get('dias_excesso', 0))
        }
    
    def _parse_comorbidades(self, comorbidades_str: str) -> List[str]:
        """Converte string de comorbidades para lista"""
        try:
            if isinstance(comorbidades_str, str):
                # Remover colchetes e split por vírgula
                comorbidades_str = comorbidades_str.strip('[]').replace("'", "").replace('"', '')
                return [c.strip() for c in comorbidades_str.split(',') if c.strip()]
            elif isinstance(comorbidades_str, list):
                return comorbidades_str
            else:
                return []
        except:
            return []
    
    def analisar_lote(self, df: pd.DataFrame, limite: int = 10) -> pd.DataFrame:
        """
        Analisa um lote de internações com Gemini 
        """
        if limite:
            df = df.head(limite)
        
        resultados = []
        
        print(f"\nANALISANDO {len(df)} INTERNAÇÕES COM GEMINI...")
        print("=" * 60)
        
        for idx, linha in df.iterrows():
            try:
                print(f"\nProcessando {idx+1}/{len(df)}: {linha.get('paciente_nome', 'N/A')} - {linha.get('patologia', 'N/A')}")
                
                # Preparar dados
                dados_internacao = self.preparar_dados_internacao(linha)
                
                # Análise da Knowledge Base
                analise_kb = medical_kb.assess_discharge_readiness(dados_internacao)
                
                # Análise do Gemini LLM - COM TRY/EXCEPT ESPECÍFICO
                try:
                    recomendacao_gemini = self.llm_service.analisar_paciente_alta(dados_internacao)
                    
                    # VERIFICAR SE A ESTRUTURA ESTÁ CORRETA
                    if not isinstance(recomendacao_gemini, dict) or 'prioridade' not in recomendacao_gemini:
                        print(f"Estrutura inválida da resposta, usando fallback")
                        recomendacao_gemini = self._estrutura_fallback(dados_internacao)
                    
                except Exception as e:
                    print(f"Erro no Gemini: {e}")
                    recomendacao_gemini = self._estrutura_fallback(dados_internacao)
                
                # Combinar resultados - COM VALIDAÇÃO
                resultado = {
                    'internacao_id': dados_internacao['internacao_id'],
                    'paciente_id': dados_internacao['paciente_id'],
                    'paciente_nome': linha.get('paciente_nome', 'N/A'),
                    'patologia': dados_internacao['patologia'],
                    'idade': dados_internacao['idade'],
                    'tempo_permanencia': dados_internacao['tempo_permanencia'],
                    'tempo_ideal': dados_internacao['tempo_ideal_patologia'],
                    'setor': dados_internacao['setor'],
                    'comorbidades': dados_internacao['comorbidades'],
                    'alerta_tempo_dataset': dados_internacao['alerta_tempo'],
                    'dias_excesso_dataset': dados_internacao['dias_excesso'],
                    
                    # Resultados da Knowledge Base
                    'score_prontidao_kb': analise_kb['readiness_score'],
                    'nivel_prontidao_kb': analise_kb['readiness_level'],
                    'fatores_kb': analise_kb['factors'],
                    
                    # Resultados do Gemini - COM VALIDAÇÃO
                    'prioridade_gemini': recomendacao_gemini.get('prioridade', 'MEDIA'),
                    'razoes_alta_gemini': recomendacao_gemini.get('razoes_alta', ['Análise realizada']),
                    'pendencias_gemini': recomendacao_gemini.get('pendencias', ['Validação necessária']),
                    'fontes_gemini': recomendacao_gemini.get('fontes_informacao', ['Sistema']),
                    'confianca_gemini': recomendacao_gemini.get('confianca', 0.5),
                    'analise_inicial_gemini': recomendacao_gemini.get('analise_inicial', ''),
                    
                    # Metadados
                    'documentos_contexto': recomendacao_gemini.get('contexto_utilizado', {}).get('documentos_encontrados', 0)
                }
                
                resultados.append(resultado)
                
                print(f"KB Score: {analise_kb['readiness_score']}/100 - {analise_kb['readiness_level']}")
                print(f"Gemini: {resultado['prioridade_gemini']} (conf: {resultado['confianca_gemini']})")
                print(f"Razões: {len(resultado['razoes_alta_gemini'])} | Pendências: {len(resultado['pendencias_gemini'])}")
                
            except Exception as e:
                logger.error(f"Erro ao processar internação {idx}: {e}")
                continue
        
        # Converter para DataFrame
        if resultados:
            df_resultados = pd.DataFrame(resultados)
        else:
            # DataFrame vazio com colunas esperadas
            df_resultados = pd.DataFrame(columns=[
                'internacao_id', 'paciente_id', 'paciente_nome', 'patologia', 'idade',
                'tempo_permanencia', 'tempo_ideal', 'setor', 'comorbidades',
                'alerta_tempo_dataset', 'dias_excesso_dataset', 'score_prontidao_kb',
                'nivel_prontidao_kb', 'fatores_kb', 'prioridade_gemini', 'razoes_alta_gemini',
                'pendencias_gemini', 'fontes_gemini', 'confianca_gemini', 'analise_inicial_gemini',
                'documentos_contexto'
            ])
        
        print(f"\nANÁLISE CONCLUÍDA: {len(df_resultados)}/{len(df)} processadas com sucesso")
        
        return df_resultados

    def _estrutura_fallback(self, dados_internacao: Dict) -> Dict:
        """Estrutura fallback quando o Gemini falha"""
        return {
            'prioridade': 'MEDIA',
            'razoes_alta': ['Análise em andamento'],
            'pendencias': ['Processamento pendente'],
            'fontes_informacao': ['Sistema de fallback'],
            'confianca': 0.3,
            'analise_inicial': 'Análise temporariamente indisponível',
            'recomendacao_original': 'MANTER_INTERNACAO'
        }
        
    def gerar_relatorio_estatistico(self, df_resultados: pd.DataFrame) -> Dict[str, Any]:
        """Gera relatório estatístico das análises"""
        
        total = len(df_resultados)
        if total == 0:
            return {}
        
        # Estatísticas de prioridade
        prioridades = df_resultados['prioridade_gemini'].value_counts()
        
        # Média de confiança
        confianca_media = df_resultados['confianca_gemini'].mean()
        
        # Concordância entre KB e Gemini
        concordancia = self._calcular_concordancia(df_resultados)
        
        # Casos mais críticos
        casos_criticos = df_resultados[
            (df_resultados['prioridade_gemini'] == 'ALTA') & 
            (df_resultados['confianca_gemini'] > 0.7)
        ].head(5)
        
        return {
            'total_analisado': total,
            'distribuicao_prioridades': prioridades.to_dict(),
            'confianca_media': round(confianca_media, 2),
            'taxa_concordancia': round(concordancia, 2),
            'casos_alta_prioridade': len(casos_criticos),
            'top_casos_criticos': casos_criticos[['paciente_nome', 'patologia', 'tempo_permanencia', 'prioridade_gemini']].to_dict('records')
        }
    
    def _calcular_concordancia(self, df: pd.DataFrame) -> float:
        """Calcula concordância entre KB e Gemini"""
        if len(df) == 0:
            return 0.0
        
        concordantes = 0
        
        for _, row in df.iterrows():
            kb_level = row['nivel_prontidao_kb']
            gemini_priority = row['prioridade_gemini']
            
            # Mapear níveis para comparação
            kb_map = {
                'ALTA_PRIORIDADE_ALTA': 'ALTA',
                'ALTA_PRIORIDADE_MEDIA': 'MEDIA', 
                'ALTA_PRIORIDADE_BAIXA': 'BAIXA',
                'MANTER_INTERNACAO': 'MANTER'
            }
            
            kb_mapped = kb_map.get(kb_level, 'MEDIA')
            
            if kb_mapped == gemini_priority:
                concordantes += 1
        
        return (concordantes / len(df)) * 100
    
    def salvar_resultados(self, df_resultados: pd.DataFrame, arquivo_saida: str):
        """Salva resultados em CSV"""
        try:
            # Converter listas para string para salvar em CSV
            df_export = df_resultados.copy()
            
            for col in ['comorbidades', 'razoes_alta_gemini', 'pendencias_gemini', 'fontes_gemini', 'fatores_kb']:
                if col in df_export.columns:
                    df_export[col] = df_export[col].apply(lambda x: '; '.join(x) if isinstance(x, list) else str(x))
            
            df_export.to_csv(arquivo_saida, index=False, encoding='utf-8')
            logger.info(f"Resultados salvos em: {arquivo_saida}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar resultados: {e}")