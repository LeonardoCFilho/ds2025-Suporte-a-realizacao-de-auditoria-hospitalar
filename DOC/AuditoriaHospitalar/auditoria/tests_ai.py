from django.test import TestCase
from unittest.mock import MagicMock, patch, Mock
from llm_service.src.knowledge_base import MedicalKnowledgeBase
from llm_service.src.gemini_integration import GeminiIntegration
from llm_service.src.rag import RAGSystem
from llm_service.src.services import LLMService

class KnowledgeBaseTests(TestCase):
    
    def setUp(self):
        self.kb = MedicalKnowledgeBase()

    def test_calculo_nivel_prontidao_alta(self):
        nivel = self.kb._get_readiness_level(85)
        self.assertEqual(nivel, 'ALTA_PRIORIDADE_ALTA')

    def test_calculo_nivel_prontidao_manter(self):
        nivel = self.kb._get_readiness_level(30)
        self.assertEqual(nivel, 'MANTER_INTERNACAO')

    def test_compliance_pagador_dentro_prazo(self):
        resultado = self.kb.check_payer_compliance('APENDICITE', 2)
        self.assertTrue(resultado['is_compliant'])
        self.assertFalse(resultado['alert_triggered'])

    def test_compliance_pagador_estourado(self):
        resultado = self.kb.check_payer_compliance('APENDICITE', 5)
        self.assertFalse(resultado['is_compliant'])
        self.assertTrue(resultado['alert_triggered'])
        self.assertEqual(resultado['excess_days'], 2)

class GeminiIntegrationTests(TestCase):
    
    @patch('llm_service.src.gemini_integration.genai')
    def test_analise_paciente_sucesso_json(self, mock_genai):
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.configure = MagicMock()
        
        mock_response = MagicMock()
        mock_response.text = '{"prioridade": "ALTA", "razoes_alta": ["Paciente estável", "Exames normais"], "pendencias": ["Nenhuma"], "fontes_informacao": ["Protocolo XYZ"], "confianca": 0.95}'
        mock_model.generate_content.return_value = mock_response

        gemini = GeminiIntegration(api_key="fake_key")
        resultado = gemini.analisar_paciente_estruturado("prompt de teste")

        self.assertIn('prioridade', resultado)
        self.assertIn('razoes_alta', resultado)

    @patch('llm_service.src.gemini_integration.genai')
    def test_analise_paciente_tratamento_erro(self, mock_genai):
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.configure = MagicMock()
        
        mock_response = MagicMock()
        mock_response.text = "Texto inválido sem JSON"
        mock_model.generate_content.return_value = mock_response

        gemini = GeminiIntegration(api_key="fake_key")
        resultado = gemini.analisar_paciente_estruturado("prompt")
        
        self.assertIn('prioridade', resultado)
        self.assertIn('razoes_alta', resultado)

class RAGSystemTests(TestCase):
    
    @patch('llm_service.src.rag.chromadb.PersistentClient')
    @patch('llm_service.src.rag.SentenceTransformer')
    def test_busca_contexto(self, mock_transformer, mock_chroma_client):
        mock_collection = MagicMock()
        mock_chroma_client.return_value.get_or_create_collection.return_value = mock_collection
        
        mock_collection.query.return_value = {
            'ids': [['doc1']],
            'distances': [[0.1]],
            'documents': [['Protocolo de Asma...']],
            'metadatas': [[{'patologia': 'ASMA'}]]
        }

        rag = RAGSystem()
        dados_paciente = {'patologia': 'ASMA', 'comorbidades': []}
        contexto = rag.buscar_contexto_relevante(dados_paciente)

        self.assertIsNotNone(contexto)
        self.assertIn('vector_store', contexto)
        self.assertIn('knowledge_base', contexto)

class ServiceOrchestrationTests(TestCase):
    
    @patch('llm_service.src.services.GeminiIntegration')
    @patch('llm_service.src.services.RAGSystem')
    def test_fluxo_completo_servico(self, MockRAG, MockGemini):
        mock_rag_instance = MockRAG.return_value
        mock_rag_instance.buscar_contexto_relevante.return_value = {
            'vector_store': [{'fonte': 'Mock', 'conteudo': 'Teste'}],
            'knowledge_base': {},
            'dados_internacao': {}
        }
        
        mock_gemini_instance = MockGemini.return_value
        mock_gemini_instance.analisar_paciente_estruturado.return_value = {
            'prioridade': 'ALTA',
            'confianca': 0.9,
            'razoes_alta': ['Teste'],
            'pendencias': [],
            'fontes_informacao': []
        }

        service = LLMService(api_key="fake")
        dados_entrada = {
            'paciente_nome': 'Teste',
            'patologia': 'PNEUMONIA',
            'tempo_permanencia': 5
        }
        
        resultado = service.analisar_paciente_alta(dados_entrada)

        self.assertIsNotNone(resultado)
        mock_rag_instance.buscar_contexto_relevante.assert_called_once()