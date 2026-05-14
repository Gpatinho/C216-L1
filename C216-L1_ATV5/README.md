# 🎓 Sistema de Alunos - API REST com PostgreSQL

API REST para gerenciamento de alunos, desenvolvida com FastAPI e PostgreSQL, containerizada com Docker Compose.

---

## 📋 Funcionalidades

- ✅ Cadastrar aluno com geração automática de ID (ex: GEC1, GES2)
- ✅ Listar todos os alunos
- ✅ Buscar aluno por ID
- ✅ Atualizar dados de um aluno
- ✅ Deletar aluno por ID
- ✅ Resetar lista de alunos
- ✅ Persistência de dados com PostgreSQL

---

## 🛠️ Tecnologias

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL 15
- Docker & Docker Compose

---

## 🚀 Como executar

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando

### 1. Clone o repositório

```bash
git clone https://github.com/Gpatinho/C216-L1.git
cd C216-L1/C216-L1_ATV5
```

### 2. Suba os containers

```bash
docker-compose up --build
```

Aguarde aparecer:
```
INFO: Uvicorn running on http://0.0.0.0:8000
```

### 3. Acesse a documentação

```
http://localhost:8000/docs
```

---

## 📖 Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/alunos/` | Cadastra um novo aluno |
| GET | `/api/v1/alunos/` | Lista todos os alunos |
| GET | `/api/v1/alunos/{aluno_id}` | Busca aluno por ID |
| PATCH | `/api/v1/alunos/{aluno_id}` | Atualiza dados do aluno |
| DELETE | `/api/v1/alunos/{aluno_id}` | Remove um aluno |
| DELETE | `/api/v1/alunos/` | Reseta a lista de alunos |

### Exemplo de cadastro

```json
POST /api/v1/alunos/
{
  "nome": "Guilherme",
  "email": "guilherme@gec.inatel.br",
  "curso": "GEC"
}
```

Resposta:
```json
{
  "mensagem": "Aluno cadastrado com sucesso!",
  "aluno": {
    "id": "GEC1",
    "nome": "Guilherme",
    "email": "guilherme@gec.inatel.br",
    "curso": "GEC",
    "matricula": 1
  }
}
```

---

## 🧪 Testes automatizados

Com a API rodando, abra um novo terminal e execute:

```bash
pytest test_main.py -v
```

Os testes cobrem:
- Adição de 3 alunos por curso (GEC e GES)
- Listagem de alunos
- Busca por ID
- Atualização de dados
- Validação de persistência
- Remoção de alunos
- Reset da lista

---

## 🐳 Estrutura Docker

```yaml
services:
  db:       # PostgreSQL 15
  api:      # FastAPI + Uvicorn
```

Os dados são persistidos em um volume Docker (`pgdata`), ou seja, não são perdidos ao reiniciar os containers.

---

## 👤 Autor

**Guilherme Patinho**  
[github.com/Gpatinho](https://github.com/Gpatinho)