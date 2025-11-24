import numpy as np #type: ignore
import pandas as pd  #type: ignore
from typing import List, Dict, Any, Tuple
from src.knowledge_base import MedicalKnowledgeBase as KnowledgeBase
import json
import logging
from sentence_transformers import SentenceTransformer  #type: ignore
import chromadb  #type: ignore
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class RAGSystem:
    """Sistema de Retrieval-Augmented Generation para contexto médico"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.knowledge_base = KnowledgeBase()
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.persist_directory = persist_directory
        
        # Inicializar ChromaDB
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection("protocolos_medicos")
        
        # Indexar conhecimento inicial
        self._indexar_conhecimento_inicial()
    
    def _indexar_conhecimento_inicial(self):
        """Indexa a base de conhecimento no vector store - VERSÃO CORRIGIDA"""
        try:
            print("Indexando base de conhecimento...")
            
            # Verificar se já existe dados
            if self.collection.count() == 0:
                documents = []
                metadatas = []
                ids = []
                
                # VERIFICAR quantas patologias temos na knowledge base
                total_patologias = len(self.knowledge_base.protocols)
                print(f"- Patologias na knowledge base: {total_patologias}")
                print(f"- Lista: {list(self.knowledge_base.protocols.keys())}")
                
                # Indexar protocolos por patologia - TODAS as patologias
                for patologia, protocolo in self.knowledge_base.protocols.items():
                    doc_text = f"""
                    Patologia: {patologia}
                    Descrição: {protocolo.get('description', 'N/A')}
                    Tempo médio de internação: {protocolo.get('avg_length_of_stay', 'N/A')} dias
                    Critérios para alta: {', '.join(protocolo.get('discharge_criteria', []))}
                    Exames necessários: {', '.join(protocolo.get('required_exams', []))}
                    Fatores de risco: {', '.join(protocolo.get('risk_factors', []))}
                    """
                    
                    documents.append(doc_text)
                    metadatas.append({
                        'tipo': 'protocolo',
                        'patologia': patologia,
                        'tempo_medio': protocolo.get('avg_length_of_stay', 0),
                        'descricao': protocolo.get('description', '')
                    })
                    ids.append(f"protocolo_{patologia}")
                    print(f"    Indexando: {patologia}")
                
                # Indexar regras de pagadores - TODAS as patologias
                for patologia, tempo_max in self.knowledge_base.payer_rules['max_length_of_stay'].items():
                    if patologia != 'DEFAULT':
                        doc_text = f"""
                        Regra pagador - {patologia}: 
                        Tempo máximo de internação: {tempo_max} dias
                        Alertas: Excesso de {tempo_max} dias gera glosa
                        """
                        
                        documents.append(doc_text)
                        metadatas.append({
                            'tipo': 'regra_pagador',
                            'patologia': patologia,
                            'tempo_maximo': tempo_max
                        })
                        ids.append(f"regra_{patologia}")
                        print(f"    Indexando regra: {patologia}")
                
                if documents:
                    print(f"Adicionando {len(documents)} documentos ao vector store...")
                    self.collection.add(
                        documents=documents,
                        metadatas=metadatas,
                        ids=ids
                    )
                    print(f" Indexados {len(documents)} documentos na base de conhecimento")
                else:
                    print(" Nenhum documento para indexar!")
                    
            else:
                print("  Base de conhecimento já está indexada")
                
        except Exception as e:
            print(f" Erro ao indexar conhecimento inicial: {e}")
            import traceback
            traceback.print_exc()
    
    def reindexar_conhecimento(self):
        """Força reindexação completa do conhecimento"""
        try:
            print("Iniciando reindexação completa...")
            
            # Limpar collection existente
            try:
                self.client.delete_collection("protocolos_medicos")
            except:
                pass  # Collection pode não existir
            
            self.collection = self.client.get_or_create_collection("protocolos_medicos")
            
            # Reindexar
            self._indexar_conhecimento_inicial()
            print(" Conhecimento reindexado com sucesso!")
            
            # Verificar o que foi indexado
            count = self.collection.count()
            print(f"Documentos indexados: {count}")
            
        except Exception as e:
            print(f"Erro na reindexação: {e}")
    
    def buscar_contexto_relevante(self, internacao_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Busca contexto relevante para análise da internação - VERSÃO CORRIGIDA
        """
        try:
            patologia = internacao_data.get('patologia', '')
            tempo_permanencia = internacao_data.get('tempo_permanencia', 0)
            
            print(f"RAG: Buscando contexto para {patologia}...")
            
            # Buscar no vector store
            query_text = f"Patologia: {patologia} Critérios para alta hospitalar Protocolo de tratamento"
            
            results = self.collection.query(
                query_texts=[query_text],
                n_results=3,  # Reduzir para documentos mais relevantes
                include=['documents', 'metadatas', 'distances']
            )
            
            # Contexto do vector store
            contexto_vector = self._processar_resultados_busca(results)
            
            # Contexto da knowledge base - VERIFICAR MÉTODOS
            print(f"RAG: Obtendo protocolo para {patologia}...")
            protocolo = self.knowledge_base.get_protocol(patologia)
            print(f"RAG: Protocolo encontrado: {bool(protocolo)}")
            
            conformidade = self.knowledge_base.check_payer_compliance(patologia, tempo_permanencia)
            print(f"RAG: Conformidade: {conformidade}")
            
            contexto_kb = {
                'protocolo_patologia': protocolo,
                'conformidade_pagador': conformidade,
                'criterios_gerais_alta': self.knowledge_base.discharge_criteria
            }
            
            # Combinar contextos
            contexto_completo = {
                'vector_store': contexto_vector,
                'knowledge_base': contexto_kb,
                'dados_internacao': internacao_data
            }
            
            return contexto_completo
            
        except Exception as e:
            print(f" RAG: Erro na busca de contexto: {e}")
            import traceback
            traceback.print_exc()
            return self._contexto_erro()
    
    def _processar_resultados_busca(self, results) -> List[Dict[str, Any]]:
        """Processa resultados da busca vectorial"""
        contexto = []
        
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                
                contexto.append({
                    'conteudo': doc,
                    'tipo': metadata.get('tipo', 'desconhecido'),
                    'patologia': metadata.get('patologia', ''),
                    'relevancia': 1 - distance,  # Converter distância para relevância
                    'fonte': 'Vector Store'
                })
        
        return contexto
    
    def _contexto_erro(self) -> Dict[str, Any]:
        """Retorna contexto padrão em caso de erro"""
        return {
            'vector_store': [],
            'knowledge_base': {
                'protocolo_patologia': {},
                'conformidade_pagador': {
                    'max_allowed_stay': 10,
                    'current_stay': 0,
                    'excess_days': 0,
                    'is_compliant': True,
                    'alert_triggered': False,
                    'compliance_level': 'COMPLIANT'
                },
                'criterios_gerais_alta': self.knowledge_base.discharge_criteria
            },
            'dados_internacao': {}
        }
    
    def adicionar_documento(self, documento: str, metadata: Dict[str, Any]):
        """Adiciona novo documento ao vector store"""
        try:
            doc_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.collection.add(
                documents=[documento],
                metadatas=[metadata],
                ids=[doc_id]
            )
            logger.info(f"Documento {doc_id} adicionado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao adicionar documento: {e}")