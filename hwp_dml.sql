-- DML queries for Hello World Pets

--
-- SELECT queries
--

-- Pets page: search for a pet by name, pet name, or pet type
SELECT * FROM pets WHERE customer_id = (SELECT customer_id FROM customers WHERE first_name = :firstName);
SELECT * FROM pets WHERE pet_name = :petName;
SELECT * FROM pets WHERE species = :species;

-- Classes page: search for a class by class name, class day, class time or class price
SELECT * FROM classes WHERE class_name = :className;
-- This query is from: https://stackoverflow.com/questions/20740696/mysql-converting-date-to-days-of-week
SELECT class_id, class_name, class_description, DAYNAME(class_day), HOUR(class_time), class_price, class_enrollments, class_seats 
FROM classes WHERE DAYNAME(class_day) = :classDay;
SELECT class_id, class_name, class_description, DAYNAME(class_day), HOUR(class_time), class_price, class_enrollments, class_seats 
FROM classes WHERE DAYNAME(class_day) = :classTime;
SELECT * FROM classes WHERE class_price = :classPrice;

-- Vets page: search for a vet by first name, last name, specialty or pet name
SELECT * FROM vets WHERE first_name = :firstName;
SELECT * FROM vets WHERE last_name = :lastName;
SELECT * FROM vets WHERE specialty = :specialty;
SELECT * FROM vets WHERE vet_id = (SELECT vet_id FROM pets WHERE pet_name = :petName);

-- Admin page: show all Customers
SELECT * FROM customers;

-- Admin page: show all Pets
SELECT * FROM pets;

-- Admin page: show all Classes
SELECT * FROM classes;

-- Admin page: show all Enrollments
SELECT * FROM enrollments;

-- Admin page: show all Teachers
SELECT * FROM teachers;

-- Admin page: show all Vets
SELECT * FROM vets;

--
-- INSERT queries
--

-- Customers page: register a new customer
INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES (:firstName, :lastName, :email, :phone, :address, :city, :state, :zip);

-- Customers page: add a pet
INSERT INTO pets (pet_name, species, breed, age, gender, vet_id, customer_id) VALUES (:petName, :petSpecies, :petBreed, :petAge, :vetId, :customerId);

-- Classes page: enroll a pet in a class by ID
INSERT INTO enrollments (pet_id, class_id) VALUES(
	(SELECT pet_id FROM pets WHERE pet_id = :petId),
	(SELECT class_id FROM classes WHERE class_id = :classId)
);

-- Admin page: add Customer
INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES (:firstName, :lastName, :email, :phone, :address, :city, :state, :zip);

-- Admin page: add Pet
INSERT INTO pets (pet_name, species, breed, age, gender, vet_id, customer_id) VALUES (:petName, :petSpecies, :petBreed, :petAge, :vetId, :customerId);

-- Admin page: add Class
INSERT INTO classes (class_name, class_description, class_day, class_time, class_price, class_enrollments, class_seats, teacher_id)
VALUES (:className, :classDescription, :classDay, :classTime, :classPrice, :classEnrollments, :classSeats,
        (SELECT teacher_id FROM teachers WHERE first_name = :teacherFirstName AND last_name = :teacherLastName)
);

-- Admin page: add Enrollment
INSERT INTO enrollments (pet_id, class_id) values (
  (SELECT pet_id FROM pets WHERE pet_name = :petName),
  (SELECT class_id FROM classes WHERE class_name = :className)
);

-- Admin page: add Vet
INSERT INTO vets (first_name, last_name, email, phone, specialty) VALUES (:firstName, :lastName, :email, :phone, :specialty);

--
-- UPDATE queries
--

-- Admin page: update Customer
UPDATE customers SET first_name = :firstName, last_name = :lastName, email = :email, phone = :phone, address = :address, city = :city, state = :state, zip_code = :zipCode
WHERE customer_id = :customerId;

-- Admin page: update Pet
UPDATE pets SET pet_name = :petName, species= :petSpecies, breed = :petBreed, age = :petAge, age= :ageInput , gender = :petGender WHERE pet_id = :petId;

-- Admin page: update Class
UPDATE classes SET class_name = :className, class_description = :classDescription, class_day = :classDay, class_time = :classTime, class_price = :classPrice, class_enrollments = :classEnrollments, class_seats = :classSeats
WHERE class_id = :classId;

-- Admin page: update Enrollment
UPDATE enrollments SET pet_id = :petId, class_id = :classId WHERE enrollment_id = :enrollmentID;

-- Admin page: update Vet
UPDATE vets SET first_name = :firstName, last_name = :lastName, email = :email, phone = :phone, specialty = :specialty
WHERE vet_id = :vetId;

-- 
-- DELETE queries
--

-- Admin page: delete Customer
DELETE FROM customers WHERE customer_id = :customerId;

-- Admin page: delete Pet
DELETE FROM pets WHERE pet_id = :petId;

-- Admin page: delete Class
DELETE FROM classes WHERE class_id = :classId;

-- Admin page: delete Enrollment
DELETE FROM enrollments WHERE enrollment_id = :enrollmentId;

-- Admin page: delete Vet
DELETE FROM vets WHERE vet_id = :vetId;

