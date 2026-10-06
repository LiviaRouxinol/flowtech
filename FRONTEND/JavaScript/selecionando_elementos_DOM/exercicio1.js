let formulario = document.getElementById("formulario");

formulario.addEventListener("submit", function () {

    let nome= document.getElementById("nome").value;
    let email= document.getElementById("email").value;
    let idade= document.getElementById("idade").value;

    alert("Cadastro realizado com Sucesso! \n" +
         "Nome:" +nome + "\n" +
        "Email:" + email + "\n" +
        "Idade:" + idade + "\n");
})