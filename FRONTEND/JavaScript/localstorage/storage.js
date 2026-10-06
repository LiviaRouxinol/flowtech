function mostrarMensagem(texto, tipo) {
    const mensagem = document.getElementById("mensagem");

    mensagem.innerHTML = `
    <div class="alert alert-${tipo}">
        ${texto}
    </div>
    `;
}

function salvarLogin() {

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    //Validação
    if(email === "") {
        mostrarMensagem("Digite o e-mail.", "danger");
        return;
    }

    if(senha === "") {
        mostrarMensagem("Digitea senha.", "danger");
        return;
    }

    // Criando objeto
    const usuario = {
        email: email,
        senha: senha
    };

    //Salvando no LocalStorage
    localStorage.setItem(
        "usuario",JSON.stringify(usuario)
    );

    mostrarMensagem(
        "Dados salvos com sucesso"
    )
    console log(usuario);

}

function buscarLogin(){

    const dados = localStorage.getItem("Usuario");

    if (dados === null) {
        mostrarMensagem(
            "Nenhum dado encontrado.",
            "warning"
        );
    }

    //convertendo JSON para objeto
    const usuario = JSON.parse(dados);

    //
    document.getElementById("resultado").
    innerHTML = `
        <div class="card">
            <div class = "card-body">
                <h5 class="card-title">
                    Dados recuperados
                </h5>
                <p>
                    <strong>E-mail:</strong>
                    ${usuario.email}
                </p>
                <p>
                    <strong>Senha:</strong>
                     ${usuario.senha}
                </p>
            </div>
        </div>
    `;
    mostrarMensagem(
        "Dados carregados com sucesso!",
        "info"
    );

}

function removerLogin() {
     localStorage.removerItem("usuario");

     document.getElementById("resultado").innerHTML = "";
     mostrarMensagem(
        "Removido.",
        "dangeri"
    )
}
////////////////////

function limparCampos(){
    document.getElementById("email").value = "";
    document.getElementById("senha").value = "";

    mostrarMensagem(
        "Campos limpos.",
        "secondary"
    )
}