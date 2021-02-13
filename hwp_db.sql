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

--
-- Table structure for table `vets`
--

DROP TABLE IF EXISTS `vets`;
CREATE TABLE IF NOT EXISTS `vets` (

  `vet_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `specialty` varchar(255) NOT NULL,
  PRIMARY KEY(`vet_id`)
);

--
-- Insert into `vets` table
--
LOCK TABLES `vets` WRITE;
INSERT INTO `vets` (first_name, last_name, email, phone, specialty, number_of_patients)
  VALUES
  ('Samantha', 'Sukej', 'ssukej@hwp.org', '6501234567', 'Feline'),
  ('Aaron', 'Wu', 'awu@hwp.org', '6509876543', 'Avian and Canine'),
  ('Michael', 'Cui', 'mcui@hwp.org', '6502481632', 'Reptile'),
  ('Elise', 'Noalhyt', 'enoalhyt@hwp.org', '6504132020', 'Canine')
);
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
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
);

--
-- Insert into `customers` table
--
LOCK TABLES `customers` WRITE;
INSERT INTO `customers` (first_name, last_name, email, phone, address, city, state, zip_code, number_of_pets)
  VALUES
  ('Mbali', 'Octavius', 'mbali@gmail.com', '7703523154', '342 Elsie Way', 'Mountain View', 'CA', '94040'),
  ('Sabina', 'Pitts', 'spitts@gmail.com', '3364952773', '2201 Deland Rd', 'Sunnyvale', 'CA', '94087'),
  ('Sundar', 'Pichai', 'sundar@google.com', '6505005931', '100 Innovation Way', 'Mountain View', 'CA', '94040'),
  ('Mira', 'Magee', 'mmagee@gmail.com', '6502381394', '597 Palomino Ave', 'Palo Alto', 'CA', '94028')
);
UNLOCK TABLES;

--
-- Table structure for table `pets`
--

DROP TABLE IF EXISTS `pets`;
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
);

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
CREATE TABLE IF NOT EXISTS `classes`(

  `class_id` int(11) NOT NULL AUTO_INCREMENT,
  `class_name` varchar(255) NOT NULL,
  `class_description` varchar(255) NOT NULL,
  `class_day` date NOT NULL,
  `class_time` datetime NOT NULL,
  `class_price` decimal NOT NULL,
  `class_enrollments` int(11) NOT NULL,
  `class_seats` int(11) NOT NULL,
  PRIMARY KEY(`class_id`),
  CONSTRAINT `class_name` UNIQUE(`class_name`)
);

--
-- Table structure for `enrollments` table (M:M Relationship)
--

DROP TABLE IF EXISTS `enrollments`;
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
);



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-28 13:23:54
