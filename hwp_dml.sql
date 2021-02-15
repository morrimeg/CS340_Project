-- DML queries for Hello World Pets

--
-- SELECT queries
--

-- Pets page: search for a pet by name, pet name, or pet type
SELECT * FROM pets where customer_id = (SELECT customer_id from customers where first_name = :firstName)
SELECT * FROM pets WHERE pet_name = :petName
SELECT * FROM pets WHERE species = :species

-- Classes page: search for a class by class name, class day, class time or class price
SELECT * FROM classes WHERE class_name = :className
-- This query is from: https://stackoverflow.com/questions/20740696/mysql-converting-date-to-days-of-week
SELECT class_id, class_name, class_description, DAYNAME(class_day), HOUR(class_time), class_price, class_enrollments, class_seats 
FROM classes WHERE DAYNAME(class_day) = :classDay
SELECT class_id, class_name, class_description, DAYNAME(class_day), HOUR(class_time), class_price, class_enrollments, class_seats 
FROM classes WHERE DAYNAME(class_day) = :classTime
SELECT * FROM classes WHERE class_price = :classPrice

-- Vets page: search for a vet by first name, last name, specialty or pet name
SELECT * FROM vets WHERE first_name = :firstName
SELECT * FROM vets WHERE last_name = :lastName
SELECT * FROM vets WHERE specialty = :specialty
SELECT * FROM vets WHERE vet_id = (SELECT vet_id from pets where pet_name = :petName)

-- Admin page: show all Customers
SELECT * from customers

-- Admin page: show all Pets
SELECT * from pets

-- Admin page: show all Classes
SELECT * from classes

-- Admin page: show all Enrollments
SELECT * from enrollments

-- Admin page: show all Vets
SELECT * from vets

--
-- INSERT queries
--

-- Customers page: register a new customer
INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES (:firstName, :lastName, :email, :phone, :address, :city, :state, :zip)

-- Customers page: add a pet
INSERT INTO pets (pet_name, species, breed, age, gender, vet_id, customer_id) VALUES (:petName, :petSpecies, :petBreed, :petAge, :vetId, :customerId)

-- Classes page: enroll a pet in a class by ID
INSERT INTO enrollments (pet_id, class_id) VALUES(
	(SELECT pet_id from pets where pet_id = :petId),
	(SELECT class_id from classes WHERE class_id = :classId)
)


-- Admin page: add Customer
INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES (:firstName, :lastName, :email, :phone, :address, :city, :state, :zip)

-- Admin page: add Pet
INSERT INTO pets (pet_name, species, breed, age, gender, vet_id, customer_id) VALUES (:petName, :petSpecies, :petBreed, :petAge, :vetId, :customerId)

-- Admin page: add Class
INSERT INTO classes (class_name, class_description, class_day, class_time, class_price, class_enrollments, class_seats)
VALUES (:class_name_Input, :class_description_Input, :class_day_Input, :class_time_Input, :class_price_Input,
		:class_enrollments_Input, :class_seats_Input)

-- Admin page: add Enrollment
INSERT INTO enrollments (pet_id, class_id) values (
  (SELECT pet_id from pets where pet_name = :petName),
  (SELECT class_id from classes where class_name = :className)

)


-- Admin page: add Vet
INSERT INTO vets (first_name, last_name, email, phone, specialty) VALUES (:firstName, :lastName, :email, :phone, :specialty)

--
-- UPDATE queries
--

-- Admin page: update Customer

-- Admin page: update Pet

-- Admin page: update Class

-- Admin page: update Enrollment

-- Admin page: update Vet

-- 
-- DELETE queries
--

-- Admin page: delete Customer

-- Admin page: delete Pet

-- Admin page: delete Class

-- Admin page: delete Enrollment

-- Admin page: delete Vet
