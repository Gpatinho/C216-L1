import os
import time
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/alunos")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AlunoModel(Base):
    __tablename__ = "alunos"

    id = Column(String, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    curso = Column(String, nullable=False)
    matricula = Column(Integer, nullable=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def criar_tabelas():
    retries = 10
    for i in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("Tabelas criadas com sucesso!")
            return
        except Exception as e:
            print(f"Aguardando banco de dados... tentativa {i+1}/{retries}")
            time.sleep(3)
    raise Exception("Não foi possível conectar ao banco de dados.")