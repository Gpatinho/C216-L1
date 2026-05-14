from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import AlunoModel, get_db, criar_tabelas

app = FastAPI(title="Sistema de Alunos", version="2.0.0")

@app.on_event("startup")
def startup():
    criar_tabelas()

# Modelos
class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: str

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None

# Função para gerar ID único por curso
def gerar_id(curso: str, db: Session) -> str:
    curso = curso.upper()
    count = db.query(AlunoModel).filter(AlunoModel.curso == curso).count()
    matricula = count + 1
    aluno_id = f"{curso}{matricula}"
    # Garante que o ID não seja reutilizado
    while db.query(AlunoModel).filter(AlunoModel.id == aluno_id).first():
        matricula += 1
        aluno_id = f"{curso}{matricula}"
    return aluno_id, matricula

# ─────────────────────────────────────────
# POST - Cadastra um novo aluno
# ─────────────────────────────────────────
@app.post("/api/v1/alunos/", status_code=201)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    aluno_id, matricula = gerar_id(aluno.curso, db)
    novo_aluno = AlunoModel(
        id=aluno_id,
        nome=aluno.nome,
        email=aluno.email,
        curso=aluno.curso.upper(),
        matricula=matricula
    )
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return {"mensagem": "Aluno cadastrado com sucesso!", "aluno": {
        "id": novo_aluno.id,
        "nome": novo_aluno.nome,
        "email": novo_aluno.email,
        "curso": novo_aluno.curso,
        "matricula": novo_aluno.matricula
    }}

# ─────────────────────────────────────────
# GET - Lista todos os alunos
# ─────────────────────────────────────────
@app.get("/api/v1/alunos/")
def listar_alunos(db: Session = Depends(get_db)):
    alunos = db.query(AlunoModel).all()
    return {"alunos": [{"id": a.id, "nome": a.nome, "email": a.email, "curso": a.curso, "matricula": a.matricula} for a in alunos]}

# ─────────────────────────────────────────
# GET - Busca aluno pelo ID
# ─────────────────────────────────────────
@app.get("/api/v1/alunos/{aluno_id}")
def buscar_aluno(aluno_id: str, db: Session = Depends(get_db)):
    aluno = db.query(AlunoModel).filter(AlunoModel.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    return {"id": aluno.id, "nome": aluno.nome, "email": aluno.email, "curso": aluno.curso, "matricula": aluno.matricula}

# ─────────────────────────────────────────
# PATCH - Atualiza parcialmente um aluno
# ─────────────────────────────────────────
@app.patch("/api/v1/alunos/{aluno_id}")
def atualizar_aluno(aluno_id: str, dados: AlunoUpdate, db: Session = Depends(get_db)):
    aluno = db.query(AlunoModel).filter(AlunoModel.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    if dados.nome:
        aluno.nome = dados.nome
    if dados.email:
        aluno.email = dados.email
    db.commit()
    db.refresh(aluno)
    return {"mensagem": "Aluno atualizado!", "aluno": {"id": aluno.id, "nome": aluno.nome, "email": aluno.email, "curso": aluno.curso}}

# ─────────────────────────────────────────
# DELETE - Remove um aluno pelo ID
# ─────────────────────────────────────────
@app.delete("/api/v1/alunos/{aluno_id}")
def deletar_aluno(aluno_id: str, db: Session = Depends(get_db)):
    aluno = db.query(AlunoModel).filter(AlunoModel.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    db.delete(aluno)
    db.commit()
    return {"mensagem": f"Aluno {aluno_id} removido com sucesso!"}

# ─────────────────────────────────────────
# DELETE - Reseta a lista de alunos
# ─────────────────────────────────────────
@app.delete("/api/v1/alunos/")
def resetar_alunos(db: Session = Depends(get_db)):
    db.query(AlunoModel).delete()
    db.commit()
    return {"mensagem": "Lista de alunos resetada com sucesso!"}