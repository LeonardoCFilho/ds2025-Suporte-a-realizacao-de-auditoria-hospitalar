# Escopo e Não Escopo - Sistema de Auditoria Hospitalar

## ESCOPO DO PROJETO

### 1. Introdução

O serviço de saúde enfrenta desafios relacionados à realização de exames, procedimentos e internações sem real necessidade clínica, seja por pressões dos pacientes ou interesses financeiros de profissionais e instituições, gerando aumento dos custos assistenciais e riscos à saúde, como infecções hospitalares.

A auditoria hospitalar é essencial para garantir a qualidade da assistência, o uso racional dos recursos e a integridade do paciente. O projeto visa desenvolver um sistema de software para apoiar a auditoria, com foco nos modelos concorrente e retrospectiva (intra).

A auditoria concorrente acompanha em tempo real procedimentos, tempo de internação e necessidade de exames, assegurando assistência ética e evitando excessos ou omissões. Já a auditoria retrospectiva revisa as contas e procedimentos após o atendimento, permitindo identificar itens desnecessários e oferecendo ferramentas de conferência, garantindo precisão e transparência entre instituições, profissionais e pacientes.

O projeto visa desenvolver um sistema de software que integra os dois modelos de auditoria — concorrente e retrospectiva — em uma única plataforma, permitindo o acompanhamento em tempo real das internações, a revisão criteriosa dos procedimentos e a gestão eficiente dos recursos hospitalares. O sistema tem como objetivo garantir uma assistência médica ética e segura, reduzir custos desnecessários e aumentar a transparência nos processos hospitalares, facilitando a identificação de excessos, a otimização do uso de exames e materiais e a preservação da saúde do paciente ao longo de toda a internação.

#### Diagrama de contexto

![alt text](https://github.com/LeonardoCFilho/ds2025-Suporte-a-realizacao-de-auditoria-hospitalar/blob/main/documentação/diagramas/1.diagrama_contexto.png)

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

#### 2.3 Funcionalidades Gerais

- **Controle de custos** por procedimento e paciente
- **Histórico de auditorias** realizadas
- **Integração com sistemas hospitalares** para coleta de dados
- **Módulo de configuração** de parâmetros de auditoria
- **Sistema de notificações** para equipes médicas e administrativa

#### Diagrama de container

![alt text](https://github.com/LeonardoCFilho/ds2025-Suporte-a-realizacao-de-auditoria-hospitalar/blob/main/documentação/diagramas/2.diagrama_container.png)

### 3. Escopo Não Funcional

- **Sistema web responsivo** acessível em diferentes dispositivos.
- **Interface intuitiva** para diferentes perfis de usuários (auditores, médicos, gestores).
- **Segurança de dados** conforme LGPD e regulamentações de saúde.
- **Performance para acompanhamento** em tempo real durante auditorias concorrentes.
- **Armazenamento seguro e confiável** de histórico de auditorias e relatórios.

### 4. Controles Éticos e de Qualidade

- **Identificação de procedimentos desnecessários** ou duplicados
- **Monitoramento de tempo ideal** de internação por patologia
- **Alertas de risco** para infecções hospitalares por permanência prolongada
- **Validação cruzada** de exames solicitados versus necessidade clínica

### 5. NÃO ESCOPO

#### 5.1 Funcionalidades Médicas

- **Não inclui** diagnósticos médicos ou recomendações clínicas
- **Não substitui** a avaliação médica profissional
- **Não realiza** prescrições ou alterações em tratamentos
- **Não interfere** diretamente nas decisões médicas

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
