from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Sistema de Alunos", version="1.0.0")

# Banco de dados em memória
alunos = []
contador_cursos = {}
ids_usados = set()

# Modelos
class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: str

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None

# Função para gerar ID único por curso (não reutilizável)
def gerar_id(curso: str) -> str:
    curso = curso.upper()
    if curso not in contador_cursos:
        contador_cursos[curso] = 1
    else:
        contador_cursos[curso] += 1
    return f"{curso}{contador_cursos[curso]}"

# ─────────────────────────────────────────
# POST - Cadastra um novo aluno
# ─────────────────────────────────────────
@app.post("/api/v1/alunos/", status_code=201)
def criar_aluno(aluno: AlunoCreate):
    aluno_id = gerar_id(aluno.curso)
    novo_aluno = {
        "id": aluno_id,
        "nome": aluno.nome,
        "email": aluno.email,
        "curso": aluno.curso.upper(),
    }
    alunos.append(novo_aluno)
    ids_usados.add(aluno_id)
    return {"mensagem": "Aluno cadastrado com sucesso!", "aluno": novo_aluno}

# ─────────────────────────────────────────
# GET - Lista todos os alunos
# ─────────────────────────────────────────
@app.get("/api/v1/alunos/")
def listar_alunos():
    return {"alunos": alunos}

# ─────────────────────────────────────────
# GET - Busca aluno pelo ID
# ─────────────────────────────────────────
@app.get("/api/v1/alunos/{aluno_id}")
def buscar_aluno(aluno_id: str):
    for aluno in alunos:
        if aluno["id"] == aluno_id:
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado.")

# ─────────────────────────────────────────
# PATCH - Atualiza parcialmente um aluno
# ─────────────────────────────────────────
@app.patch("/api/v1/alunos/{aluno_id}")
def atualizar_aluno(aluno_id: str, dados: AlunoUpdate):
    for aluno in alunos:
        if aluno["id"] == aluno_id:
            if dados.nome is not None:
                aluno["nome"] = dados.nome
            if dados.email is not None:
                aluno["email"] = dados.email
            return {"mensagem": "Aluno atualizado!", "aluno": aluno}
    raise HTTPException(status_code=404, detail="Aluno não encontrado.")

# ─────────────────────────────────────────
# DELETE - Remove um aluno pelo ID
# ─────────────────────────────────────────
@app.delete("/api/v1/alunos/{aluno_id}")
def deletar_aluno(aluno_id: str):
    for aluno in alunos:
        if aluno["id"] == aluno_id:
            alunos.remove(aluno)
            return {"mensagem": f"Aluno {aluno_id} removido com sucesso!"}
    raise HTTPException(status_code=404, detail="Aluno não encontrado.")

# ─────────────────────────────────────────
# DELETE - Reseta a lista de alunos
# ─────────────────────────────────────────
@app.delete("/api/v1/alunos/")
def resetar_alunos():
    alunos.clear()
    contador_cursos.clear()
    ids_usados.clear()
    return {"mensagem": "Lista de alunos resetada com sucesso!"}