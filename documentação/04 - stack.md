## Frontend
- Framework: React.js ou Vue.js.  
- Nova tela: **Lista de pacientes com potencial de alta** (Prioridade, Razões, Pendências).  
- Ações: **Aceitar**, **Aguardar**, **Rejeitar** e filtro por setor.

## Backend
- Linguagem: Python.  
- Framework: Django ou Flask.  
- Novo serviço: **Agente de Desospitalização (RAG)** para gerar lista priorizada de alta.  
- API: `GET /desospitalizacao` e `POST /desospitalizacao/{id}/decisao`.  
- Job diário (06:30) para atualização da lista.  
- Auditoria e LGPD: registrar recomendações, fontes e decisões humanas.

## Banco de Dados
- Primário: PostgreSQL.  
- Armazena dados clínicos, **trechos de referência** e decisões do auditor.

## Infraestrutura e DevOps
- Cloud: AWS, GCP ou Azure.  
- Conteinerização: Docker e Kubernetes.  
- **Jobs agendados** e **monitoramento** do agente (sucesso, latência, aceitação).  
- **Mascaramento de PII** nas saídas.

## Objetivos
- Desenvolvimento rápido e aberto à IA.  
- **Apoiar auditoria com recomendações explicáveis**.  
- **Alta sempre revisada por humano**.  
- **Reduzir permanência sem aumentar readmissão.**
