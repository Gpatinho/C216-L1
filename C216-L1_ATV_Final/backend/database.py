import os
import time
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/reservas")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Tabela N para M: sala_recursos
sala_recursos = Table(
    "sala_recursos",
    Base.metadata,
    Column("sala_id", Integer, ForeignKey("salas.id"), primary_key=True),
    Column("recurso_id", Integer, ForeignKey("recursos.id"), primary_key=True),
)

class Sala(Base):
    __tablename__ = "salas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    capacidade = Column(Integer, nullable=False)
    localizacao = Column(String, nullable=False)
    reservas = relationship("Reserva", back_populates="sala")
    recursos = relationship("Recurso", secondary=sala_recursos, back_populates="salas")

class Recurso(Base):
    __tablename__ = "recursos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    salas = relationship("Sala", secondary=sala_recursos, back_populates="recursos")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    reservas = relationship("Reserva", back_populates="usuario")

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    sala_id = Column(Integer, ForeignKey("salas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    data = Column(String, nullable=False)
    hora_inicio = Column(String, nullable=False)
    hora_fim = Column(String, nullable=False)
    status = Column(String, default="ativa")
    sala = relationship("Sala", back_populates="reservas")
    usuario = relationship("Usuario", back_populates="reservas")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def criar_tabelas():
    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            print("Tabelas criadas com sucesso!")
            return
        except Exception as e:
            print(f"Aguardando banco... tentativa {i+1}/10")
            time.sleep(3)
    raise Exception("Não foi possível conectar ao banco.")