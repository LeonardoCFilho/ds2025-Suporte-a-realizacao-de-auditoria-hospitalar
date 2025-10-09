from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from core.models import Patologia, Procedimento, ProcedimentoPadrao, Paciente
from auditoria.models import Internacao, ItemConta, Auditoria


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpar',
            action='store_true',
            help='Limpa todos os dados antes de popular',
        )

    def handle(self, *args, **kwargs):
        limpar = kwargs['limpar']

        if limpar:
            self.stdout.write(self.style.WARNING('⚠️  Limpando banco de dados...'))
            Auditoria.objects.all().delete()
            ItemConta.objects.all().delete()
            Internacao.objects.all().delete()
            Paciente.objects.all().delete()
            ProcedimentoPadrao.objects.all().delete()
            Procedimento.objects.all().delete()
            Patologia.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('✓ Banco de dados limpo'))

        self.stdout.write('Iniciando população de dados...\n')

        # Criar usuários
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✓ Usuário admin criado'))

        if not User.objects.filter(username='auditor').exists():
            User.objects.create_user('auditor', 'auditor@example.com', 'auditor123')
            self.stdout.write(self.style.SUCCESS('✓ Usuário auditor criado'))

        if not User.objects.filter(username='medico').exists():
            User.objects.create_user('medico', 'medico@example.com', 'medico123')
            self.stdout.write(self.style.SUCCESS('✓ Usuário medico criado'))

        auditor = User.objects.get(username='auditor')

        # Criar Patologias
        patologias_data = [
            {'nome': 'Pneumonia', 'codigo_cid': 'J18.9', 'tempo_internacao_ideal': 7, 'descricao': 'Infecção dos pulmões'},
            {'nome': 'Apendicite Aguda', 'codigo_cid': 'K35.8', 'tempo_internacao_ideal': 3, 'descricao': 'Inflamação do apêndice'},
            {'nome': 'Infarto Agudo do Miocárdio', 'codigo_cid': 'I21.9', 'tempo_internacao_ideal': 5, 'descricao': 'Ataque cardíaco'},
            {'nome': 'Fratura de Fêmur', 'codigo_cid': 'S72.9', 'tempo_internacao_ideal': 10, 'descricao': 'Fratura do osso da coxa'},
            {'nome': 'AVC Isquêmico', 'codigo_cid': 'I63.9', 'tempo_internacao_ideal': 8, 'descricao': 'Derrame cerebral'},
            {'nome': 'Diabetes Descompensada', 'codigo_cid': 'E14.9', 'tempo_internacao_ideal': 4, 'descricao': 'Descontrole glicêmico'},
            {'nome': 'Insuficiência Cardíaca', 'codigo_cid': 'I50.9', 'tempo_internacao_ideal': 6, 'descricao': 'Falência cardíaca'},
            {'nome': 'DPOC Agudizada', 'codigo_cid': 'J44.1', 'tempo_internacao_ideal': 5, 'descricao': 'Doença pulmonar obstrutiva crônica'},
            {'nome': 'Pielonefrite', 'codigo_cid': 'N10', 'tempo_internacao_ideal': 7, 'descricao': 'Infecção renal'},
            {'nome': 'Colecistite Aguda', 'codigo_cid': 'K81.0', 'tempo_internacao_ideal': 4, 'descricao': 'Inflamação da vesícula'},
        ]

        patologias = {}
        for data in patologias_data:
            patologia, created = Patologia.objects.get_or_create(
                codigo_cid=data['codigo_cid'],
                defaults=data
            )
            patologias[data['codigo_cid']] = patologia
            if created:
                self.stdout.write(f'✓ Patologia: {patologia.nome}')

        # Criar Procedimentos
        procedimentos_data = [
            {'nome': 'Raio-X de Tórax', 'codigo': 'RX001', 'valor_padrao': Decimal('80.00'), 'descricao': 'Radiografia do tórax'},
            {'nome': 'Hemograma Completo', 'codigo': 'LAB001', 'valor_padrao': Decimal('35.00'), 'descricao': 'Exame de sangue completo'},
            {'nome': 'Tomografia Computadorizada', 'codigo': 'TC001', 'valor_padrao': Decimal('450.00'), 'descricao': 'TC de qualquer região'},
            {'nome': 'Eletrocardiograma', 'codigo': 'ECG001', 'valor_padrao': Decimal('60.00'), 'descricao': 'ECG de 12 derivações'},
            {'nome': 'Ultrassonografia Abdominal', 'codigo': 'US001', 'valor_padrao': Decimal('120.00'), 'descricao': 'US de abdome total'},
            {'nome': 'Ressonância Magnética', 'codigo': 'RM001', 'valor_padrao': Decimal('800.00'), 'descricao': 'RM de qualquer região'},
            {'nome': 'Antibiótico - Ceftriaxona', 'codigo': 'MED001', 'valor_padrao': Decimal('45.00'), 'descricao': 'Antibiótico injetável'},
            {'nome': 'Analgésico - Dipirona', 'codigo': 'MED002', 'valor_padrao': Decimal('8.00'), 'descricao': 'Analgésico comum'},
            {'nome': 'Cirurgia de Apendicectomia', 'codigo': 'CIR001', 'valor_padrao': Decimal('3500.00'), 'descricao': 'Remoção do apêndice'},
            {'nome': 'Diária de UTI', 'codigo': 'INT001', 'valor_padrao': Decimal('1200.00'), 'descricao': 'Diária em UTI'},
            {'nome': 'Diária de Enfermaria', 'codigo': 'INT002', 'valor_padrao': Decimal('400.00'), 'descricao': 'Diária em enfermaria'},
            {'nome': 'Diária de Apartamento', 'codigo': 'INT003', 'valor_padrao': Decimal('600.00'), 'descricao': 'Diária em apartamento'},
            {'nome': 'Glicemia em Jejum', 'codigo': 'LAB002', 'valor_padrao': Decimal('25.00'), 'descricao': 'Dosagem de glicose'},
            {'nome': 'Ureia e Creatinina', 'codigo': 'LAB003', 'valor_padrao': Decimal('40.00'), 'descricao': 'Função renal'},
            {'nome': 'Insulina NPH', 'codigo': 'MED003', 'valor_padrao': Decimal('35.00'), 'descricao': 'Insulina de ação intermediária'},
            {'nome': 'Ecocardiograma', 'codigo': 'ECO001', 'valor_padrao': Decimal('180.00'), 'descricao': 'Ultrassom do coração'},
            {'nome': 'Gasometria Arterial', 'codigo': 'LAB004', 'valor_padrao': Decimal('55.00'), 'descricao': 'Análise de gases no sangue'},
            {'nome': 'Cateterismo Cardíaco', 'codigo': 'PROC001', 'valor_padrao': Decimal('2500.00'), 'descricao': 'Cateterismo diagnóstico'},
            {'nome': 'Hemocultura', 'codigo': 'LAB005', 'valor_padrao': Decimal('80.00'), 'descricao': 'Cultura de sangue'},
            {'nome': 'Cirurgia de Colecistectomia', 'codigo': 'CIR002', 'valor_padrao': Decimal('4200.00'), 'descricao': 'Remoção da vesícula'},
        ]

        procedimentos = {}
        for data in procedimentos_data:
            procedimento, created = Procedimento.objects.get_or_create(
                codigo=data['codigo'],
                defaults=data
            )
            procedimentos[data['codigo']] = procedimento
            if created:
                self.stdout.write(f'✓ Procedimento: {procedimento.nome}')

        # Criar Base de Conhecimento (Procedimentos Padrão)
        procedimentos_padrao_data = [
            # Pneumonia
            {'patologia': 'J18.9', 'procedimento': 'RX001', 'quantidade_maxima': 2, 'obrigatorio': True},
            {'patologia': 'J18.9', 'procedimento': 'LAB001', 'quantidade_maxima': 3, 'obrigatorio': True},
            {'patologia': 'J18.9', 'procedimento': 'MED001', 'quantidade_maxima': 7, 'obrigatorio': True},
            {'patologia': 'J18.9', 'procedimento': 'LAB005', 'quantidade_maxima': 2, 'obrigatorio': True},
            # Apendicite
            {'patologia': 'K35.8', 'procedimento': 'US001', 'quantidade_maxima': 1, 'obrigatorio': True},
            {'patologia': 'K35.8', 'procedimento': 'LAB001', 'quantidade_maxima': 2, 'obrigatorio': True},
            {'patologia': 'K35.8', 'procedimento': 'CIR001', 'quantidade_maxima': 1, 'obrigatorio': True},
            # IAM
            {'patologia': 'I21.9', 'procedimento': 'ECG001', 'quantidade_maxima': 5, 'obrigatorio': True},
            {'patologia': 'I21.9', 'procedimento': 'LAB001', 'quantidade_maxima': 4, 'obrigatorio': True},
            {'patologia': 'I21.9', 'procedimento': 'INT001', 'quantidade_maxima': 3, 'obrigatorio': False},
            {'patologia': 'I21.9', 'procedimento': 'ECO001', 'quantidade_maxima': 2, 'obrigatorio': True},
            {'patologia': 'I21.9', 'procedimento': 'PROC001', 'quantidade_maxima': 1, 'obrigatorio': False},
            # Diabetes
            {'patologia': 'E14.9', 'procedimento': 'LAB002', 'quantidade_maxima': 6, 'obrigatorio': True},
            {'patologia': 'E14.9', 'procedimento': 'MED003', 'quantidade_maxima': 4, 'obrigatorio': True},
            {'patologia': 'E14.9', 'procedimento': 'LAB001', 'quantidade_maxima': 2, 'obrigatorio': True},
            # Colecistite
            {'patologia': 'K81.0', 'procedimento': 'US001', 'quantidade_maxima': 1, 'obrigatorio': True},
            {'patologia': 'K81.0', 'procedimento': 'CIR002', 'quantidade_maxima': 1, 'obrigatorio': True},
            {'patologia': 'K81.0', 'procedimento': 'LAB001', 'quantidade_maxima': 2, 'obrigatorio': True},
        ]

        for data in procedimentos_padrao_data:
            ProcedimentoPadrao.objects.get_or_create(
                patologia=patologias[data['patologia']],
                procedimento=procedimentos[data['procedimento']],
                defaults={
                    'quantidade_maxima': data['quantidade_maxima'],
                    'obrigatorio': data['obrigatorio']
                }
            )

        self.stdout.write('✓ Base de conhecimento configurada\n')

        # Criar Pacientes
        pacientes_data = [
            {'nome': 'João Silva', 'cpf': '123.456.789-00', 'data_nascimento': '1965-03-15', 'setor_atual': 'ENFERMARIA'},
            {'nome': 'Maria Santos', 'cpf': '987.654.321-00', 'data_nascimento': '1978-07-22', 'setor_atual': 'UTI'},
            {'nome': 'Pedro Oliveira', 'cpf': '456.789.123-00', 'data_nascimento': '1990-11-05', 'setor_atual': 'APARTAMENTO'},
            {'nome': 'Ana Costa', 'cpf': '321.654.987-00', 'data_nascimento': '1985-01-30', 'setor_atual': 'ENFERMARIA'},
            {'nome': 'Carlos Souza', 'cpf': '789.123.456-00', 'data_nascimento': '1972-09-18', 'setor_atual': 'UTI'},
            {'nome': 'Juliana Pereira', 'cpf': '147.258.369-00', 'data_nascimento': '1992-05-10', 'setor_atual': 'APARTAMENTO'},
            {'nome': 'Roberto Alves', 'cpf': '369.258.147-00', 'data_nascimento': '1958-12-03', 'setor_atual': 'ENFERMARIA'},
            {'nome': 'Fernanda Lima', 'cpf': '258.147.369-00', 'data_nascimento': '1980-08-25', 'setor_atual': 'UTI'},
            {'nome': 'Paulo Mendes', 'cpf': '741.852.963-00', 'data_nascimento': '1995-02-14', 'setor_atual': 'ENFERMARIA'},
            {'nome': 'Beatriz Rocha', 'cpf': '963.852.741-00', 'data_nascimento': '1970-11-30', 'setor_atual': 'APARTAMENTO'},
            {'nome': 'Lucas Ferreira', 'cpf': '159.753.486-00', 'data_nascimento': '1988-06-20', 'setor_atual': 'ENFERMARIA'},
            {'nome': 'Camila Nunes', 'cpf': '486.159.753-00', 'data_nascimento': '1993-09-08', 'setor_atual': 'UTI'},
            {'nome': 'Ricardo Martins', 'cpf': '357.159.486-00', 'data_nascimento': '1962-04-17', 'setor_atual': 'APARTAMENTO'},
            {'nome': 'Patricia Gomes', 'cpf': '864.297.531-00', 'data_nascimento': '1975-01-22', 'setor_atual': 'ENFERMARIA'},
            {'nome': 'Anderson Silva', 'cpf': '531.864.297-00', 'data_nascimento': '1987-07-11', 'setor_atual': 'UTI'},
        ]

        pacientes = []
        for data in pacientes_data:
            paciente, created = Paciente.objects.get_or_create(
                cpf=data['cpf'],
                defaults=data
            )
            pacientes.append(paciente)
            if created:
                self.stdout.write(f'✓ Paciente: {paciente.nome}')

        self.stdout.write('\n📋 Criando internações...\n')

        now = timezone.now()
        internacoes_criadas = []

        # INTERNAÇÕES ATIVAS COM ALERTA
        # 1. João Silva - Pneumonia (10 dias, ideal 7)
        int1, _ = Internacao.objects.get_or_create(
            paciente=pacientes[0],
            status='ATIVA',
            defaults={
                'patologia': patologias['J18.9'],
                'data_entrada': now - timedelta(days=10),
                'setor': 'ENFERMARIA',
                'alerta_tempo': True,
                'observacoes': 'Pneumonia bilateral, em antibioticoterapia há 10 dias'
            }
        )
        internacoes_criadas.append(int1)

        # 2. Maria Santos - IAM (8 dias, ideal 5)
        int2, _ = Internacao.objects.get_or_create(
            paciente=pacientes[1],
            status='ATIVA',
            defaults={
                'patologia': patologias['I21.9'],
                'data_entrada': now - timedelta(days=8),
                'setor': 'UTI',
                'alerta_tempo': True,
                'observacoes': 'Pós-IAM com STENT, aguardando vaga em enfermaria'
            }
        )
        internacoes_criadas.append(int2)

        # 3. Roberto Alves - AVC (12 dias, ideal 8)
        int3, _ = Internacao.objects.get_or_create(
            paciente=pacientes[6],
            status='ATIVA',
            defaults={
                'patologia': patologias['I63.9'],
                'data_entrada': now - timedelta(days=12),
                'setor': 'ENFERMARIA',
                'alerta_tempo': True,
                'observacoes': 'AVC isquêmico, reabilitação em andamento'
            }
        )
        internacoes_criadas.append(int3)

        # 4. Fernanda Lima - DPOC (7 dias, ideal 5)
        int4, _ = Internacao.objects.get_or_create(
            paciente=pacientes[7],
            status='ATIVA',
            defaults={
                'patologia': patologias['J44.1'],
                'data_entrada': now - timedelta(days=7),
                'setor': 'UTI',
                'alerta_tempo': True,
                'observacoes': 'DPOC agudizada, em ventilação mecânica'
            }
        )
        internacoes_criadas.append(int4)

        # INTERNAÇÕES ATIVAS NORMAIS
        # 5. Pedro Oliveira - Apendicite (2 dias, ideal 3)
        int5, _ = Internacao.objects.get_or_create(
            paciente=pacientes[2],
            status='ATIVA',
            defaults={
                'patologia': patologias['K35.8'],
                'data_entrada': now - timedelta(days=2),
                'setor': 'APARTAMENTO',
                'alerta_tempo': False,
                'observacoes': 'Pós-operatório de apendicectomia, evoluindo bem'
            }
        )
        internacoes_criadas.append(int5)

        # 6. Juliana Pereira - Pielonefrite (4 dias, ideal 7)
        int6, _ = Internacao.objects.get_or_create(
            paciente=pacientes[5],
            status='ATIVA',
            defaults={
                'patologia': patologias['N10'],
                'data_entrada': now - timedelta(days=4),
                'setor': 'APARTAMENTO',
                'alerta_tempo': False,
                'observacoes': 'Pielonefrite aguda, boa resposta ao antibiótico'
            }
        )
        internacoes_criadas.append(int6)

        # 7. Lucas Ferreira - Diabetes (2 dias, ideal 4)
        int7, _ = Internacao.objects.get_or_create(
            paciente=pacientes[10],
            status='ATIVA',
            defaults={
                'patologia': patologias['E14.9'],
                'data_entrada': now - timedelta(days=2),
                'setor': 'ENFERMARIA',
                'alerta_tempo': False,
                'observacoes': 'Diabetes descompensada, ajuste de insulina'
            }
        )
        internacoes_criadas.append(int7)

        # INTERNAÇÕES FINALIZADAS (para auditoria retrospectiva)
        # 8. Ana Costa - Apendicite FINALIZADA
        int8, _ = Internacao.objects.get_or_create(
            paciente=pacientes[3],
            status='ALTA',
            defaults={
                'patologia': patologias['K35.8'],
                'data_entrada': now - timedelta(days=7),
                'data_saida': now - timedelta(days=3),
                'setor': 'ENFERMARIA',
                'observacoes': 'Alta hospitalar sem complicações'
            }
        )
        internacoes_criadas.append(int8)

        # 9. Carlos Souza - IAM FINALIZADO
        int9, _ = Internacao.objects.get_or_create(
            paciente=pacientes[4],
            status='ALTA',
            defaults={
                'patologia': patologias['I21.9'],
                'data_entrada': now - timedelta(days=12),
                'data_saida': now - timedelta(days=4),
                'setor': 'UTI',
                'observacoes': 'Alta para acompanhamento ambulatorial'
            }
        )
        internacoes_criadas.append(int9)

        # 10. Beatriz Rocha - Colecistite FINALIZADA
        int10, _ = Internacao.objects.get_or_create(
            paciente=pacientes[9],
            status='ALTA',
            defaults={
                'patologia': patologias['K81.0'],
                'data_entrada': now - timedelta(days=8),
                'data_saida': now - timedelta(days=2),
                'setor': 'APARTAMENTO',
                'observacoes': 'Pós-operatório de colecistectomia, alta em bom estado'
            }
        )
        internacoes_criadas.append(int10)

        # 11. Paulo Mendes - Pneumonia FINALIZADA
        int11, _ = Internacao.objects.get_or_create(
            paciente=pacientes[8],
            status='ALTA',
            defaults={
                'patologia': patologias['J18.9'],
                'data_entrada': now - timedelta(days=10),
                'data_saida': now - timedelta(days=1),
                'setor': 'ENFERMARIA',
                'observacoes': 'Pneumonia tratada com sucesso'
            }
        )
        internacoes_criadas.append(int11)

        # 12. Camila Nunes - Diabetes FINALIZADA
        int12, _ = Internacao.objects.get_or_create(
            paciente=pacientes[11],
            status='ALTA',
            defaults={
                'patologia': patologias['E14.9'],
                'data_entrada': now - timedelta(days=7),
                'data_saida': now - timedelta(days=2),
                'setor': 'UTI',
                'observacoes': 'Glicemia controlada, alta com insulina ajustada'
            }
        )
        internacoes_criadas.append(int12)

        self.stdout.write(f'✓ {len(internacoes_criadas)} internações criadas\n')

        # Criar Itens de Conta para internações finalizadas
        self.stdout.write('💰 Criando itens de conta...\n')

        # Itens para int8 (Ana Costa - Apendicite) - PENDENTES
        if ItemConta.objects.filter(internacao=int8).count() == 0:
            ItemConta.objects.create(internacao=int8, procedimento=procedimentos['US001'], quantidade=1, valor_unitario=procedimentos['US001'].valor_padrao, status='PENDENTE')
            ItemConta.objects.create(internacao=int8, procedimento=procedimentos['LAB001'], quantidade=2, valor_unitario=procedimentos['LAB001'].valor_padrao, status='PENDENTE')
            ItemConta.objects.create(internacao=int8, procedimento=procedimentos['CIR001'], quantidade=1, valor_unitario=procedimentos['CIR001'].valor_padrao, status='PENDENTE')
            ItemConta.objects.create(internacao=int8, procedimento=procedimentos['TC001'], quantidade=2, valor_unitario=procedimentos['TC001'].valor_padrao, status='PENDENTE')  # EXCESSO
            ItemConta.objects.create(internacao=int8, procedimento=procedimentos['INT002'], quantidade=4, valor_unitario=procedimentos['INT002'].valor_padrao, status='PENDENTE')
            self.stdout.write('✓ Itens criados para Ana Costa (5 itens, 1 em excesso)')

        # Itens para int9 (Carlos Souza - IAM) - AUDITADOS
        if ItemConta.objects.filter(internacao=int9).count() == 0:
            ItemConta.objects.create(internacao=int9, procedimento=procedimentos['ECG001'], quantidade=4, valor_unitario=procedimentos['ECG001'].valor_padrao, status='APROVADO', justificativa='Conforme protocolo de IAM')
            ItemConta.objects.create(internacao=int9, procedimento=procedimentos['LAB001'], quantidade=3, valor_unitario=procedimentos['LAB001'].valor_padrao, status='APROVADO', justificativa='Dentro do padrão')
            ItemConta.objects.create(internacao=int9, procedimento=procedimentos['INT001'], quantidade=3, valor_unitario=procedimentos['INT001'].valor_padrao, status='APROVADO', justificativa='Diárias necessárias')
            ItemConta.objects.create(internacao=int9, procedimento=procedimentos['RM001'], quantidade=1, valor_unitario=procedimentos['RM001'].valor_padrao, status='GLOSADO', justificativa='Não previsto no protocolo')
            ItemConta.objects.create(internacao=int9, procedimento=procedimentos['ECO001'], quantidade=2, valor_unitario=procedimentos['ECO001'].valor_padrao, status='APROVADO', justificativa='Ecocardiograma necessário')
            self.stdout.write('✓ Itens criados para Carlos Souza (5 itens, 1 glosado)')

        # Itens para int10 (Beatriz - Colecistite) - PENDENTES
        if ItemConta.objects.filter(internacao=int10).count() == 0:
            ItemConta.objects.create(internacao=int10, procedimento=procedimentos['US001'], quantidade=1, valor_unitario=procedimentos['US001'].valor_padrao, status='PENDENTE')
            ItemConta.objects.create(internacao=int10, procedimento=procedimentos['CIR002'], quantidade=1, valor_unitario=procedimentos['CIR002'].valor_padrao, status='PENDENTE')
            ItemConta.objects.create(internacao=int10, procedimento=procedimentos['LAB001'], quantidade=2, valor_unitario=procedimentos['LAB001'].valor_padrao, status='PENDENTE')
            ItemConta.objects.create(internacao=int10, procedimento=procedimentos['INT003'], quantidade=6, valor_unitario=procedimentos['INT003'].valor_padrao, status='PENDENTE')
            ItemConta.objects.create(internacao=int10, procedimento=procedimentos['RM001'], quantidade=1, valor_unitario=procedimentos['RM001'].valor_padrao, status='PENDENTE')  # EXCESSO
            self.stdout.write('✓ Itens criados para Beatriz Rocha (5 itens, 1 desnecessário)')

        # Itens para int11 (Paulo - Pneumonia) - MISTOS
        if ItemConta.objects.filter(internacao=int11).count() == 0:
            ItemConta.objects.create(internacao=int11, procedimento=procedimentos['RX001'], quantidade=2, valor_unitario=procedimentos['RX001'].valor_padrao, status='APROVADO', justificativa='Raio-X de controle')
            ItemConta.objects.create(internacao=int11, procedimento=procedimentos['LAB001'], quantidade=3, valor_unitario=procedimentos['LAB001'].valor_padrao, status='APROVADO', justificativa='Hemogramas necessários')
            ItemConta.objects.create(internacao=int11, procedimento=procedimentos['MED001'], quantidade=9, valor_unitario=procedimentos['MED001'].valor_padrao, status='GLOSADO', justificativa='Quantidade acima do protocolo (máx 7)')
            ItemConta.objects.create(internacao=int11, procedimento=procedimentos['LAB005'], quantidade=2, valor_unitario=procedimentos['LAB005'].valor_padrao, status='APROVADO', justificativa='Hemoculturas indicadas')
            ItemConta.objects.create(internacao=int11, procedimento=procedimentos['INT002'], quantidade=9, valor_unitario=procedimentos['INT002'].valor_padrao, status='PENDENTE')
            self.stdout.write('✓ Itens criados para Paulo Mendes (5 itens, 1 glosado)')

        # Itens para int12 (Camila - Diabetes) - PENDENTES
        if ItemConta.objects.filter(internacao=int12).count() == 0:
            ItemConta.objects.create(internacao=int12, procedimento=procedimentos['LAB002'], quantidade=6, valor_unitario=procedimentos['LAB002'].valor_padrao, status='PENDENTE')
            ItemConta.objects.create(internacao=int12, procedimento=procedimentos['MED003'], quantidade=4, valor_unitario=procedimentos['MED003'].valor_padrao, status='PENDENTE')
            ItemConta.objects.create(internacao=int12, procedimento=procedimentos['LAB001'], quantidade=2, valor_unitario=procedimentos['LAB001'].valor_padrao, status='PENDENTE')
            ItemConta.objects.create(internacao=int12, procedimento=procedimentos['INT001'], quantidade=5, valor_unitario=procedimentos['INT001'].valor_padrao, status='PENDENTE')
            ItemConta.objects.create(internacao=int12, procedimento=procedimentos['TC001'], quantidade=1, valor_unitario=procedimentos['TC001'].valor_padrao, status='PENDENTE')  # DESNECESSÁRIO
            self.stdout.write('✓ Itens criados para Camila Nunes (5 itens, 1 desnecessário)')

        self.stdout.write('\n📊 Criando auditorias...\n')

        # Auditoria 1 - Carlos Souza (IAM)
        Auditoria.objects.get_or_create(
            internacao=int9,
            tipo='RETROSPECTIVA',
            defaults={
                'auditor': auditor,
                'observacoes': 'Auditoria retrospectiva: RM não estava prevista no protocolo de IAM. Demais itens aprovados conforme padrão.',
                'itens_glosados': 1,
                'valor_glosado': procedimentos['RM001'].valor_padrao
            }
        )
        self.stdout.write('✓ Auditoria retrospectiva: Carlos Souza (IAM)')

        # Auditoria 2 - Paulo Mendes (Pneumonia)
        Auditoria.objects.get_or_create(
            internacao=int11,
            tipo='RETROSPECTIVA',
            defaults={
                'auditor': auditor,
                'observacoes': 'Auditoria retrospectiva: Antibiótico em quantidade excessiva (9 doses quando o máximo é 7). Glosado o excesso.',
                'itens_glosados': 1,
                'valor_glosado': procedimentos['MED001'].valor_padrao * 2
            }
        )
        self.stdout.write('✓ Auditoria retrospectiva: Paulo Mendes (Pneumonia)')

        # Auditoria 3 - João Silva (Pneumonia - Concorrente)
        Auditoria.objects.get_or_create(
            internacao=int1,
            tipo='CONCORRENTE',
            defaults={
                'auditor': auditor,
                'observacoes': 'Auditoria concorrente: Paciente ultrapassou tempo ideal de internação. Solicitado parecer médico para alta.',
                'itens_glosados': 0,
                'valor_glosado': Decimal('0.00')
            }
        )
        self.stdout.write('✓ Auditoria concorrente: João Silva (Pneumonia)')

        # Auditoria 4 - Maria Santos (IAM - Concorrente)
        Auditoria.objects.get_or_create(
            internacao=int2,
            tipo='CONCORRENTE',
            defaults={
                'auditor': auditor,
                'observacoes': 'Auditoria concorrente: Paciente em UTI há 8 dias (ideal 5). Aguardando transferência para enfermaria.',
                'itens_glosados': 0,
                'valor_glosado': Decimal('0.00')
            }
        )
        self.stdout.write('✓ Auditoria concorrente: Maria Santos (IAM)')

        # Auditoria 5 - Roberto Alves (AVC - Concorrente)
        Auditoria.objects.get_or_create(
            internacao=int3,
            tipo='CONCORRENTE',
            defaults={
                'auditor': auditor,
                'observacoes': 'Auditoria concorrente: Paciente com AVC há 12 dias. Processo de reabilitação em andamento, necessário parecer de fisioterapia.',
                'itens_glosados': 0,
                'valor_glosado': Decimal('0.00')
            }
        )
        self.stdout.write('✓ Auditoria concorrente: Roberto Alves (AVC)')

        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ Dados populados com sucesso!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        self.stdout.write('\n📊 RESUMO:')
        self.stdout.write(f'   • {Patologia.objects.count()} patologias')
        self.stdout.write(f'   • {Procedimento.objects.count()} procedimentos')
        self.stdout.write(f'   • {ProcedimentoPadrao.objects.count()} procedimentos padrão (base de conhecimento)')
        self.stdout.write(f'   • {Paciente.objects.count()} pacientes')
        self.stdout.write(f'   • {Internacao.objects.filter(status="ATIVA").count()} internações ativas')
        self.stdout.write(f'   • {Internacao.objects.filter(status="ALTA").count()} internações finalizadas')
        self.stdout.write(f'   • {ItemConta.objects.count()} itens de conta')
        self.stdout.write(f'   • {Auditoria.objects.count()} auditorias registradas')
        
        alertas = Internacao.objects.filter(status='ATIVA').count()
        com_alerta = sum(1 for i in Internacao.objects.filter(status='ATIVA') if i.excedeu_tempo_ideal())
        self.stdout.write(f'   • {com_alerta} internações com alerta de tempo')

        self.stdout.write('\n👥 CREDENCIAIS:')
        self.stdout.write('   • Admin: admin / admin123')
        self.stdout.write('   • Auditor: auditor / auditor123')
        self.stdout.write('   • Médico: medico / medico123')
        
        self.stdout.write('\n🌐 ACESSO:')
        self.stdout.write('   http://127.0.0.1:8000/')
        
        self.stdout.write('\n📋 FUNCIONALIDADES PARA TESTAR:')
        self.stdout.write('   1. Dashboard - Visão geral com alertas')
        self.stdout.write('   2. Monitoramento - 7 internações ativas (4 com alerta)')
        self.stdout.write('   3. Controle de Altas - 4 pacientes prontos para alta')
        self.stdout.write('   4. Análise de Contas - 5 contas finalizadas para auditar')
        self.stdout.write('   5. Histórico - 5 auditorias registradas')
        
        self.stdout.write('\n💡 DICA: Use --limpar para resetar o banco antes de popular')
        self.stdout.write('   python manage.py popular_dados --limpar\n')