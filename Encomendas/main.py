from flask import Flask, render_template, request, redirect

app = Flask(__name__)

encomendas = []
proximo_id = 1

# Stock simulado (mais tarde vem do microserviço de catálogo)
stock = {
    "Nike Pegasus": {40: 5, 41: 3, 42: 10},
    "Adidas Samba": {40: 0, 42: 2},
}

@app.get("/")
def pagina_inicial():
    return render_template("index.html", encomendas=encomendas)

@app.get("/encomendas")
def listar_encomendas():
    return encomendas

@app.get("/encomendas/<int:id>")
def ver_encomenda(id):
    for e in encomendas:
        if e["id"] == id:
            return e
    return {"erro": "Encomenda não encontrada"}, 404

@app.post("/encomendas")
def criar_encomenda():
    global proximo_id
    modelo = request.form["modelo"]
    tamanho = int(request.form["tamanho"])
    quantidade = int(request.form["quantidade"])

    disponivel = stock.get(modelo, {}).get(tamanho, 0)
    if disponivel < quantidade:
        return {"erro": "Sem stock para esse modelo/tamanho"}, 400

    encomenda = {
        "id": proximo_id,
        "modelo": modelo,
        "tamanho": tamanho,
        "quantidade": quantidade,
        "estado": "AGUARDA_PAGAMENTO",
    }
    encomendas.append(encomenda)
    proximo_id += 1
    return redirect("/")

# Será chamado pelo microserviço de pagamentos
@app.post("/encomendas/<int:id>/pagamento")
def confirmar_pagamento(id):
    for e in encomendas:
        if e["id"] == id:
            e["estado"] = "PAGA"
            return e
    return {"erro": "Encomenda não encontrada"}, 404

if __name__ == "__main__":
    app.run(host="0.0.0.0")