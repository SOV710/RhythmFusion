-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: music_recommendation
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.24.04.1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add song',7,'add_song'),(26,'Can change song',7,'change_song'),(27,'Can delete song',7,'delete_song'),(28,'Can view song',7,'view_song'),(29,'Can add playlist',8,'add_playlist'),(30,'Can change playlist',8,'change_playlist'),(31,'Can delete playlist',8,'delete_playlist'),(32,'Can view playlist',8,'view_playlist'),(33,'Can add recommendation log',9,'add_recommendationlog'),(34,'Can change recommendation log',9,'change_recommendationlog'),(35,'Can delete recommendation log',9,'delete_recommendationlog'),(36,'Can view recommendation log',9,'view_recommendationlog'),(37,'Can add blacklisted token',10,'add_blacklistedtoken'),(38,'Can change blacklisted token',10,'change_blacklistedtoken'),(39,'Can delete blacklisted token',10,'delete_blacklistedtoken'),(40,'Can view blacklisted token',10,'view_blacklistedtoken'),(41,'Can add outstanding token',11,'add_outstandingtoken'),(42,'Can change outstanding token',11,'change_outstandingtoken'),(43,'Can delete outstanding token',11,'delete_outstandingtoken'),(44,'Can view outstanding token',11,'view_outstandingtoken');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(7,'music','song'),(8,'playlist','playlist'),(9,'recommendation','recommendationlog'),(5,'sessions','session'),(10,'token_blacklist','blacklistedtoken'),(11,'token_blacklist','outstandingtoken'),(6,'user','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-08 12:11:45.291755'),(2,'contenttypes','0002_remove_content_type_name','2025-04-08 12:11:45.353096'),(3,'auth','0001_initial','2025-04-08 12:11:45.572776'),(4,'auth','0002_alter_permission_name_max_length','2025-04-08 12:11:45.625734'),(5,'auth','0003_alter_user_email_max_length','2025-04-08 12:11:45.634968'),(6,'auth','0004_alter_user_username_opts','2025-04-08 12:11:45.643568'),(7,'auth','0005_alter_user_last_login_null','2025-04-08 12:11:45.651449'),(8,'auth','0006_require_contenttypes_0002','2025-04-08 12:11:45.653830'),(9,'auth','0007_alter_validators_add_error_messages','2025-04-08 12:11:45.658807'),(10,'auth','0008_alter_user_username_max_length','2025-04-08 12:11:45.663021'),(11,'auth','0009_alter_user_last_name_max_length','2025-04-08 12:11:45.667020'),(12,'auth','0010_alter_group_name_max_length','2025-04-08 12:11:45.674884'),(13,'auth','0011_update_proxy_permissions','2025-04-08 12:11:45.679781'),(14,'auth','0012_alter_user_first_name_max_length','2025-04-08 12:11:45.683825'),(15,'user','0001_initial','2025-04-08 12:11:45.938322'),(16,'admin','0001_initial','2025-04-08 12:11:46.053889'),(17,'admin','0002_logentry_remove_auto_add','2025-04-08 12:11:46.064103'),(18,'admin','0003_logentry_add_action_flag_choices','2025-04-08 12:11:46.071233'),(19,'music','0001_initial','2025-04-08 12:11:46.084951'),(20,'music','0002_remove_song_duration_song_school','2025-04-08 12:11:46.153185'),(21,'playlist','0001_initial','2025-04-08 12:11:46.322053'),(22,'recommendation','0001_initial','2025-04-08 12:11:46.391026'),(23,'sessions','0001_initial','2025-04-08 12:11:46.424472'),(24,'recommendation','0002_drop_api_tables','2025-05-01 17:41:18.468012'),(25,'playlist','0002_alter_playlist_options_rename_user_playlist_owner_and_more','2025-05-03 15:59:57.079323'),(26,'token_blacklist','0001_initial','2025-05-03 15:59:57.194891'),(27,'token_blacklist','0002_outstandingtoken_jti_hex','2025-05-03 15:59:57.239755'),(28,'token_blacklist','0003_auto_20171017_2007','2025-05-03 15:59:57.257814'),(29,'token_blacklist','0004_auto_20171017_2013','2025-05-03 15:59:57.302505'),(30,'token_blacklist','0005_remove_outstandingtoken_jti','2025-05-03 15:59:57.345909'),(31,'token_blacklist','0006_auto_20171017_2113','2025-05-03 15:59:57.374106'),(32,'token_blacklist','0007_auto_20171017_2214','2025-05-03 15:59:57.509705'),(33,'token_blacklist','0008_migrate_to_bigautofield','2025-05-03 15:59:57.667109'),(34,'token_blacklist','0010_fix_migrate_to_bigautofield','2025-05-03 15:59:57.685738'),(35,'token_blacklist','0011_linearizes_history','2025-05-03 15:59:57.687802'),(36,'token_blacklist','0012_alter_outstandingtoken_user','2025-05-03 15:59:57.696455');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2c25m31ujdo2ebjzmvnkwtkycuga68vg','.eJxVjEEOwiAQRe_C2hCYlgFcuvcMZMpMpWpoUtqV8e7apAvd_vfef6lE21rS1mRJE6uzsur0uw2UH1J3wHeqt1nnua7LNOhd0Qdt-jqzPC-H-3dQqJVvbSyZICPGGKh3gZxBdA6YACKDtZ46AewzGuyERgD0NuToTeYMiKDeH7cTNq0:1uBcvK:BOReFs9-YQiplCk2qeuU0A2akBj7h70yuQ0-G4zT7rs','2025-05-18 17:14:42.320097'),('2mtoqu03v6xiwk3bwefiny1cywfo0wgs','.eJxVjMsOwiAQRf-FtSGAlIdL9_0GMsMMUjU0Ke3K-O_apAvd3nPOfYkE21rT1nlJE4mL0OL0uyHkB7cd0B3abZZ5busyodwVedAux5n4eT3cv4MKvX5rwxELW4gaNCEZV0wOXAoam11kV0BjiN4rZZWPCgwoosD-7HBAZQbx_gAM8Thc:1u2Tiy:8lK6ncrBcHqk5ytHMk0548VxSkH3MdvN8w4j_Id9BVs','2025-04-23 11:36:08.618078'),('gq27kvn4yz89yx4vry0g8ydn22b9hqau','.eJxVjMsOwiAQRf-FtSGAlIdL9_0GMsMMUjU0Ke3K-O_apAvd3nPOfYkE21rT1nlJE4mL0OL0uyHkB7cd0B3abZZ5busyodwVedAux5n4eT3cv4MKvX5rwxELW4gaNCEZV0wOXAoam11kV0BjiN4rZZWPCgwoosD-7HBAZQbx_gAM8Thc:1u2SB8:FhCl0Fqd7_ja75GKqtjuHBBCeg5KlTjLvwboW2Zdsns','2025-04-23 09:57:06.010314'),('y8jt73v44tln8k4o1j05qjpsfm62ss7k','.eJxVjMsOwiAQRf-FtSGAlIdL9_0GMsMMUjU0Ke3K-O_apAvd3nPOfYkE21rT1nlJE4mL0OL0uyHkB7cd0B3abZZ5busyodwVedAux5n4eT3cv4MKvX5rwxELW4gaNCEZV0wOXAoam11kV0BjiN4rZZWPCgwoosD-7HBAZQbx_gAM8Thc:1u27ox:RVJu5hmcVQ8wWI-KDOhlyQv7M8YXp5cCtbYfURkcwWY','2025-04-22 12:12:51.694993');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `music_song`
--

DROP TABLE IF EXISTS `music_song`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `music_song` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `artist` varchar(255) NOT NULL,
  `school` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `music_song`
--

LOCK TABLES `music_song` WRITE;
/*!40000 ALTER TABLE `music_song` DISABLE KEYS */;
INSERT INTO `music_song` VALUES (1,'Sunny','yorushika','jpop'),(2,'That\'s Why I Gave Up on Music','yorushika','jpop');
/*!40000 ALTER TABLE `music_song` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlists`
--

DROP TABLE IF EXISTS `playlists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playlists` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `owner_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `playlist_playlist_owner_id_name_798f2454_uniq` (`owner_id`,`name`),
  CONSTRAINT `playlist_playlist_owner_id_1072c3f8_fk_users_id` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlists`
--

LOCK TABLES `playlists` WRITE;
/*!40000 ALTER TABLE `playlists` DISABLE KEYS */;
/*!40000 ALTER TABLE `playlists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlists_songs`
--

DROP TABLE IF EXISTS `playlists_songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playlists_songs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `playlist_id` bigint NOT NULL,
  `song_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `playlist_playlist_songs_playlist_id_song_id_647c955f_uniq` (`playlist_id`,`song_id`),
  KEY `playlist_playlist_songs_song_id_c456a98c_fk_music_song_id` (`song_id`),
  CONSTRAINT `playlist_playlist_so_playlist_id_8be6fd09_fk_playlist_` FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`id`),
  CONSTRAINT `playlist_playlist_songs_song_id_c456a98c_fk_music_song_id` FOREIGN KEY (`song_id`) REFERENCES `music_song` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlists_songs`
--

LOCK TABLES `playlists_songs` WRITE;
/*!40000 ALTER TABLE `playlists_songs` DISABLE KEYS */;
/*!40000 ALTER TABLE `playlists_songs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

LOCK TABLES `token_blacklist_blacklistedtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
INSERT INTO `token_blacklist_blacklistedtoken` VALUES (1,'2025-05-04 07:00:35.193898',19),(2,'2025-05-04 07:48:59.174851',21),(3,'2025-05-04 16:35:55.136016',22),(4,'2025-05-05 00:40:30.831240',23),(5,'2025-05-05 04:23:10.258459',25),(6,'2025-05-05 04:25:42.166822',26),(7,'2025-05-05 04:27:16.377103',27),(8,'2025-05-05 04:54:14.376448',28),(9,'2025-05-05 04:54:48.286502',29),(10,'2025-05-05 04:55:09.332901',30),(11,'2025-05-05 05:21:21.914367',31),(12,'2025-05-05 12:59:31.383329',32),(13,'2025-05-05 13:02:54.968892',33),(14,'2025-05-05 15:38:05.552351',35),(15,'2025-05-05 16:34:31.698079',36);
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id` (`user_id`),
  CONSTRAINT `token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
INSERT INTO `token_blacklist_outstandingtoken` VALUES (1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjM3NTc0MSwiaWF0IjoxNzQ2Mjg5MzQxLCJqdGkiOiJlOTllNGY0MzdkMTY0NzY4YWVmM2RkZGI3ZWNmNWY5ZiIsInVzZXJfaWQiOjJ9.aPgX-7XUahbpgMA4vvlruQ2RjqQSimnGc_0CfwgPMwY','2025-05-03 16:22:21.399328','2025-05-04 16:22:21.000000',2,'e99e4f437d164768aef3dddb7ecf5f9f'),(2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjM3NzE4NCwiaWF0IjoxNzQ2MjkwNzg0LCJqdGkiOiJiODUyY2IzZWQ4NWQ0ZWI4OWRiYTczOGEyYjU0MjA4OCIsInVzZXJfaWQiOjJ9._8rh8Grvb9YmLIaWnD3ojKc-XJVhkmyhKlDp5jdSrMw','2025-05-03 16:46:24.166442','2025-05-04 16:46:24.000000',2,'b852cb3ed85d4eb89dba738a2b542088'),(3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQxMTA1MywiaWF0IjoxNzQ2MzI0NjUzLCJqdGkiOiJhMTkyNzE5ZmNkMmE0NjE0YmMyNzEwYWRiNDJjMDY1NiIsInVzZXJfaWQiOjJ9.iSTpPzCgDiE6aH9HFsPDwlNe7naR25XbDEb9rghchOc','2025-05-04 02:10:53.607081','2025-05-05 02:10:53.000000',2,'a192719fcd2a4614bc2710adb42c0656'),(4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQxMTI1NywiaWF0IjoxNzQ2MzI0ODU3LCJqdGkiOiIxY2IzMjFmYmJiZTQ0MzNhODJlMTk1ZjgyNDBlYTMxNiIsInVzZXJfaWQiOjJ9.UoH-xtzHLwjlqXnQtpBHUZA9FuG40Ay7LulMRvQPLW4','2025-05-04 02:14:17.077007','2025-05-05 02:14:17.000000',2,'1cb321fbbbe4433a82e195f8240ea316'),(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQxMTMwOCwiaWF0IjoxNzQ2MzI0OTA4LCJqdGkiOiIyMWE5MDdiMmU3MjU0MjQwODhhNGVjNjY5MWJkOGQ3OCIsInVzZXJfaWQiOjJ9.FTnHNFfzSRLx_j8Tnex-0Z8K1EvO09NsGy9xHhEIuFc','2025-05-04 02:15:08.683722','2025-05-05 02:15:08.000000',2,'21a907b2e725424088a4ec6691bd8d78'),(6,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQxMTM3OCwiaWF0IjoxNzQ2MzI0OTc4LCJqdGkiOiI2NmJkZjc3YTUzY2M0NGNhODg5MWI3YjU2Y2MyNjdmNyIsInVzZXJfaWQiOjJ9.TOoR4tcRDSRAYwqC_NE4Pw6_fK9xZonAgXt_y4WGdgU','2025-05-04 02:16:18.411688','2025-05-05 02:16:18.000000',2,'66bdf77a53cc44ca8891b7b56cc267f7'),(7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQxMTQzMiwiaWF0IjoxNzQ2MzI1MDMyLCJqdGkiOiI4MGU0NDE0OTQ4MmE0MzM1YTY4NWFjMzEzYmNkNjJmZSIsInVzZXJfaWQiOjJ9.l5hF8SGr6Ftyc3JmJPkI0VDRkOVkLErrjwkiqFo5bMo','2025-05-04 02:17:12.369035','2025-05-05 02:17:12.000000',2,'80e44149482a4335a685ac313bcd62fe'),(8,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQxMTQ1MywiaWF0IjoxNzQ2MzI1MDUzLCJqdGkiOiI5YmIyM2JhMmNiZmY0ODJiYTBhYTFhYmIzYzc0MmJlZiIsInVzZXJfaWQiOjJ9.1TP1ObD5wTXyISN4DKkHsPWzm4CpP_Fgc7GJcCWVOV0','2025-05-04 02:17:33.877032','2025-05-05 02:17:33.000000',2,'9bb23ba2cbff482ba0aa1abb3c742bef'),(9,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQxMTU4MCwiaWF0IjoxNzQ2MzI1MTgwLCJqdGkiOiIzN2U0NmM4NWZiY2Y0Njc3ODJkMDJlYzgyMTFhY2EyNiIsInVzZXJfaWQiOjJ9.sSrP72CBDkJeMUAvrXx7R0EVi7IYtYyCUcjNlFnpJtE','2025-05-04 02:19:40.859485','2025-05-05 02:19:40.000000',2,'37e46c85fbcf467782d02ec8211aca26'),(10,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQxMTcyNCwiaWF0IjoxNzQ2MzI1MzI0LCJqdGkiOiI2OTRhZWNhYTcwMWE0NzMyYWQ4NWYwYjM1MDliYWFlNiIsInVzZXJfaWQiOjJ9.bRWiD5nLR8U58mziuWOAy2VUcb8BlL_1E3Fcmig8KRM','2025-05-04 02:22:04.725095','2025-05-05 02:22:04.000000',2,'694aecaa701a4732ad85f0b3509baae6'),(11,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQxMTc0MiwiaWF0IjoxNzQ2MzI1MzQyLCJqdGkiOiJhZWE5YTk3NDg1YzU0OTY4YTE4MDljZGY1MjhiZDU1NiIsInVzZXJfaWQiOjJ9.7aFiW3Iw5YC0XZBe8-bzCLHQ7I85w4GRvvDW8T0e1YA','2025-05-04 02:22:22.942449','2025-05-05 02:22:22.000000',2,'aea9a97485c54968a1809cdf528bd556'),(12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQyMjA5MSwiaWF0IjoxNzQ2MzM1NjkxLCJqdGkiOiI4YzQyNGUxZTI4MWY0OWU3ODc3Mjk5NDY0OTAwOTE1MSIsInVzZXJfaWQiOjJ9.vBAXEU7cqluHGhccat3uMUaxLhlkvANqzXvs3myk18c','2025-05-04 05:14:51.780013','2025-05-05 05:14:51.000000',2,'8c424e1e281f49e78772994649009151'),(13,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQyNzE5OCwiaWF0IjoxNzQ2MzQwNzk4LCJqdGkiOiI4MWQ2NjFlZWZkMDE0ZTU0YjE1NGU1ZmRlNTQ1YmFiMyIsInVzZXJfaWQiOjJ9.vCeY3zAoXeQ6No6OV1ewT7AryPeQehNP8SxMwPcBC7k','2025-05-04 06:39:58.344190','2025-05-05 06:39:58.000000',2,'81d661eefd014e54b154e5fde545bab3'),(14,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQyNzM1NSwiaWF0IjoxNzQ2MzQwOTU1LCJqdGkiOiJjMjk2ZjIxM2U1OTY0MzRkODUyZWQ0ZTVkYjA3ZmY5MiIsInVzZXJfaWQiOjJ9.G9BJQseF6FK1yR3QQL2J7MzeepIcke7t5D1pW3GVdJk','2025-05-04 06:42:35.434831','2025-05-05 06:42:35.000000',2,'c296f213e596434d852ed4e5db07ff92'),(15,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQyNzU3MiwiaWF0IjoxNzQ2MzQxMTcyLCJqdGkiOiIwN2I0NjgwNjU4MjY0NTVlOTljMDk5NWEwMzcyODIyZCIsInVzZXJfaWQiOjJ9.cCYqAhpkFyA4M44rLKliAq-qS8Ph7Td4qmwl5MQbg2E','2025-05-04 06:46:12.272750','2025-05-05 06:46:12.000000',2,'07b468065826455e99c0995a0372822d'),(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQyNzU5NywiaWF0IjoxNzQ2MzQxMTk3LCJqdGkiOiJjMGM1ZDBlNGExNTE0N2RjYmNhZTFmN2E3MmZkMDllZSIsInVzZXJfaWQiOjJ9.J9Ms00c3H9pjoDRA2xVirgk6VfOxJVrG90GsWwEN1gw','2025-05-04 06:46:37.884833','2025-05-05 06:46:37.000000',2,'c0c5d0e4a15147dcbcae1f7a72fd09ee'),(17,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQyNzYzMCwiaWF0IjoxNzQ2MzQxMjMwLCJqdGkiOiIzOWIwYjM4NmE3NmE0MmE3ODJmNmUxODMyNDM1MDE5NSIsInVzZXJfaWQiOjJ9.qn_SmBi1_2oM3kt1aLftgIxmL_OzMkJds_Y6Z0qFPWY','2025-05-04 06:47:10.648558','2025-05-05 06:47:10.000000',2,'39b0b386a76a42a782f6e18324350195'),(18,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQyODE1NSwiaWF0IjoxNzQ2MzQxNzU1LCJqdGkiOiI5NzU2YWM0MTQ4OWE0M2NmYjdhZjUxZTc1MjVmNTM5ZSIsInVzZXJfaWQiOjJ9.OKnp_KWpUZ7cKhVq0k8YUqctIHU4iUhvgAF2ZQ6dU5g','2025-05-04 06:55:55.977530','2025-05-05 06:55:55.000000',2,'9756ac41489a43cfb7af51e7525f539e'),(19,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQyODQzNSwiaWF0IjoxNzQ2MzQyMDM1LCJqdGkiOiIwMTJjNWEwMTYxMzM0OTUzOTY4ZWI5YTBkODEwYzQ3OCIsInVzZXJfaWQiOjJ9.BvrwztF-hdIS2JULCabuvI2hbtgWeGM43SjnwzMsg3Q','2025-05-04 07:00:35.154879','2025-05-05 07:00:35.000000',2,'012c5a0161334953968eb9a0d810c478'),(20,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQyOTQ2MywiaWF0IjoxNzQ2MzQzMDYzLCJqdGkiOiJiZWMxOTM5YTBjM2Q0NjhiODAzMmU5MGIyNjczNWRiNiIsInVzZXJfaWQiOjJ9.Rjc1Pxv6FVZ9VPFCLu34yx2pPKNKvvNhxQty1qMxWrQ','2025-05-04 07:17:43.185177','2025-05-05 07:17:43.000000',2,'bec1939a0c3d468b8032e90b26735db6'),(21,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQzMTMzOSwiaWF0IjoxNzQ2MzQ0OTM5LCJqdGkiOiJiMmI1MGEyMzYxNWM0NTBjYTVjZmIyYjUwZDkwNTZhMSIsInVzZXJfaWQiOjJ9.OGoVEb11sYSsgHGA22NKtmqALYsbzMw2gvdSVT60ADE','2025-05-04 07:48:59.141002','2025-05-05 07:48:59.000000',2,'b2b50a23615c450ca5cfb2b50d9056a1'),(22,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQ2Mjk1NSwiaWF0IjoxNzQ2Mzc2NTU1LCJqdGkiOiJlNjJlYTBiOWY3ODY0YjZjYjUzOGNiMWYwYmZiMjNmYyIsInVzZXJfaWQiOjJ9.19SQDEiRociaiGXXCutBfqB75M8sqxSLpcdtv--QOvo','2025-05-04 16:35:55.102570','2025-05-05 16:35:55.000000',2,'e62ea0b9f7864b6cb538cb1f0bfb23fc'),(23,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQ5MjAzMCwiaWF0IjoxNzQ2NDA1NjMwLCJqdGkiOiI5MTg5MGYwYzNlZjY0MGJhOTJmNTQ4MGUxYTc1N2FjYSIsInVzZXJfaWQiOjJ9.AH5IyF518n_vQnME1L8OmiQOxJnOu8x8HT3PK_emBUk','2025-05-05 00:40:30.803828','2025-05-06 00:40:30.000000',2,'91890f0c3ef640ba92f5480e1a757aca'),(24,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjQ5MjI1MSwiaWF0IjoxNzQ2NDA1ODUxLCJqdGkiOiJiMjY2MjZhYTBkZDg0MGQ4YjIzNzE0N2JhMTY3ZjFiMyIsInVzZXJfaWQiOjJ9.RilPVQlkzoXrFOfiCtezt7bIDx5noI50iRbkTfHeEDA','2025-05-05 00:44:11.037491','2025-05-06 00:44:11.000000',2,'b26626aa0dd840d8b237147ba167f1b3'),(25,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjUwNTM5MCwiaWF0IjoxNzQ2NDE4OTkwLCJqdGkiOiI0ZTFmMDZiNTQyNmQ0MWExOGNhNjBkMmVkYzQ5MDMyYiIsInVzZXJfaWQiOjJ9.dHyWkdaE6W4AzcmFtFxYz-htqqLA67iDzfdP0XO9_qg','2025-05-05 04:23:10.233330','2025-05-06 04:23:10.000000',2,'4e1f06b5426d41a18ca60d2edc49032b'),(26,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjUwNTU0MiwiaWF0IjoxNzQ2NDE5MTQyLCJqdGkiOiIxNDQ1Njc4ZjAyMTY0OTZhYWI4MDVhMTMwYTgyM2M0YSIsInVzZXJfaWQiOjJ9.7_EAsrmr6duqd5NxUn-GJNQZRU1q5U77BGJTvAjmFvw','2025-05-05 04:25:42.140487','2025-05-06 04:25:42.000000',2,'1445678f0216496aab805a130a823c4a'),(27,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjUwNTYzNiwiaWF0IjoxNzQ2NDE5MjM2LCJqdGkiOiJlMTA4NzM4YWViYTg0YWVjYmViMGE2ZjA0ZGM4ODU5ZSIsInVzZXJfaWQiOjJ9.WVjefoaUKNgshjD81ugh2mpa09Ghr0nYhMoocfrf8WY','2025-05-05 04:27:16.348283','2025-05-06 04:27:16.000000',2,'e108738aeba84aecbeb0a6f04dc8859e'),(28,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjUwNzI1NCwiaWF0IjoxNzQ2NDIwODU0LCJqdGkiOiI5YmNlOGY4MmM1ZmI0YjFkOTU0ZDNhYTA3ZTU0NWYyMyIsInVzZXJfaWQiOjJ9.L2tvsTkxrTM2z0sBR1aOw-ZGGV8xzsRsRX_iN4cjxNg','2025-05-05 04:54:14.341610','2025-05-06 04:54:14.000000',2,'9bce8f82c5fb4b1d954d3aa07e545f23'),(29,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjUwNzI4OCwiaWF0IjoxNzQ2NDIwODg4LCJqdGkiOiI3OTcwMWI3ZGM3Y2M0NTQ1YjIyYjYwMTgyMTQ2YzgyZiIsInVzZXJfaWQiOjJ9.hWpWL4tdW3EUjepl21j771PCIdAWOpxIh5oMFOuN50M','2025-05-05 04:54:48.260391','2025-05-06 04:54:48.000000',2,'79701b7dc7cc4545b22b60182146c82f'),(30,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjUwNzMwOSwiaWF0IjoxNzQ2NDIwOTA5LCJqdGkiOiJiYzEzNDVmNGYyZjE0OWYyYWQxODU0M2FlYTNiYTc3OCIsInVzZXJfaWQiOjJ9.nUOEQcKxpFS2Gx_GF0FcMuhpJEVcdfIn1Y_CpzinG78','2025-05-05 04:55:09.307882','2025-05-06 04:55:09.000000',2,'bc1345f4f2f149f2ad18543aea3ba778'),(31,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjUwODg4MSwiaWF0IjoxNzQ2NDIyNDgxLCJqdGkiOiIyYjU0MGMzNjA0ZWE0OTY4OWQzNjRlYjBkMmNkNmQ5OSIsInVzZXJfaWQiOjJ9.5oklgMStyoulySL5QZIU4x09R7R3am3GDDDDWAjyoTI','2025-05-05 05:21:21.887021','2025-05-06 05:21:21.000000',2,'2b540c3604ea49689d364eb0d2cd6d99'),(32,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjUzNjM3MSwiaWF0IjoxNzQ2NDQ5OTcxLCJqdGkiOiI2NDAwMTQ3ZDU0Yjg0YzRjOGVjYjgxZjVmYjJkNDQ0OSIsInVzZXJfaWQiOjJ9.MbBILVSaYGOTaSwkxO9KRmaa9DPIrav8jJ7jVHGr-jE','2025-05-05 12:59:31.332091','2025-05-06 12:59:31.000000',2,'6400147d54b84c4c8ecb81f5fb2d4449'),(33,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjUzNjU3NCwiaWF0IjoxNzQ2NDUwMTc0LCJqdGkiOiJkNWMzMGVlZjA5YmI0MGM5YjRjYjhmOTg1YTM1YWIxNCIsInVzZXJfaWQiOjJ9.Og1WTpI_W9gUaD2jBDCtC6U7sjBOZEiSYJHWfvO9uOA','2025-05-05 13:02:54.943360','2025-05-06 13:02:54.000000',2,'d5c30eef09bb40c9b4cb8f985a35ab14'),(34,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjUzODk1MSwiaWF0IjoxNzQ2NDUyNTUxLCJqdGkiOiJkYWVlNjE2OWMxM2M0NWE5ODdlZjM4ZmI5NjY3NTdkMCIsInVzZXJfaWQiOjJ9.ZLDUuEJ0CiOh8l1v4-I-oqObafej-cL_12pWfscgU9g','2025-05-05 13:42:31.048570','2025-05-06 13:42:31.000000',2,'daee6169c13c45a987ef38fb966757d0'),(35,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjU0NTUyNSwiaWF0IjoxNzQ2NDU5MTI1LCJqdGkiOiI0Yzk3YTY3YWZhNTY0OTc4YWJiZDRkYWQ2MGIwMTRjNSIsInVzZXJfaWQiOjJ9.fx1Ou9LlNMfVnFkNHNEF-Gv_8mbKvpvVJD57mFWNiww','2025-05-05 15:32:05.422379','2025-05-06 15:32:05.000000',2,'4c97a67afa564978abbd4dad60b014c5'),(36,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjU0ODkxMSwiaWF0IjoxNzQ2NDYyNTExLCJqdGkiOiJkZTlhZTViNjM3NzY0MzZjYjBiNWRjN2Q4ZDg0MjJkYyIsInVzZXJfaWQiOjh9.bzknqEZzJEBvTu1BOoWus-xi5rXXNOvCPEh_T2V7lQE','2025-05-05 16:28:31.576750','2025-05-06 16:28:31.000000',8,'de9ae5b63776436cb0b5dc7d8d8422dc');
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `bio` longtext NOT NULL,
  `birth_date` date DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'pbkdf2_sha256$720000$38FRV3ALC9sz7kWDLskWF3$DBNoHB2GnJHZAvQCogis9CdH7krhT6vn1O0kH+BKtwo=','2025-05-04 17:14:42.318050',1,'chris','','','chris916911179@outlook.com',1,1,'2025-04-08 12:12:25.800242','',NULL,'','2025-04-08 12:12:25.941703','2025-04-08 12:12:25.941712'),(2,'pbkdf2_sha256$720000$TOdJKDWRSrUf91NrujifSu$2QsoPxh/UTfmJPP8ChqDypLc3LPoItfEpVs3qGumPu4=',NULL,0,'admin','','','',0,1,'2025-05-03 16:17:22.773997','',NULL,'','2025-05-03 16:17:22.899918','2025-05-03 16:17:22.899925'),(8,'pbkdf2_sha256$720000$dnMtxGAA5PV05D9fYX4N2W$l2oCkyl4VwhnSZsBlXmqMLwjd6eqjyCwRNdx7Tq1QzE=',NULL,0,'test','','','test@example.com',0,1,'2025-05-05 16:28:31.318578','',NULL,'','2025-05-05 16:28:31.445923','2025-05-05 16:28:31.445930');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_groups`
--

DROP TABLE IF EXISTS `users_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_groups_user_id_group_id_fc7788e8_uniq` (`user_id`,`group_id`),
  KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_groups_user_id_f500bee5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_groups`
--

LOCK TABLES `users_groups` WRITE;
/*!40000 ALTER TABLE `users_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_permissions`
--

DROP TABLE IF EXISTS `users_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_permissions_user_id_permission_id_3b86cbdf_uniq` (`user_id`,`permission_id`),
  KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_permissions_user_id_92473840_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_permissions`
--

LOCK TABLES `users_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-11  1:37:19
