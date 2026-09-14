from flask import Flask, render_template, request

from src.utils.logger import configurar_logger

app = Flask(__name__)

logger = configurar_logger("flask_demo")

# Simula um "banco" simples em memória, só para o demo visual
fornecedores_cadastrados = []


@app.route("/", methods=["GET", "POST"])
def cadastro():
    mensagem = None

    if request.method == "POST":
        nome = request.form.get("nome")
        cnpj = request.form.get("cnpj")
        categoria = request.form.get("categoria")

        fornecedores_cadastrados.append({
            "nome": nome,
            "cnpj": cnpj,
            "categoria": categoria,
        })

        logger.info(f"Fornecedor recebido via formulário: {nome} ({cnpj})")

        mensagem = "Fornecedor cadastrado com sucesso!"

    return render_template("cadastro.html", mensagem=mensagem)


if __name__ == "__main__":
    app.run(debug=True, port=5000)