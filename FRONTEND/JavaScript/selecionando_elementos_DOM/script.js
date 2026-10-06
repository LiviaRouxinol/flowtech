let botao = document.getElementById("botao");

botao.addEventListener("click", function() {
    alert("Você clicou!");
});

let texto = document.getElementById("texto")

texto.addEventListener("mouseover", function() {
    texto.innerText = "Mouse detectsdo!";
});

let campo = document.getElementById("campo");

campo.addEventListener("keydown",function() {
    console.log("Tecla pressionada");
});