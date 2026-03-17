# Sistema de Agendamento - Salão da Leila

Este projeto é uma API para gerenciamento de agendamentos de um salão de beleza, permitindo cadastrar clientes, serviços e realizar agendamentos com validações de regras de negócio.

O sistema também possui um frontend simples para interação com a API.

---

# Tecnologias Utilizadas

Backend
- Python 3.8+
- Flask 2.0+
- SQLAlchemy 2.0+ 
- SQLite 3.x

Frontend
- HTML5
- CSS3
- JavaScript

---

# Funcionalidades

Clientes
- Criar cliente
- Listar clientes

Serviços
- Listar serviços disponíveis
- Criar serviços
- Atualizar serviços
- Deletar serviços

Agendamentos
- Criar agendamento
- Listar agendamentos
- Atualizar agendamento
- Excluir agendamento

Relatórios
- Desempenho semanal do salão

---

# Regras de Negócio

- Um cliente não pode possuir dois agendamentos na mesma semana.
- Alterações de data só podem ser feitas até **2 dias antes do agendamento** (exceto para administrador).

---

# Como Rodar o Projeto

## 1 - Clonar o repositório

```bash
git clone https://github.com/renzoyuta/salao-api-dsin.git
```

## 2 - Entrar na pasta do backend
```bash
cd backend
```

## 3 - Criar e ativar o ambiente virtual
```bash
python -m venv venv
.venv\Scripts\activate
```

## 4 - Instalar dependências
```
pip install -r requirements.txt
```

## 5 - Rodar o servidor
```
python main.py
```

## 6 - Abrir o frontend
```
Localizado em: ./cabeleleira_leira/frontend/index.html
```

---

# Estrutura do banco de dados

```sql
-- Tabela de Clientes
clientes {
  id INTEGER PRIMARY KEY
  nome TEXT UNIQUE
  telefone TEXT
}

-- Tabela de Serviços
servicos {
  id INTEGER PRIMARY KEY
  nome TEXT UNIQUE
  preco FLOAT
}

-- Tabela de Agendamentos
agendamentos {
  id INTEGER PRIMARY KEY
  cliente_id INTEGER (FK → clientes.id)
  data DATE
  status TEXT
  valor FLOAT
}

-- Tabela de Relacionamento (N:N)
agendamento_servicos {
  agendamento_id INTEGER (FK → agendamentos.id)
  servico_id INTEGER (FK → servicos.id)
}
```

# Endpoints da API

## Clientes
```
GET	/clientes   Lista todos os clientes
POST /clientes  Cria um novo cliente
```

## Serviços
```
GET	/servicos   Lista todos os serviços
POST /servicos  Cria um serviço
PUT /servicos/<id>  Atualiza um serviço
DELETE /servicos/<id> Deleta um serviço
```

## Agendamentos
```

GET	/agendamentos	Lista todos os agendamentos
POST /agendamentos	Cria um novo agendamento
PUT	/agendamentos/<id>	Edita um agendamento
PUT	/agendamentos/<id>/status	Altera o status
GET	/agendamentos/historico     Busca por período
GET	/agendamentos/relatorio-semanal	    Relatório de desempenho
```

---

# Vídeo de demonstração

Devido ao limite do Github (100MB), o vídeo de demonstração está hospedado no Youtube:

Link: https://youtu.be/iD34xsTRgj8

Duração 3:39

---

# Licença

Este projeto foi desenvolvido para fins de avaliação técnica

# Agradecimento

Agradecimento à equipe de recrutamento da DSIN pela oportunidade