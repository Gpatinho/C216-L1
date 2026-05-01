from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Sistema de Alunos", version="1.0.0")

# Banco de dados em memória
alunos = []
contador_cursos = {}

# Modelo de entrada para criar aluno
class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: str

# Modelo de entrada para atualização parcial (PATCH)
class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None

# Função para gerar matrícula automática
def gerar_matricula(curso: str) -> str:
    curso = curso.upper()
    if curso not in contador_cursos:
        contador_cursos[curso] = 1
    else:
        contador_cursos[curso] += 1
    return f"{curso}{contador_cursos[curso]}"

# ─────────────────────────────────────────
# GET - Lista todos os alunos
# ─────────────────────────────────────────
@app.get("/alunos")
def listar_alunos():
    return {"alunos": alunos}

# ─────────────────────────────────────────
# POST - Cadastra um novo aluno
# ─────────────────────────────────────────
@app.post("/alunos", status_code=201)
def criar_aluno(aluno: AlunoCreate):
    matricula = gerar_matricula(aluno.curso)
    novo_aluno = {
        "nome": aluno.nome,
        "email": aluno.email,
        "curso": aluno.curso.upper(),
        "matricula": matricula
    }
    alunos.append(novo_aluno)
    return {"mensagem": "Aluno cadastrado com sucesso!", "aluno": novo_aluno}

# ─────────────────────────────────────────
# PUT - Atualiza todos os dados do aluno
# ─────────────────────────────────────────
@app.put("/alunos/{matricula}")
def atualizar_aluno(matricula: str, dados: AlunoCreate):
    for aluno in alunos:
        if aluno["matricula"] == matricula:
            aluno["nome"] = dados.nome
            aluno["email"] = dados.email
            aluno["curso"] = dados.curso.upper()
            return {"mensagem": "Aluno atualizado com sucesso!", "aluno": aluno}
    raise HTTPException(status_code=404, detail="Aluno não encontrado.")

# ─────────────────────────────────────────
# PATCH - Atualiza parcialmente o aluno
# ─────────────────────────────────────────
@app.patch("/alunos/{matricula}")
def atualizar_parcial(matricula: str, dados: AlunoUpdate):
    for aluno in alunos:
        if aluno["matricula"] == matricula:
            if dados.nome is not None:
                aluno["nome"] = dados.nome
            if dados.email is not None:
                aluno["email"] = dados.email
            return {"mensagem": "Aluno atualizado parcialmente!", "aluno": aluno}
    raise HTTPException(status_code=404, detail="Aluno não encontrado.")

# ─────────────────────────────────────────
# DELETE - Remove um aluno
# ─────────────────────────────────────────
@app.delete("/alunos/{matricula}")
def deletar_aluno(matricula: str):
    for aluno in alunos:
        if aluno["matricula"] == matricula:
            alunos.remove(aluno)
            return {"mensagem": f"Aluno {matricula} removido com sucesso!"}
    raise HTTPException(status_code=404, detail="Aluno não encontrado.")