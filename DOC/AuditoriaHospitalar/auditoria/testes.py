# auditoria/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta, date

from core.models import Paciente, Patologia, Procedimento
from .models import Internacao, ItemConta, Auditoria


class AuditoriaModelTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.patologia_rapida = Patologia.objects.create(
            nome="Apendicite", 
            codigo_cid="K35.8",  
            tempo_internacao_ideal=3
        )
        cls.patologia_longa = Patologia.objects.create(
            nome="Pneumonia Grave", 
            codigo_cid="J18.9",  
            tempo_internacao_ideal=10
        )
        cls.paciente = Paciente.objects.create(
            nome="João da Silva",
            cpf="111.111.111-11",    
            data_nascimento=date(1990, 1, 1) 
        )

    def test_internacao_excedeu_tempo_ideal(self):
        """
        Testa a lógica do models.py [RF004]
        Verifica se 'excedeu_tempo_ideal' retorna True quando o tempo é ultrapassado.
        """
        data_antiga = timezone.now() - timedelta(days=5)
        internacao = Internacao.objects.create(
            paciente=self.paciente,
            patologia=self.patologia_rapida, 
            data_entrada=data_antiga,
            setor='ENFERMARIA'
        )
        
        self.assertTrue(internacao.excedeu_tempo_ideal())
        self.assertEqual(internacao.dias_excesso(), 2)

    def test_internacao_nao_excedeu_tempo(self):
        """
        Testa a lógica do models.py [RF002]
        Verifica se 'excedeu_tempo_ideal' retorna False quando dentro do prazo.
        """
        data_recente = timezone.now() - timedelta(days=5)
        internacao = Internacao.objects.create(
            paciente=self.paciente,
            patologia=self.patologia_longa, 
            data_entrada=data_recente,
            setor='UTI'
        )
        
        self.assertFalse(internacao.excedeu_tempo_ideal())
        self.assertEqual(internacao.dias_excesso(), 0)

    def test_item_conta_calcula_valor_total(self):
        """
        Testa a lógica do models.py
        Verifica se o 'valor_total' é calculado automaticamente no 'save()'.
        """
        procedimento = Procedimento.objects.create(
            nome="Cateter", 
            codigo="C1234",          
            valor_padrao=100.00     
        )
        internacao = Internacao.objects.create(
            paciente=self.paciente,
            patologia=self.patologia_rapida,
            setor='ENFERMARIA'
        )
        item = ItemConta.objects.create(
            internacao=internacao,
            procedimento=procedimento,
            quantidade=3,
            valor_unitario=100.00 
        )
        
        self.assertEqual(item.valor_total, 300.00)


class AuditoriaViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='auditor', password='123')
        
        cls.patologia_uti = Patologia.objects.create(
            nome="Pneumonia", 
            codigo_cid="J18.0", 
            tempo_internacao_ideal=7
        )
        cls.patologia_enf = Patologia.objects.create(
            nome="Fratura", 
            codigo_cid="S72.0", 
            tempo_internacao_ideal=5
        )
        cls.paciente_uti = Paciente.objects.create(
            nome="Maria Oliveira", 
            cpf="222.222.222-22", 
            data_nascimento=date(1985, 5, 15)
        )
        cls.paciente_enf = Paciente.objects.create(
            nome="Carlos Pereira", 
            cpf="333.333.333-33", 
            data_nascimento=date(1970, 11, 30)
        )
        cls.procedimento = Procedimento.objects.create(
            nome="Antibiótico", 
            codigo="P555", 
            valor_padrao=50.00
        )

        cls.internacao_uti = Internacao.objects.create(
            paciente=cls.paciente_uti,
            patologia=cls.patologia_uti, # 
            data_entrada=timezone.now() - timedelta(days=10), 
            status='ATIVA',
            setor='UTI'
        )
        cls.internacao_enf = Internacao.objects.create(
            paciente=cls.paciente_enf,
            patologia=cls.patologia_enf, 
            data_entrada=timezone.now() - timedelta(days=2), 
            status='ATIVA',
            setor='ENFERMARIA'
        )
        cls.internacao_alta = Internacao.objects.create(
            paciente=cls.paciente_enf,
            patologia=cls.patologia_enf,
            data_entrada=timezone.now() - timedelta(days=10),
            data_saida=timezone.now() - timedelta(days=1),
            status='ALTA',
            setor='ENFERMARIA'
        )

        cls.item_pendente = ItemConta.objects.create(
            internacao=cls.internacao_alta,
            procedimento=cls.procedimento,
            quantidade=5,
            valor_unitario=50.00, 
            status='PENDENTE'
        )
        cls.item_aprovado = ItemConta.objects.create(
            internacao=cls.internacao_alta,
            procedimento=cls.procedimento,
            quantidade=2,
            valor_unitario=50.00,
            status='APROVADO'
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='auditor', password='123')

    def test_redirect_if_not_logged_in(self):
        """Testa se views @login_required redirecionam"""
        self.client.logout()
        response = self.client.get(reverse('auditoria:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_dashboard_view_RF010(self):
        """Testa a view 'dashboard' (views.py)"""
        response = self.client.get(reverse('auditoria:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auditoria/dashboard.html')
        
        self.assertEqual(response.context['total_internacoes'], 2) 
        self.assertEqual(response.context['total_alertas'], 1) 

    def test_monitoramento_view_RF001(self):
        """Testa a view 'monitoramento_tempo_real' (views.py)"""
        response = self.client.get(reverse('auditoria:monitoramento'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auditoria/monitoramento.html')
        self.assertEqual(len(response.context['internacoes']), 2)

    def test_monitoramento_filtro_setor_RF003(self):
        """Testa o FILTRO da 'monitoramento_tempo_real' (views.py)"""
        url = reverse('auditoria:monitoramento') + '?setor=UTI'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['internacoes']), 1)
        self.assertEqual(response.context['internacoes'][0].paciente.nome, "Maria Oliveira")
        self.assertEqual(response.context['setor_filtro'], 'UTI')

    def test_controle_altas_view_RF007(self):
        """Testa 'controle_altas', que só deve listar pacientes com tempo excedido (views.py)"""
        response = self.client.get(reverse('auditoria:controle_altas'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auditoria/controle_altas.html')
        
        self.assertEqual(len(response.context['prontas_alta']), 1)
        self.assertEqual(response.context['prontas_alta'][0].paciente.nome, "Maria Oliveira")

    def test_efetivar_alta_view_POST_RF009(self):
        """Testa a ação POST de 'efetivar_alta' (views.py)"""
        url = reverse('auditoria:efetivar_alta', args=[self.internacao_enf.id])
        response = self.client.post(url)
        
        self.internacao_enf.refresh_from_db()

        self.assertEqual(self.internacao_enf.status, 'ALTA')
        self.assertIsNotNone(self.internacao_enf.data_saida)
        self.assertRedirects(response, reverse('auditoria:controle_altas'))

    def test_analise_contas_view_RF014(self):
        """Testa 'analise_contas', que só deve listar internações com 'ALTA' (views.py)"""
        response = self.client.get(reverse('auditoria:analise_contas'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auditoria/analise_contas.html')
        self.assertEqual(len(response.context['internacoes']), 1)
        self.assertEqual(response.context['internacoes'][0].status, 'ALTA')

    def test_detalhe_conta_view_RF014(self):
        """Testa 'detalhe_conta' e o cálculo de totais (views.py)"""
        url = reverse('auditoria:detalhe_conta', args=[self.internacao_alta.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auditoria/detalhe_conta.html')
        
        self.assertEqual(response.context['valor_total'], 350.00) 
        self.assertEqual(response.context['total_glosado'], 0)
        self.assertEqual(len(response.context['itens']), 2)

    def test_validar_item_POST_glosar_RF027_RF028(self):
        """Testa a ação POST de 'validar_item' para GLOSAR (views.py)"""
        url = reverse('auditoria:validar_item', args=[self.item_pendente.id])
        post_data = {
            'acao': 'glosar',
            'justificativa': 'Quantidade excessiva'
        }
        response = self.client.post(url, post_data)

        self.item_pendente.refresh_from_db()
        
        self.assertEqual(self.item_pendente.status, 'GLOSADO')
        self.assertEqual(self.item_pendente.justificativa, 'Quantidade excessiva')
        
        expected_redirect = reverse('auditoria:detalhe_conta', args=[self.internacao_alta.id])
        self.assertRedirects(response, expected_redirect)

    def test_validar_item_POST_aprovar_RF027(self):
        """Testa a ação POST de 'validar_item' para APROVAR (views.py)"""
        url = reverse('auditoria:validar_item', args=[self.item_pendente.id])
        post_data = { 'acao': 'aprovar', 'justificativa': 'Aprovado' }
        self.client.post(url, post_data)
        
        self.item_pendente.refresh_from_db()
        self.assertEqual(self.item_pendente.status, 'APROVADO')
        self.assertEqual(self.item_pendente.justificativa, 'Aprovado')

    def test_historico_auditorias_view_RF033(self):
        """Testa a view 'historico_auditorias' (views.py)"""
        Auditoria.objects.create(
            internacao=self.internacao_alta,
            tipo='RETROSPECTIVA',
            auditor=self.user,
            observacoes='Auditoria de teste'
        )
        
        response = self.client.get(reverse('auditoria:historico'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auditoria/historico.html')
        self.assertEqual(len(response.context['auditorias']), 1)

    def test_historico_auditorias_busca_RF034(self):
        """Testa a BUSCA em 'historico_auditorias' (views.py)"""
        Auditoria.objects.create(
            internacao=self.internacao_alta, 
            tipo='RETROSPECTIVA',
            auditor=self.user,
            observacoes='Auditoria de teste'
        )
        
        url = reverse('auditoria:historico') + '?busca=Carlos'
        response = self.client.get(url)
        self.assertEqual(len(response.context['auditorias']), 1)
        self.assertEqual(response.context['termo_busca'], 'Carlos')

        url = reverse('auditoria:historico') + '?busca=Inexistente'
        response = self.client.get(url)
        self.assertEqual(len(response.context['auditorias']), 0)