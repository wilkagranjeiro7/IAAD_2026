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
-- Table structure for table `cartoes`
--

DROP TABLE IF EXISTS `cartoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cartoes` (
  `id_cartao` int NOT NULL AUTO_INCREMENT,
  `tipo_cartao` varchar(10) NOT NULL,
  `tempo_cartao` varchar(10) NOT NULL,
  `id_partida` int NOT NULL,
  `id_jogador` int NOT NULL,
  PRIMARY KEY (`id_cartao`),
  KEY `fk_cartoes_partidas_idx` (`id_partida`),
  KEY `fk_cartoes_jogadores_idx` (`id_jogador`),
  CONSTRAINT `fk_cartoes_jogadores` FOREIGN KEY (`id_jogador`) REFERENCES `jogadores` (`id_jogador`),
  CONSTRAINT `fk_cartoes_partidas` FOREIGN KEY (`id_partida`) REFERENCES `partidas` (`id_partida`)
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cartoes`
--

LOCK TABLES `cartoes` WRITE;
/*!40000 ALTER TABLE `cartoes` DISABLE KEYS */;
INSERT INTO `cartoes` VALUES (1,'Amarelo','34',1,8),(2,'Amarelo','67',1,14),(3,'Amarelo','89',1,7),(7,'Amarelo','41',3,25),(8,'Amarelo','73',3,6),(15,'Amarelo','38',6,17),(16,'Amarelo','62',6,26),(17,'Amarelo','90+3',6,21),(18,'Amarelo','31',7,51),(19,'Amarelo','59',7,64),(20,'Amarelo','84',7,50),(21,'Amarelo','22',8,73),(22,'Amarelo','66',8,84),(23,'Amarelo','79',8,76),(24,'Amarelo','15',9,68),(25,'Vermelho','70',9,75),(26,'Amarelo','85',9,47),(27,'Amarelo','42',10,80),(28,'Amarelo','67',10,86),(29,'Amarelo','88',10,57),(30,'Amarelo','37',11,88),(31,'Amarelo','63',11,52),(32,'Amarelo','90+1',11,82),(33,'Amarelo','19',12,69),(34,'Amarelo','58',12,74),(35,'Vermelho','81',12,72),(36,'Amarelo','28',13,128),(37,'Amarelo','54',13,95),(38,'Amarelo','76',13,96),(39,'Amarelo','13',14,116),(40,'Amarelo','44',14,107),(41,'Amarelo','80',14,118),(42,'Amarelo','33',15,106),(43,'Amarelo','67',15,109),(44,'Amarelo','41',16,119),(45,'Amarelo','72',16,93),(46,'Amarelo','22',17,115),(47,'Vermelho','61',17,117),(48,'Amarelo','29',18,108),(49,'Amarelo','68',18,91),(50,'Amarelo','86',18,105),(51,'Amarelo','26',19,140),(52,'Amarelo','58',19,150),(53,'Amarelo','37',20,161),(54,'Amarelo','64',20,170),(55,'Amarelo','83',20,158),(56,'Amarelo','19',21,159),(57,'Amarelo','55',21,139),(58,'Vermelho','88',21,162),(59,'Amarelo','31',22,168),(60,'Amarelo','74',22,149),(61,'Amarelo','45+1',23,171),(62,'Amarelo','68',23,135),(63,'Vermelho','90+3',23,173),(64,'Amarelo','43',24,165),(65,'Amarelo','77',24,151),(66,'Amarelo','38',25,191),(67,'Amarelo','71',25,184),(68,'Amarelo','27',26,212),(69,'Amarelo','59',26,206),(70,'Amarelo','84',26,201),(71,'Amarelo','41',27,180),(72,'Amarelo','73',27,205),(73,'Vermelho','89',27,203),(74,'Amarelo','21',28,216),(75,'Amarelo','68',28,195),(76,'Amarelo','18',29,214),(77,'Amarelo','55',29,219),(78,'Amarelo','33',30,194),(79,'Amarelo','70',30,208),(80,'Amarelo','87',30,190),(81,'Amarelo','39',31,225),(82,'Amarelo','62',31,260),(83,'Amarelo','85',31,228),(84,'Amarelo','27',32,238),(85,'Amarelo','73',32,250),(86,'Amarelo','15',33,254),(87,'Amarelo','58',33,224),(88,'Amarelo','82',33,249),(89,'Amarelo','35',34,241),(90,'Amarelo','71',34,256),(91,'Amarelo','29',35,240),(92,'Vermelho','75',35,239),(93,'Amarelo','44',36,261),(94,'Amarelo','69',36,251),(95,'Amarelo','42',37,315),(96,'Amarelo','77',37,326),(97,'Amarelo','38',38,337),(98,'Amarelo','67',38,348),(99,'Amarelo','89',38,334),(100,'Amarelo','28',39,340),(101,'Amarelo','63',39,314),(102,'Amarelo','26',40,352),(103,'Vermelho','79',40,324),(104,'Amarelo','34',41,346),(105,'Amarelo','70',41,319),(106,'Amarelo','49',42,332),(107,'Amarelo','81',42,323),(108,'Amarelo','32',43,282),(109,'Amarelo','67',43,268),(110,'Amarelo','25',44,293),(111,'Amarelo','58',44,305),(112,'Amarelo','19',45,291),(113,'Vermelho','77',45,296),(114,'Amarelo','41',46,302),(115,'Amarelo','74',46,281),(116,'Amarelo','35',47,301),(117,'Amarelo','68',47,270),(118,'Amarelo','29',48,289),(119,'Amarelo','63',48,283),(120,'Amarelo','37',49,392),(121,'Amarelo','72',49,359),(122,'Amarelo','27',50,382),(123,'Amarelo','64',50,368),(124,'Amarelo','48',51,372),(125,'Vermelho','89',51,391),(126,'Amarelo','33',52,378),(127,'Amarelo','70',52,357),(128,'Amarelo','18',53,379),(129,'Amarelo','56',53,385),(130,'Amarelo','42',54,366),(131,'Amarelo','79',54,360),(132,'Amarelo','41',55,415),(133,'Amarelo','75',55,403),(134,'Amarelo','34',56,436),(135,'Amarelo','69',56,425),(136,'Amarelo','28',57,427),(137,'Amarelo','71',57,402),(138,'Amarelo','37',58,438),(139,'Amarelo','82',58,410),(140,'Amarelo','27',59,437),(141,'Amarelo','63',59,401),(142,'Amarelo','44',60,426),(143,'Vermelho','86',60,417),(144,'Amarelo','38',61,458),(145,'Amarelo','72',61,447),(146,'Amarelo','26',62,480),(147,'Amarelo','59',62,469),(148,'Amarelo','84',62,478),(149,'Amarelo','23',63,476),(150,'Amarelo','61',63,481),(151,'Amarelo','34',64,466),(152,'Amarelo','78',64,456),(153,'Amarelo','31',65,470),(154,'Amarelo','74',65,446),(155,'Amarelo','45+1',66,477),(156,'Vermelho','82',66,460),(157,'Amarelo','43',67,525),(158,'Amarelo','77',67,493),(159,'Amarelo','28',68,513),(160,'Amarelo','56',68,502),(161,'Amarelo','84',68,515),(162,'Amarelo','37',69,511),(163,'Amarelo','69',69,490),(164,'Amarelo','41',70,500),(165,'Amarelo','76',70,520),(166,'Amarelo','23',71,504),(167,'Vermelho','68',71,505),(168,'Amarelo','35',72,528),(169,'Amarelo','64',72,509),(170,'Amarelo','88',72,524);
/*!40000 ALTER TABLE `cartoes` ENABLE KEYS */;
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
