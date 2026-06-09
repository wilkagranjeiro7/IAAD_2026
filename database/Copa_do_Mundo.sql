-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`selecoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`selecoes` (
  `id_selecao` INT NOT NULL AUTO_INCREMENT,
  `nome_selecao` VARCHAR(50) NOT NULL,
  `continente` VARCHAR(30) NOT NULL,
  `tecnico` VARCHAR(50) NOT NULL,
  `titulos` INT NOT NULL,
  PRIMARY KEY (`id_selecao`))
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
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
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
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_partidas_selecao2`
    FOREIGN KEY (`id_selecao_2`)
    REFERENCES `mydb`.`selecoes` (`id_selecao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_partidas_vencedor`
    FOREIGN KEY (`vencedor`)
    REFERENCES `mydb`.`selecoes` (`id_selecao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_partidas_estadios`
    FOREIGN KEY (`id_estadio`)
    REFERENCES `mydb`.`estadios` (`id_estadio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_partidas_arbitros`
    FOREIGN KEY (`id_arbitro`)
    REFERENCES `mydb`.`arbitros` (`id_arbitro`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
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
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_gols_jogador`
    FOREIGN KEY (`id_jogador`)
    REFERENCES `mydb`.`jogadores` (`id_jogador`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
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
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_cartoes_jogadores`
    FOREIGN KEY (`id_jogador`)
    REFERENCES `mydb`.`jogadores` (`id_jogador`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
