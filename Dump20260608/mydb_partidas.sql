-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	9.7.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '982bf473-5ec3-11f1-99e3-b04f13e544f5:1-110';

--
-- Table structure for table `partidas`
--

DROP TABLE IF EXISTS `partidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partidas` (
  `id_partida` int NOT NULL AUTO_INCREMENT,
  `data_partida` date NOT NULL,
  `id_estadio` int NOT NULL,
  `id_selecao_1` int NOT NULL,
  `id_selecao_2` int NOT NULL,
  `id_arbitro` int NOT NULL,
  `quantidade_gols_selecao_1` int NOT NULL,
  `quantidade_gols_selecao_2` int NOT NULL,
  `vencedor` int DEFAULT NULL,
  PRIMARY KEY (`id_partida`),
  KEY `fk_partidas_selecao1_idx` (`id_selecao_1`),
  KEY `fk_partidas_selecao2_idx` (`id_selecao_2`),
  KEY `fk_partidas_vencedor_idx` (`vencedor`),
  KEY `fk_partidas_estadios_idx` (`id_estadio`),
  KEY `fk_partidas_arbitros_idx` (`id_arbitro`),
  CONSTRAINT `fk_partidas_arbitros` FOREIGN KEY (`id_arbitro`) REFERENCES `arbitros` (`id_arbitro`),
  CONSTRAINT `fk_partidas_estadios` FOREIGN KEY (`id_estadio`) REFERENCES `estadios` (`id_estadio`),
  CONSTRAINT `fk_partidas_selecao1` FOREIGN KEY (`id_selecao_1`) REFERENCES `selecoes` (`id_selecao`),
  CONSTRAINT `fk_partidas_selecao2` FOREIGN KEY (`id_selecao_2`) REFERENCES `selecoes` (`id_selecao`),
  CONSTRAINT `fk_partidas_vencedor` FOREIGN KEY (`vencedor`) REFERENCES `selecoes` (`id_selecao`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partidas`
--

LOCK TABLES `partidas` WRITE;
/*!40000 ALTER TABLE `partidas` DISABLE KEYS */;
INSERT INTO `partidas` VALUES (1,'2026-06-11',12,51,52,1,2,1,51),(3,'2026-06-16',12,51,53,3,3,0,51),(6,'2026-06-22',14,52,53,6,1,2,53),(7,'2026-06-12',15,55,56,7,1,1,NULL),(8,'2026-06-13',16,57,58,8,0,2,58),(9,'2026-06-17',15,55,57,9,3,0,55),(10,'2026-06-18',9,56,58,10,2,0,56),(11,'2026-06-22',16,55,58,11,1,0,55),(12,'2026-06-23',9,56,57,12,4,0,56),(13,'2026-06-13',1,59,60,13,2,0,59),(14,'2026-06-14',4,61,62,14,1,1,NULL),(15,'2026-06-18',1,59,61,15,4,0,59),(16,'2026-06-19',6,60,62,16,2,0,60),(17,'2026-06-23',4,59,62,17,5,0,59),(18,'2026-06-24',6,60,61,18,1,1,NULL),(19,'2026-06-13',2,63,64,19,3,1,63),(20,'2026-06-14',10,65,66,20,1,2,66),(21,'2026-06-18',2,63,65,1,2,0,63),(22,'2026-06-19',11,64,66,2,0,3,66),(23,'2026-06-24',10,63,66,3,2,2,NULL),(24,'2026-06-25',11,64,65,4,1,1,NULL),(25,'2026-06-14',3,67,68,5,3,0,67),(26,'2026-06-15',8,69,70,6,2,1,69),(27,'2026-06-19',3,67,69,7,1,1,NULL),(28,'2026-06-20',9,68,70,8,3,0,68),(29,'2026-06-24',8,67,70,9,5,0,67),(30,'2026-06-25',9,68,69,10,0,2,69),(31,'2026-06-14',5,71,72,11,2,2,NULL),(32,'2026-06-15',7,73,74,12,1,0,73),(33,'2026-06-19',5,71,73,13,1,1,NULL),(34,'2026-06-20',7,72,74,14,2,0,72),(35,'2026-06-25',1,71,74,15,3,0,71),(36,'2026-06-26',4,72,73,16,1,2,73),(37,'2026-06-15',6,75,76,17,1,1,NULL),(38,'2026-06-16',16,77,78,18,1,0,77),(39,'2026-06-20',1,75,77,19,2,0,75),(40,'2026-06-21',16,76,78,20,3,1,76),(41,'2026-06-26',15,75,78,1,2,0,75),(42,'2026-06-27',1,76,77,2,1,1,NULL),(43,'2026-06-15',13,79,80,3,2,1,79),(44,'2026-06-16',12,81,82,4,1,2,82),(45,'2026-06-20',13,79,81,5,4,0,79),(46,'2026-06-21',12,80,82,6,3,0,80),(47,'2026-06-26',2,79,82,7,5,0,79),(48,'2026-06-27',10,80,81,8,2,0,80),(49,'2026-06-16',4,83,84,9,2,1,83),(50,'2026-06-17',7,85,86,10,3,0,85),(51,'2026-06-21',4,83,85,11,1,1,NULL),(52,'2026-06-22',6,84,86,12,2,0,84),(53,'2026-06-27',1,83,86,13,4,0,83),(54,'2026-06-28',4,84,85,14,1,2,85),(55,'2026-06-16',2,87,88,15,3,0,87),(56,'2026-06-17',11,89,90,16,2,1,89),(57,'2026-06-21',2,87,89,17,2,0,87),(58,'2026-06-22',10,88,90,18,1,1,NULL),(59,'2026-06-28',3,87,90,19,5,0,87),(60,'2026-06-29',8,88,89,20,0,2,89),(61,'2026-06-17',5,91,92,1,2,1,91),(62,'2026-06-18',3,93,94,2,1,1,NULL),(63,'2026-06-22',5,91,93,3,4,0,91),(64,'2026-06-23',8,92,94,4,2,0,92),(65,'2026-06-29',2,91,94,5,3,0,91),(66,'2026-06-30',7,92,93,6,2,0,92),(67,'2026-06-18',1,95,96,7,1,0,95),(68,'2026-06-19',4,97,98,8,2,2,NULL),(69,'2026-06-23',1,95,97,9,3,1,95),(70,'2026-06-24',6,96,98,10,2,0,96),(71,'2026-06-30',3,95,98,11,4,0,95),(72,'2026-07-01',5,96,97,12,1,1,NULL);
/*!40000 ALTER TABLE `partidas` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-08 18:51:11
