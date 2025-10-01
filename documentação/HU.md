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

### HU05 – Relatórios de Internações Prolongadas
Como Auditor, eu quero gerar relatórios de internações prolongadas com justificativas médicas, para embasar decisões de auditoria e glosas.

**Critérios de Aceite:**
- Deve exibir lista de pacientes com internação acima do tempo ideal.
- Deve incluir justificativa médica vinculada.
- Deve permitir exportação e impressão.

**Prioridade:** Alta

### HU06 – Análise de Contas Médicas
Como Auditor, eu quero analisar contas médicas após a alta, para identificar cobranças indevidas.

**Critérios de Aceite:**
- Deve exibir lista detalhada de procedimentos lançados.
- Deve permitir marcação de inconsistências.
- Deve manter histórico de análises por paciente.

**Prioridade:** Alta

### HU07 – Validação de Procedimentos
Como Auditor, eu quero validar se os procedimentos realizados são compatíveis com a patologia, para evitar cobranças desnecessárias.

**Critérios de Aceite:**

- O sistema deve comparar procedimentos realizados com base de conhecimento por patologia.
- Deve sinalizar divergências.
- Deve registrar decisão do auditor.

**Prioridade:** Alta

### HU08 – Glosa Automática
Como Auditor, eu quero que o sistema realize glosas automáticas de itens em excesso ou desnecessários, para reduzir custos e aumentar a eficiência.

**Critérios de Aceite:**
- O sistema deve glosar automaticamente itens fora dos padrões configurados.
- Deve registrar justificativa da glosa.
- Deve permitir revisão manual pelo auditor.

**Prioridade:** Alta

### HU09 – Base de Conhecimento
Como Auditor, eu quero acessar uma base de conhecimento com padrões de procedimentos por patologia, para ter embasamento técnico nas auditorias.

**Critérios de Aceite:**
- Deve armazenar procedimentos recomendados por patologia.
- Deve ser consultável por auditores durante análises.
- Deve ser atualizado periodicamente por administradores.  

**Prioridade:** Média

### HU10 – Conferência de Materiais e Medicamentos
Como Auditor, eu quero verificar materiais e medicamentos lançados na conta, para identificar inconsistências ou duplicidades.

**Critérios de Aceite:**
- Deve listar materiais e medicamentos por atendimento.
- Deve destacar lançamentos duplicados.
- Deve permitir registrar decisão do auditor.

**Prioridade:** Alta

### HU11 – Aprovação ou Rejeição de Itens
Como Gestor Hospitalar, eu quero aprovar ou rejeitar itens da conta hospitalar, para assegurar transparência e conformidade.

**Critérios de Aceite:**
- Deve permitir aprovar/rejeitar itens individualmente.
- Deve registrar justificativas.
- Deve gerar relatório final da decisão.

**Prioridade:** Alta

### HU12 – Controle de Custos por Paciente
Como Gestor Hospitalar, eu quero controlar os custos por paciente e procedimento, para ter clareza sobre gastos e otimizar recursos.

**Critérios de Aceite:**
- Deve consolidar custos por paciente.
- Deve permitir visualização por procedimento.
- Deve exportar relatórios financeiros.

**Prioridade:** Alta

### HU13 – Histórico de Auditorias
Como Auditor, eu quero acessar o histórico de auditorias realizadas, para consultar decisões passadas e evitar redundâncias.

**Critérios de Aceite:**
- Deve armazenar auditorias por paciente.
- Deve ser pesquisável por data, nome ou número de atendimento.
- Deve permitir visualização em PDF.

**Prioridade:** Média

### HU14 – Integração com Sistemas Hospitalares
Como Administrador de TI, eu quero integrar o sistema com os sistemas hospitalares via API, para coletar dados automaticamente sem retrabalho manual.

**Critérios de Aceite:**
- Deve consumir dados via API.
- Deve permitir configuração de endpoints.
- Deve atualizar informações em tempo quase real.

**Prioridade:** Alta

### HU15 – Relatórios de Custos e Sinistralidade
Como gestor de operadora de saúde, eu quero gerar relatórios de custos e sinistralidade, para ter base para negociar reajustes de contrato.

**Critérios de Aceite:**
- Relatórios devem incluir custos totais, por paciente e por setor.
- Deve apresentar indicadores de sinistralidade mensal/anual.
- Deve exportar relatórios em PDF/Excel.

**Prioridade:** Alta

### HU16 – Configuração de Parâmetros de Auditoria
Como Administrador de TI, eu quero configurar parâmetros de auditoria (tempo de internação, regras de glosa, padrões de patologia), para adaptar o sistema às políticas da instituição.

**Critérios de Aceite:**
- Deve permitir configurar limites por patologia.
- Deve salvar diferentes perfis de parametrização.
- Deve aplicar automaticamente as regras configuradas.

**Prioridade:** Alta

### HU17 – Notificações Automáticas
Como Auditor, eu quero receber notificações automáticas do sistema, para não perder prazos nem deixar de acompanhar alterações importantes.

**Critérios de Aceite:**
- Notificações devem ser enviadas por e-mail e no sistema.
- Devem ser configuráveis por tipo de evento.
- Devem registrar data/hora do envio.

**Prioridade:** Média

### HU18 – Identificação de Procedimentos Duplicados
Como Auditor, eu quero que o sistema identifique procedimentos desnecessários ou duplicados, para garantir ética e evitar cobranças indevidas.

**Critérios de Aceite:**
- Deve comparar lançamentos repetidos.
- Deve sinalizar inconsistências automaticamente.
- Deve permitir confirmação manual pelo auditor.

**Prioridade:** Alta

### HU19 – Monitoramento do Tempo Ideal de Internação
Como Médico, eu quero que o sistema monitore o tempo ideal de internação por patologia, para reduzir riscos desnecessários ao paciente.

**Critérios de Aceite:**
- Deve exibir tempo previsto de internação.
- Deve comparar tempo real com tempo padrão.
- Deve emitir alertas quando ultrapassado.

**Prioridade:** Alta

### HU20 – Alertas de Risco de Infecção
Como Auditor, eu quero receber alertas de risco de infecção hospitalar por permanência prolongada, para acionar medidas preventivas.

**Critérios de Aceite:**
- Deve emitir alertas quando tempo de internação ultrapassar limite crítico.
- Deve registrar justificativa médica vinculada.
- Deve incluir os alertas nos relatórios do paciente.

**Prioridade:** Alta

### HU21 – Validação Cruzada de Exames
Como Médico, eu quero que o sistema valide exames solicitados versus necessidade clínica, para coibir pedidos excessivos e preservar a segurança do paciente.

**Critérios de Aceite:**
- Deve comparar exames solicitados com diagnóstico informado.
- eve emitir alertas de incompatibilidade.
- Deve permitir revisão manual do auditor.

**Prioridade:** Alta

### HU22 – Acesso Multidispositivo
Como Administrador de TI, eu quero acessar o sistema em diferentes dispositivos (PC, tablet, celular), para acompanhar auditorias de qualquer lugar.

**Critérios de Aceite:**
- Sistema deve ser responsivo.
- Deve funcionar em navegadores modernos.
- Deve manter desempenho em diferentes telas.

**Prioridade:** Média

### HU23 – Interface Intuitiva
Como Gestor Hospitalar, eu quero que a interface do sistema seja intuitiva, para realizar análises sem necessidade de treinamento extenso.

**Critérios de Aceite:**
- Deve ter design simples e organizado.
- Deve usar nomenclatura próxima da prática hospitalar.
- Deve ter tutoriais e ajuda contextual.

**Prioridade:** Média

### HU24 – Conformidade com LGPD
Como Gestor Hospitalar, eu quero que os dados sejam tratados conforme a LGPD, para assegurar a privacidade e segurança dos pacientes.

**Critérios de Aceite:**
- Dados pessoais devem ser criptografados.
- Deve haver gestão de consentimento.
- Deve permitir anonimização de dados quando solicitado.

**Prioridade:** Alta

### HU25 – Performance em Tempo Real
Como Administrador de TI, eu quero que o sistema seja rápido e estável no acompanhamento em tempo real, para não perder prazos durante auditorias concorrentes.

**Critérios de Aceite:**
- Deve processar dados em tempo real com baixa latência.
- Deve suportar múltiplos acessos simultâneos.
- Deve garantir disponibilidade mínima de 99%.

**Prioridade:** Alta

### HU26 – Armazenamento Seguro de Histórico
Como Administrador de TI, eu quero armazenar o histórico de auditorias e relatórios em ambiente seguro, para preservar informações críticas a longo prazo.

**Critérios de Aceite:**
- Deve armazenar auditorias por tempo indeterminado.
- Deve usar backup automático em nuvem segura.
- Deve registrar logs de acesso.

**Prioridade:** Alta