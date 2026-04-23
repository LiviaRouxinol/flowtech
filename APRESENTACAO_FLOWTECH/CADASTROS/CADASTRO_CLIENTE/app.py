from flask import Flask, render_template, request, redirect, url_for, flash
from models.cliente import Cliente 

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


# --- ROTAS ---

@app.route("/")
def index():
    # Redireciona para a função 'listar_clientes' (que renderiza o lista.html)
    return redirect(url_for("listar_clientes"))

@app.route("/clientes") # Rota para a página principal de clientes
def cliente():
    return render_template("cliente.html", cliente=Cliente.find_all(order_by="nome"))

# ROTA PARA LISTAR
@app.route("/clientes/listar")
def listar_clientes():
    todos_clientes = Cliente.find_all(order_by="nome") # Para pegar os dados
    return render_template('lista.html', cliente=todos_clientes)

@app.route("/cliente/novo")
def novo_cliente():
    return render_template("formulario_cliente.html", cliente=None)

@app.route("/cliente/salvar", methods=["POST"])
def salvar_cliente():
    dados = get_cliente_form()
    novo_cliente = Cliente(**dados) 
    erros = novo_cliente.validate()

    if erros:
        for erro in erros:
            flash(erro, "erro")
        # IMPORTANTE: Pegamos a lista real do banco para a tabela não quebrar
        lista_do_banco = Cliente.find_all(order_by="nome")
        # Passamos 'lista_do_banco' para a variável 'cliente'
        return render_template("lista.html", cliente=lista_do_banco, form_dados=dados)

    try:
        novo_cliente.insert() 
        flash("Cliente cadastrado com sucesso.", "sucesso")
        return redirect(url_for("listar_clientes")) 
    except Exception as e:
        flash(f"Erro ao cadastrar cliente: {e}", "erro")
        lista_do_banco = Cliente.find_all(order_by="nome")
        return render_template("lista.html", cliente=lista_do_banco, form_dados=dados)

@app.route("/cliente/excluir/<int:id>", methods=["GET", "POST"]) # Adicionado GET para o link funcionar
def excluir_cliente(id):
    try:
        Cliente.safe_delete(id) 
        flash("Cliente excluído com sucesso.", "sucesso")
    except Exception as e:
        flash(f"Erro ao excluir cliente: {e}", "erro")
    return redirect(url_for("listar_clientes"))

if __name__ == "__main__":
    app.run(debug=True)
