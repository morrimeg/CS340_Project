-- MySQL dump 10.16  Distrib 10.1.35-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: hwp
-- ------------------------------------------------------
-- Server version	10.1.35-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

USE `cs340_lundgret`;

--
-- Table structure for table `vets`
--

DROP TABLE IF EXISTS `vets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE IF NOT EXISTS `vets` (

  `vet_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `specialty` varchar(255) NOT NULL,
  PRIMARY KEY(`vet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Insert into `vets` table
--
LOCK TABLES `vets` WRITE;
/*!40000 ALTER TABLE `vets` DISABLE KEYS */;
INSERT INTO `vets` (first_name, last_name, email, phone, specialty)
  VALUES
  ('Samantha', 'Sukej', 'ssukej@hwp.org', '6501234567', 'Feline'),
  ('Aaron', 'Wu', 'awu@hwp.org', '6509876543', 'Avian and Canine'),
  ('Michael', 'Cui', 'mcui@hwp.org', '6502481632', 'Reptile'),
  ('Elise', 'Noalhyt', 'enoalhyt@hwp.org', '6504132020', 'Canine')
;
/*!40000 ALTER TABLE `vets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE IF NOT EXISTS `customers` (

  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zip_code` char(5) NOT NULL,
  PRIMARY KEY(`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Insert into `customers` table
--
LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` (first_name, last_name, email, phone, address, city, state, zip_code)
  VALUES
  ('Mbali', 'Octavius', 'mbali@gmail.com', '7703523154', '342 Elsie Way', 'Mountain View', 'CA', '94040'),
  ('Sabina', 'Pitts', 'spitts@gmail.com', '3364952773', '2201 Deland Rd', 'Sunnyvale', 'CA', '94087'),
  ('Sundar', 'Pichai', 'sundar@google.com', '6505005931', '100 Innovation Way', 'Mountain View', 'CA', '94040'),
  ('Mira', 'Magee', 'mmagee@gmail.com', '6502381394', '597 Palomino Ave', 'Palo Alto', 'CA', '94028')
;
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pets`
--

DROP TABLE IF EXISTS `pets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE IF NOT EXISTS `pets` (

  `pet_id` int(11) NOT NULL AUTO_INCREMENT,
  `pet_name` varchar(255) NOT NULL,
  `species` varchar(255) NOT NULL,
  `breed` varchar(255) NOT NULL,
  `age` int(11) NOT NULL,
  `gender` binary NOT NULL,
  `vet_id` int(11),
  `customer_id` int(11) NOT NULL,
  PRIMARY KEY(`pet_id`),
  CONSTRAINT 
    foreign key(`vet_id`) references vets(vet_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT
    foreign key(`customer_id`) references customers(customer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Insert into `pets`
--
LOCK TABLES `pets` WRITE, `vets` READ, `customers` READ;
/*!40000 ALTER TABLE `pets` DISABLE KEYS */;

INSERT INTO `pets` (pet_name, species, breed, age, gender, vet_id, customer_id) values ('Kirby', 'Canine', 'Cavalier King Charles Spaniel', 1, 0,
  (SELECT vet_id FROM vets WHERE first_name = 'Elise' and last_name = 'Noalhyt'),
  (SELECT customer_id FROM customers WHERE first_name = 'Mbali' and last_name = 'Octavius')
);

INSERT INTO `pets` (pet_name, species, breed, age, gender, vet_id, customer_id) values ('Scout', 'Canine', 'Springer Spaniel', 11, 0,
  (SELECT vet_id FROM vets WHERE first_name = 'Elise' and last_name = 'Noalhyt'),
  (SELECT customer_id FROM customers WHERE first_name = 'Mira' and last_name = 'Magee')
);

INSERT INTO `pets` (pet_name, species, breed, age, gender, vet_id, customer_id) values ('Chairman Meow', 'Feline', 'Persian', 14, 0,
  (SELECT vet_id FROM vets WHERE first_name = 'Samantha' and last_name = 'Sukej'),
  (SELECT customer_id FROM customers WHERE first_name = 'Sundar' and last_name = 'Pichai')
);
/*!40000 ALTER TABLE `pets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE IF NOT EXISTS `classes`(

  `class_id` int(11) NOT NULL AUTO_INCREMENT,
  `class_name` varchar(255) NOT NULL,
  `class_description` varchar(255) NOT NULL,
  `class_day` date NOT NULL,
  `class_time` datetime NOT NULL,
  `class_price` decimal NOT NULL,
  `class_enrollments` int(11) NOT NULL,
  `class_seats` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  PRIMARY KEY(`class_id`),
  CONSTRAINT
    foreign key(`teacher_id`) references teachers(teacher_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `class_name` UNIQUE(`class_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

-- 
-- Insert into `classes`
--
LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;

INSERT INTO `classes` (class_name, class_description, class_day, class_time, class_price, class_enrollments, class_seats) values ('Puppy Training', 'For puppies age 5-8 weeks. Learn basic commands and get socialized', '2021-02-15', '2021-02-15 13:00:00', 100.00, 5, 10);
INSERT INTO `classes` (class_name, class_description, class_day, class_time, class_price, class_enrollments, class_seats) values ('Cat Walking', 'Train your cat to walk on a leash just like dogs!', '2021-03-01', '2021-03-01 10:00:00', 150.00, 10, 15);
INSERT INTO `classes` (class_name, class_description, class_day, class_time, class_price, class_enrollments, class_seats) values ('Young Dog Training', 'For dogs aged 1-4. Learn basic commands and behavioral tips and tricks.', '2021-02-27', '2021-02-27 14:00:00', 80.00, 4, 8);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE IF NOT EXISTS `teachers` (

  `teacher_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  PRIMARY KEY(`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Insert into `teachers` table
--
LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` (first_name, last_name, email, phone)
  VALUES
  ('Camille', 'Massoneau', 'cmass@hwp.org', '6501392347'),
  ('Harrison', 'Hemsworth', 'hhems@hwp.org', '650983243'),
  ('Sonia', 'Nordstrom', 'snord@hwp.org', '6509761632'),
  ('Claire', 'Pond', 'cpond@hwp.org', '6502120820')
;
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for `enrollments` table (M:M Relationship)
--

DROP TABLE IF EXISTS `enrollments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE IF NOT EXISTS `enrollments` (

  `enrollment_id` int(11) NOT NULL AUTO_INCREMENT,
  `pet_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  PRIMARY KEY(`enrollment_id`),
  CONSTRAINT
    foreign key(`pet_id`) references pets(pet_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT
    foreign key(`class_id`) references classes(class_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Insert into Enrollments
--
LOCK TABLES `enrollments` WRITE, `pets` READ, `classes` READ;
/*!40000 ALTER TABLE `enrollments` DISABLE KEYS */;
INSERT INTO `enrollments` (pet_id, class_id) values (
  (SELECT pet_id FROM pets WHERE pet_name = "Kirby"),
  (SELECT class_id FROM classes WHERE class_name = 'Puppy Training')
);

INSERT INTO `enrollments` (pet_id, class_id) values (
  (SELECT pet_id FROM pets WHERE pet_name = 'Chairman Meow'),
  (SELECT class_id FROM classes WHERE class_name = 'Cat Walking')

);


INSERT INTO `enrollments` (pet_id, class_id) values (
  (SELECT pet_id FROM pets WHERE pet_name = 'Kirby'),
  (SELECT class_id FROM classes WHERE class_name = 'Young Dog Training')

);
/*!40000 ALTER TABLE `enrollments` ENABLE KEYS */;
UNLOCK TABLES;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-28 13:23:54
