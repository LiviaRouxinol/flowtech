#Atividade 1 - DDL: criando a estrutura

CREATE DATABASE GameZone; #cria o banco
USE GameZoneDB; #informa o mysql qual banco vamos usar 


#ATIVIDADE 2 - Criando tabela de Clientes

CREATE TABLE clientes (
	clientes_id INT AUTO_INCREMENT PRIMARY KEY UNIQUE,
    clientes_nome VARCHAR(100) NOT NULL,
    clientes_email VARCHAR(100) UNIQUE NOT NULL,
    clientes_cidade VARCHAR(80) NOT NULL,
    clientes_dt_cadastro DATE NOT NULL);
    
    
#ATIVIDADE 3 - Criando tabela jogos

CREATE TABLE jogos (
	jogos_id INT UNIQUE AUTO_INCREMENT PRIMARY KEY,
    jogos_nome VARCHAR(100) NOT NULL,
    jogos_genero VARCHAR(50) NOT NULL,
    jogos_plataforma VARCHAR(50) NOT NULL,
    jogos_preco DECIMAL(10,2) NOT NULL,
    jogos_estoque INT NOT NULL);
    
#ATIVIDADE 4 - Criando a tabela vendas

CREATE TABLE vendas(
	vendas_id INT UNIQUE AUTO_INCREMENT PRIMARY KEY, 
    clientes_id INT NOT NULL,
    jogos_id INT NOT NULL,
    vendas_quantidade INT NOT NULL,
    vendas_dt_venda DATE NOT NULL,
		FOREIGN KEY (clientes_id)
			REFERENCES clientes(clientes_id),
            
		FOREIGN KEY (jogos_id)
			REFERENCES jogos(jogos_id)
);

#ATIVIDADE 5 - inserindo dados de clientes

INSERT INTO clientes
(clientes_nome, clientes_email, clientes_cidade, clientes_dt_cadastro)
VALUES
('Lucas Martins', 'lucas@gmail.cm', 'Campinas', '2026-03-01'),
('Mariana Souza', 'mariana@gmail.cm', 'Jundiaí', '2026-03-02'),
('Pedro Oliveira', 'pedro@gmail.cm', 'Campinas', '2026-03-03'),
('Ana Clara', 'ana@gmail.cm', 'Sorocaba', '2026-03-05'),
('Gabriel Santos', 'gabriel@gmail.cm', 'Jundiaí', '2026-03-07'),
('Julia Ferreira', 'julia@gmail.cm', 'Campinas', '2026-03-10');

#ATIVIDADE 6 - inserir jogos

INSERT INTO jogos
(jogos_nome, jogos_genero, jogos_plataforma, jogos_preco, jogos_estoque)
VALUES 
('Minecrafit', 'Aventura', 'PC', 99.90, 15),
('EA Sports FC', 'Esporte', 'PlayStation 5', 299.90, 8),
('Mario Kart', 'Corrida', 'Nitendo Switch', 249.90, 10),
('The Sims 4', 'Simulação', 'PC', 89.90, 20),
('Spider Men 2', 'Ação', 'PlayStation 5', 349.90, 5),
('Stardew Valley', 'Simulação', 'PC', 39.90, 25);

#ATIVIDADE 7 - inserir vendas

INSERT INTO vendas
( clientes_id, jogos_id, vendas_quantidade, vendas_dt_venda)
VALUES
(1, 1, 1, '2026-04-01'),
(2, 2, 1, '2026-04-02'),
(3, 6, 2, '2026-04-03'),
(4, 3, 1, '2026-04-05'),
(5, 5, 1, '2026-04-06'),
(1, 6, 1, '2026-04-06');

SELECT * FROM clientes;

SELECT * FROM jogos; 

SELECT jogos_nome, jogos_plataforma, jogos_preco
FROM jogos;

SELECT * FROM clientes WHERE clientes_cidade = 'Campinas';

SELECT * FROM jogos WHERE jogos_preco <100.00;

SELECT * FROM jogos WHERE jogos_estoque >10.00;

SELECT * FROM jogos WHERE jogos_plataforma ='PC';

SELECT * FROM jogos WHERE jogos_genero ='Simulação';

SELECT * FROM clientes WHERE clientes_nome ='Mariana Souza';

#10
SELECT * FROM jogos ORDER BY jogos_preco ASC;

#11
SELECT * FROM jogos ORDER BY jogos_preco DESC;

#PARTE 4

UPDATE jogos
SET jogos_preco = 109.90
WHERE jogos_nome = 'Minecraft';

SELECT *
FROM jogos
WHERE jogos_nome = 'Minecraft';

UPDATE jogos
SET jogos_estoque = 12
WHERE jogos_nome = 'Spider-Man 2';

SELECT *
FROM jogos
WHERE jogos_nome = 'Spider-Man 2';

UPDATE clientes
SET clientes_cidade = 'Sorocaba'
WHERE clientes_nome = 'Julia Ferreira';

SELECT *
FROM clientes
WHERE clientes_nome = 'Julia Ferreira';

INSERT INTO jogos
(jogos_nome, jogos_genero, jogos_plataforma, jogos_preco, jogos_estoque)
VALUES
('Hollow Knight', 'Aventura', 'PC', 46.90, 18);

SELECT * FROM jogos
WHERE jogos_nome = 'Hollow Knight';

DELETE FROM jogos
WHERE jogos_nome = 'Hollow Knight';

SELECT *
FROM jogos
WHERE jogos_nome = 'Hollow Knight';

#ATIVIDADE 10
SELECT * FROM vendas;

SELECT * FROM vendas
WHERE vendas_dt_venda > '2026-04-03';

SELECT 
c.clientes_nome AS Clientes,
j.jogos_nome AS Jogos,
v.vendas_quantidade AS Qtd,
v.vendas_dt_venda AS Datas
FROM vendas v
JOIN clientes c ON v.clientes_id = c.clientes_id
JOIN jogos j ON j.jogos_id = j.jogos_id;
    
SELECT c.clientes_nome AS Clientes, j.jogos_nome AS Jogos, v.vendas_quantidade AS Qtd, v.vendas_dt_venda AS Datas
FROM vendas v
JOIN clientes c ON v.clientes_id = c.clientes_id
JOIN jogos j ON v.jogos_id = j.jogos_id
WHERE c.clientes_nome = 'Lucas Martins';

SELECT c.clientes_nome AS Clientes, j.jogos_nome AS Jogos, v.vendas_quantidade AS Qtd, j.jogos_preco AS Preco, v.vendas_quantidade * j.jogos_preco AS Total
FROM vendas v
JOIN clientes c ON v.clientes_id = c.clientes_id
JOIN jogos j ON v.jogos_id = j.jogos_id;

# COMENTÁRIOS FINAIS 
# Banco de dados é um local interno onde são armazenados dados específicos a partir da criação de tabelas. Ele permite também inserir, alterar e apagar dados das tabelas que criamos inicialmente.

# Chave primária é um campo que identifica cada registro de uma tabela de forma única. Ela não pode se repetir e normalmente é utilizada para identificar cada linha da tabela.

# Chave estrangeira é um campo que faz ligação entre duas tabelas. Ela utiliza a chave primária de outra tabela para relacionar os dados entre elas.

# DDL (Data Definition Language) é utilizada para criar e modificar a estrutura do banco de dados, como criar tabelas, alterar tabelas ou excluir tabelas. Exemplos: CREATE, ALTER e DROP.

# DML (Data Manipulation Language) é utilizada para inserir, alterar e excluir os dados que estão dentro das tabelas. Exemplos: INSERT, UPDATE e DELETE.

# DQL (Data Query Language) é utilizada para consultar e buscar informações que estão armazenadas no banco de dados. O principal comando é o SELECT.

# WHERE é utilizado para colocar uma condição na consulta, fazendo com que sejam mostrados apenas os dados que atendem à condição informada.

# ORDER BY é utilizado para organizar os resultados de uma consulta. Podemos organizar os dados em ordem crescente (ASC) ou decrescente (DESC).

# JOIN é utilizado para juntar informações de duas ou mais tabelas que possuem algum campo relacionado entre elas. Dessa forma, podemos consultar dados de tabelas diferentes em uma mesma consulta.
