-- MySQL dump 10.13   Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version    9.7.0

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
-- Table structure for table `selecoes`
--

DROP TABLE IF EXISTS `selecoes`; -- CORRIGIDO: Uso de crases válidas
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `selecoes` ( -- CORRIGIDO: Uso de crases válidas
  `id_selecao` int NOT NULL AUTO_INCREMENT,
  `nome_selecao` varchar(50) NOT NULL,
  `continente` varchar(30) NOT NULL,
  `tecnico` varchar(50) NOT NULL,
  `titulos` int NOT NULL,
  `id_grupo` int DEFAULT NULL,
  PRIMARY KEY (`id_selecao`),
  KEY `fk_selecoes_grupos` (`id_grupo`),
  CONSTRAINT `fk_selecoes_grupos` FOREIGN KEY (`id_grupo`) REFERENCES `grupos` (`id_grupo`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selecoes`
--

LOCK TABLES `selecoes` WRITE;
/*!40000 ALTER TABLE `selecoes` DISABLE KEYS */;
INSERT INTO `selecoes` VALUES -- CORRIGIDO: Caracteres ocultos e quebras de linha limpos
(1,'Mexico','América','Javier Aguirre',0,1),
(2,'Coreia do Sul','Ásia','Hong Myung-bo',0,1),
(3,'República Tcheca','Europa','Ivan Hasek',0,1),
(4,'Africa do Sul','África','Hugo Broos',0,1),
(5,'Canadá','América','Jesse Marsch',0,2),
(6,'Suíça','Europa','Murat Yakin',0,2),
(7,'Catar','Ásia','Tintín Márquez',0,2),
(8,'Bósnia','Europa','Sergej Barbarez',0,2),
(9,'Brasil','América','Dorival Junior',5,3),
(10,'Marrocos','África','Walid Regragui',0,3),
(11,'Escócia','Europa','Steve Clarke',0,3),
(12,'Haiti','América','Sébastien Migné',0,3),
(13,'Estados Unidos','América','Mauricio Pochettino',0,4),
(14,'Austrália','Ásia','Tony Popovic',0,4),
(15,'Paraguai','América','Gustavo Alfaro',0,4),
(16,'Turquia','Europa','Vincenzo Montella',0,4),
(17,'Alemanha','Europa','Julian Nagelsmann',4,5),
(18,'Equador','América','Sebastián Beccacece',0,5),
(19,'Costa do Marfim','África','Emerse Faé',0,5),
(20,'Curaçau','América','Dick Advocaat',0,5),
(21,'Holanda','Europa','Ronald Koeman',0,6),
(22,'Japão','Ásia','Hajime Moriyasu',0,6),
(23,'Suécia','Europa','Jon Dahl Tomasson',0,6),
(24,'Tunísia','África','Kais Yaâkoubi',0,6),
(25,'Bélgica','Europa','Domenico Tedesco',0,7),
(26,'Egito','África','Hossam Hassan',0,7),
(27,'Irã','Ásia','Amir Ghalenoei',0,7),
(28,'Nova Zelândia','Oceania','Darren Bazeley',0,7),
(29,'Espanha','Europa','Luis de la Fuente',1,8),
(30,'Uruguai','América','Marcelo Bielsa',2,8),
(31,'Arábia Saudita','Ásia','Hervé Renard',0,8),
(32,'Cabo Verde','África','Bubista',0,8),
(33,'França','Europa','Didier Deschamps',2,9),
(34,'Senegal','África','Pape Thiaw',0,9),
(35,'Noruega','Europa','Ståle Solbakken',0,9),
(36,'Iraque','Ásia','Jesús Casas',0,9),
(37,'Argentina','América','Lionel Scaloni',3,10),
(38,'Áustria','Europa','Ralf Rangnick',0,10),
(39,'Argélia','África','Vladimir Petković',0,10),
(40,'Jordânia','Ásia','Jamal Sellami',0,10),
(41,'Portugal','Europa','Roberto Martínez',0,11),
(42,'Colômbia','América','Néstor Lorenzo',0,11),
(43,'Uzbequistão','Ásia','Srečko Katanec',0,11),
(44,'RD Congo','África','Sébastien Desabre',0,11),
(45,'Inglaterra','Europa','Thomas Tuchel',1,12),
(46,'Croácia','Europa','Zlatko Dalić',0,12),
(47,'Gana','África','Otto Addo',0,12),
(48,'Panamá','América','Thomas Christiansen',0,12);
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
