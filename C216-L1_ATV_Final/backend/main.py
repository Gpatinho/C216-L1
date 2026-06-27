from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from database import Sala, Recurso, Usuario, Reserva, get_db, criar_tabelas

app = FastAPI(title="Sistema de Reservas de Salas", version="1.0.0")

@app.on_event("startup")
def startup():
    criar_tabelas()

# ── Schemas ──────────────────────────────────────────
class SalaCreate(BaseModel):
    nome: str
    capacidade: int
    localizacao: str

class SalaUpdate(BaseModel):
    nome: Optional[str] = None
    capacidade: Optional[int] = None
    localizacao: Optional[str] = None

class RecursoCreate(BaseModel):
    nome: str

class UsuarioCreate(BaseModel):
    nome: str
    email: str

class ReservaCreate(BaseModel):
    sala_id: int
    usuario_id: int
    data: str
    hora_inicio: str
    hora_fim: str

class ReservaUpdate(BaseModel):
    data: Optional[str] = None
    hora_inicio: Optional[str] = None
    hora_fim: Optional[str] = None
    status: Optional[str] = None

# ── SALAS ────────────────────────────────────────────
@app.get("/salas")
def listar_salas(db: Session = Depends(get_db)):
    salas = db.query(Sala).all()
    return [{"id": s.id, "nome": s.nome, "capacidade": s.capacidade, "localizacao": s.localizacao,
             "recursos": [r.nome for r in s.recursos]} for s in salas]

@app.get("/salas/{sala_id}")
def buscar_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada.")
    return {"id": sala.id, "nome": sala.nome, "capacidade": sala.capacidade,
            "localizacao": sala.localizacao, "recursos": [r.nome for r in sala.recursos]}

@app.post("/salas", status_code=201)
def criar_sala(sala: SalaCreate, db: Session = Depends(get_db)):
    nova = Sala(nome=sala.nome, capacidade=sala.capacidade, localizacao=sala.localizacao)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return {"mensagem": "Sala criada!", "sala": {"id": nova.id, "nome": nova.nome}}

@app.put("/salas/{sala_id}")
def atualizar_sala(sala_id: int, dados: SalaUpdate, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada.")
    if dados.nome: sala.nome = dados.nome
    if dados.capacidade: sala.capacidade = dados.capacidade
    if dados.localizacao: sala.localizacao = dados.localizacao
    db.commit()
    db.refresh(sala)
    return {"mensagem": "Sala atualizada!", "sala": {"id": sala.id, "nome": sala.nome}}

@app.delete("/salas/{sala_id}")
def deletar_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada.")
    db.query(Reserva).filter(Reserva.sala_id == sala_id).delete()
    sala.recursos.clear()
    db.delete(sala)
    db.commit()
    return {"mensagem": f"Sala {sala_id} removida!"}

# ── RECURSOS ─────────────────────────────────────────
@app.get("/recursos")
def listar_recursos(db: Session = Depends(get_db)):
    recursos = db.query(Recurso).all()
    return [{"id": r.id, "nome": r.nome} for r in recursos]

@app.post("/recursos", status_code=201)
def criar_recurso(recurso: RecursoCreate, db: Session = Depends(get_db)):
    novo = Recurso(nome=recurso.nome)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"mensagem": "Recurso criado!", "recurso": {"id": novo.id, "nome": novo.nome}}

@app.post("/salas/{sala_id}/recursos/{recurso_id}")
def adicionar_recurso_sala(sala_id: int, recurso_id: int, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.id == sala_id).first()
    recurso = db.query(Recurso).filter(Recurso.id == recurso_id).first()
    if not sala or not recurso:
        raise HTTPException(status_code=404, detail="Sala ou recurso não encontrado.")
    sala.recursos.append(recurso)
    db.commit()
    return {"mensagem": f"Recurso '{recurso.nome}' adicionado à sala '{sala.nome}'!"}

# ── USUÁRIOS ─────────────────────────────────────────
@app.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return [{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios]

@app.post("/usuarios", status_code=201)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    novo = Usuario(nome=usuario.nome, email=usuario.email)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"mensagem": "Usuário criado!", "usuario": {"id": novo.id, "nome": novo.nome}}

@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    db.query(Reserva).filter(Reserva.usuario_id == usuario_id).delete()
    db.delete(usuario)
    db.commit()
    return {"mensagem": f"Usuário {usuario_id} removido!"}

# ── RESERVAS ─────────────────────────────────────────
@app.get("/reservas")
def listar_reservas(db: Session = Depends(get_db)):
    reservas = db.query(Reserva).all()
    return [{"id": r.id, "sala": r.sala.nome, "usuario": r.usuario.nome,
             "data": r.data, "hora_inicio": r.hora_inicio, "hora_fim": r.hora_fim,
             "status": r.status} for r in reservas]

@app.get("/reservas/{reserva_id}")
def buscar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    r = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")
    return {"id": r.id, "sala": r.sala.nome, "usuario": r.usuario.nome,
            "data": r.data, "hora_inicio": r.hora_inicio, "hora_fim": r.hora_fim, "status": r.status}

@app.post("/reservas", status_code=201)
def criar_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    nova = Reserva(sala_id=reserva.sala_id, usuario_id=reserva.usuario_id,
                   data=reserva.data, hora_inicio=reserva.hora_inicio, hora_fim=reserva.hora_fim)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return {"mensagem": "Reserva criada!", "reserva": {"id": nova.id, "status": nova.status}}

@app.put("/reservas/{reserva_id}")
def atualizar_reserva(reserva_id: int, dados: ReservaUpdate, db: Session = Depends(get_db)):
    r = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")
    if dados.data: r.data = dados.data
    if dados.hora_inicio: r.hora_inicio = dados.hora_inicio
    if dados.hora_fim: r.hora_fim = dados.hora_fim
    if dados.status: r.status = dados.status
    db.commit()
    db.refresh(r)
    return {"mensagem": "Reserva atualizada!", "reserva": {"id": r.id, "status": r.status}}

@app.delete("/reservas/{reserva_id}")
def cancelar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    r = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")
    r.status = "cancelada"
    db.commit()
    return {"mensagem": f"Reserva {reserva_id} cancelada!"}