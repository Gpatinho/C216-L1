import httpx
import pytest

BASE_URL = "http://localhost:8000/api/v1/alunos"

# Reseta antes de tudo
def setup_module():
    httpx.delete(f"{BASE_URL}/")

# ─────────────────────────────────────────
# POST - Cadastrar 3 alunos por curso
# ─────────────────────────────────────────
def test_criar_aluno_gec1():
    r = httpx.post(f"{BASE_URL}/", json={"nome": "Guilherme", "email": "guilherme@gec.inatel.br", "curso": "GEC"})
    assert r.status_code == 201
    assert r.json()["aluno"]["id"] == "GEC1"

def test_criar_aluno_gec2():
    r = httpx.post(f"{BASE_URL}/", json={"nome": "Carlos", "email": "carlos@gec.inatel.br", "curso": "GEC"})
    assert r.status_code == 201
    assert r.json()["aluno"]["id"] == "GEC2"

def test_criar_aluno_gec3():
    r = httpx.post(f"{BASE_URL}/", json={"nome": "Ana", "email": "ana@gec.inatel.br", "curso": "GEC"})
    assert r.status_code == 201
    assert r.json()["aluno"]["id"] == "GEC3"

def test_criar_aluno_ges1():
    r = httpx.post(f"{BASE_URL}/", json={"nome": "Elisa", "email": "elisa@ges.inatel.br", "curso": "GES"})
    assert r.status_code == 201
    assert r.json()["aluno"]["id"] == "GES1"

def test_criar_aluno_ges2():
    r = httpx.post(f"{BASE_URL}/", json={"nome": "Pedro", "email": "pedro@ges.inatel.br", "curso": "GES"})
    assert r.status_code == 201
    assert r.json()["aluno"]["id"] == "GES2"

def test_criar_aluno_ges3():
    r = httpx.post(f"{BASE_URL}/", json={"nome": "Julia", "email": "julia@ges.inatel.br", "curso": "GES"})
    assert r.status_code == 201
    assert r.json()["aluno"]["id"] == "GES3"

# ─────────────────────────────────────────
# GET - Listar todos os alunos
# ─────────────────────────────────────────
def test_listar_alunos():
    r = httpx.get(f"{BASE_URL}/")
    assert r.status_code == 200
    assert len(r.json()["alunos"]) >= 6

# ─────────────────────────────────────────
# GET - Buscar por ID
# ─────────────────────────────────────────
def test_buscar_aluno_existente():
    r = httpx.get(f"{BASE_URL}/GEC1")
    assert r.status_code == 200
    assert r.json()["id"] == "GEC1"

def test_buscar_aluno_inexistente():
    r = httpx.get(f"{BASE_URL}/XXX99")
    assert r.status_code == 404

# ─────────────────────────────────────────
# PATCH - Atualizar dados
# ─────────────────────────────────────────
def test_atualizar_aluno():
    r = httpx.patch(f"{BASE_URL}/GEC1", json={"nome": "Guilherme Patinho", "email": "novo@gec.inatel.br"})
    assert r.status_code == 200
    assert r.json()["aluno"]["nome"] == "Guilherme Patinho"

# ─────────────────────────────────────────
# Validar persistência - reinicia e verifica
# ─────────────────────────────────────────
def test_persistencia():
    r = httpx.get(f"{BASE_URL}/GEC1")
    assert r.status_code == 200
    assert r.json()["nome"] == "Guilherme Patinho"

# ─────────────────────────────────────────
# DELETE - Remover aluno
# ─────────────────────────────────────────
def test_deletar_aluno():
    r = httpx.delete(f"{BASE_URL}/GES3")
    assert r.status_code == 200

def test_deletar_inexistente():
    r = httpx.delete(f"{BASE_URL}/XXX99")
    assert r.status_code == 404

# ─────────────────────────────────────────
# DELETE - Resetar lista
# ─────────────────────────────────────────
def test_resetar_alunos():
    r = httpx.delete(f"{BASE_URL}/")
    assert r.status_code == 200

def test_listar_apos_reset():
    r = httpx.get(f"{BASE_URL}/")
    assert r.status_code == 200
    assert r.json()["alunos"] == []