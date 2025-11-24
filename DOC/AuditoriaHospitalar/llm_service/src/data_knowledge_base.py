data_protocols = {
            'APENDICITE': {
                'description': 'Apendicite aguda pós-operatória',
                'avg_length_of_stay': 2,
                'discharge_criteria': [
                    'Sinais vitais estáveis por 24h',
                    'Tolerância à dieta oral estabelecida',
                    'Controle adequado da dor com medicação oral',
                    'Ausência de febre (>38°C) por 24h',
                    'Mobilização adequada',
                    'Corte cirúrgico sem sinais de infecção'
                ],
                'required_exams': ['Hemograma', 'Proteína C reativa'],
                'risk_factors': ['Idade >65 anos', 'Comorbidades múltiplas', 'Perfuração']
            },
            'PNEUMONIA': {
                'description': 'Pneumonia adquirida na comunidade',
                'avg_length_of_stay': 5,
                'discharge_criteria': [
                    'Melhora clínica sustentada',
                    'Saturação O2 >92% em ar ambiente',
                    'Hidratação oral adequada',
                    'Febril há mais de 48h',
                    'Troca para antibioticoterapia oral possível',
                    'Estabilidade hemodinâmica'
                ],
                'required_exams': ['Raio-X tórax', 'Hemograma', 'Gasometria arterial'],
                'risk_factors': ['Idade >65 anos', 'DPOC', 'Insuficiência cardíaca', 'Diabetes']
            },
            'FRATURA_FEMUR': {
                'description': 'Fratura de fêmur pós-redução cirúrgica',
                'avg_length_of_stay': 7,
                'discharge_criteria': [
                    'Controle adequado da dor com medicação oral',
                    'Mobilização com auxílio estabelecida',
                    'Ausência de complicações tromboembólicas',
                    'Condições domiciliares adequadas',
                    'Plano de reabilitação definido',
                    'Suporte social disponível'
                ],
                'required_exams': ['Raio-X controle', 'Doppler venoso'],
                'risk_factors': ['Osteoporose', 'Idade avançada', 'Comorbidades neurológicas']
            },
            'INSUF_CARDIACA': {
                'description': 'Insuficiência cardíaca descompensada',
                'avg_length_of_stay': 6,
                'discharge_criteria': [
                    'Estabilidade hemodinâmica',
                    'Diurese adequada (>0.5ml/kg/h)',
                    'Peso corporal estável ou em redução',
                    'Otimização da terapia medicamentosa',
                    'Saturação O2 estável em ar ambiente',
                    'Plano de cuidados estabelecido'
                ],
                'required_exams': ['Ecocardiograma', 'Eletrólitos', 'Função renal', 'BNP'],
                'risk_factors': ['Fração de ejeção <30%', 'Comorbidades renais', 'Arritmias']
            },
            'PANCREATITE': {
                'description': 'Pancreatite aguda',
                'avg_length_of_stay': 4,
                'discharge_criteria': [
                    'Controle adequado da dor com medicação oral',
                    'Tolerância à dieta oral estabelecida',
                    'Função renal estável',
                    'Enzimas pancreáticas em redução',
                    'Sem necessidade de suporte nutricional parenteral',
                    'Ausência de complicações locais'
                ],
                'required_exams': ['Amilase', 'Lipase', 'Tomografia abdominal', 'Função renal'],
                'risk_factors': ['Etiologia biliar', 'Consumo alcoólico', 'Hipertrigliceridemia']
            },
            'SEPSE': {
                'description': 'Sepse/Síndrome da resposta inflamatória sistêmica',
                'avg_length_of_stay': 10,
                'discharge_criteria': [
                    'Estabilidade hemodinâmica sem vasopressores',
                    'Resolução da fonte infecciosa',
                    'Melhora dos parâmetros inflamatórios',
                    'Função renal estável',
                    'Troca para antibioticoterapia oral possível',
                    'Ausência de disfunção orgânica'
                ],
                'required_exams': ['Hemograma serial', 'Proteína C reativa', 'Cultura', 'Função renal'],
                'risk_factors': ['Idade >65 anos', 'Imunossupressão', 'Comorbidades múltiplas']
            },
            'DIABETES_DESCOMP': {
                'description': 'Descompensação diabética (Cetoacidose/Estado hiperglicêmico)',
                'avg_length_of_stay': 4,
                'discharge_criteria': [
                    'Controle glicêmico adequado',
                    'Estado de hidratação normalizado',
                    'Equilíbrio acidobásico restabelecido',
                    'Plano de insulinoterapia estabelecido',
                    'Educação em diabetes reforçada',
                    'Condições para autocuidado adequadas'
                ],
                'required_exams': ['Glicemia capilar', 'Gasometria', 'Eletrólitos', 'Corpos cetônicos'],
                'risk_factors': ['Diabetes tipo 1', 'Infecções intercorrentes', 'Adesão terapêutica inadequada']
            },
            'ASMA_GRAVE': {
                'description': 'Crise de asma grave',
                'avg_length_of_stay': 3,
                'discharge_criteria': [
                    'Saturação O2 >92% em ar ambiente',
                    'Melhora significativa da dispneia',
                    'Uso de beta-2 agonista <4h',
                    'Pico de fluxo expiratório >70% do previsto',
                    'Plano de ação para asma estabelecido',
                    'Condições para seguimento ambulatorial'
                ],
                'required_exams': ['Gasometria', 'Raio-X tórax', 'Pico de fluxo expiratório'],
                'risk_factors': ['Asma de difícil controle', 'Comorbidades respiratórias', 'Histórico de intubação']
            },
            'CIRURGIA_CARDIO': {
                'description': 'Pós-operatório de cirurgia cardíaca',
                'avg_length_of_stay': 5,
                'discharge_criteria': [
                    'Estabilidade hemodinâmica',
                    'Controle adequado da dor',
                    'Função renal preservada',
                    'Deambulação adequada',
                    'Condições da ferida cirúrgica satisfatórias',
                    'Plano de anticoagulação estabelecido'
                ],
                'required_exams': ['Ecocardiograma', 'Eletrólitos', 'Coagulograma', 'Raio-X tórax'],
                'risk_factors': ['Idade >70 anos', 'Disfunção ventricular', 'Comorbidades múltiplas']
            },
            'AVC_ISQUEMICO': {
                'description': 'Acidente Vascular Cerebral Isquêmico',
                'avg_length_of_stay': 8,
                'discharge_criteria': [
                    'Estabilidade neurológica',
                    'Controle de fatores de risco',
                    'Função deglutória preservada',
                    'Mobilização com auxílio possível',
                    'Plano de reabilitação estabelecido',
                    'Suporte social adequado'
                ],
                'required_exams': ['Tomografia cranial', 'Ressonância magnética', 'Doppler de carótidas'],
                'risk_factors': ['FA não tratada', 'Hipertensão arterial', 'Dislipidemia', 'Tabagismo']
            }
        }

data_discharge_criteria = {
            'vital_signs_ranges': {
                'blood_pressure_systolic': (90, 160),
                'blood_pressure_diastolic': (60, 100),
                'heart_rate': (50, 100),
                'respiratory_rate': (12, 20),
                'temperature': (36.0, 37.8),
                'oxygen_saturation': (92, 100)
            },
            'functional_status': [
                'Consciente e orientado',
                'Via aérea pérvia',
                'Hidratação oral adequada',
                'Controle da dor adequado',
                'Mobilização possível',
                'Alimentação por via oral'
            ],
            'social_factors': [
                'Suporte domiciliar adequado',
                'Condições de moradia apropriadas',
                'Acesso a cuidados de follow-up',
                'Transporte disponível'
            ]
        }

data_load_player_rules = {
            'max_length_of_stay': {
                'APENDICITE': 3,
                'PNEUMONIA': 7,
                'FRATURA_FEMUR': 10,
                'INSUF_CARDIACA': 8,
                'PANCREATITE': 6,
                'SEPSE': 14,
                'DIABETES_DESCOMP': 5,
                'ASMA_GRAVE': 4,
                'CIRURGIA_CARDIO': 7,
                'AVC_ISQUEMICO': 12,
                'DEFAULT': 10
            },
            'audit_flags': {
                'extended_stay_threshold': 0.3,  # 30% acima do tempo médio
                'high_cost_procedures': ['CIRURGIA_CARDIO', 'SEPSE', 'AVC_ISQUEMICO'],
                'frequent_readmission_risk': ['INSUF_CARDIACA', 'DPOC', 'DIABETES_DESCOMP']
            }
        }
