-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8mb4 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`grupos` (ADICIONADA)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`grupos` (
  `id_grupo` INT NOT NULL AUTO_INCREMENT,
  `nome_grupo` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`id_grupo`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `mydb`.`selecoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`selecoes` (
  `id_selecao` INT NOT NULL AUTO_INCREMENT,
  `nome_selecao` VARCHAR(50) NOT NULL,
  `continente` VARCHAR(30) NOT NULL,
  `tecnico` VARCHAR(50) NOT NULL,
  `titulos` INT NOT NULL,
  `id_grupo` INT NULL, -- Adicionado para ligar com a tabela grupos
  PRIMARY KEY (`id_selecao`),
  INDEX `fk_selecoes_grupos_idx` (`id_grupo` ASC) VISIBLE,
  CONSTRAINT `fk_selecoes_grupos`
    FOREIGN KEY (`id_grupo`)
    REFERENCES `mydb`.`grupos` (`id_grupo`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `mydb`.`estadios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`estadios` (
  `id_estadio` INT NOT NULL AUTO_INCREMENT,
  `nome_estadio` VARCHAR(80) NOT NULL,
  `cidade` VARCHAR(50) NOT NULL,
  `pais` VARCHAR(50) NOT NULL,
  `capacidade` INT NOT NULL,
  PRIMARY KEY (`id_estadio`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `mydb`.`jogadores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`jogadores` (
  `id_jogador` INT NOT NULL AUTO_INCREMENT,
  `nome_jogador` VARCHAR(60) NOT NULL,
  `posicao` VARCHAR(30) NOT NULL,
  `numero_camisa` INT NOT NULL,
  `data_nascimento` DATE NOT NULL,
  `id_selecao` INT NOT NULL,
  PRIMARY KEY (`id_jogador`),
  INDEX `fk_jogadores_selecoes_idx` (`id_selecao` ASC) VISIBLE,
  CONSTRAINT `fk_jogadores_selecoes`
    FOREIGN KEY (`id_selecao`)
    REFERENCES `mydb`.`selecoes` (`id_selecao`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `mydb`.`arbitros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`arbitros` (
  `id_arbitro` INT NOT NULL AUTO_INCREMENT,
  `nome_arbitro` VARCHAR(100) NOT NULL,
  `pais_origem` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_arbitro`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `mydb`.`partidas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`partidas` (
  `id_partida` INT NOT NULL AUTO_INCREMENT,
  `data_partida` DATE NOT NULL,
  `id_estadio` INT NOT NULL,
  `id_selecao_1` INT NOT NULL,
  `id_selecao_2` INT NOT NULL,
  `id_arbitro` INT NOT NULL,
  `quantidade_gols_selecao_1` INT NOT NULL,
  `quantidade_gols_selecao_2` INT NOT NULL,
  `vencedor` INT NULL,
  PRIMARY KEY (`id_partida`),
  INDEX `fk_partidas_selecao1_idx` (`id_selecao_1` ASC) VISIBLE,
  INDEX `fk_partidas_selecao2_idx` (`id_selecao_2` ASC) VISIBLE,
  INDEX `fk_partidas_vencedor_idx` (`vencedor` ASC) VISIBLE,
  INDEX `fk_partidas_estadios_idx` (`id_estadio` ASC) VISIBLE,
  INDEX `fk_partidas_arbitros_idx` (`id_arbitro` ASC) VISIBLE,
  CONSTRAINT `fk_partidas_selecao1`
    FOREIGN KEY (`id_selecao_1`)
    REFERENCES `mydb`.`selecoes` (`id_selecao`)
    ON DELETE CASCADE -- Atualizado para CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_partidas_selecao2`
    FOREIGN KEY (`id_selecao_2`)
    REFERENCES `mydb`.`selecoes` (`id_selecao`)
    ON DELETE CASCADE -- Atualizado para CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_partidas_vencedor`
    FOREIGN KEY (`vencedor`)
    REFERENCES `mydb`.`selecoes` (`id_selecao`)
    ON DELETE SET NULL -- Se a seleção sumir, o vencedor fica NULL em vez de apagar a partida
    ON UPDATE CASCADE,
  CONSTRAINT `fk_partidas_estadios`
    FOREIGN KEY (`id_estadio`)
    REFERENCES `mydb`.`estadios` (`id_estadio`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_partidas_arbitros`
    FOREIGN KEY (`id_arbitro`)
    REFERENCES `mydb`.`arbitros` (`id_arbitro`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `mydb`.`gols`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`gols` (
  `id_gol` INT NOT NULL AUTO_INCREMENT,
  `tempo_gol` VARCHAR(10) NOT NULL,
  `id_partida` INT NOT NULL,
  `id_jogador` INT NOT NULL,
  PRIMARY KEY (`id_gol`),
  INDEX `fk_gols_partidas_idx` (`id_partida` ASC) VISIBLE,
  INDEX `fk_gols_jogador_idx` (`id_jogador` ASC) VISIBLE,
  CONSTRAINT `fk_gols_partidas`
    FOREIGN KEY (`id_partida`)
    REFERENCES `mydb`.`partidas` (`id_partida`)
    ON DELETE CASCADE -- Atualizado para CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_gols_jogador`
    FOREIGN KEY (`id_jogador`)
    REFERENCES `mydb`.`jogadores` (`id_jogador`)
    ON DELETE CASCADE -- Atualizado para CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `mydb`.`cartoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`cartoes` (
  `id_cartao` INT NOT NULL AUTO_INCREMENT,
  `tipo_cartao` VARCHAR(10) NOT NULL,
  `tempo_cartao` VARCHAR(10) NOT NULL,
  `id_partida` INT NOT NULL,
  `id_jogador` INT NOT NULL,
  PRIMARY KEY (`id_cartao`),
  INDEX `fk_cartoes_partidas_idx` (`id_partida` ASC) VISIBLE,
  INDEX `fk_cartoes_jogadores_idx` (`id_jogador` ASC) VISIBLE,
  CONSTRAINT `fk_cartoes_partidas`
    FOREIGN KEY (`id_partida`)
    REFERENCES `mydb`.`partidas` (`id_partida`)
    ON DELETE CASCADE -- Atualizado para CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_cartoes_jogadores`
    FOREIGN KEY (`id_jogador`)
    REFERENCES `mydb`.`jogadores` (`id_jogador`)
    ON DELETE CASCADE -- Atualizado para CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- =================================--------------------
-- SEÇÃO DE TRIGGERS (Agrupadas no final para estabilidade)
-- =================================--------------------

DELIMITER $$

-- Trigger 1 - Impedir inserção de jogadores com menos de 18 anos
CREATE TRIGGER trg_verifica_idade_jogador
BEFORE INSERT ON jogadores
FOR EACH ROW
BEGIN
    IF TIMESTAMPDIFF(YEAR, NEW.data_nascimento, CURDATE()) < 18 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: O jogador não pode ser menor de 18 anos.';
    END IF;
END$$

-- Trigger 2 - Validar se o jogador que fez o gol pertence a uma das duas seleções daquela partida
CREATE TRIGGER trg_valida_autor_gol
BEFORE INSERT ON gols
FOR EACH ROW
BEGIN
    DECLARE v_id_selecao_jogador INT;
    DECLARE v_id_sel1 INT;
    DECLARE v_id_sel2 INT;

    -- Descobre a seleção do jogador
    SELECT id_selecao INTO v_id_selecao_jogador FROM jogadores WHERE id_jogador = NEW.id_jogador;
    
    -- Descobre as duas seleções da partida
    SELECT id_selecao_1, id_selecao_2 INTO v_id_sel1, v_id_sel2 FROM partidas WHERE id_partida = NEW.id_partida;

    IF v_id_selecao_jogador <> v_id_sel1 AND v_id_selecao_jogador <> v_id_sel2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Este jogador não pertence a nenhuma das seleções desta partida.';
    END IF;
END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;