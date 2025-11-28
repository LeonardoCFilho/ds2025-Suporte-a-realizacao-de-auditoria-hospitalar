# Escopo e Não Escopo - Sistema de Auditoria Hospitalar

## ESCOPO DO PROJETO

### 1. Introdução

O serviço de saúde enfrenta desafios relacionados à realização de exames, procedimentos e internações sem real necessidade clínica, seja por pressões dos pacientes ou interesses financeiros de profissionais e instituições, gerando aumento dos custos assistenciais e riscos à saúde, como infecções hospitalares.

A auditoria hospitalar é essencial para garantir a qualidade da assistência, o uso racional dos recursos e a integridade do paciente. O projeto visa desenvolver um sistema de software para apoiar a auditoria, com foco nos modelos concorrente e retrospectiva (intra).

A auditoria concorrente acompanha em tempo real procedimentos, tempo de internação e necessidade de exames, assegurando assistência ética e evitando excessos ou omissões. Já a auditoria retrospectiva revisa as contas e procedimentos após o atendimento, permitindo identificar itens desnecessários e oferecendo ferramentas de conferência, garantindo precisão e transparência entre instituições, profissionais e pacientes.

O projeto visa desenvolver um sistema de software que integra os dois modelos de auditoria — concorrente e retrospectiva — em uma única plataforma, permitindo o acompanhamento em tempo real das internações, a revisão criteriosa dos procedimentos e a gestão eficiente dos recursos hospitalares. O sistema tem como objetivo garantir uma assistência médica ética e segura, reduzir custos desnecessários e aumentar a transparência nos processos hospitalares, facilitando a identificação de excessos, a otimização do uso de exames e materiais e a preservação da saúde do paciente ao longo de toda a internação.

Além dos módulos de auditoria concorrente e retrospectiva, o sistema contará com um **agente de inteligência artificial** baseado em RAG (Retrieval-Augmented Generation).  

Esse agente tem como função **identificar pacientes com potencial de desospitalização**, priorizando casos com base em critérios clínicos, administrativos e de segurança.  

O objetivo é apoiar o auditor e o time assistencial na **redução de permanências desnecessárias**, sem comprometer a segurança do paciente, e oferecer **explicações claras** sobre o motivo de cada recomendação.


#### Diagrama de contexto

![alt text](https://github.com/LeonardoCFilho/ds2025-Suporte-a-realizacao-de-auditoria-hospitalar/blob/main/DOC/diagramas/1.diagrama_contexto.png)

### 2. Escopo Funcional

#### 2.1 Auditoria Concorrente

- **Monitoramento em tempo real** de pacientes internados (UTI, enfermaria, apartamentos)
- **Sistema de alertas** para identificar internações que excedem o tempo necessário
- **Interface para auditores** verificarem a necessidade de continuidade da internação
- **Módulo de controle de altas** para evitar esquecimentos da equipe médica
- **Dashboard de acompanhamento** do tempo de permanência por paciente
- **Relatórios de internações prolongadas** com justificativas médicas

#### 2.2 Auditoria Retrospectiva

- **Sistema de análise de contas médicas** após o atendimento
- **Módulo de validação de procedimentos** realizados versus patologia
- **Funcionalidade de glosa automática** para itens em excesso ou desnecessários
- **Base de conhecimento** com padrões de procedimentos por patologia
- **Interface de conferência** de materiais e medicamentos utilizados
- **Sistema de aprovação/rejeição** de itens da conta hospitalar

#### 2.3 Agente de Desospitalização (IA RAG)

- **Geração de lista diária** de pacientes com potencial de alta hospitalar
- **Classificação por prioridade (Alta, Média, Baixa)** conforme critérios clínicos e operacionais
- **Justificativas automáticas** com base em dados do prontuário, protocolos e regras do pagador
- **Identificação de pendências** (exames, pareceres, documentos administrativos)
- **Interface integrada** para que auditores e médicos validem ou rejeitem recomendações
- **Registro de decisões humanas** e motivos (para auditoria e aprendizado futuro)

#### 2.4 Funcionalidades Gerais

- **Controle de custos** por procedimento e paciente
- **Histórico de auditorias** realizadas
- **Integração com sistemas hospitalares** para coleta de dados
- **Módulo de configuração** de parâmetros de auditoria
- **Sistema de notificações** para equipes médicas e administrativa

#### Diagrama de container

![alt text](https://github.com/LeonardoCFilho/ds2025-Suporte-a-realizacao-de-auditoria-hospitalar/blob/main/DOC/diagramas/2.diagrama_container.png)

### 3. Escopo Não Funcional

- **Sistema web responsivo** acessível em diferentes dispositivos.
- **Interface intuitiva** para diferentes perfis de usuários (auditores, médicos, gestores).
- **Segurança de dados** conforme LGPD e regulamentações de saúde.
- **Performance para acompanhamento** em tempo real durante auditorias concorrentes.
- **Armazenamento seguro e confiável** de histórico de auditorias e relatórios.
- **Explicabilidade da IA:** todas as recomendações do agente devem exibir as fontes de informação usadas (ex.: prontuário, protocolo, regra administrativa), garantindo transparência e rastreabilidade.


### 4. Controles Éticos e de Qualidade

- **Identificação de procedimentos desnecessários** ou duplicados
- **Monitoramento de tempo ideal** de internação por patologia
- **Alertas de risco** para infecções hospitalares por permanência prolongada
- **Validação cruzada** de exames solicitados versus necessidade clínica
- **Revisão humana obrigatória** das recomendações do agente antes de qualquer alta
- **Auditoria de decisões da IA**, com registro de justificativas e acompanhamento de resultados clínicos


### 5. NÃO ESCOPO

#### 5.1 Funcionalidades Médicas

- **Não inclui** diagnósticos médicos ou recomendações clínicas
- **Não substitui** a avaliação médica profissional
- **Não realiza** prescrições ou alterações em tratamentos
- **Não interfere** diretamente nas decisões médicas
- **O agente de desospitalização não substitui a decisão médica**: ele apenas recomenda casos com base em critérios e dados disponíveis, devendo sempre haver validação por profissional de saúde.


#### 5.2 Sistemas Externos

- **Não inclui** desenvolvimento de prontuário eletrônico
- **Não contempla** sistema de agendamento de consultas
- **Não abrange** controle de estoque hospitalar completo
- **Não inclui** sistema financeiro/faturamento completo

#### 5.3 Aspectos Operacionais

- **Não contempla** treinamento de auditores
- **Não inclui** definição de protocolos médicos
- **Não abrange** gestão de recursos humanos
- **Não contempla** manutenção de equipamentos hospitalares

#### 5.4 Integrações Complexas

- **Não inclui** integração com sistemas de outras operadoras
- **Não contempla** interface com órgãos reguladores (ANS)
- **Não abrange** sistema de teleconsulta ou telemedicina
- **Não inclui** módulos de pesquisa científica

## PREMISSAS

- Integração via API com sistemas hospitalares existentes
- Banco de dados com informações de procedimentos padrão por patologia
- Conformidade com LGPD
- Conformidade com regulamentações da ANVISA aplicáveis a processos hospitalares e segurança do paciente
- Sistema web responsivo para acesso em diferentes dispositivos

### 6. RESTRIÇÕES

- Dependência de dados precisos dos sistemas hospitalares
- Necessidade de parametrização inicial dos padrões de procedimentos
- Limitação às auditorias concorrente e intra (não preventiva)
- Foco em operadoras de planos de saúde e hospitais privados
- Dependência da qualidade dos dados clínicos e administrativos para que o agente de desospitalização gere recomendações confiáveis.

