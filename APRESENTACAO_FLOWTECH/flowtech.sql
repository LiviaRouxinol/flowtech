-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
SHOW WARNINGS;
-- -----------------------------------------------------
-- Schema flowtech
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema flowtech
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `flowtech` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
SHOW WARNINGS;
USE `flowtech` ;

-- -----------------------------------------------------
-- Table `cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cliente` (
  `cliente_id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `CNPJ` VARCHAR(14) NOT NULL,
  `e_mail` VARCHAR(100) NOT NULL,
  `endereco` VARCHAR(255) NOT NULL,
  `telefone` VARCHAR(17) NOT NULL,
  PRIMARY KEY (`cliente_id`),
  UNIQUE INDEX `CNPJ` (`CNPJ` ASC) VISIBLE,
  UNIQUE INDEX `e_mail` (`e_mail` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `produto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `produto` (
  `produto_id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `categoria` VARCHAR(100) NOT NULL,
  `tipo_produto` VARCHAR(100) NOT NULL,
  `estoque_minimo` INT NOT NULL,
  `validade` DATE NULL DEFAULT NULL,
  `lote` VARCHAR(50) NOT NULL,
  `localizacao` VARCHAR(100) NOT NULL,
  `RFID` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`produto_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `estoque`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `estoque` (
  `estoque_id` INT NOT NULL AUTO_INCREMENT,
  `quantidade` INT NOT NULL,
  `produto_id` INT NOT NULL,
  PRIMARY KEY (`estoque_id`),
  INDEX `produto_id` (`produto_id` ASC) VISIBLE,
  CONSTRAINT `estoque_ibfk_1`
    FOREIGN KEY (`produto_id`)
    REFERENCES `produto` (`produto_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `fornecedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fornecedor` (
  `fornecedor_id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `CNPJ` VARCHAR(18) NOT NULL,
  `telefone` VARCHAR(17) NOT NULL,
  `e_mail` VARCHAR(100) NOT NULL,
  `endereco` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`fornecedor_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `funcionario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `funcionario` (
  `funcionario_id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `CPF` VARCHAR(14) NOT NULL,
  `e_mail` VARCHAR(50) NOT NULL,
  `setor` VARCHAR(100) NOT NULL,
  `cargo` VARCHAR(100) NOT NULL,
  `salario` DECIMAL(10,2) NOT NULL,
  `turno` VARCHAR(100) NOT NULL,
  `senha` VARCHAR(200) NOT NULL,
  `telefone` VARCHAR(17) NOT NULL,
  `data_nascimento` DATE NOT NULL,
  PRIMARY KEY (`funcionario_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `pedido_entrada`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pedido_entrada` (
  `pedido_entrada_id` INT NOT NULL AUTO_INCREMENT,
  `data_hora` DATETIME(6) NOT NULL,
  `descricao` VARCHAR(250) NOT NULL,
  `status_pedido` VARCHAR(20) NOT NULL,
  `fornecedor_id` INT NOT NULL,
  `estoque_id` INT NOT NULL,
  `funcionario_id` INT NOT NULL,
  PRIMARY KEY (`pedido_entrada_id`),
  INDEX `fornecedor_id` (`fornecedor_id` ASC) VISIBLE,
  INDEX `estoque_id` (`estoque_id` ASC) VISIBLE,
  INDEX `funcionario_id` (`funcionario_id` ASC) VISIBLE,
  CONSTRAINT `pedido_entrada_ibfk_1`
    FOREIGN KEY (`fornecedor_id`)
    REFERENCES `fornecedor` (`fornecedor_id`),
  CONSTRAINT `pedido_entrada_ibfk_2`
    FOREIGN KEY (`estoque_id`)
    REFERENCES `estoque` (`estoque_id`),
  CONSTRAINT `pedido_entrada_ibfk_3`
    FOREIGN KEY (`funcionario_id`)
    REFERENCES `funcionario` (`funcionario_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `itempedido_entrada`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `itempedido_entrada` (
  `itempedido_entrada_id` INT NOT NULL AUTO_INCREMENT,
  `preco_custo` DECIMAL(10,2) NOT NULL,
  `quantidade` INT NOT NULL,
  `produto_id` INT NOT NULL,
  `pedido_entrada_id` INT NOT NULL,
  PRIMARY KEY (`itempedido_entrada_id`),
  INDEX `fk_produto` (`produto_id` ASC) VISIBLE,
  INDEX `fk_pedido` (`pedido_entrada_id` ASC) VISIBLE,
  CONSTRAINT `fk_pedido`
    FOREIGN KEY (`pedido_entrada_id`)
    REFERENCES `pedido_entrada` (`pedido_entrada_id`),
  CONSTRAINT `fk_produto`
    FOREIGN KEY (`produto_id`)
    REFERENCES `produto` (`produto_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `pedido_saida`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pedido_saida` (
  `pedido_saida_id` INT NOT NULL AUTO_INCREMENT,
  `data_hora` DATETIME(6) NOT NULL,
  `status_pedido` VARCHAR(20) NOT NULL,
  `descricao` VARCHAR(250) NOT NULL,
  `cliente_id` INT NOT NULL,
  `estoque_id` INT NOT NULL,
  `funcionario_id` INT NOT NULL,
  PRIMARY KEY (`pedido_saida_id`),
  INDEX `cliente_id` (`cliente_id` ASC) VISIBLE,
  INDEX `funcionario_id` (`funcionario_id` ASC) VISIBLE,
  INDEX `estoque_id` (`estoque_id` ASC) VISIBLE,
  CONSTRAINT `pedido_saida_ibfk_1`
    FOREIGN KEY (`cliente_id`)
    REFERENCES `cliente` (`cliente_id`),
  CONSTRAINT `pedido_saida_ibfk_2`
    FOREIGN KEY (`funcionario_id`)
    REFERENCES `funcionario` (`funcionario_id`),
  CONSTRAINT `pedido_saida_ibfk_3`
    FOREIGN KEY (`estoque_id`)
    REFERENCES `estoque` (`estoque_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `itempedido_saida`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `itempedido_saida` (
  `itempedido_saida_id` INT NOT NULL AUTO_INCREMENT,
  `preco_unitario` DECIMAL(10,2) NOT NULL,
  `quantidade` INT NOT NULL,
  `preco_venda` DECIMAL(10,2) NOT NULL,
  `fornecedor` VARCHAR(100) NOT NULL,
  `produto_id` INT NOT NULL,
  `pedido_saida_id` INT NOT NULL,
  PRIMARY KEY (`itempedido_saida_id`),
  INDEX `produto_id` (`produto_id` ASC) VISIBLE,
  INDEX `pedido_saida_id` (`pedido_saida_id` ASC) VISIBLE,
  CONSTRAINT `itempedido_saida_ibfk_1`
    FOREIGN KEY (`produto_id`)
    REFERENCES `produto` (`produto_id`),
  CONSTRAINT `itempedido_saida_ibfk_2`
    FOREIGN KEY (`pedido_saida_id`)
    REFERENCES `pedido_saida` (`pedido_saida_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `movimentacao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movimentacao` (
  `movimentacao_id` INT NOT NULL AUTO_INCREMENT,
  `data_horamov` DATETIME(6) NOT NULL,
  `tipo_mov` VARCHAR(7) NOT NULL,
  `quantidade` INT NOT NULL,
  `observacao` VARCHAR(255) NULL DEFAULT NULL,
  `estoque_id` INT NOT NULL,
  `funcionario_id` INT NOT NULL,
  PRIMARY KEY (`movimentacao_id`),
  INDEX `estoque_id` (`estoque_id` ASC) VISIBLE,
  INDEX `funcionario_id` (`funcionario_id` ASC) VISIBLE,
  CONSTRAINT `movimentacao_ibfk_1`
    FOREIGN KEY (`estoque_id`)
    REFERENCES `estoque` (`estoque_id`),
  CONSTRAINT `movimentacao_ibfk_2`
    FOREIGN KEY (`funcionario_id`)
    REFERENCES `funcionario` (`funcionario_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;