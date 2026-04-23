from flask import Flask, render_template, request, redirect, url_for, flash
from models.cliente import Cliente 
from models.fornecedor import Fornecedor

app = Flask(__name__)
app.secret_key = "chave_secreta"

# --- FUNÇÕES DE AUXÍLIO ---
def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def get_cliente_form():
    return {
        "nome": request.form.get("nome", "").strip(),
        "cnpj": request.form.get("cnpj", "").strip(),
        "e_mail": request.form.get("e_mail", "").strip(),
        "endereco": request.form.get("endereco", "").strip(),
        "telefone": request.form.get("telefone", "").strip(),
    }

def get_fornecedor_form():
    return {
        "nome": request.form.get("nome", "").strip(),
        "cnpj": request.form.get("cnpj", "").strip(),
        "telefone": request.form.get("telefone", "").strip(),
        "e_mail": request.form.get("e_mail", "").strip(),
        "endereco": request.form.get("endereco", "").strip()
    }

# --- INDEX ---
@app.route("/")
def index():
    todos_clientes = Cliente.find_all() 
    return render_template("dashboard.html", clientes=todos_clientes)

# --- ROTAS DAS TABELAS ---
@app.route("/clientes")
def listar_clientes():
    return render_template("formulario_cliente.html")

@app.route("/fornecedores")
def fornecedores():
    return render_template("fornecedor.html")

@app.route("/funcionarios")
def funcionarios():
    return render_template("formulario_funcionario.html")

@app.route("/pedidos")
def novo_pedido(): 
    return render_template("formulario_pedido.html")

@app.route("/estoque")
def estoque():
    return render_template("formulario_estoque.html")

@app.route("/produtos")
def produtos():
    return render_template("produtos.html")

@app.route("/dashboard")
def dashboard():
    todos_clientes = Cliente.query.all()
    return render_template("dashboard.html", clientes=todos_clientes)


# --- API AUXILIAR ---
@app.route("/api/fornecedor/<int:fornecedor_id>")
def api_fornecedor(fornecedor_id):
    fornecedor = Fornecedor.find_by_id(fornecedor_id)
    if not fornecedor:
        return {"erro": "não encontrado"}, 404
    return {"id": fornecedor["fornecedor_id"], "nome": fornecedor["nome"], "cnpj": fornecedor["cnpj"]}

if __name__ == "__main__":
    app.run(debug=True)
