# Auditoria Hospitalar

Sistema de auditoria hospitalar desenvolvido em Django.

## Requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes do Python)
- Git

## Instalação e Configuração

### 1. Clonar o repositório

```bash
git clone https://github.com/LeonardoCFilho/ds2025-Suporte-a-realizacao-de-auditoria-hospitalar.git
cd ds2025-Suporte-a-realizacao-de-auditoria-hospitalar/DOC/AuditoriaHospitalar
```

### 2. Criar ambiente virtual

Crie um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv venv
```

### 2. Ativar o ambiente virtual

**No Linux/Mac:**

```bash
source venv/bin/activate
```

**No Windows:**

```bash
venv\Scripts\activate
```

### 3. Instalar dependências

Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

### 4. Configurar o banco de dados

Execute as migrações para criar as tabelas no banco de dados:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Popular o BD (recomendado)

Para popular o BD, com dados pré-definidos rode:

```bash
python manage.py popular_dados 
```

P.s.: `--limpar` pode ser concatenado ao final do comando para esvaziar o BD.

### 5. Executar o servidor de desenvolvimento

Inicie o servidor local:

```bash
python manage.py runserver
```

O sistema estará disponível em: `http://127.0.0.1:8000/`

## Estrutura do Projeto

```
AuditoriaHospitalar/
├── AuditoriaHospitalar/    # Configurações do projeto
├── db.sqlite3              # Banco de dados SQLite
├── manage.py               # Script de gerenciamento Django
├── README.md               # Este arquivo
└── requirements.txt        # Dependências do projeto
```
