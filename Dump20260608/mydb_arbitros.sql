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
-- Table structure for table `arbitros`
--

DROP TABLE IF EXISTS `arbitros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arbitros` (
  `id_arbitro` int NOT NULL AUTO_INCREMENT,
  `nome_arbitro` varchar(100) NOT NULL,
  `pais_origem` varchar(50) NOT NULL,
  PRIMARY KEY (`id_arbitro`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arbitros`
--

LOCK TABLES `arbitros` WRITE;
/*!40000 ALTER TABLE `arbitros` DISABLE KEYS */;
INSERT INTO `arbitros` VALUES (1,'Michael Oliver','Inglaterra'),(2,'Anthony Taylor','Inglaterra'),(3,'François Letexier','França'),(4,'Clément Turpin','França'),(5,'Felix Zwayer','Alemanha'),(6,'Maurizio Mariani','Itália'),(7,'Danny Makkelie','Holanda'),(8,'Espen Eskås','Noruega'),(9,'Szymon Marciniak','Polônia'),(10,'João Pinheiro','Portugal'),(11,'István Kovács','Romênia'),(12,'Slavko Vinčić','Eslovênia'),(13,'Alejandro Hernández Hernández','Espanha'),(14,'Glenn Nyberg','Suécia'),(15,'Sandro Schärer','Suíça'),(16,'Yael Falcón Pérez','Argentina'),(17,'Darío Herrera','Argentina'),(18,'Facundo Tello','Argentina'),(19,'Ramon Abatti','Brasil'),(20,'Raphael Claus','Brasil'),(21,'Wilton Sampaio','Brasil'),(22,'Cristian Garay','Chile'),(23,'Andrés Rojas','Colômbia'),(24,'Juan Gabriel Benítez','Paraguai'),(25,'Kevin Ortega','Peru'),(26,'Gustavo Tejera','Uruguai'),(27,'Jesús Valenzuela','Venezuela'),(28,'Drew Fischer','Canadá'),(29,'Juan Calderón','Costa Rica'),(30,'Héctor Said Martínez','Honduras'),(31,'Oshane Nation','Jamaica'),(32,'César Ramos','México'),(33,'Katia García','México'),(34,'Iván Barton','El Salvador'),(35,'Ismail Elfath','Estados Unidos'),(36,'Tori Penso','Estados Unidos'),(37,'Adham Makhadmeh','Jordânia'),(38,'Ning Ma','China'),(39,'Alireza Faghani','Austrália'),(40,'Yusuke Araki','Japão'),(41,'Abdulrahman Al Jassim','Catar'),(42,'Khalid Al Turais','Arábia Saudita'),(43,'Omar Al Ali','Emirados Árabes Unidos'),(44,'Ilgiz Tantashev','Uzbequistão'),(45,'Mustapha Ghorbal','Argélia'),(46,'Pierre Atcho','Gabão'),(47,'Amin Mohamed','Egito'),(48,'Jalal Jayed','Marrocos'),(49,'Dahane Beida','Mauritânia'),(50,'Omar Abdulkadir Artan','Somália'),(51,'Abongile Tom','África do Sul'),(52,'Campbell-Kirk Kawana-Waugh','Nova Zelândia');
/*!40000 ALTER TABLE `arbitros` ENABLE KEYS */;
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
