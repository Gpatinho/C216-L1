import httpx
import pytest

BASE_URL = "http://localhost:8000/api/v1/alunos"

# ─────────────────────────────────────────
# POST - Cadastrar alunos
# ─────────────────────────────────────────
def test_criar_aluno_gec1():
    response = httpx.post(f"{BASE_URL}/", json={"nome": "Guilherme", "email": "guilherme@gec.inatel.br", "curso": "GEC"})
    assert response.status_code == 201
    assert response.json()["aluno"]["id"] == "GEC1"

def test_criar_aluno_gec2():
    response = httpx.post(f"{BASE_URL}/", json={"nome": "Carlos", "email": "carlos@gec.inatel.br", "curso": "GEC"})
    assert response.status_code == 201
    assert response.json()["aluno"]["id"] == "GEC2"

def test_criar_aluno_gec3():
    response = httpx.post(f"{BASE_URL}/", json={"nome": "Ana", "email": "ana@gec.inatel.br", "curso": "GEC"})
    assert response.status_code == 201
    assert response.json()["aluno"]["id"] == "GEC3"

def test_criar_aluno_ges1():
    response = httpx.post(f"{BASE_URL}/", json={"nome": "Elisa", "email": "elisa@ges.inatel.br", "curso": "GES"})
    assert response.status_code == 201
    assert response.json()["aluno"]["id"] == "GES1"

def test_criar_aluno_ges2():
    response = httpx.post(f"{BASE_URL}/", json={"nome": "Pedro", "email": "pedro@ges.inatel.br", "curso": "GES"})
    assert response.status_code == 201
    assert response.json()["aluno"]["id"] == "GES2"

def test_criar_aluno_ges3():
    response = httpx.post(f"{BASE_URL}/", json={"nome": "Julia", "email": "julia@ges.inatel.br", "curso": "GES"})
    assert response.status_code == 201
    assert response.json()["aluno"]["id"] == "GES3"

# ─────────────────────────────────────────
# GET - Listar todos os alunos
# ─────────────────────────────────────────
def test_listar_alunos():
    response = httpx.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert len(response.json()["alunos"]) >= 6

# ─────────────────────────────────────────
# GET - Buscar aluno por ID
# ─────────────────────────────────────────
def test_buscar_aluno_existente():
    response = httpx.get(f"{BASE_URL}/GEC1")
    assert response.status_code == 200
    assert response.json()["id"] == "GEC1"

def test_buscar_aluno_inexistente():
    response = httpx.get(f"{BASE_URL}/XXX99")
    assert response.status_code == 404

# ─────────────────────────────────────────
# PATCH - Atualizar dados de um aluno
# ─────────────────────────────────────────
def test_atualizar_aluno():
    response = httpx.patch(f"{BASE_URL}/GEC1", json={"nome": "Guilherme Patinho", "email": "novo@gec.inatel.br"})
    assert response.status_code == 200
    assert response.json()["aluno"]["nome"] == "Guilherme Patinho"

def test_atualizar_aluno_inexistente():
    response = httpx.patch(f"{BASE_URL}/XXX99", json={"nome": "Ninguem"})
    assert response.status_code == 404

# ─────────────────────────────────────────
# DELETE - Remover aluno por ID
# ─────────────────────────────────────────
def test_deletar_aluno():
    response = httpx.delete(f"{BASE_URL}/GES3")
    assert response.status_code == 200

def test_deletar_aluno_inexistente():
    response = httpx.delete(f"{BASE_URL}/XXX99")
    assert response.status_code == 404

# ─────────────────────────────────────────
# DELETE - Resetar lista de alunos
# ─────────────────────────────────────────
def test_resetar_alunos():
    response = httpx.delete(f"{BASE_URL}/")
    assert response.status_code == 200

def test_listar_apos_reset():
    response = httpx.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json()["alunos"] == []