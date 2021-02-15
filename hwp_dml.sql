-- DML queries for Hello World Pets

--
-- SELECT queries
--

-- Pets page: search for a pet by name, pet name, or pet type

-- Classes page: search for a class by class name, class day, class time or class price

-- Vets page: search for a vet by first name, last name, specialty or pet name
SELECT * FROM vets WHERE first_name = :firstName
SELECT * FROM vets WHERE last_name = :lastName
SELECT * FROM vets WHERE specialty = :specialty
SELECT * FROM vets WHERE vet_id = (SELECT vet_id from pets where pet_name = :petName)

-- Admin page: show all Customers
SELECT * from customers

-- Admin page: show all Pets

-- Admin page: show all Classes

-- Admin page: show all Enrollments

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

-- Admin page: add Customer
INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES (:firstName, :lastName, :email, :phone, :address, :city, :state, :zip)

-- Admin page: add Pet

-- Admin page: add Class

-- Admin page: add Enrollment

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
