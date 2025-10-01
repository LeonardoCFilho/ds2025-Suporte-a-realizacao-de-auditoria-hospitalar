# Princípios de Design - Sistema de Auditoria Hospitalar

## 1. SOLID Principles

### S - Single Responsibility Principle

**Uma classe/módulo = uma responsabilidade**

- `ServicoAuditoria` → gerencia auditorias
- `ServicoNotificacao` → envia alertas e emails
- `GeradorRelatorio` → cria relatórios
- `CalculadorCustos` → calcula valores

**Benefício:** Mudanças isoladas, fácil manutenção.

### O - Open/Closed Principle

**Aberto para extensão, fechado para modificação**

```
interface Auditoria
    └── AuditoriaConcorrente
    └── AuditoriaRetrospectiva
    └── (futura) AuditoriaPreventiva  // sem modificar código existente
```

**Benefício:** Adicionar novos tipos sem quebrar o existente.

### L - Liskov Substitution Principle

**Subtipos devem ser substituíveis por seus tipos base**

Todo `Auditor` pode ser tratado como `Usuario` sem surpresas.
Todo `Medico` pode ser tratado como `Usuario` sem comportamentos inesperados.

**Benefício:** Polimorfismo confiável.

### I - Interface Segregation Principle

**Interfaces específicas, não genéricas**

```
interface MonitorTempoReal
    └── monitorar_pacientes()
    └── emitir_alertas()

interface AnalisadorContas
    └── analisar_conta()
    └── validar_procedimentos()
```

**Benefício:** Classes implementam apenas o que precisam.

### D - Dependency Inversion Principle

**Dependa de abstrações, não de implementações**

```
ServicoAuditoria depende de → interface RepositorioPacientes
    └── RepositorioPostgreSQL (implementação)
    └── RepositorioMySQL (implementação)
    └── RepositorioMock (testes)
```

**Benefício:** Fácil trocar implementações, testabilidade.

## 2. Princípios Complementares

### DRY - Don't Repeat Yourself

**Não duplique lógica**

- Validações em funções reutilizáveis
- Cálculos de negócio centralizados
- Evitar copiar/colar código

### KISS - Keep It Simple

**Escolha a solução mais simples**

- Evitar over-engineering
- Não adicionar complexidade desnecessária
- Refatorar apenas quando necessário

### Separation of Concerns

**Separar responsabilidades em camadas**

```
Apresentação → Validação de entrada, formatação
Aplicação → Casos de uso, orquestração
Domínio → Regras de negócio
Infraestrutura → Banco de dados, APIs externas
```

## 3. Design Patterns Principais

### Repository Pattern

Abstrair acesso a dados do banco.

<!-- ### Strategy Pattern

Diferentes algoritmos de validação por patologia. -->

### Observer Pattern

Sistema de notificações e alertas (HU02, HU15).

<!-- ### Factory Pattern

Criação de diferentes tipos de relatórios. -->

## 4. Diretrizes Específicas do Projeto

### Regras de Negócio

- Lógica de glosa no domínio, não nos controllers
- Validações de procedimentos centralizadas
- Padrões de patologia em base de conhecimento

### Performance

- Cache para consultas frequentes
- Paginação em listagens grandes
- WebSockets para tempo real (HU01, HU02)

### Conformidade

- LGPD: criptografia de dados sensíveis
- Backup automático regular
- Controle de acesso por permissões

### Testabilidade

- Interfaces para permitir mocks.
- Testes de unidade e integração orientados a regras de negócio.