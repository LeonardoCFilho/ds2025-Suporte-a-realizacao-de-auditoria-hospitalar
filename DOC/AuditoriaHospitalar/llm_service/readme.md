# 🏥 Sistema de Análise de Altas Hospitalares

## 📋 Sobre o Projeto
Para entender as saidas do sistema

## 🔧 Como Funciona

### Base de Dados
- 1.000 pacientes simulados
- 1.500 internações
- 10 doenças diferentes

### Componentes
- **Memória do Sistema**: Protocolos médicos e regras
- **IA Gemini**: Análise inteligente dos casos
- **Orquestração**: Coordenação do processo

## 📊 Resultados da Análise

Cada paciente recebe:

| Campo | Significado |
|-------|-------------|
| **Prioridade** | ALTA (urgente) / MÉDIA / BAIXA / MANTER |
| **Razões para Alta** | Porque considerar a alta |
| **Pendências** | O que falta para alta |
| **Confiança** | 0-100% de certeza |

## 🎯 Interpretação

- **ALTA**: "Avaliação URGENTE para alta"
- **MÉDIA**: "Pode considerar alta"  
- **BAIXA**: "Talvez pensar em alta"
- **MANTER**: "Continuar internado"

### Passos Rápidos
1. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
 - **Criar arquivo** .env: GEMINI_API_KEY=sua_chave_aqui.
 - **Executar sistema**: python executar_batch.py
 - **Execução rápida**: python execucao_teste.py
 - **Reindexar base de conhecimento**: python reindexar_rag.py
   
