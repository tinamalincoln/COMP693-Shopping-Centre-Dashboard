/*
   COMP693 S2 2025 - Industry Project
   Script file for MySQL DBMS
   Created By: Tina Ma
   Description: Create the shopping centre database and related tables
   Created Date: 28/07/2025
   Updated Date: 09/08/2025
   Version: 1.1
*/

-- Create a new database
CREATE DATABASE shoppingcentre;

-- Use shoppingcentre database to create related tables based on the ERD
USE shoppingcentre;

-- 1. City lookup
CREATE TABLE city (
  id   INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Classification lookup
CREATE TABLE classification (
  id   INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

-- 3. Centre Type lookup
CREATE TABLE centre_type (
  id   INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

-- 4. Shopping Centre “fact” table
CREATE TABLE shopping_centre (
  id                 INT AUTO_INCREMENT PRIMARY KEY,
  city_id            INT NOT NULL,
  classification_id  INT DEFAULT NULL,
  centre_type_id     INT DEFAULT NULL,
  name               VARCHAR(255)    NOT NULL,
  osm_name           VARCHAR(255)    DEFAULT NULL,
  image_filename     VARCHAR(100)    DEFAULT NULL,
  location           TEXT            DEFAULT NULL,
  date_opened        DATE            DEFAULT NULL,
  site_area_ha       DECIMAL(10,4)   DEFAULT NULL,
  covered_parking_num    INT UNSIGNED DEFAULT 0,
  uncovered_parking_num  INT UNSIGNED DEFAULT 0,
  redevelopments     TEXT            DEFAULT NULL,
  levels             TINYINT UNSIGNED DEFAULT NULL,
  total_retail_space DECIMAL(12,2)   DEFAULT NULL,
  created_at             TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at             TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_city       FOREIGN KEY (city_id)           REFERENCES city(id)           ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_class      FOREIGN KEY (classification_id) REFERENCES classification(id) ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_type       FOREIGN KEY (centre_type_id)    REFERENCES centre_type(id)    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT uq_city_name UNIQUE (city_id, name)
);



