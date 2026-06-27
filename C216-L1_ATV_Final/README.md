# 🏢 Sistema de Reservas de Salas

Sistema completo para gerenciamento de reservas de salas, desenvolvido com FastAPI, Flask, PostgreSQL e Docker Compose.

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Backend | FastAPI + Python 3.11 |
| Frontend | Flask + HTML/CSS |
| Banco de dados | PostgreSQL 15 |
| Testes | Pytest + HTTPX |
| Orquestração | Docker Compose |

---

## 🚀 Como executar

### Pré-requisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando

### 1. Clone o repositório
```bash
git clone https://github.com/Gpatinho/C216-L1.git
cd C216-L1/projeto-final
```

### 2. Suba todos os containers
```bash
docker-compose up --build
```

### 3. Acesse o sistema
| Serviço | URL |
|---------|-----|
| Frontend (Flask) | http://localhost:5000 |
| Backend (FastAPI Docs) | http://localhost:8000/docs |

---

## 📋 Funcionalidades

### Salas
- Cadastrar, editar e deletar salas
- Adicionar recursos às salas (projetor, ar-condicionado, etc.)

### Reservas
- Criar reservas com data e horário
- Editar reservas ativas
- Cancelar reservas

### Usuários
- Cadastrar e deletar usuários

---

## 🗄️ Banco de Dados

```
salas          → id, nome, capacidade, localizacao
recursos       → id, nome
sala_recursos  → sala_id, recurso_id  (N para M)
usuarios       → id, nome, email
reservas       → id, sala_id, usuario_id, data, hora_inicio, hora_fim, status  (N para 1)
```

### Relações
- **N para M**: Uma sala pode ter vários recursos, e um recurso pode estar em várias salas
- **N para 1**: Uma reserva pertence a uma sala e a um usuário

---

## 🔗 Endpoints do Backend

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/salas` | Lista todas as salas |
| GET | `/salas/{id}` | Busca sala por ID |
| POST | `/salas` | Cria nova sala |
| PUT | `/salas/{id}` | Atualiza sala |
| DELETE | `/salas/{id}` | Deleta sala |
| GET | `/reservas` | Lista todas as reservas |
| GET | `/reservas/{id}` | Busca reserva por ID |
| POST | `/reservas` | Cria nova reserva |
| PUT | `/reservas/{id}` | Atualiza reserva |
| DELETE | `/reservas/{id}` | Cancela reserva |
| GET | `/usuarios` | Lista usuários |
| POST | `/usuarios` | Cria usuário |
| DELETE | `/usuarios/{id}` | Deleta usuário |
| GET | `/recursos` | Lista recursos |
| POST | `/recursos` | Cria recurso |
| POST | `/salas/{id}/recursos/{id}` | Adiciona recurso à sala |

---

## 🐳 Estrutura Docker

```
docker-compose up --build   # sobe todos os serviços
docker-compose down         # para os serviços
docker-compose logs -f      # visualiza logs
```

---

## 👤 Autor

**Guilherme Felipe Ribeiro**  
Matrícula: 2042  
[github.com/Gpatinho](https://github.com/Gpatinho)