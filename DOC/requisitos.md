# Documento de Requisitos - Sistema de Auditoria Hospitalar

## 1. Requisitos Funcionais

### 1.1 Auditoria Concorrente
- RF001 - O Sistema deve exibir a lista de pacientes internados em diferentes setores (UTI, enfermaria, apartamentos).
- RF002 - O Sistema deve mostrar o tempo de permanência atualizado em tempo real.
- RF003 - O Sistema deve permitir filtrar pacientes por setor.
- RF004 - O Sistema deve gerar alertas visuais e sonoros quando um paciente ultrapassar o tempo previsto de internação.
- RF005 - O Sistema deve permitir configurar alertas por patologia.
- RF006 - O Sistema deve registrar quando um alerta for tratado.
- RF007 - O Sistema deve disponibilizar um módulo de controle de altas para listar pacientes prontos para alta.
- RF008 - O Sistema deve enviar lembretes automáticos de alta para a equipe médica.
- RF009 - O Sistema deve registrar data e hora da efetivação da alta.
- RF010 - O Sistema deve disponibilizar um dashboard com gráficos e indicadores de tempo de permanência por paciente.
- RF011 - O Sistema deve permitir filtros no dashboard por setor, patologia ou período.
- RF012 - O Sistema deve exportar relatórios do dashboard em PDF ou Excel.
- RF013 - O Sistema deve gerar relatórios de internações prolongadas com justificativas médicas.

### 1.2 Auditoria Retrospectiva
- RF014 - O Sistema deve exibir lista detalhada de procedimentos lançados em contas médicas.
- RF015 - O Sistema deve permitir a marcação de inconsistências em contas médicas.
- RF016 - O Sistema deve manter histórico de análises de contas por paciente.
- RF017 - O Sistema deve validar se os procedimentos realizados são compatíveis com a patologia do paciente.
- RF018 - O Sistema deve sinalizar divergências entre procedimentos realizados e a base de conhecimento.
- RF019 - O Sistema deve registrar a decisão do auditor em validações de procedimentos.
- RF020 - O Sistema deve realizar glosas automáticas de itens em excesso ou desnecessários.
- RF021 - O Sistema deve registrar justificativas de glosas automáticas.
- RF022 - O Sistema deve permitir revisão manual das glosas pelo auditor.
- RF023 - O Sistema deve disponibilizar uma base de conhecimento com procedimentos recomendados por patologia.
- RF024 - O Sistema deve permitir que auditores consultem a base de conhecimento durante análises.
- RF025 - O Sistema deve permitir atualização periódica da base de conhecimento por administradores.
- RF026 - O Sistema deve disponibilizar uma interface de conferência de materiais e medicamentos utilizados.

### 1.3 Funcionalidades Gerais
- RF027 - O Sistema deve permitir aprovar ou rejeitar itens individualmente em contas hospitalares.
- RF028 - O Sistema deve registrar justificativas para aprovações e rejeições.
- RF029 - O Sistema deve gerar relatório final com decisões de aprovação ou rejeição.
- RF030 - O Sistema deve consolidar custos por paciente.
- RF031 - O Sistema deve permitir visualização de custos por procedimento.
- RF032 - O Sistema deve exportar relatórios financeiros em PDF ou Excel.
- RF033 - O Sistema deve armazenar histórico de auditorias realizadas.
- RF034 - O Sistema deve permitir pesquisa no histórico de auditorias por data, nome ou número de atendimento.
- RF035 - O Sistema deve disponibilizar visualização de auditorias em formato PDF.
- RF036 - O Sistema deve integrar-se com sistemas hospitalares via API para coleta automática de dados.
- RF037 - O Sistema deve permitir configuração de endpoints de integração.
- RF038 - O Sistema deve atualizar informações coletadas em tempo quase real.
- RF039 - O Sistema deve permitir configurar parâmetros de auditoria (tempo de internação, regras de glosa, padrões por patologia).
- RF040 - O Sistema deve salvar diferentes perfis de parametrização de auditoria.
- RF041 - O Sistema deve aplicar automaticamente as regras configuradas de auditoria.
- RF042 - O Sistema deve enviar notificações automáticas por e-mail e pelo sistema.
- RF043 - O Sistema deve permitir configuração de notificações por tipo de evento.
- RF044 - O Sistema deve registrar data e hora do envio das notificações.
- RF045 - O Usuário deve poder gerar relatórios de custos e sinistralidade mensais ou anuais.

---

## 2. Requisitos Não Funcionais

### 2.1 Usabilidade
- RNF001 - O Sistema deve ser web responsivo e acessível em diferentes dispositivos.
- RNF002 - O Sistema deve disponibilizar interface intuitiva para diferentes perfis de usuários (auditores, médicos, gestores).

### 2.2 Segurança
- RNF003 - O Sistema deve armazenar dados em conformidade com a LGPD.
- RNF004 - O Sistema deve criptografar dados sensíveis.
- RNF005 - O Sistema deve realizar backup automático periódico dos dados.
- RNF006 - O Sistema deve implementar controle de acesso por permissões.

### 2.3 Performance
- RNF007 - O Sistema deve suportar acompanhamento em tempo real de auditorias concorrentes.
- RNF008 - O Sistema deve utilizar cache para consultas frequentes.
- RNF009 - O Sistema deve implementar paginação em listagens grandes.
- RNF010 - O Sistema deve utilizar WebSockets para atualizações em tempo real.

### 2.4 Confiabilidade
- RNF011 - O Sistema deve armazenar de forma segura e confiável o histórico de auditorias e relatórios.
- RNF012 - O Sistema deve registrar logs de eventos críticos para auditoria de uso.

### 2.5 Manutenibilidade
- RNF013 - O Sistema deve ser implementado seguindo princípios SOLID.
- RNF014 - O Sistema deve separar responsabilidades em camadas (apresentação, aplicação, domínio, infraestrutura).
- RNF015 - O Sistema deve centralizar regras de negócio e validações para evitar duplicidade.

### 2.6 Testabilidade
- RNF016 - O Sistema deve permitir criação de testes automatizados unitários e de integração.
- RNF017 - O Sistema deve disponibilizar interfaces para uso de mocks em testes.

---
