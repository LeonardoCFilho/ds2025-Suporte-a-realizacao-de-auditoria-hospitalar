# Histórias de Usuário - Sistema de Auditoria Hospitalar

### HU01 – Monitoramento em Tempo Real
Como Auditor, eu quero monitorar pacientes internados, para que eu possa identificar casos que ultrapassaram o tempo ideal de permanência e agir rapidamente.

**Critérios de Aceite:**
- O sistema deve exibir a lista de pacientes internados em diferentes setores (UTI, enfermaria, apartamentos).
- Deve mostrar o tempo de permanência atualizado em tempo real.
- Deve permitir filtrar pacientes por setor.

**Prioridade:** Alta

### HU02 – Alertas de Internações Prolongadas
Como Auditor, eu quero receber alertas automáticos quando um paciente ultrapassar o tempo previsto de internação, para que eu possa intervir de forma preventiva.

**Critérios de Aceite:**
- O sistema deve gerar alertas visuais e sonoros.
- Alertas devem ser configuráveis por patologia.
- Deve registrar quando um alerta foi tratado.

**Prioridade:** Alta

### HU03 – Controle de Altas
Como Médico, eu quero acessar um módulo de controle de altas, para evitar esquecimentos da equipe médica e reduzir custos desnecessários.

**Critérios de Aceite:**
- Deve listar pacientes prontos para alta segundo parâmetros definidos.
- Deve enviar lembretes automáticos para equipe médica.
- Deve registrar a data/hora da efetivação da alta.

**Prioridade:** Alta

### HU04 – Dashboard de Permanência
Como Gestor Hospitalar, eu quero visualizar um dashboard com tempo de permanência por paciente, para acompanhar indicadores de desempenho assistencial e financeiro.

**Critérios de Aceite:**
- Dashboard deve apresentar gráficos e indicadores em tempo real.
- Deve permitir filtrar por setor, patologia ou período.
- Deve exportar relatórios em PDF/Excel.

**Prioridade:** Alta

### HU05 – Análise de Contas Médicas
Como Auditor, eu quero analisar contas médicas após a alta, para identificar cobranças indevidas.

**Critérios de Aceite:**
- Deve exibir lista detalhada de procedimentos lançados.
- Deve permitir marcação de inconsistências.
- Deve manter histórico de análises por paciente.

**Prioridade:** Alta

### HU06 – Validação de Procedimentos
Como Auditor, eu quero validar se os procedimentos realizados são compatíveis com a patologia, para evitar cobranças desnecessárias.

**Critérios de Aceite:**

- O sistema deve comparar procedimentos realizados com base de conhecimento por patologia.
- Deve sinalizar divergências.
- Deve registrar decisão do auditor.

**Prioridade:** Alta

### HU07 – Glosa Automática
Como Auditor, eu quero que o sistema realize glosas automáticas de itens em excesso ou desnecessários, para reduzir custos e aumentar a eficiência.

**Critérios de Aceite:**
- O sistema deve glosar automaticamente itens fora dos padrões configurados.
- Deve registrar justificativa da glosa.
- Deve permitir revisão manual pelo auditor.

**Prioridade:** Alta

### HU08 – Base de Conhecimento
Como Auditor, eu quero acessar uma base de conhecimento com padrões de procedimentos por patologia, para ter embasamento técnico nas auditorias.

**Critérios de Aceite:**
- Deve armazenar procedimentos recomendados por patologia.
- Deve ser consultável por auditores durante análises.
- Deve ser atualizado periodicamente por administradores.  

**Prioridade:** Média


### HU09 – Aprovação ou Rejeição de Itens
Como Gestor Hospitalar, eu quero aprovar ou rejeitar itens da conta hospitalar, para assegurar transparência e conformidade.

**Critérios de Aceite:**
- Deve permitir aprovar/rejeitar itens individualmente.
- Deve registrar justificativas.
- Deve gerar relatório final da decisão.

**Prioridade:** Alta

### HU10 – Controle de Custos por Paciente
Como Gestor Hospitalar, eu quero controlar os custos por paciente e procedimento, para ter clareza sobre gastos e otimizar recursos.

**Critérios de Aceite:**
- Deve consolidar custos por paciente.
- Deve permitir visualização por procedimento.
- Deve exportar relatórios financeiros.

**Prioridade:** Alta

### HU11 – Histórico de Auditorias
Como Auditor, eu quero acessar o histórico de auditorias realizadas, para consultar decisões passadas e evitar redundâncias.

**Critérios de Aceite:**
- Deve armazenar auditorias por paciente.
- Deve ser pesquisável por data, nome ou número de atendimento.
- Deve permitir visualização em PDF.

**Prioridade:** Média

### HU12 – Integração com Sistemas Hospitalares
Como Administrador de TI, eu quero integrar o sistema com os sistemas hospitalares via API, para coletar dados automaticamente sem retrabalho manual.

**Critérios de Aceite:**
- Deve consumir dados via API.
- Deve permitir configuração de endpoints.
- Deve atualizar informações em tempo quase real.

**Prioridade:** Alta

### HU13 – Relatórios de Custos e Sinistralidade
Como gestor de operadora de saúde, eu quero gerar relatórios de custos e sinistralidade, para ter base para negociar reajustes de contrato.

**Critérios de Aceite:**
- Relatórios devem incluir custos totais, por paciente e por setor.
- Deve apresentar indicadores de sinistralidade mensal/anual.
- Deve exportar relatórios em PDF/Excel.

**Prioridade:** Alta

### HU14 – Configuração de Parâmetros de Auditoria
Como Administrador de TI, eu quero configurar parâmetros de auditoria (tempo de internação, regras de glosa, padrões de patologia), para adaptar o sistema às políticas da instituição.

**Critérios de Aceite:**
- Deve permitir configurar limites por patologia.
- Deve salvar diferentes perfis de parametrização.
- Deve aplicar automaticamente as regras configuradas.

**Prioridade:** Alta

### HU15 – Notificações Automáticas
Como Auditor, eu quero receber notificações automáticas do sistema, para não perder prazos nem deixar de acompanhar alterações importantes.

**Critérios de Aceite:**
- Notificações devem ser enviadas por e-mail e no sistema.
- Devem ser configuráveis por tipo de evento.
- Devem registrar data/hora do envio.

**Prioridade:** Médi