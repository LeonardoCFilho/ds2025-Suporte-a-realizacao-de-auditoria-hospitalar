# Priorização de Requisitos - Sistema de Auditoria Hospitalar

## Status de Implementação

| Código | Descrição | Status | Categoria |
|--------|-----------|--------|-----------|
| RF001 | Lista de pacientes internados por setor | Implementado | Auditoria Concorrente |
| RF002 | Tempo de permanência atualizado | Implementado | Auditoria Concorrente |
| RF003 | Filtrar pacientes por setor | Implementado | Auditoria Concorrente |
| RF004 | Alertas visuais para tempo excedido | Implementado | Auditoria Concorrente |
| RF007 | Módulo de controle de altas | Implementado | Auditoria Concorrente |
| RF009 | Registro de data/hora da alta | Implementado | Auditoria Concorrente |
| RF010 | Dashboard com indicadores | Implementado | Auditoria Concorrente |
| RF014 | Lista de procedimentos em contas | Implementado | Auditoria Retrospectiva |
| RF015 | Marcação de inconsistências | Implementado | Auditoria Retrospectiva |
| RF016 | Histórico de análises | Implementado | Auditoria Retrospectiva |
| RF027 | Aprovar/rejeitar itens | Implementado | Funcionalidades Gerais |
| RF028 | Justificativas para decisões | Implementado | Funcionalidades Gerais |
| RF030 | Consolidação de custos | Implementado | Funcionalidades Gerais |
| RF033 | Histórico de auditorias | Implementado | Funcionalidades Gerais |
| RF034 | Pesquisa no histórico | Implementado | Funcionalidades Gerais |

**Total Implementado:** 15 de 45 requisitos funcionais (33%)

---

## Matriz de Priorização

| Prioridade | Código | Descrição | Complexidade | Impacto | Dependências |
|------------|--------|-----------|--------------|---------|--------------|
| **ALTA** | RF005 | Configurar alertas por patologia | Média | Alto | - |
| **ALTA** | RF006 | Registrar tratamento de alertas | Baixa | Alto | RF005 |
| **ALTA** | RF008 | Lembretes automáticos de alta | Média | Alto | RF042 |
| **ALTA** | RF017 | Validar compatibilidade procedimento x patologia | Alta | Crítico | RF023 |
| **ALTA** | RF018 | Sinalizar divergências | Média | Crítico | RF017, RF023 |
| **ALTA** | RF019 | Registrar decisão do auditor | Baixa | Alto | RF017 |
| **ALTA** | RF020 | Glosas automáticas | Alta | Crítico | RF017, RF023 |
| **ALTA** | RF021 | Justificativas de glosas automáticas | Baixa | Alto | RF020 |
| **ALTA** | RF022 | Revisão manual de glosas | Média | Alto | RF020 |
| **ALTA** | RF023 | Base de conhecimento por patologia | Alta | Crítico | - |
| **ALTA** | RF024 | Consulta à base durante análises | Baixa | Alto | RF023 |
| **ALTA** | RF025 | Atualização periódica da base | Média | Médio | RF023 |
| **ALTA** | RF042 | Notificações automáticas por e-mail | Média | Alto | - |
| **ALTA** | RF043 | Configuração de notificações | Baixa | Médio | RF042 |
| **ALTA** | RF044 | Registro de envio de notificações | Baixa | Médio | RF042 |
| **MÉDIA** | RF011 | Filtros no dashboard | Baixa | Médio | - |
| **MÉDIA** | RF012 | Exportar dashboard em PDF/Excel | Média | Médio | - |
| **MÉDIA** | RF013 | Relatórios de internações prolongadas | Média | Médio | - |
| **MÉDIA** | RF026 | Conferência de materiais e medicamentos | Média | Médio | - |
| **MÉDIA** | RF029 | Relatório final de aprovações/rejeições | Média | Médio | - |
| **MÉDIA** | RF031 | Visualização de custos por procedimento | Baixa | Médio | - |
| **MÉDIA** | RF032 | Exportar relatórios financeiros | Média | Médio | - |
| **MÉDIA** | RF035 | Visualização de auditorias em PDF | Média | Baixo | - |
| **MÉDIA** | RF045 | Relatórios de sinistralidade | Média | Médio | - |
| **BAIXA** | RF036 | Integração via API | Alta | Baixo | - |
| **BAIXA** | RF037 | Configuração de endpoints | Baixa | Baixo | RF036 |
| **BAIXA** | RF038 | Atualização em tempo quase real | Alta | Baixo | RF036 |
| **BAIXA** | RF039 | Configurar parâmetros de auditoria | Média | Baixo | - |
| **BAIXA** | RF040 | Perfis de parametrização | Média | Baixo | RF039 |
| **BAIXA** | RF041 | Aplicação automática de regras | Média | Baixo | RF039, RF040 |
