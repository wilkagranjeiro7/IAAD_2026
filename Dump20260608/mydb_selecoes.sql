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
-- Table structure for table `selecoes`
--

DROP TABLE IF EXISTS `selecoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `selecoes` (
  `id_selecao` int NOT NULL AUTO_INCREMENT,
  `nome_selecao` varchar(50) NOT NULL,
  `continente` varchar(30) NOT NULL,
  `tecnico` varchar(50) NOT NULL,
  `titulos` int NOT NULL,
  `id_grupo` int DEFAULT NULL,
  PRIMARY KEY (`id_selecao`),
  KEY `fk_selecoes_grupos` (`id_grupo`),
  CONSTRAINT `fk_selecoes_grupos` FOREIGN KEY (`id_grupo`) REFERENCES `grupos` (`id_grupo`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selecoes`
--

LOCK TABLES `selecoes` WRITE;
/*!40000 ALTER TABLE `selecoes` DISABLE KEYS */;
INSERT INTO `selecoes` VALUES (51,'México','América','Jaime Lozano',0,1),(52,'Coreia do Sul','Ásia','Jürgen Klinsmann',0,1),(53,'República Tcheca','Europa','Jaroslav Šilhavý',0,1),(55,'Canadá','América','Jesse Marsch',0,2),(56,'Suíça','Europa','Murat Yakin',0,2),(57,'Catar','Ásia','Tintín Márquez',0,2),(58,'Bósnia','Europa','Sergej Barbarez',0,2),(59,'Brasil','América','Carlo Ancelotti',5,3),(60,'Marrocos','África','Walid Regragui',0,3),(61,'Escócia','Europa','Steve Clarke',0,3),(62,'Haiti','América','Gabriel Calderón',0,3),(63,'Estados Unidos','América','Gregg Berhalter',0,4),(64,'Austrália','Ásia','Graham Arnold',0,4),(65,'Paraguai','América','Daniel Garnero',0,4),(66,'Turquia','Europa','Vincenzo Montella',0,4),(67,'Alemanha','Europa','Julian Nagelsmann',4,5),(68,'Equador','América','Félix Sánchez',0,5),(69,'Costa do Marfim','África','Emerse Faé',0,5),(70,'Curaçau','América','Dick Advocaat',0,5),(71,'Holanda','Europa','Ronald Koeman',0,6),(72,'Japão','Ásia','Hajime Moriyasu',0,6),(73,'Suécia','Europa','Jon Dahl Tomasson',0,6),(74,'Tunísia','África','Mondher Kebaier',0,6),(75,'Bélgica','Europa','Domenico Tedesco',0,7),(76,'Egito','África','Rui Vitória',0,7),(77,'Irã','Ásia','Amir Ghalenoei',0,7),(78,'Nova Zelândia','Oceania','Darren Bazeley',0,7),(79,'Espanha','Europa','Luis de la Fuente',1,8),(80,'Uruguai','América','Marcelo Bielsa',2,8),(81,'Arábia Saudita','Ásia','Roberto Mancini',0,8),(82,'Cabo Verde','África','Bubista',0,8),(83,'França','Europa','Didier Deschamps',2,9),(84,'Senegal','África','Aliou Cissé',0,9),(85,'Noruega','Europa','Ståle Solbakken',0,9),(86,'Iraque','Ásia','Jesús Casas',0,9),(87,'Argentina','América','Lionel Scaloni',3,10),(88,'Áustria','Europa','Ralf Rangnick',0,10),(89,'Argélia','África','Djamel Belmadi',0,10),(90,'Jordânia','Ásia','Hussein Ammouta',0,10),(91,'Portugal','Europa','Roberto Martínez',0,11),(92,'Colômbia','América','Néstor Lorenzo',0,11),(93,'Uzbequistão','Ásia','Srečko Katanec',0,11),(94,'RD Congo','África','Sébastien Desabre',0,11),(95,'Inglaterra','Europa','Tomas Tuchel',1,12),(96,'Croácia','Europa','Zlatko Dalić',0,12),(97,'Gana','África','Chris Hughton',0,12),(98,'Panamá','América','Thomas Christiansen',0,12),(99,'Africa do Sul','Africa','Hugo Bross',0,1);
/*!40000 ALTER TABLE `selecoes` ENABLE KEYS */;
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

-- Dump completed on 2026-06-08 18:51:12
