    # Agente de Desospitalização (RAG) – Documento de Diretrizes

## 1. Propósito
Estabelecer diretrizes para o desenvolvimento de um **agente de inteligência artificial** (modelo RAG – Retrieval-Augmented Generation) voltado ao apoio da **auditoria hospitalar e gestão de leitos**, com foco na **identificação de pacientes com potencial de alta** e na **redução de permanências desnecessárias**, mantendo a segurança assistencial.

---

## 2. Objetivos Iniciais
- Auxiliar auditores e gestores na **priorização de casos para desospitalização**.  
- Fornecer **razões explicáveis** para cada recomendação.  
- Apoiar decisões de alta **sem substituí-las**.  
- Promover **redução de custos** mantendo qualidade e segurança clínica.

---

## 3. Escopo Previsto
O agente deverá:
- Analisar dados clínicos e administrativos de internações.  
- Sugerir pacientes com **potencial de alta hospitalar**.  
- Exibir **prioridade e justificativa** de cada sugestão.  
- Indicar **pendências** que impedem a alta.  
- Garantir **revisão humana obrigatória** antes de qualquer decisão.

O agente **não substituirá decisões médicas ou auditoriais** e **não fará prescrições**.

---

## 4. Etapas e Definições Pendentes
As especificações técnicas e operacionais serão definidas em conjunto com o time de desenvolvimento e produto.  
Itens que exigem definição posterior:
- **Formato e frequência de geração das recomendações** (ex.: diário, sob demanda).  
- **Integrações** com prontuário e sistemas de auditoria.  
- **Estrutura de dados** e campos necessários.  
- **Critérios de priorização e regras clínicas** (a serem validados pela equipe assistencial).  
- **Padrão de exibição** no frontend e pontos de interação com o usuário.  
- **Processo de validação humana** e registro de decisões.  
- **Indicadores de desempenho** (aceitação, tempo de internação, readmissão).  
- **Regras de segurança e LGPD** específicas para o agente.

---

## 5. Requisitos Essenciais de Projeto
- **Explicabilidade:** toda recomendação deve citar suas fontes.  
- **Revisão humana obrigatória:** nenhuma alta automática.  
- **Rastreabilidade:** cada recomendação e decisão devem ser auditáveis.  
- **Privacidade:** nenhuma informação pessoal sensível deve ser exibida nas saídas.  
- **Modularidade:** o agente deve ser um componente separado, integrável ao sistema principal.  
- **Monitoramento:** métricas básicas de desempenho e confiabilidade devem ser acompanhadas.  

---

## 6. Responsabilidades
- **Time de Auditoria:** definir critérios clínicos e operacionais para as recomendações.  
- **Time de Desenvolvimento:** estruturar ingestão de dados, lógica do agente e integrações.  
- **Gestão do Projeto:** garantir alinhamento entre objetivo assistencial e entrega técnica.  