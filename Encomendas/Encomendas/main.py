from flask import Flask, jsonify, render_template, request, redirect

app = Flask(__name__)

# Cópia simulada do catálogo, com a mesma estrutura do serviço produtos.
# Mais tarde isto passa a ser um pedido ao serviço produtos.
catalogo = {
    1: {"marca": "Nike", "modelo": "Air Force 1", "preco": 99.99,
        "stocks": {"40": 5, "41": 10, "42": 2}},
    2: {"marca": "Adidas", "modelo": "Superstar", "preco": 89.99,
        "stocks": {"39": 4, "41": 8, "42": 6}},
}

encomendas = []
proximo_id = 1

@app.get("/")
def pagina_inicial():
    return render_template("index.html", encomendas=encomendas)

@app.get("/encomendas")
def listar_encomendas():
    return jsonify(encomendas)

@app.get("/encomendas/<int:encomenda_id>")
def obter_encomenda(encomenda_id):
    encomenda = next((e for e in encomendas if e["id"] == encomenda_id), None)
    if not encomenda:
        return jsonify({"erro": "Encomenda não encontrada"}), 404
    return jsonify(encomenda)

@app.post("/encomendas")
def criar_encomenda():
    global proximo_id
    produto_id = int(request.form["produto_id"])
    tamanho = request.form["tamanho"]
    quantidade = int(request.form["quantidade"])

    produto = catalogo.get(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    if produto["stocks"].get(tamanho, 0) < quantidade:
        return jsonify({"erro": "Sem stock para esse tamanho"}), 400

    encomenda = {
        "id": proximo_id,
        "produto_id": produto_id,
        "modelo": produto["marca"] + " " + produto["modelo"],
        "tamanho": tamanho,
        "quantidade": quantidade,
        "total": round(produto["preco"] * quantidade, 2),
        "estado": "AGUARDA_PAGAMENTO",
    }
    encomendas.append(encomenda)
    proximo_id += 1
    return redirect("/")

# Será chamada pelo serviço de pagamentos quando o pagamento for confirmado
@app.post("/encomendas/<int:encomenda_id>/pagamento")
def confirmar_pagamento(encomenda_id):
    encomenda = next((e for e in encomendas if e["id"] == encomenda_id), None)
    if not encomenda:
        return jsonify({"erro": "Encomenda não encontrada"}), 404
    encomenda["estado"] = "PAGA"
    return jsonify(encomenda)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)