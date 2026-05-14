-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: clinic_db
-- ------------------------------------------------------
-- Server version	8.0.45-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `sr_code` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `sr_code` (`sr_code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'admin','scrypt:32768:8:1$Y1Qm6DpCpWncKxEp$bce86f39865b8dc16b9e990856d8dfbfde0dd31fbbb3c77b2d0ed05c09c793d82b07cd3d7a304496e9403364b9995f31b4eeb37804be6261dbe00bbb7f27831a');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medical_records`
--

DROP TABLE IF EXISTS `medical_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `sr_code` varchar(20) DEFAULT NULL,
  `fullname` varchar(255) DEFAULT NULL,
  `college` varchar(100) DEFAULT NULL,
  `program` varchar(100) DEFAULT NULL,
  `year_level` varchar(20) DEFAULT NULL,
  `blood_type` varchar(10) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `parent_contact` varchar(50) DEFAULT NULL,
  `visit_history` text,
  `allergies` varchar(255) DEFAULT 'None',
  `medications` varchar(255) DEFAULT 'None',
  `referral_status` varchar(100) DEFAULT 'Clear',
  PRIMARY KEY (`record_id`),
  KEY `sr_code` (`sr_code`),
  CONSTRAINT `medical_records_ibfk_1` FOREIGN KEY (`sr_code`) REFERENCES `students` (`sr_code`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_records`
--

LOCK TABLES `medical_records` WRITE;
/*!40000 ALTER TABLE `medical_records` DISABLE KEYS */;
INSERT INTO `medical_records` VALUES (1,'12-34567','Dela Cruz, Juan A.','Engineering','Computer Engineering','2nd','O+','2006-01-18','Alangilan, Batangas City, Batangas','09958744457','Visit: Fever-July 03, 2026','Asthma','None','Clear'),(3,'24-09937','Mangubat, Angelica S.','CICS','Computer Science',NULL,NULL,NULL,NULL,NULL,NULL,'None','None','Clear'),(4,'20-12345','Santos, Jose L.','Engineering','Computer Engineering',NULL,'B+','2001-06-15','Rosario, Batangas','09685321478','Headache-February 12, 2026','NONE','None','Clear');
/*!40000 ALTER TABLE `medical_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sr_code` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sr_code` (`sr_code`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'12-34567','scrypt:32768:8:1$x5Pc9Uj5X65lAn21$0d1e5ddc38fb16c30d1eb5caba8c79956c9661883b282f55d3af80c64db46026c1aa5968e8d9c42c36d95d2ad28f0fb7b286db100a6dc3a2c36c730340482e13'),(9,'24-09937','scrypt:32768:8:1$qqsJ3mjnEy9NYLPo$a4aa318acb402edbad060d33b62432bec35a854fdbfc6a45d863be6f9728240c1402f3055bc9eb88a9d6c897007c48206c3cb3c2149469666c70ecc74d4a0c59'),(10,'20-12345','scrypt:32768:8:1$oKkoWO1wFFApqIpn$dcc964d84ff51e9f9490c6737bfa903b1ebe2ccdd9aae7257f36e685164c78d6dc5afaf1004128fe196ecafb55909015924283bd253c20a2becebbacc552df7d');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-13  8:14:06
