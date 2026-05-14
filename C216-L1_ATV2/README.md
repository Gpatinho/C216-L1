# 🎓 CRUD de Alunos - Docker

Sistema de gerenciamento de alunos desenvolvido em Python e containerizado com Docker.

---

## 📋 Funcionalidades

- ✅ Cadastrar aluno com geração automática de matrícula
- ✅ Listar todos os alunos cadastrados
- ✅ Atualizar dados de um aluno
- ✅ Deletar aluno por matrícula

---

## 🛠️ Tecnologias

- Python 3.11
- Docker

---

## 🚀 Como executar

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando

### 1. Clone o repositório

```bash
git clone https://github.com/Gpatinho/C216-L1.git
cd C216-L1/C216-L1_ATV2
```

### 2. Construa a imagem Docker

```bash
docker build -t sistema_faculdade .
```

### 3. Execute o container

```bash
docker run -it sistema_faculdade
```

---

## 📖 Como usar

Ao iniciar, o menu será exibido no terminal:

```
1-Criar 2-Listar 3-Atualizar 4-Deletar 5-Sair
Escolha:
```

| Opção | Ação |
|-------|------|
| 1 | Cadastrar novo aluno |
| 2 | Listar todos os alunos |
| 3 | Atualizar dados de um aluno |
| 4 | Deletar um aluno |
| 5 | Encerrar o programa |

### Exemplo de uso

```
Escolha: 1
Nome: Guilherme
Email: guilherme@gec.inatel.br
Curso: GEC
Aluno cadastrado! Matrícula: GEC1
```

---

## 🐳 Verificar containers

```bash
docker ps -a
```

---

## 👤 Autor

**Guilherme Patinho**  
[github.com/Gpatinho](https://github.com/Gpatinho)