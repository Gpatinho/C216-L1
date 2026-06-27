import httpx
import pytest
import time

BASE_URL = "http://localhost:8000"

sala_id = None
usuario_id = None
reserva_id = None
recurso_id = None

# Email único a cada execução
EMAIL = f"teste.{int(time.time())}@inatel.br"

# ─────────────────────────────────────────
# RECURSOS
# ─────────────────────────────────────────
def test_criar_recurso():
    global recurso_id
    r = httpx.post(f"{BASE_URL}/recursos", json={"nome": "Projetor"})
    assert r.status_code == 201
    recurso_id = r.json()["recurso"]["id"]

def test_listar_recursos():
    r = httpx.get(f"{BASE_URL}/recursos")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

# ─────────────────────────────────────────
# SALAS
# ─────────────────────────────────────────
def test_criar_sala():
    global sala_id
    r = httpx.post(f"{BASE_URL}/salas", json={
        "nome": "Sala Teste",
        "capacidade": 10,
        "localizacao": "Bloco A, 1º andar"
    })
    assert r.status_code == 201
    sala_id = r.json()["sala"]["id"]

def test_listar_salas():
    r = httpx.get(f"{BASE_URL}/salas")
    assert r.status_code == 200
    assert len(r.json()) >= 1

def test_buscar_sala():
    r = httpx.get(f"{BASE_URL}/salas/{sala_id}")
    assert r.status_code == 200
    assert r.json()["id"] == sala_id

def test_buscar_sala_inexistente():
    r = httpx.get(f"{BASE_URL}/salas/99999")
    assert r.status_code == 404

def test_atualizar_sala():
    r = httpx.put(f"{BASE_URL}/salas/{sala_id}", json={
        "nome": "Sala Teste Atualizada",
        "capacidade": 20,
        "localizacao": "Bloco B, 2º andar"
    })
    assert r.status_code == 200
    assert r.json()["sala"]["nome"] == "Sala Teste Atualizada"

def test_adicionar_recurso_sala():
    r = httpx.post(f"{BASE_URL}/salas/{sala_id}/recursos/{recurso_id}")
    assert r.status_code == 200

# ─────────────────────────────────────────
# USUÁRIOS
# ─────────────────────────────────────────
def test_criar_usuario():
    global usuario_id
    r = httpx.post(f"{BASE_URL}/usuarios", json={
        "nome": "Guilherme Teste",
        "email": EMAIL
    })
    assert r.status_code == 201
    usuario_id = r.json()["usuario"]["id"]

def test_listar_usuarios():
    r = httpx.get(f"{BASE_URL}/usuarios")
    assert r.status_code == 200
    assert len(r.json()) >= 1

# ─────────────────────────────────────────
# RESERVAS
# ─────────────────────────────────────────
def test_criar_reserva():
    global reserva_id
    assert usuario_id is not None, "usuario_id não foi criado"
    r = httpx.post(f"{BASE_URL}/reservas", json={
        "sala_id": sala_id,
        "usuario_id": usuario_id,
        "data": "2026-12-01",
        "hora_inicio": "09:00",
        "hora_fim": "11:00"
    })
    assert r.status_code == 201
    reserva_id = r.json()["reserva"]["id"]

def test_listar_reservas():
    r = httpx.get(f"{BASE_URL}/reservas")
    assert r.status_code == 200
    assert len(r.json()) >= 1

def test_buscar_reserva():
    assert reserva_id is not None, "reserva_id não foi criado"
    r = httpx.get(f"{BASE_URL}/reservas/{reserva_id}")
    assert r.status_code == 200
    assert r.json()["id"] == reserva_id

def test_buscar_reserva_inexistente():
    r = httpx.get(f"{BASE_URL}/reservas/99999")
    assert r.status_code == 404

def test_atualizar_reserva():
    assert reserva_id is not None
    r = httpx.put(f"{BASE_URL}/reservas/{reserva_id}", json={
        "data": "2026-12-15",
        "hora_inicio": "14:00",
        "hora_fim": "16:00"
    })
    assert r.status_code == 200

def test_cancelar_reserva():
    assert reserva_id is not None
    r = httpx.delete(f"{BASE_URL}/reservas/{reserva_id}")
    assert r.status_code == 200

# ─────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────
def test_deletar_usuario():
    assert usuario_id is not None
    r = httpx.delete(f"{BASE_URL}/usuarios/{usuario_id}")
    assert r.status_code == 200

def test_deletar_sala():
    assert sala_id is not None
    r = httpx.delete(f"{BASE_URL}/salas/{sala_id}")
    assert r.status_code == 200

def test_deletar_sala_inexistente():
    r = httpx.delete(f"{BASE_URL}/salas/99999")
    assert r.status_code == 404