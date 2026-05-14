# 🎓 CRUD de Alunos em Python

Programa básico em Python que roda no terminal e permite realizar um CRUD de alunos de uma faculdade.

---

## 📋 Funcionalidades

- ✅ Cadastrar aluno com geração automática de matrícula
- ✅ Listar todos os alunos cadastrados
- ✅ Atualizar dados de um aluno
- ✅ Deletar aluno por matrícula

---

## 🛠️ Tecnologias

- Python 3.11+

---

## 🚀 Como executar

### Pré-requisitos

- [Python](https://www.python.org/downloads/) instalado

### 1. Clone o repositório

```bash
git clone https://github.com/Gpatinho/C216-L1.git
cd C216-L1/C216-L1_ATV1
```

### 2. Execute o programa

```bash
python sistema_faculdade.py
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

Escolha: 2
{'nome': 'Guilherme', 'email': 'guilherme@gec.inatel.br', 'curso': 'GEC', 'matricula': 'GEC1'}
```

A matrícula é gerada automaticamente no formato `CURSO + número sequencial` (ex: `GEC1`, `GES2`).

---

## ⚠️ Observação

Os dados são armazenados em memória. Ao encerrar o programa, as informações são perdidas.

---

## 👤 Autor

**Guilherme Patinho**  
[github.com/Gpatinho](https://github.com/Gpatinho)