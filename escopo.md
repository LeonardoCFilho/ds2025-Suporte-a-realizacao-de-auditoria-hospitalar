# Escopo e Não Escopo - Sistema de Auditoria Hospitalar

## ESCOPO DO PROJETO

### 1. Auditoria Concorrente

- **Monitoramento em tempo real** de pacientes internados (UTI, enfermaria, apartamentos)
- **Sistema de alertas** para identificar internações que excedem o tempo necessário
- **Interface para auditores** verificarem a necessidade de continuidade da internação
- **Módulo de controle de altas** para evitar esquecimentos da equipe médica
- **Dashboard de acompanhamento** do tempo de permanência por paciente
- **Relatórios de internações prolongadas** com justificativas médicas

### 2. Auditoria Intra (Retrospectiva)

- **Sistema de análise de contas médicas** após o atendimento
- **Módulo de validação de procedimentos** realizados versus patologia
- **Funcionalidade de glosa automática** para itens em excesso ou desnecessários
- **Base de conhecimento** com padrões de procedimentos por patologia
- **Interface de conferência** de materiais e medicamentos utilizados
- **Sistema de aprovação/rejeição** de itens da conta hospitalar

### 3. Funcionalidades Gerais

- **Controle de custos** por procedimento e paciente
- **Histórico de auditorias** realizadas
- **Integração com sistemas hospitalares** para coleta de dados
- **Relatórios gerenciais** de custos e sinistralidade
- **Módulo de configuração** de parâmetros de auditoria
- **Sistema de notificações** para equipes médicas e administrativa

### 4. Controles Éticos e de Qualidade

- **Identificação de procedimentos desnecessários** ou duplicados
- **Monitoramento de tempo ideal** de internação por patologia
- **Alertas de risco** para infecções hospitalares por permanência prolongada
- **Validação cruzada** de exames solicitados versus necessidade clínica

## NÃO ESCOPO DO PROJETO

### 1. Funcionalidades Médicas

- **Não inclui** diagnósticos médicos ou recomendações clínicas
- **Não substitui** a avaliação médica profissional
- **Não realiza** prescrições ou alterações em tratamentos
- **Não interfere** diretamente nas decisões médicas

### 2. Sistemas Externos

- **Não inclui** desenvolvimento de prontuário eletrônico
- **Não contempla** sistema de agendamento de consultas
- **Não abrange** controle de estoque hospitalar completo
- **Não inclui** sistema financeiro/faturamento completo

### 3. Aspectos Operacionais

- **Não contempla** treinamento de auditores
- **Não inclui** definição de protocolos médicos
- **Não abrange** gestão de recursos humanos
- **Não contempla** manutenção de equipamentos hospitalares

### 4. Integrações Complexas

- **Não inclui** integração com sistemas de outras operadoras
- **Não contempla** interface com órgãos reguladores (ANS)
- **Não abrange** sistema de teleconsulta ou telemedicina
- **Não inclui** módulos de pesquisa científica

## PREMISSAS

- Sistema web responsivo para acesso em diferentes dispositivos
- Integração via API com sistemas hospitalares existentes
- Banco de dados com informações de procedimentos padrão por patologia
- Interface intuitiva para diferentes perfis de usuários (auditores, médicos, gestores)
- Conformidade com LGPD e regulamentações de saúde

## RESTRIÇÕES

- Dependência de dados precisos dos sistemas hospitalares
- Necessidade de parametrização inicial dos padrões de procedimentos
- Limitação às auditorias concorrente e intra (não preventiva)
- Foco em operadoras de planos de saúde e hospitais privados
