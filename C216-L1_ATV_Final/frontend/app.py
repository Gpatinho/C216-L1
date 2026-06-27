from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API = "http://backend:8000"

@app.route("/")
def home():
    salas = requests.get(f"{API}/salas").json()
    reservas = requests.get(f"{API}/reservas").json()
    return render_template("home.html", salas=salas, reservas=reservas)

# ── SALAS ────────────────────────────────────────────
@app.route("/salas")
def salas():
    salas = requests.get(f"{API}/salas").json()
    recursos = requests.get(f"{API}/recursos").json()
    return render_template("salas.html", salas=salas, recursos=recursos)

@app.route("/salas/criar", methods=["POST"])
def criar_sala():
    requests.post(f"{API}/salas", json={
        "nome": request.form["nome"],
        "capacidade": int(request.form["capacidade"]),
        "localizacao": request.form["localizacao"]
    })
    return redirect(url_for("salas"))

@app.route("/salas/deletar/<int:sala_id>")
def deletar_sala(sala_id):
    requests.delete(f"{API}/salas/{sala_id}")
    return redirect(url_for("salas"))

@app.route("/salas/editar/<int:sala_id>", methods=["POST"])
def editar_sala(sala_id):
    requests.put(f"{API}/salas/{sala_id}", json={
        "nome": request.form["nome"],
        "capacidade": int(request.form["capacidade"]),
        "localizacao": request.form["localizacao"]
    })
    return redirect(url_for("salas"))

@app.route("/salas/<int:sala_id>/recurso/<int:recurso_id>")
def adicionar_recurso(sala_id, recurso_id):
    requests.post(f"{API}/salas/{sala_id}/recursos/{recurso_id}")
    return redirect(url_for("salas"))

# ── RESERVAS ─────────────────────────────────────────
@app.route("/reservas")
def reservas():
    reservas = requests.get(f"{API}/reservas").json()
    salas = requests.get(f"{API}/salas").json()
    usuarios = requests.get(f"{API}/usuarios").json()
    return render_template("reservas.html", reservas=reservas, salas=salas, usuarios=usuarios)

@app.route("/reservas/criar", methods=["POST"])
def criar_reserva():
    requests.post(f"{API}/reservas", json={
        "sala_id": int(request.form["sala_id"]),
        "usuario_id": int(request.form["usuario_id"]),
        "data": request.form["data"],
        "hora_inicio": request.form["hora_inicio"],
        "hora_fim": request.form["hora_fim"]
    })
    return redirect(url_for("reservas"))

@app.route("/reservas/cancelar/<int:reserva_id>")
def cancelar_reserva(reserva_id):
    requests.delete(f"{API}/reservas/{reserva_id}")
    return redirect(url_for("reservas"))

@app.route("/reservas/editar/<int:reserva_id>", methods=["POST"])
def editar_reserva(reserva_id):
    requests.put(f"{API}/reservas/{reserva_id}", json={
        "data": request.form["data"],
        "hora_inicio": request.form["hora_inicio"],
        "hora_fim": request.form["hora_fim"]
    })
    return redirect(url_for("reservas"))

# ── USUÁRIOS ─────────────────────────────────────────
@app.route("/usuarios")
def usuarios():
    usuarios = requests.get(f"{API}/usuarios").json()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/usuarios/criar", methods=["POST"])
def criar_usuario():
    requests.post(f"{API}/usuarios", json={
        "nome": request.form["nome"],
        "email": request.form["email"]
    })
    return redirect(url_for("usuarios"))

@app.route("/usuarios/deletar/<int:usuario_id>")
def deletar_usuario(usuario_id):
    requests.delete(f"{API}/usuarios/{usuario_id}")
    return redirect(url_for("usuarios"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# rota extra para criar recurso via form
@app.route("/recursos/criar", methods=["POST"])
def criar_recurso():
    requests.post(f"{API}/recursos", json={"nome": request.form["nome"]})
    return redirect(url_for("salas"))